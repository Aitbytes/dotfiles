# Auth Troubleshooting

## Getting your LinkedIn cookies

The most reliable method:

1. Log into `https://www.linkedin.com` in your browser
2. Open **Developer Tools** (F12) → **Network** tab
3. Refresh the page
4. Click any request to `www.linkedin.com`
5. In **Request Headers**, copy the full `Cookie:` value
6. Export it:

```bash
export LINKEDIN_COOKIE_HEADER='<paste full cookie>'
linkedin-dm status
```

## Required cookies

Your cookie header MUST include:

- `li_at` — authentication token
- `JSESSIONID` — session ID (typically `"ajax:..."`)

Missing these will produce "li_at cookie was deleted" or "token is no longer valid" errors.

## Optional: x-li-track and x-li-page-instance

For more reliable sessions, extract these headers from the same Network tab request:

```bash
export LINKEDIN_XLI_TRACK='{"clientVersion":"1.13.X","mpVersion":...}'
export LINKEDIN_XLI_PAGE_INSTANCE='urn:li:page:messaging_thread;...'
```

Without them, `linkedin-dm` uses hardcoded defaults that work in most cases.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `li_at cookie was deleted` | Expired/invalid cookie | Re-extract fresh cookie |
| `unexpected status code 302` | LinkedIn redirecting to login | Cookie missing JSESSIONID |
| `x-li-track is empty, using default` | Warning only | OK to ignore |
| `pageInstance is empty, using default` | Warning only | OK to ignore |

## Storing secrets in Vault

Instead of exporting every time, store in HashiCorp Vault:

```bash
vault kv put kv-v2/cli-envs/linkedin \
  LINKEDIN_COOKIE_HEADER='<cookie>'
```

Then load on demand:

```bash
source ~/scripts/vault-env linkedin
linkedin-dm list
```
