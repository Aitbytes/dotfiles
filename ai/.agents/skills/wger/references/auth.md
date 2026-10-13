# Authentication & Setup

wger API v2 supports two authentication methods. **Prefer JWT** for new integrations. All requests must include an `Authorization` header.

## Token Auth (legacy)

```bash
# Login to obtain token
curl -sk -X POST "$WGER_URL/api/v2/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"'"$WGER_USERNAME"'","password":"'"$WGER_PASSWORD"'"}'
# Response: {"token":"2bb7d72..."}

# Use token in all subsequent requests
curl -sk -H "Authorization: Token $WGER_TOKEN" "$WGER_URL/api/v2/..."
```

The `/api/v2/login/` endpoint returns a DRF token. Tokens never expire but can be regenerated from the web UI under User → API Key.

## JWT Auth (recommended)

```bash
# Obtain JWT pair (access + refresh)
curl -sk -X POST "$WGER_URL/api/v2/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"'"$WGER_USERNAME"'","password":"'"$WGER_PASSWORD"'"}'
# Response: {"access":"eyJ...","refresh":"eyJ..."}

# Use access token
curl -sk -H "Authorization: Bearer $WGER_JWT_ACCESS" "$WGER_URL/api/v2/..."

# Refresh the access token when it expires
curl -sk -X POST "$WGER_URL/api/v2/token/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh":"'"$WGER_JWT_REFRESH"'"}'

# Verify a token is still valid
curl -sk -X POST "$WGER_URL/api/v2/token/verify" \
  -H "Content-Type: application/json" \
  -d '{"token":"'"$WGER_JWT_ACCESS"'"}'
```

Access tokens expire after a configurable duration (typically 10 minutes). Refresh tokens last much longer.

## SSL Certificate Handling

Self-hosted wger instances commonly use self-signed certificates. Use `-k` with curl or `verify=False` with Python requests:

```bash
curl -sk https://...
```

```python
import requests
requests.post(url, json=data, verify=False)
```

## Quick Discovery

```bash
# Check server version
curl -sk "$WGER_URL/api/v2/version/"

# List available exercises, categories, muscles, equipment
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercisecategory/" | jq '.results'
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/muscle/" | jq '.results'
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/equipment/" | jq '.results'

# List languages and licenses
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/language/" | jq '.results'
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/license/" | jq '.results'

# List weight and repetition units
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/setting-weightunit/" | jq '.results'
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/setting-repetitionunit/" | jq '.results'
```

## Repetition Units Reference

| id | Name | unit_type |
|----|------|-----------|
| 1 | Repetitions | REPETITIONS |
| 2 | Until Failure | REPETITIONS |
| 3 | Seconds | TIME |
| 4 | Minutes | TIME |
| 5 | Miles | DISTANCE |
| 6 | Kilometers | DISTANCE |
| 7 | Max Reps | REPETITIONS |
| 8 | Meters | DISTANCE |

## Weight Units Reference

| id | Name |
|----|------|
| 1 | kg |
| 2 | lb |
| 3 | Body Weight |
| 4 | Plates |
| 5 | Kilometers Per Hour |
| 6 | Miles Per Hour |

## Response Format

All list endpoints follow standard DRF pagination:

```json
{
  "count": 846,
  "next": "https://...?limit=20&offset=20",
  "previous": null,
  "results": [...]
}
```

Use `?limit=N` to control page size and follow `"next"` URLs for pagination.
