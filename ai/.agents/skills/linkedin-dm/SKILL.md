---
name: linkedin-dm
description: Read LinkedIn direct messages from the terminal using LinkedIn's internal GraphQL API. Use when the user wants to check LinkedIn DMs, read conversations, export message history, or find which DMs need replies. Supports JSON output for agent consumption.
---

# linkedin-dm

CLI for reading LinkedIn direct messages via the same GraphQL API the LinkedIn web app uses — no Matrix bridge required.

## Setup

```bash
# Install binary
go install github.com/Aitbytes/linkedin-dm/cmd/linkedin-dm@latest

# Or download from releases
curl -L https://github.com/Aitbytes/linkedin-dm/releases/latest/download/linkedin-dm-linux-amd64 -o ~/.local/bin/linkedin-dm
chmod +x ~/.local/bin/linkedin-dm
```

## Authentication

### Which env vars each command needs

| Command | `LINKEDIN_COOKIE_HEADER` | `LINKEDIN_LI_AT` |
|---------|--------------------------|-------------------|
| `status` | ✅ Sufficient alone (verified 2026-10-13) | ✅ Works |
| `list` | ✅ Required | ❌ Not enough |
| `read` | ✅ Required | ❌ Not enough |

### Getting cookies

1. Open LinkedIn in your browser, F12 → **Network** tab
2. Refresh the page
3. Click any request to `www.linkedin.com`
4. Copy the full `Cookie:` request header value

```bash
export LINKEDIN_COOKIE_HEADER='li_at=...; JSESSIONID="ajax:..."; bcookie=...'
```

### Vault (agent path — 2026-10-13)

Cookie lives at `kv-v2/blithe/agents-scratch/linkedin` (agent-WRITABLE path — the renewal
loop is fully agent-drivable: steel login → CDP harvest → vault put, user only taps 2FA).

```bash
export LINKEDIN_COOKIE_HEADER="$(~/.opencode/tools/env-guard.sh linkedin)"
linkedin-dm list --json --unread
```

`env-guard linkedin` does the AppRole login + field read and prints the raw header
(command-substitution safe — no eval, no special-char mangling).

Legacy path `kv-v2/cli-envs/linkedin` was lost in the 2026-10-13 vault rebuild; agents-scratch
is the live location. Raw Vault CLI still works for interactive users:

```bash
export LINKEDIN_COOKIE_HEADER="$(vault kv get -field=LINKEDIN_COOKIE_HEADER kv-v2/blithe/agents-scratch/linkedin)"
```

## Usage

```bash
# Status check (minimal auth)
linkedin-dm status

# List conversations
linkedin-dm list --json                          # All conversations as JSON
linkedin-dm list --unread                        # Only unread
linkedin-dm list --json --unread                 # Unread as JSON

# Read a conversation
linkedin-dm read 3                               # Human-readable
linkedin-dm read 0 --json                        # Structured JSON
linkedin-dm read 0 --json --plain                # Clean JSON, no stderr logs
```

## Agent-friendly patterns

### Find conversations needing replies

```bash
linkedin-dm list --json --unread 2>/dev/null | jq '[.[] | {index, title: .title, last_message: .last_message}]'
```

### Read all unread conversations

```bash
linkedin-dm list --json --unread 2>/dev/null | jq -r '.[].index' | while read idx; do
  linkedin-dm read "$idx" --json --plain 2>/dev/null
done
```

### Filter conversations by date range

```bash
linkedin-dm list --json 2>/dev/null | jq '[.[] | select(.last_activity_at >= "2026-07-01")]'
```

## How It Works

Uses [`linkedingo`](https://github.com/mautrix/linkedin/tree/main/pkg/linkedingo), the same Go library that powers `mautrix-linkedin`. It speaks LinkedIn's internal GraphQL API (`voyagerMessagingGraphQL`) with proper browser fingerprinting headers.

## Known Limitations

- **No send support**: read-only — use the LinkedIn web app to reply
- **Cookie expires ~24h**: LinkedIn sessions are short-lived
- **No real-time**: each `read` is a full HTTP request (no SSE streaming)
- **vault-env compatibility**: `source vault-env linkedin` may silently drop `LINKEDIN_COOKIE_HEADER` due to special characters; use `env-guard linkedin` or the raw Vault CLI instead

## References

- [Auth troubleshooting](references/auth-troubleshooting.md)
- [mautrix-linkedin](https://github.com/mautrix/linkedin)