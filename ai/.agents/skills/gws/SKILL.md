---
name: gws
description: "Interact with Google Workspace APIs via the gws CLI. Fetch and modify Gmail, Google Sheets, Drive, Calendar, and more. Use when working with Gmail labels/messages, reading/writing Google Sheets, or any Google Workspace automation."
---

## What I do

Document the `gws` CLI tool (`~/.local/bin/gws`) — a streamlined wrapper around Google Workspace REST APIs. Covers service names, argument conventions, Gmail operations, Sheets operations, and pitfalls learned the hard way.


## Architecture

```
gws <service> <resource> <action> [--params JSON] [--json JSON]
```

- **service**: Google API service name (lowercase, e.g. `gmail`, `sheets`, `drive`)
- **resource**: REST resource path segments (e.g. `users messages get`)
- **action**: HTTP method implied by the verb at the end (`get`, `list`, `create`, `modify`, `append`...)

Parameters are passed as a **JSON string via `--params`**, not as CLI flags.

Request body is passed as a **JSON string via `--json`**.


## Known services

| gws name | Google API |
|---|---|
| `gmail` | Gmail API v1 |
| `sheets` | Google Sheets API v4 |
| `drive` | Google Drive API v3 |
| `calendar` | Calendar API v3 |
| `admin-reports` | Admin SDK Reports |
| `docs` | Google Docs API v1 |
| `slides` | Google Slides API v1 |
| `tasks` | Google Tasks API v1 |
| `people` | People API v1 |
| `chat` | Google Chat API v1 |
| `classroom` | Classroom API v1 |
| `forms` | Google Forms API v1 |
| `keep` | Google Keep API v1 |
| `meet` | Google Meet API v2 |
| `workflow` / `wf` | Workflow (custom) |

For unlisted APIs, use `<api>:<version>` syntax (e.g. `youtube:v3`).

**🚨 Common mistake**: `spreadsheets` is NOT a valid service — use `sheets`.


## Argument conventions

### `--params` — URL/query parameters

All API parameters that would go in the URL path or query string are passed as a single JSON object:

```bash
gws gmail users messages list \
  --params '{"userId": "me", "q": "is:unread", "maxResults": 10}'

gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "abc123", "range": "Sheet1!A1:D10"}'
```

**🚨 Common mistake**: Do NOT pass `--spreadsheetId`, `--range`, etc. as CLI flags. They must be inside `--params '{"spreadsheetId": "...", "range": "..."}'`.

### `--json` — Request body

POST/PUT request bodies are passed via `--json`:

```bash
gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "MyLabel", "labelListVisibility": "labelShow"}'

gws gmail users messages modify \
  --params '{"userId": "me", "id": "msg123"}' \
  --json '{"addLabelIds": ["Label_1"], "removeLabelIds": ["UNREAD"]}'
```

### Output

- **stdout**: JSON response from the API
- **stderr**: Diagnostic noise (keyring backend messages, progress, etc.) — always discard stderr when piping to `jq` or `python3 -c`

```bash
gws ... 2>/dev/null | python3 -c "import json, sys; ..."
```

### Authentication

The tool uses the system keyring for credentials. Expect the first call to print `Using keyring backend: keyring` on stderr. This is normal and harmless.


## Gmail operations

### List messages with search query

```bash
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:example.com is:unread -label:Processed", "labelIds": ["Label_6"], "maxResults": 50}'
```

- `q`: Gmail search syntax (same as the Gmail search box)
- `labelIds`: Filter to messages with specific labels (array of label ID strings)
- `resultSizeEstimate` in response is **unreliable** — always paginate to get the real count

### Get a message (headers only)

```bash
gws gmail users messages get \
  --params '{"userId": "me", "id": "msg123", "format": "metadata", "metadataHeaders": ["Date", "Subject", "From"]}'
```

- `format: "minimal"` — only labelIds
- `format: "metadata"` — headers you request + labelIds
- `format: "full"` — full body (base64url-encoded in payload.parts[].body.data)

### Get a message (full body)

```bash
gws gmail users messages get \
  --params '{"userId": "me", "id": "msg123", "format": "full"}'
```

The body is in `payload.parts[]` as base64url. Decode with:
```python
import base64
decoded = base64.urlsafe_b64decode(data + "===").decode("utf-8", errors="replace")
```

### Modify labels

```bash
gws gmail users messages modify \
  --params '{"userId": "me", "id": "msg123"}' \
  --json '{"addLabelIds": ["Label_2"], "removeLabelIds": ["UNREAD"]}'
```

### List all labels

```bash
gws gmail users labels list --params '{"userId": "me"}'
```

Returns array of `{id, name, type, ...}`. Use this to resolve label names to IDs dynamically.

### Create a label

```bash
gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "MyLabel", "labelListVisibility": "labelShow", "messageListVisibility": "show"}'
```

### Resolving label IDs by name (robust pattern)

Never hardcode label IDs — Gmail labels can be deleted/recreated with new IDs. Instead:

```python
def resolve_label_id(name):
    resp = gws("gmail", "users", "labels", "list",
               "--params", json.dumps({"userId": "me"}),
               timeout=15)
    if not resp:
        return None
    for label in resp.get("labels", []):
        if label.get("name") == name:
            return label["id"]
    return None
```


## Sheets operations

### Read values

```bash
gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "abc123", "range": "Sheet1!A1:D10"}'
```

Returns `{range, majorDimension, values: [[...], ...]}`.

### Append rows

```bash
gws sheets spreadsheets values append \
  --params '{"spreadsheetId": "abc123", "range": "Sheet1!A:L", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["col1", "col2", ...], ...]}'
```

Rows are appended after the last non-empty row in the specified range.

### Count data rows

```python
resp = gws("sheets", "spreadsheets", "values", "get",
           "--params", json.dumps({"spreadsheetId": SHEET_ID, "range": "Sheet1!A:A"}))
n = sum(1 for row in resp.get("values", []) if row)
return max(n - 1, 0)  # subtract header
```


## Pitfalls & lessons learned

1. **Service name**: `sheets` not `spreadsheets`. `gmail` not `gmail/v1`.
2. **Parameters**: Always `--params '{"key": "value"}'`, never `--key value`.
3. **Two JSON flags**: `--params` for URL/query params, `--json` for request body.
4. **Stderr noise**: Always `2>/dev/null` when piping to JSON parsers.
5. **resultSizeEstimate**: Unreliable in Gmail list responses. Paginate for real counts.
6. **Label IDs are ephemeral**: If a label is deleted and recreated, its ID changes. Resolve by name at runtime, don't hardcode.
7. **Message ordering**: `messages.list` returns newest first by default (by `internalDate`).
8. **Gmail filter changes**: If a Gmail filter stops applying a label, the script silently finds nothing. Log which label is being queried.
9. **Base64 decoding**: Gmail body data uses `urlsafe_b64decode`, needs `+ "==="` padding.
10. **EML Date headers**: Use `email.utils.parsedate_to_datetime()` not manual regex — handles all RFC 2822 formats. Times are in the header's timezone (usually UTC).
