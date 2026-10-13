# Runbook: reddit-app credentials

> **STATUS: STANDBY (2026-10-13)** — Reddit programmatic auth changed; the
> client-credentials path is unreliable. Do not re-seed or reactivate without
> an explicit user decision. Kept for the day Reddit is re-enabled.

**Registry id**: `reddit-app` · **Class**: static · **Vault**: `kv-v2/cli-envs/reddit`
**Consumers**: `~/.opencode/tools/reddit_scraper.py`, skill `reddit-research`, skill `retail-research` (Wave 3)
**Fields**: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`
**Probe**: `source ~/scripts/vault-env reddit && curl -s -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" -d grant_type=client_credentials https://www.reddit.com/api/v1/access_token | jq -r '.access_token'`
**Renewal trigger**: every 90 days, or immediately if the probe fails / Reddit shows the app as revoked.

## Renew (regenerate secret)

1. Open https://www.reddit.com/prefs/apps (logged in as the app owner)
2. Find the script app → click **edit** → the secret is shown / regenerate it
3. Update Vault (interactive shell, AppRole is read-only by design):
   ```bash
   vault kv patch kv-v2/cli-envs/reddit REDDIT_CLIENT_SECRET='NEW_SECRET'
   ```
4. Run the probe — must return a token
5. Update the registry: `last_rotated = today`

## Notes

- Client ID never expires; only the secret rotates. If the whole app is lost, recreate: **script app**, redirect `http://localhost:0`.
- Reddit script-app credentials do NOT depend on Vault rebuilds — but the Vault COPY is the only copy (recovered 2026-10-13 from session history after the vault rebuild wiped cli-envs).
