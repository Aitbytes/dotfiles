# Runbook: iProyal residential proxy

**Registry id**: `iproyal-proxy` · **Class**: managed service credential
**Config file**: `~/.config/proxy-conf` (chmod 600 — plaintext by necessity: python tools + curl read it directly; the one accepted exception to the no-plaintext rule, documented here)
**Consumers**: `~/dotfiles/ai/tools/*` via `_shared_runtime.load_proxy_config` (auto), `lbc_fetch.py` (explicit), curl one-offs via `env-guard proxy`
**Probe**: `curl -s --proxy "http://$(grep -o 'http://[^"]*' ~/.config/proxy-conf | sed 's|http://||')" http://ip-api.com/json/?fields=country --max-time 30`
**Renewal trigger**: on probe failure (non-geo plain exit test above) or at iproyal plan renewal — check the iproyal dashboard for the subscription end date; rotate by replacing the password in proxy-conf.

## The one thing to remember

**Geo-targeting goes ON THE PASSWORD**: `..._country-fr` suffix → French residential exit. Port 12321 (or 12322). Username-suffix variants were flaky on this plan — don't use them.

## The leboncoin unlock (verified 2026-10-13)

Plain curl through even a FR exit → DataDome 403 (TLS fingerprint).
Winner: `curl_cffi` + `impersonate="chrome"` → HTTP 200 with full `__NEXT_DATA__` listing data.
Script: `agent-shared/scripts/lbc_fetch.py`. Recipe: `env-guard proxy-fr`.
Expect ~30% 403s → retry. NEVER scrape leboncoin from the home IP (flags it).

## Incident 2026-10-13 (do not repeat)

The refactor plan initially RETIRED this proxy based on session evidence of "dead proxy"
failures — wrong diagnosis: the proxy was alive; per-site DataDome TLS fingerprinting was
the real blocker, and the fix is curl_cffi impersonation (session 01a1320d proves the
full stack). Reverted same day. Lesson for W7: probe a credential AT its consumers
before declaring it dead; "flaky on site X" ≠ "dead credential".
