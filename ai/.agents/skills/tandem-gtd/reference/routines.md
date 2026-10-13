# Routines — Full Reference

Load this when you need: habit tracking, supplement protocols, cron-scheduled routines with windows and items.

Routines are recurring card-file routines with cron scheduling, time windows, and per-item tracking.

## Endpoints

```bash
# List routines
GET /api/routines

# Create routine
POST /api/routines

# Get routine
GET /api/routines/{id}

# Update routine
PATCH /api/routines/{id}

# Delete routine
DELETE /api/routines/{id}
```

## Create Routine — Full Example

```bash
POST /api/routines
-d '{
  "title": "Morning Routine",
  "description": "Daily morning habits",
  "cronExpression": "daily",
  "estimatedMins": 30,
  "windows": [
    {
      "title": "Morning Supplements",
      "targetTime": "08:00",
      "sortOrder": 0,
      "constraint": "empty_stomach",
      "items": [
        {"name": "Vitamin D", "dosage": "2000 IU", "form": "softgel", "sortOrder": 0},
        {"name": "Magnesium", "dosage": "400mg", "form": "capsule", "sortOrder": 1,
         "rampSchedule": {"type": "step", "steps": [
           {"fromDay": 1, "toDay": 7, "dosage": "200mg"},
           {"fromDay": 8, "toDay": 14, "dosage": "400mg"}
         ]}}
      ]
    }
  ]
}'
```

## Routine Fields

| Field | Description |
|-------|-------------|
| `title` | Routine name |
| `description` | Optional description |
| `cronExpression` | `daily`, `weekdays`, `weekly:1` (1=Monday), etc. |
| `routineType` | `static` (default) or `dynamic` (protocol) |
| `estimatedMins` | Estimated duration |
| `windows` | Array of time windows |
| `windows[].title` | Window name |
| `windows[].targetTime` | Target time (HH:MM) |
| `windows[].sortOrder` | Display order |
| `windows[].constraint` | e.g., `empty_stomach`, `with_food` |
| `windows[].items` | Array of items to track |

## Item Forms

`capsule`, `softgel`, `tablet`, `powder`, `liquid`, `gummy`, `patch`, `injection`

## Ramp Schedules

Items can have a `rampSchedule` of type `step` with an array of `{fromDay, toDay, dosage}` steps. This gradually increases dosage over time.

## Logging

```bash
# Log window completion
POST /api/routines/{id}/log
-d '{"windowId": "<window-id>", "date": "2026-06-12", "status": "completed"}'

# Toggle individual item in a log
PATCH /api/routines/{id}/log
-d '{"windowId": "<window-id>", "date": "2026-06-12", "itemId": "<item-id>", "taken": true}'
```
