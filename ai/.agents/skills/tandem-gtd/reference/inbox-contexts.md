# Inbox & Contexts — Full Reference

Load this when you need: full inbox operations beyond capture, inbox filtering, or context CRUD with custom fields.

## Inbox

The GTD inbox captures unprocessed thoughts. Items can be processed into tasks, projects, or discarded.

### Endpoints

```bash
# List inbox items
GET /api/inbox
# Optional query: ?status=UNPROCESSED|PROCESSED|all

# Capture an item
POST /api/inbox
-d '{"content": "Fix the leaking faucet", "notes": "Under the kitchen sink"}'
# Optional fields: externalLinkUrl, externalLinkLabel, sourceLabel

# Update an item
PATCH /api/inbox/{id} -d '{"content": "Updated content"}'

# Process item (marks as PROCESSED — this is the GTD "clarify" step)
POST /api/inbox/{id}/process
-d '{"decision": "actionable"}'
# -> creates a TASK from the item (isNextAction=true); response includes {task}

POST /api/inbox/{id}/process
-d '{"decision": "not_actionable", "disposition": "trash"|"someday"|"reference"}'
# -> someday creates a SOMEDAY MAYBE project; trash/reference just file the item

# ⚠️ Body is REQUIRED. Calling POST /api/inbox/{id}/process without a body
# crashes the handler with HTTP 500. The CLI (fixed 2026-10-26) sends it:
#   tandem inbox process <id>                                          # actionable
#   tandem inbox process <id> --decision not_actionable --disposition trash

# Delete
DELETE /api/inbox/{id}
```

### Inbox Workflow

1. `POST /api/inbox` — dump thoughts (sourceLabel helps track origin)
2. `GET /api/inbox?status=UNPROCESSED` — review uncategorized items
3. `POST /api/inbox/{id}/process` — clarify and mark as processed
4. During processing, create tasks/projects from the inbox item content

---

## Contexts

GTD contexts tag where/when a task can be done (e.g., `@Computer`, `@Phone`). Auto-seeded with defaults on first access.

### Default Contexts

`@Computer`, `@Phone`, `@Office`, `@Home`, `@Errands`, `@Anywhere`, `@Agenda`

### Endpoints

```bash
# List all contexts (includes default + custom)
GET /api/contexts

# Create a custom context
POST /api/contexts
-d '{"name": "@Garden", "color": "#22C55E", "icon": "🌿"}'

# Update context
PATCH /api/contexts/{id} -d '{"name": "@Yard", "color": "#84CC16"}'

# Delete context
DELETE /api/contexts/{id}
```

### Using Contexts

To filter tasks by context, first get the context ID from `GET /api/contexts`, then use:

```bash
GET /api/tasks?contextId=<context-id>&status=NOT_STARTED
```
