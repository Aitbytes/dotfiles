# Runbook: linkedin cookie (LINKEDIN_COOKIE_HEADER)

**Registry id**: `linkedin-cookie` · **Class**: session-cookie, expires ~24 h
**Vault**: `kv-v2/blithe/agents-scratch/linkedin` (agent-writable since 2026-10-13)
**Consumer**: `linkedin-dm` CLI, skill `linkedin-dm`
**Probe**: `export LINKEDIN_COOKIE_HEADER="$(~/.opencode/tools/env-guard.sh linkedin)" && linkedin-dm status`
**Renewal trigger**: probe-driven, NOT calendar — renew on demand when the probe fails.
**last_rotated**: 2026-10-13 (via steel login + CDP harvest, user 2FA)

## Renew — agent-driven (~2 min, user taps 2FA once)

1. Steel browser login (user action): navigate Steel UI (http://192.168.1.50:3000) to linkedin.com login
   — OR ask the agent to drive it via `BU_CDP_URL=http://192.168.1.50:9223 browser-use` (user taps 2FA on phone)
2. Agent harvests cookies over CDP (httpOnly `li_at` included):
   ```bash
   export BU_CDP_URL=http://192.168.1.50:9223
   browser-use <<'PY'
   new_tab("https://www.linkedin.com/feed/")   # redirect to feed = session alive
   r = cdp("Network.getCookies", urls=["https://www.linkedin.com", "https://linkedin.com"])
   header = "; ".join(f"{c['name']}={c['value']}" for c in r.get("cookies", []))
   import json, os
   open("/tmp/li_put.json","w").write(json.dumps({"LINKEDIN_COOKIE_HEADER": header}))
   os.chmod("/tmp/li_put.json", 0o600)
   print("harvested", len(header), "chars")
   PY
   ```
3. Agent writes Vault (AppRole CAN write agents-scratch/* — flat JSON, no argv exposure):
   ```bash
   vault kv put kv-v2/blithe/agents-scratch/linkedin @/tmp/li_put.json   # after approle login
   ```
4. Probe: `linkedin-dm status && linkedin-dm list --json --unread | jq length`
5. shred temp files; update this runbook's last_rotated.

## Gotchas

- `vault kv put path @file` takes a FLAT JSON ({"FIELD": "value"}) — nesting {"data": {...}} creates a literal "data" field.
- `env-guard linkedin` prints the raw header for command substitution; never eval cookie values.
- Read path needs a live token: AppRole (agents) or interactive `vault login` (humans). The stale `~/.vault-token` file produces silent 403 → confusing "cookie not present" errors; env-guard handles the login.
- Cookie dies ~24 h — probe, don't schedule.
