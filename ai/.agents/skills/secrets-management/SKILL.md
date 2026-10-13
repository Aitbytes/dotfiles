---
name: secrets-management
description: "Manage CLI secrets via HashiCorp Vault — never store API keys, tokens, or credentials on disk. Load secrets on-demand with a single command. When to use me ? : When setting up a new machine, adding or using secrets and API keys, rotating credentials, debugging 'secret not found' errors"
---

## What I do

Explain the vault-env workflow: how to store secrets in HashiCorp Vault and load them into your shell on demand, so no credentials ever touch your filesystem.


## Architecture

```
┌─────────────────────────────┐
│   ~/scripts/vault-env       │  ← helper script (sourced, never executed)
│   alias: venv <namespace>   │
└──────────┬──────────────────┘
           │  AppRole login (role agent-workstation)
           │  secret_id: keyring (secret-tool/kwalletd6) > 0600 file > $env
           │  → 30-min token in a shell-local var, NEVER exported
           ▼
┌─────────────────────────────┐
│  Vault (kv-v2/cli-envs/)    │  policy `agents`: read-only
│  ├── ai-keys/               │  Anthropic, OpenAI, Gemini, OpenRouter, ZAI
│  ├── aws/                   │  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
│  ├── cloudflare/            │  CLOUDFLARE_API_KEY
│  ├── github/                │  GH_TOKEN
│  └── reddit/                │  REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
└──────────┬──────────────────┘
           │  export lines via eval (secrets only)
           ▼
┌─────────────────────────────┐
│  Current shell  $ENV        │
│  Secrets live only in RAM   │  token dies with the call (30 min)
│  Gone when terminal closes  │
└─────────────────────────────┘
```

## Authentication model (2026-10-13)

No hardcoded tokens, no root in env — ever. Root is break-glass only
(paper + `.secrets`, custody rule from incident 2026-10-03 / #199).

1. Valid `VAULT_TOKEN` / token helper → used as-is (interactive users)
2. Otherwise AppRole `agent-workstation` mints a 30-min token (policy
   `agents` = read-only on `blithe/*`, `cloudflare/*`, `cli-envs/*`,
   PLUS full write on the scratch zone `kv-v2/blithe/agents-scratch/*`)
   — note: on Vault 2.1.x the `auth/approle/role/<name>/login` route
   answers "unsupported path"; the working login endpoint is the legacy
   `auth/approle/login` (role_id + secret_id), which is what this
   script uses
3. `role_id` (not secret): `~/.config/vault/approle-role-id`
4. `secret_id` (30 d TTL): OS keyring via `secret-tool` (symlinked in
   `~/.local/bin`, served by kwalletd6), fallback 0600 file
   `~/.config/vault/approle-secret-id`

- CIDR binding deliberately absent: traefik SNATs, Vault sees `172.18.0.3`.
  Becomes possible when Vault moves to the LXC with direct tailnet
  exposure (vlan20-design §9 #1).
- Emergency kill of ALL agent access:
  `vault destroy -f auth/approle/role/agent-workstation/secret-id`
- Rotate the secret_id (30 d):
  `vault write -f -field=secret_id auth/approle/role/agent-workstation/secret-id | nix-shell -p libsecret --run 'secret-tool store --label="Vault AppRole secret_id" service vault-env username approle-secret-id'`

## Usage

### Loading secrets

```bash
# Single namespace
source ~/scripts/vault-env ai-keys

# Multiple namespaces
source ~/scripts/vault-env ai-keys aws cloudflare

# Everything
source ~/scripts/vault-env --all

# Or use the shortcut (available in new shells)
venv ai-keys
```

Agents get in with zero interaction (AppRole bootstrap). Interactive users with an existing token keep working; otherwise you'll be prompted by `vault login` once.

### Storing a new secret

```bash
# Authenticate to Vault first if needed
vault login

# Write a new namespace
vault kv put kv-v2/cli-envs/my-service \
  MY_API_KEY='sk-abc123' \
  MY_API_SECRET='xyz789'

# Verify
vault kv get kv-v2/cli-envs/my-service
```

### Rotating a secret

```bash
# Patch a single key in an existing namespace
vault kv patch kv-v2/cli-envs/ai-keys OPENAI_API_KEY='sk-new-key-here'

# Or replace the whole namespace
vault kv put kv-v2/cli-envs/ai-keys \
  ANTHROPIC_API_KEY='sk-ant-...' \
  OPENAI_API_KEY='sk-...' \
  GEMINI_API_KEY='...' \
  GOOGLE_API_KEY='...' \
  GOOGLE_SEARCH_ENGINE_ID='...' \
  OPENROUTER_API_KEY='sk-or-...' \
  ZAI_API_KEY='...'
```

### Listing available namespaces

```bash
vault kv list kv-v2/cli-envs
```

## How `~/scripts/vault-env` works internally

1. Checks you're sourcing it (not executing directly)
2. Checks Vault auth — prompts for token if needed
3. Fetches the requested namespace(s) from `kv-v2/cli-envs/<name>`
4. Parses JSON response and runs `eval` on `export KEY='value'` lines in the current shell
5. Secrets are injected directly into shell memory — never printed to stdout, never written to disk

## Security properties

| Property | Old (~/.config/secret-envs) | New (vault-env) |
|---|---|---|
| On disk | Plaintext, world-readable | Nothing on disk |
| In memory | Always loaded at shell start | Only when explicitly requested |
| Scoped | All secrets, all the time | Per-namespace on-demand |
| Shareable | File must be copied | `source vault-env` works from any machine |
| Auditable | Just a text file | Vault audit log |
| Revocable | Must rotate every key | Revoke Vault token, all access gone |

## Vault setup prerequisites

```bash
# VAULT_ADDR must be set (hardcoded in the script)
export VAULT_ADDR='https://hashi-vault.aitbytes.fyi'

# Vault must be unsealed and reachable
vault status

# Root token or token with policies granting read to kv-v2/cli-envs/*
vault login
```

## Dependencies

- `vault` CLI (Vault 1.x+ with KV v2 support)
- `jq` (JSON parsing)
- Vault server running at `https://hashi-vault.aitbytes.fyi`

## Troubleshooting

**"Vault authentication required"** — you're not logged in. Run `vault login` first, or source `vault-env` in interactive mode which will prompt you.

**"Path not found: X"** — the namespace doesn't exist. Run `vault kv list kv-v2/cli-envs` to see what's available, then `vault kv put` to create it.

**"This script must be sourced, not executed"** — run `source ~/scripts/vault-env <name>`, not `~/scripts/vault-env <name>`.

**Secrets not appearing in env** — confirm they're actually in Vault: `vault kv get kv-v2/cli-envs/<name>`. If the data is there but not loading, check `jq` is installed.

**Eval not working** — the script uses `eval` to inject exports. Make sure you're using bash or zsh.

## Migration from old approach

The previous setup stored secrets in `~/.config/secret-envs` (world-readable, sourced at shell start). Migration steps:

1. Seed Vault: `vault kv put kv-v2/cli-envs/<ns> KEY1='val1' KEY2='val2' ...`
2. Verify: `source ~/scripts/vault-env <ns>`
3. Delete old file: `rm ~/.config/secret-envs`
4. Update shell rc: replace `source ~/.config/secret-envs` with `alias venv='source ~/scripts/vault-env'`

This was completed on 2026-05-31. All 14 environment variables now live in `kv-v2/cli-envs/`.
