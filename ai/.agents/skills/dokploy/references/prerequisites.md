## Prerequisites

The following environment variables are expected:

- `DOKPLOY_URL` — base URL of your Dokploy instance. **This is required** — the default `http://localhost:3000` is unlikely to work unless self-hosting locally.
- `DOKPLOY_API_KEY` — API key generated from Dokploy dashboard > Settings > API Keys.

If not set, the skill will ask for them.

### Loading secrets via Vault (recommended)

Never store API keys on disk. Use the secrets-management skill to load them into your shell:

```bash
# One-time: store in Vault
vault kv put kv-v2/cli-envs/dokploy \
  DOKPLOY_URL='https://your-dokploy.example.com' \
  DOKPLOY_API_KEY='pk_...'

# Every session: load on demand
source ~/scripts/vault-env dokploy
# or: venv dokploy
```

This injects `$DOKPLOY_URL` and `$DOKPLOY_API_KEY` into the current shell only — nothing touches disk.

**⚠️ Environment variables are per-`bash`-call only.** Each `bash` tool invocation spawns a fresh shell. You MUST chain vault loading + API calls in a single `bash` command block. [See tips.md](tips.md) for the full anti-pattern guide.

**⚠️ Vault TLS pitfall:** The Vault server may present a cert that doesn't match `hashi-vault.aitbytes.fyi`. If `vault-env` fails authentication, prepend `export VAULT_SKIP_VERIFY=true &&` before sourcing. [See tips.md](tips.md) for details.

## Architecture

Dokploy exposes a tRPC-based API with two handler paths:

1. **OpenAPI handler** (`/api/{router}.{procedure}`) — Recommended. Uses individual query params for GET, JSON body for POST. This is the path used by the OpenAPI spec.
2. **tRPC handler** (`/api/trpc/{router}.{procedure}`) — Alternative. Uses `?input=<URL-encoded JSON>` for everything.

**Prefer the OpenAPI handler format** as it's cleaner for scripting.

### Authentication

All requests require an `x-api-key` header with a valid API key. The API key must be generated with a specific organization ID in its metadata.

```bash
# Base curl template
curl -s -H "x-api-key: $DOKPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  "$DOKPLOY_URL/api/{router}.{procedure}"
```

### URL Conventions

- **GET queries**: Pass params as individual query string parameters
  ```
  GET /api/application.one?applicationId=abc123
  GET /api/project.all
  GET /api/deployment.all?applicationId=abc123
  ```
- **POST mutations**: Send JSON body
  ```
  POST /api/application.create  ← JSON body: {"name":"my-app","environmentId":"env-id"}
  POST /api/application.deploy  ← JSON body: {"applicationId":"abc123"}
  ```

## Resource Hierarchy

```
Organization
 └── Project (projectId)
      └── Environment (environmentId)
           ├── Application (applicationId, appName)
           ├── Compose (composeId)
           ├── MySQL (mysqlId)
           ├── PostgreSQL (postgresId)
           ├── Redis (redisId)
           ├── MongoDB (mongoId)
           └── MariaDB (mariadbId)
```

Each service is created within an environment. Services can be moved between environments.

### Service ID naming conventions

`applicationId`, `composeId`, `postgresId`, `mysqlId`, `redisId`, `mongoId`, `mariadbId`, `environmentId`, `projectId`, `serverId`, `destinationId`, `domainId`, `deploymentId`, etc.

## Response Shapes

Dokploy endpoints return inconsistent response shapes. Know what to expect:

| Operation | Response shape |
|---|---|
| `*.create` | **Nested** — `project.create` returns `{"project":{...}, "environment":{...}}`. Most other creates return the full object directly. |
| `*.one`, `*.all` | Full object or array of objects |
| `*.update` | `true` (boolean) — not the updated object |
| `*.saveEnvironment`, `*.saveBuildType`, `*.saveGithubProvider` | `true` (boolean) |
| `*.deploy`, `*.redeploy` | Full object (may be empty if no deployment triggers) |
| `*.delete`, `*.remove` | Full deleted object |
| `*.start`, `*.stop` | Full object |
| `*.search` | **Returns `{"message":"Not found","code":"NOT_FOUND"}` when no results** — not `[]`. Treat as empty list. |
| `*.move` | Full object |

When extracting IDs from `project.create`:
```bash
PROJECT_ID=$(echo "$RESP" | jq -r '.project.projectId')
ENV_ID=$(echo "$RESP" | jq -r '.environment.environmentId')
```
