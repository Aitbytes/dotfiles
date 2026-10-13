# Tasks — Full Reference

Load this when you need: task dependencies, history/snapshots, bulk operations, NLP parsing, or the full task field reference.

## Full Task Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Required, 1-500 chars |
| `notes` | string | Optional markdown notes |
| `status` | enum | `NOT_STARTED`, `IN_PROGRESS`, `WAITING`, `COMPLETED`, `DROPPED` |
| `projectId` | string\|null | Parent project |
| `contextId` | string\|null | GTD context (e.g. `@Computer`) |
| `estimatedMins` | int\|null | Estimated time in minutes |
| `energyLevel` | enum\|null | `LOW`, `MEDIUM`, `HIGH` |
| `scheduledDate` | string\|null | When to work on it |
| `dueDate` | string\|null | Deadline |
| `isNextAction` | boolean | Marked as next action |
| `isMilestone` | boolean | Is a milestone |
| `percentComplete` | int | 0-100 |
| `actualMinutes` | int\|null | Tracked actual time |
| `version` | int | Optimistic concurrency version |
| `externalLinkUrl` | string\|null | URL reference |
| `externalLinkLabel` | string\|null | URL label |

## List Tasks — Query Parameters

```bash
GET /api/tasks
```

| Param | Description |
|-------|-------------|
| `projectId` | Filter by project |
| `contextId` | Filter by context |
| `status` | Filter by status |
| `isNextAction=true` | Only next actions |
| `due=today` | Due today |
| `due=tomorrow` | Due tomorrow |
| `due=overdue` | Past due |
| `due=YYYY-MM-DD` | Due on specific date |
| `dueBefore` | Due before date |
| `dueAfter` | Due after date |
| `scheduled` | Scheduled for date |
| `scheduledBefore` | Scheduled before date |
| `scheduledAfter` | Scheduled after date |

## CRUD Endpoints

```bash
# Create
POST /api/tasks
-d '{"title": "Call dentist", "contextId": "<ctx-id>", "energyLevel": "LOW", "estimatedMins": 15}'

# Update (PATCH with id in body + version)
PATCH /api/tasks
-d '{"id": "<task-id>", "status": "COMPLETED", "version": 1}'

# Delete
DELETE "/api/tasks?id=<task-id>"
```

## Complete / Uncomplete

```bash
# Mark complete (triggers cascade to unblock successors)
POST /api/tasks/{id}/complete

# Revert completion
POST /api/tasks/{id}/uncomplete
```

## Available & Tickler

```bash
# Tasks that are not deferred and not blocked
GET /api/tasks/available

# Deferred/tickler tasks
GET /api/tasks/tickler
```

## Bulk Operations

```bash
# Bulk update
PATCH /api/tasks/bulk
-d '{"ids": ["id1", "id2"], "updates": {"status": "COMPLETED"}}'

# Bulk delete
DELETE /api/tasks/bulk
-d '{"ids": ["id1", "id2"]}'
```

## Natural Language Parsing

Parse natural language into task fields:

```bash
POST /api/tasks/parse
-d '{"text": "Call dentist tomorrow @Phone high energy 15min"}'
```

Returns structured task fields extracted from the text.

## Task Dependencies

Create predecessor/successor relationships between tasks.

```bash
# List dependencies for a task
GET /api/tasks/{id}/dependencies

# Add a dependency (this task depends on predecessor)
POST /api/tasks/{id}/dependencies
-d '{"predecessorId": "<other-task-id>", "type": "FINISH_TO_START", "lagMinutes": 0}'
```

**Dependency types:**
- `FINISH_TO_START` — Predecessor must finish before this starts
- `START_TO_START` — Predecessor must start before this starts
- `FINISH_TO_FINISH` — Predecessor must finish before this finishes
- `START_TO_FINISH` — Predecessor must start before this finishes

## Task History & Snapshots

```bash
# Change history for a task
GET /api/tasks/{id}/history

# Snapshots (restore points)
GET /api/tasks/{id}/snapshots

# Cascade trace (what happened when completing)
GET /api/tasks/{id}/cascade-trace

# Revert to a snapshot
POST /api/tasks/{id}/revert
-d '{"snapshotId": "<snap-id>"}'
```
