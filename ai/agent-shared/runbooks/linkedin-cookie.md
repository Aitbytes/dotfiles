# Runbook: linkedin cookie (LINKEDIN_COOKIE_HEADER)

**Registry id**: `linkedin-cookie` · **Class**: session-cookie, expires ~24 h
**Vault**: `kv-v2/cli-envs/linkedin` · **Consumer**: `linkedin-dm` CLI, skill `linkedin-dm`
**Probe**: `source ~/scripts/vault-env linkedin; linkedin-dm status` (needs only LI_AT) · full check: `linkedin-dm list --json | head -5` (needs full cookie header)
**Renewal trigger**: probe-driven, NOT calendar — renew on demand when the probe fails.

## Renew (semi-automated, ~2 min, you tap 2FA)

1. Ask the agent to run the browser-use/Steel login flow, OR manual:
   - Open linkedin.com in your browser, log in (2FA = your phone tap)
2. F12 → Network tab → refresh → click any request to `www.linkedin.com`
3. Copy the full `Cookie:` request header value
4. Store via RAW Vault CLI (special chars `; " =` break eval-style loading):
   ```bash
   vault kv put kv-v2/cli-envs/linkedin LINKEDIN_COOKIE_HEADER='li_at=...; JSESSIONID="ajax:..."; bcookie=...'
   ```
5. Probe: `linkedin-dm status` then `linkedin-dm list --json --unread | head`
6. Update registry: `last_rotated = today`

## Gotchas (from the skill)

- `source vault-env linkedin` can silently mangle the cookie (special chars) → use raw `vault kv get -field=LINKEDIN_COOKIE_HEADER` for loading:
  ```bash
  export LINKEDIN_COOKIE_HEADER="$(vault kv get -field=LINKEDIN_COOKIE_HEADER kv-v2/cli-envs/linkedin)"
  ```
- Cookie dies ~24 h — do not schedule, probe instead.
- Namespace was lost in the 2026-10-13 Vault rebuild and NOT re-seeded (cookie would be stale anyway) — first seed = this runbook, step 4.
