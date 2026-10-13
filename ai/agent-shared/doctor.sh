#!/usr/bin/env bash
# doctor.sh — research toolchain health check (research-stack refactor, W6.2/W7.2)
# Wired into: deep_research.md Phase 1. Run manually anytime.
# Output: one line per check, [ok]/[FAIL]/[warn] + summary. Exit 0 if no FAIL.

set -u
PASS=0; FAIL=0; WARN=0
line() { local s="$1"; shift; printf '%-8s %s\n' "[$s]" "$*"; case "$s" in ok) PASS=$((PASS+1));; FAIL) FAIL=$((FAIL+1));; warn) WARN=$((WARN+1));; esac; }

# 1. Steel (LAN browser)
if timeout 10 curl -sf http://192.168.1.50:3000/v1/health | grep -q '"ok"'; then line ok "steel: healthy"; else line FAIL "steel: unhealthy/unreachable (docker compose up -d on 192.168.1.50)"; fi

# 2. Proxy (plain exit; no geo suffix)
P=$(grep -o 'http://[^"]*' "$HOME/.config/proxy-conf" 2>/dev/null | head -1 | sed 's|http://||')
if [ -n "$P" ]; then
  C=$(timeout 30 curl -s --proxy "http://$P" "http://ip-api.com/json/?fields=country" --max-time 25 2>/dev/null)
  [ -n "$C" ] && line ok "proxy: alive ($C)" || line FAIL "proxy: dead (ip-api via proxy empty)"
else line FAIL "proxy: ~/.config/proxy-conf missing"; fi

# 3. Vault AppRole (the agent read/write path)
export VAULT_ADDR="${VAULT_ADDR:-https://hashi-vault.aitbytes.fyi}"
RID=$(cat "$HOME/.config/vault/approle-role-id" 2>/dev/null)
SID=$(secret-tool lookup service vault-env username approle-secret-id 2>/dev/null || cat "$HOME/.config/vault/approle-secret-id" 2>/dev/null)
TOK=""
if [ -n "$RID" ] && [ -n "$SID" ]; then
  TOK=$(env -u VAULT_TOKEN vault write -field=token auth/approle/login role_id="$RID" secret_id="$SID" 2>/dev/null)
fi
[ -n "$TOK" ] && line ok "vault approle: login ok" || line FAIL "vault approle: login FAILED (agent cred path down; see secrets-management skill)"

# 4. LinkedIn cookie: LIVE probe (linkedin-dm status), not just presence
if [ -n "$TOK" ]; then
  if command -v linkedin-dm >/dev/null 2>&1; then
    if CK=$(VAULT_TOKEN="$TOK" VAULT_ADDR="$VAULT_ADDR" bash -c 'export LINKEDIN_COOKIE_HEADER="$(env -u VAULT_TOKEN "'"'$HOME'"'/dotfiles/opencode/.opencode/tools/env-guard.sh linkedin" 2>/dev/null || VAULT_TOKEN="$VAULT_TOKEN" vault kv get -field=LINKEDIN_COOKIE_HEADER kv-v2/blithe/agents-scratch/linkedin 2>/dev/null)"; linkedin-dm status' 2>/dev/null) && echo "$CK" | grep -q Authenticated; then
      line ok "linkedin: live probe OK ($(echo "$CK" | head -1 | cut -d' ' -f1-4))"
    else
      line warn "linkedin: cookie present but DEAD — renew via runbook linkedin-cookie.md (~2 min, agent-drivable)"
    fi
  else
    CK=$(VAULT_TOKEN="$TOK" vault kv get -field=LINKEDIN_COOKIE_HEADER kv-v2/blithe/agents-scratch/linkedin 2>/dev/null)
    [ -n "$CK" ] && line warn "linkedin cookie: present but linkedin-dm missing — install before trusting" || line warn "linkedin cookie: absent — renew via runbook linkedin-cookie.md"
  fi
else line warn "linkedin: skipped (no vault auth)"; fi

# 5. Reddit
line warn "reddit: STANDBY (auth changed 2026-10-13) — no probe by design"

# 6. youtube.py deps resolve + reachability
if timeout 60 uv run --with requests --with certifi python3 -c "import requests; requests.get('https://www.youtube.com', timeout=15)" >/dev/null 2>&1; then line ok "youtube.py: deps + reachability ok"; else line FAIL "youtube.py: deps or network fail"; fi

# 6b. curl_cffi resolves (lbc_fetch.py dependency — the leboncoin unlock)
if timeout 60 uv run --with curl_cffi python3 -c "import curl_cffi" >/dev/null 2>&1; then line ok "curl_cffi: resolvable (lbc_fetch OK)"; else line FAIL "curl_cffi: not resolvable — lbc_fetch will die"; fi

# 6c. linkedin-dm binary
command -v linkedin-dm >/dev/null 2>&1 && line ok "linkedin-dm: binary present" || line FAIL "linkedin-dm: binary missing (~/.local/bin/linkedin-dm)"

# 6d. Proxy FR exit (the leboncoin unlock depends on _country-fr, not the plain pool)
if [ -n "$P" ]; then
  CFR=$(timeout 30 curl -s --proxy "http://${P%%@*}_country-fr@${P#*@}" "http://ip-api.com/json/?fields=country" --max-time 25 2>/dev/null)
  echo "$CFR" | grep -q 'France' && line ok "proxy FR-exit: France confirmed (_country-fr)" || line FAIL "proxy FR-exit: got '${CFR:-nothing}' — leboncoin unlock compromised"
fi

# 6e. web_scraper.py (the documented wrapper needs requests+certifi+bs4)
if timeout 60 uv run --with requests --with certifi --with beautifulsoup4 python3 ~/.opencode/tools/web_scraper.py --help >/dev/null 2>&1; then line ok "web_scraper: deps ok via documented wrapper"; else line FAIL "web_scraper: deps broken (bs4?)"; fi

# 6f. steel venv websocket-client (steel_cdp.py dependency)
"~/.agents/skills/steel-browser/.venv/bin/python" -c "import websocket" >/dev/null 2>&1 && line ok "steel venv: websocket-client ok" || line FAIL "steel venv: websocket-client missing (rebuild venv)"

# 7. playwright-cli
V=$(timeout 30 npx --no-install @playwright/cli --version 2>/dev/null)
[ -n "$V" ] && line ok "playwright-cli: $V" || line FAIL "playwright-cli: not runnable"

# 8. sites.json freshness (rows older than 90d = unknown per staleness law)
SJ="$HOME/.agents/skills/steel-browser/sites.json"
if [ -r "$SJ" ]; then
  STALE=$(python3 - "$SJ" <<'PY'
import json,sys,datetime
d=json.load(open(sys.argv[1]))
now=datetime.date.today(); stale=[]
for s in d["sites"]:
    lv=s.get("last_verified")
    if not lv: stale.append(s["site"]); continue
    if (now-datetime.date.fromisoformat(lv)).days>90: stale.append(s["site"])
print(f"{len(stale)}/{len(d['sites'])}")
if stale[:6]: print("|stale: "+", ".join(stale[:6])+("…" if len(stale)>6 else ""))
PY
)
  N=$(echo "$STALE" | head -1); DET=$(echo "$STALE" | tail -1)
  [ "${N%%/*}" = "0" ] && line ok "sites.json: all rows fresh ($N stale)" || line warn "sites.json: $N rows stale/undated — probe before trusting $DET"
else line FAIL "sites.json: missing at $SJ"; fi

echo "────────────────────────────"
echo "summary: $PASS ok, $WARN warn, $FAIL fail"
[ "$FAIL" -eq 0 ]
