# Projects — Full Reference

Load this when you need: sub-projects, baselines, project templates, create-with-tasks, or the full project field reference.

## Full Project Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Required, 1-200 chars |
| `description` | string\|null | |
| `type` | enum | `SEQUENTIAL`, `PARALLEL`, `SINGLE_ACTIONS` |
| `childType` | enum | `SEQUENTIAL`, `PARALLEL` (for sub-projects) |
| `status` | enum | `ACTIVE`, `ON_HOLD`, `COMPLETED`, `DROPPED`, `SOMEDAY_MAYBE` |
| `outcome` | string\|null | Desired outcome |
| `areaId` | string\|null | Area of focus |
| `goalId` | string\|null | Linked goal |
| `teamId` | string\|null | Team ownership |
| `isSomedayMaybe` | boolean | Archived someday/maybe |
| `startDate` | string\|null | |
| `endDate` | string\|null | |
| `version` | int | Optimistic concurrency |

## CRUD Endpoints

```bash
# List projects
GET /api/projects
# Optional: ?status=ACTIVE&areaId=<id>&someday=true

# Create project
POST /api/projects
-d '{"title": "Redesign website", "type": "SEQUENTIAL", "outcome": "New site live"}'

# Create with initial tasks
POST /api/projects/create-with-tasks
-d '{"title": "Website Launch", "tasks": [{"title": "Design mockups"}, {"title": "Develop"}]}'

# Get/update/delete
GET /api/projects/{id}
PATCH /api/projects/{id} -d '{"status": "COMPLETED", "version": 1}'
DELETE /api/projects/{id}

# Tasks within a project
GET /api/projects/{id}/tasks
POST /api/projects/{id}/tasks -d '{"title": "New task"}'

# Full tree view
GET /api/projects/outline
```

## Sub-Projects

```bash
# Create child project
POST /api/projects/{id}/children -d '{"title": "Phase 1", "type": "SEQUENTIAL"}'

# Reorder children
PATCH /api/projects/{id}/children/reorder -d '{"childIds": ["id1", "id2"]}'

# Move project to a different parent
PATCH /api/projects/{id}/move -d '{"newParentId": "<parent-id>"}'
```

## Baselines

Snapshot a project at a point in time for progress tracking.

```bash
# View current baseline
GET /api/projects/{id}/baseline

# Create a baseline
POST /api/projects/{id}/baseline -d '{"name": "Q2 Baseline"}'

# Project history
GET /api/projects/{id}/history
```

## Project Templates

Reusable project blueprints with pre-defined tasks.

```bash
# List templates
GET /api/project-templates

# Create template
POST /api/project-templates
-d '{"title": "Website Launch",
     "description": "Standard website launch checklist",
     "type": "SEQUENTIAL",
     "taskTemplates": [
       {"title": "Design mockups", "estimatedMins": 120},
       {"title": "Develop frontend", "estimatedMins": 480},
       {"title": "QA testing", "estimatedMins": 240}
     ]}'

# Get template
GET /api/project-templates/{id}

# Create project from template
POST /api/project-templates/{id}/instantiate
-d '{"variables": {}}'

# Save existing project as template
POST /api/projects/{id}/save-as-template
-d '{"title": "My Template", "teamId": "<optional-team-id>"}'

# Hide/unhide template
POST /api/project-templates/{id}/hide
DELETE /api/project-templates/{id}/hide

# Delete template
DELETE /api/project-templates/{id}
```
