#!/usr/bin/env bash
# env-guard — single source of proxy/credential policy for the research toolchain
# (research-stack refactor, W3.1; lives next to the tools it guards)
#
#   env-guard proxy         export HTTP_PROXY/HTTPS_PROXY for curl / one-off commands
#   env-guard proxy-fr      print the FR-geo recipe (password suffix + curl_cffi) — the leboncoin unlock
#   env-guard direct        explain when to go direct (playwright can't use the authed proxy)
#   env-guard linkedin      print the RAW LINKEDIN_COOKIE_HEADER (substitution-safe; approle login included)
#   env-guard renew <id>    print the renewal runbook for a registered credential
#
# Exit codes: 0 ok, 1 bad usage/missing config, 2 approle login failure, 3 cookie empty/missing, 4 unknown credential id.

set -euo pipefail
PROXY_CONF="$HOME/.config/proxy-conf"

case "${1:-}" in
  proxy)
    # Emit export lines for sourcing:  eval "$(env-guard proxy)"
    if [ -r "$PROXY_CONF" ]; then
      grep -E '^export (HTTP_PROXY|HTTPS_PROXY)=' "$PROXY_CONF" || { echo "warn: no proxy lines in $PROXY_CONF" >&2; exit 1; }
    else
      echo "error: $PROXY_CONF missing" >&2
      exit 1
    fi
    ;;
  proxy-fr)
    cat <<'EOF'
FR-GEO RESIDENTIAL RECIPE (verified live 2026-10-13, from session 01a1320d):

  Geo-targeting goes ON THE PASSWORD (username suffix also exists but was
  flaky on this plan): append `_country-fr` to the password, port 12321:

      PW=$(grep -o ':[^:@]*@' ~/.config/proxy-conf | head -1 | tr -d ':@')
      PROXY_USER=$(grep -o 'http://[^:]*' "$HOME/.config/proxy-conf" | head -1 | sed 's|http://||')
      PROXY="http://${PROXY_USER}:${PW}_country-fr@geo.iproyal.com:12321"

  Plain proxy (no suffix) = rotating worldwide exit.
  Port 12322 also accepts the suffix (alternative pass-through).

  WHY curl_cffi: DataDome fingerprints the TLS handshake — plain curl gets a
  774-byte 403 even through a French residential IP. curl_cffi impersonates
  Chrome's TLS stack byte-for-byte:

      uv run --with curl_cffi python3 script.py

      from curl_cffi import requests
      r = requests.get(url, impersonate="chrome",
                       proxies={"http": PROXY, "https": PROXY},
                       headers={"Accept-Language": "fr-FR,fr;q=0.9"}, timeout=60)

  Parse leboncoin SSR pages from the __NEXT_DATA__ JSON blob:
      props.pageProps.searchData.ads  ->  [{subject, price_cents, location.city, url, list_id}]

  Expect ~30% 403s on first attempts — retry once or twice; the session
  verified 200s come through on retry (lbc_fetch.py in agent-shared/scripts).

  NEVER point this at leboncoin from your HOME IP (playwright/chrome direct):
  that flags the home IP with DataDome ("automated activity").
EOF
    ;;
  direct)
    cat <<'EOF'
DIRECT POLICY (when NOT to use the proxy):
  - playwright-cli / Chromium: CANNOT pass the authenticated proxy (embedded
    user:pass). Always unset proxy vars first:
        unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
  - Steel browser (LAN 192.168.1.50): direct by design.
  - youtube.py / research tools: proxy_mode="auto" — they use the proxy and
    auto-fall back to direct on slow/dead proxy. No manual action needed.
EOF
    ;;
  linkedin)
    # Prints the RAW cookie header on stdout (command-substitution safe).
    # Usage:  export LINKEDIN_COOKIE_HEADER="$(env-guard linkedin)"
    # Requires: AppRole bootstrap (role-id file + keyring secret_id) — the
    # agent auth path; interactive users can also vault login and read directly.
    set -a; [ -r "${HOME}/.config/vault/VAULT_ADDR" ] && . "${HOME}/.config/vault/VAULT_ADDR"; set +a
    export VAULT_ADDR="${VAULT_ADDR:-https://hashi-vault.aitbytes.fyi}"
    RID=$(cat "$HOME/.config/vault/approle-role-id")
    SID=$(secret-tool lookup service vault-env username approle-secret-id) \
      || SID=$(cat "$HOME/.config/vault/approle-secret-id")
    TOK=$(env -u VAULT_TOKEN vault write -field=token auth/approle/login \
      role_id="$RID" secret_id="$SID" 2>/dev/null)
    [ -n "${TOK:-}" ] || { echo "env-guard: approle login failed" >&2; exit 2; }
    COOKIE=$(VAULT_TOKEN="$TOK" vault kv get -field=LINKEDIN_COOKIE_HEADER \
      kv-v2/blithe/agents-scratch/linkedin 2>/dev/null)
    [ -n "${COOKIE:-}" ] || { echo "env-guard: cookie empty — renew (see runbook linkedin-cookie)" >&2; exit 3; }
    printf '%s' "$COOKIE"
    ;;
  renew)
    id="${2:-}"
    [ -z "$id" ] && { echo "usage: env-guard renew <credential-id>" >&2; exit 1; }
    book="$HOME/dotfiles/ai/agent-shared/runbooks/$id.md"
    if [ -f "$book" ]; then cat "$book"; else echo "unknown credential id: $id" >&2; echo "known: $(ls "$HOME/dotfiles/ai/agent-shared/runbooks/" 2>/dev/null | sed 's/\.md//' | paste -sd' ' -)" >&2; exit 2; fi
    ;;
  "")
    sed -n '2,7p' "$0"
    echo "subcommands: proxy | proxy-fr | direct | renew <id>"
    ;;
  *)
    echo "unknown subcommand: $1" >&2
    exit 1
    ;;
esac
