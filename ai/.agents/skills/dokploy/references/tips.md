## Tips

### 🛡️ Critical: One shell, one action

**Environment variables do NOT persist across `bash` tool invocations.** Each `bash` call spawns a fresh shell. Secrets loaded via `source ~/scripts/vault-env dokploy` are gone in the next call.

✅ **Do this** — chain everything in one `bash` invocation:
```bash
set -a && source ~/scripts/vault-env dokploy 2>&1
curl -s -H "x-api-key: $DOKPLOY_API_KEY" "$DOKPLOY_URL/api/project.all" | jq '.'
```

❌ **Never do this** — the second call has no `$DOKPLOY_API_KEY`:
```bash
# Call 1:
source ~/scripts/vault-env dokploy
# Call 2 (separate bash invocation):
curl -s -H "x-api-key: $DOKPLOY_API_KEY" ...  # $DOKPLOY_API_KEY is empty!
```

If you must split calls, either store the values in a temp file or export them explicitly at the top of each subsequent `bash` command block.

### 🛡️ Vault TLS certificate mismatch

The vault server at `hashi-vault.aitbytes.fyi` presents a Traefik default certificate whose SAN does NOT match the hostname. This causes `vault-env`'s auth check (`vault token lookup`) to fail with:
```
x509: certificate is valid for ...traefik.default, not hashi-vault.aitbytes.fyi
```

**Fix**: Export `VAULT_SKIP_VERIFY=true` BEFORE sourcing vault-env, so that ALL vault commands inside the script inherit it:
```bash
export VAULT_SKIP_VERIFY=true && source ~/scripts/vault-env dokploy
```

❌ This does NOT work — `VAULT_SKIP_VERIFY=true` only applies to the `set -a` command, NOT to `source` after `&&`:
```bash
VAULT_SKIP_VERIFY=true set -a && source ~/scripts/vault-env dokploy  # WRONG
```

### 🛡️ No subshells after source

Avoid `$(...)` command substitution or pipes after `source` — they spawn subshells that don't inherit the exported variables:
```bash
# ❌ WRONG: the curl inside $() runs in a subshell with no env vars
export VAULT_SKIP_VERIFY=true && source ~/scripts/vault-env dokploy && echo "$(curl ... $$DOKPLOY_URL ...)"

# ✅ RIGHT: use ; or && to chain commands in the same shell
export VAULT_SKIP_VERIFY=true && source ~/scripts/vault-env dokploy && curl -s ...
```

---

1. **Always use `project.all` for discovery** — it returns the complete project tree with all services and their IDs.
2. **Update is a merge, not replace** — when updating a service, only include the fields you want to change plus the required ID field.
3. **saveEnvironment replaces ALL env vars** — always include the full env string, not just additions.
4. **Deploy after config changes** — after setting env vars, git providers, or build types, call `.deploy` or `.redeploy`.
5. **Check deployment status** — use `deployment.all` with the applicationId to monitor deployment progress.
6. **Response format**: Successful responses return the data directly (not wrapped in `{"data":...}`). Auth failures return `{"message": "Unauthorized"}`. Valid API keys with the right organization metadata are essential.
   - `*.create` (project): `{"project":{...}, "environment":{...}}` — nested, extract IDs via `.project.projectId`
   - `*.create` (other): full object directly
   - `*.update`, `*.save*`: `true` (boolean, not the updated object)
   - `*.search`: `{"message":"Not found"}` when empty — treat as empty list, not error
   - `*.remove`/`*.delete`: full deleted object
7. **Service IDs follow naming conventions**: `applicationId`, `composeId`, `postgresId`, `mysqlId`, `redisId`, `mongoId`, `mariadbId`, `environmentId`, `projectId`, `serverId`, `destinationId`, `domainId`, `deploymentId`, etc.
8. **Move uses `targetEnvironmentId`**, not `environmentId` — all `*.move` endpoints require `targetEnvironmentId`.
9. **Database password constraints**: No `$ ! ' " \ /` or space characters. Password validation will reject these.
10. **Docker image defaults may be wrong**: `mongo:15` and `mariadb:6` don't exist on Docker Hub. Specify a valid image tag or use the known-working defaults (mongo:7, mariadb:11).
11. **Compose template deploy requires non-null `serverId`**: Pass `""` (empty string) if you don't have a remote server.
12. **Backups need a destination first**: `destinationId` is required for `backup.create`. Use `destination.all` to find existing destinations, or `destination.create` to make one.
13. **Load secrets via Vault**: Use `source ~/scripts/vault-env dokploy` to load `DOKPLOY_URL` and `DOKPLOY_API_KEY` into the current shell without writing them to disk.
