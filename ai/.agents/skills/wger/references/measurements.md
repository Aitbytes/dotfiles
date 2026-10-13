# Measurements & Gallery

Body measurement tracking and progress photo gallery.

## Measurement Categories

Define what you want to measure (Chest, Waist, Bicep, etc.):

```bash
# List
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/measurement-category/" | jq .

# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/measurement-category/" \
  -d '{"name":"Chest","unit":"cm"}' | jq .

# Delete
curl -sk -X DELETE -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/measurement-category/1/"
```

**Fields:** `name`, `unit` (e.g. `"cm"`, `"in"`, `"kg"`).

## Measurements

Record values for each category:

```bash
# List
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/measurement/" | jq .

# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/measurement/" \
  -d '{"category":1,"date":"2025-06-15","value":105.5,"notes":"Flexed after pump"}' | jq .

# Filter by category
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/measurement/?category=1" | jq .

# Filter by date range
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/measurement/?date__gte=2025-01-01&date__lte=2025-06-01" | jq .

# Delete
curl -sk -X DELETE -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/measurement/1/"
```

**Fields:** `category` (required), `date` (required, YYYY-MM-DD), `value` (0–5000, 2 decimal places), `notes`.

## Gallery (Progress Photos)

Upload and manage progress photos. Uses multipart form data:

```bash
# List photos
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/gallery/" | jq .

# Upload
curl -sk -X POST -H "Authorization: Token $TOKEN" \
  -F "image=@/path/to/photo.jpg" \
  -F "date=2025-06-15" \
  -F "description=Front relaxed, morning" \
  "$WGER_URL/api/v2/gallery/" | jq .

# Update description (PATCH)
curl -sk -X PATCH -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/gallery/1/" \
  -d '{"description":"Updated description"}' | jq .

# Delete
curl -sk -X DELETE -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/gallery/1/"
```

**Fields:** `image` (file upload), `date` (YYYY-MM-DD), `description`. `height` and `width` are auto-detected on upload.

**Filters:** `id`, `date`, `description`.
