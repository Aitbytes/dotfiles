# Weight Tracking

Track body weight over time with dated entries.

## CRUD

```bash
# List weight entries
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/weightentry/" | jq .

# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/weightentry/" \
  -d '{"date":"2025-06-15T08:00:00Z","weight":82.5}' | jq .

# Delete
curl -sk -X DELETE -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/weightentry/1/"
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Auto-assigned |
| `date` | datetime | When the weight was recorded |
| `weight` | decimal | Weight value (30–600 kg/lb, 2 decimal places) |
| `user` | int | Read-only, auto-set from auth |

## Filtering

All fields support Django filter lookups:

```bash
# Date range
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/weightentry/?date__gte=2025-01-01&date__lte=2025-12-31" | jq .

# Weight above threshold
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/weightentry/?weight__gte=80" | jq .

# Multiple IDs
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/weightentry/?id__in=1,2,3" | jq .
```

Supported lookups: `exact`, `in` (for id), `gt`, `gte`, `lt`, `lte` (for weight and date).
