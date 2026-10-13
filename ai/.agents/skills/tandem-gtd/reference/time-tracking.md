# Time Tracking — Full Reference

Load this when you need: focus timer, time audit entries, or calendar events.

## Timer

Focus timer for tracking time spent on tasks.

```bash
# Start timer on a task
POST /api/timer/start
-d '{"taskId": "<task-id>"}'
# Returns: {"timer": {...}, "startedAt": "..."}

# Get current timer state
GET /api/timer

# Stop timer (returns elapsed, optionally auto-logs to time audit)
POST /api/timer/stop

# Adjust elapsed time
POST /api/timer/adjust
-d '{"adjustedMinutes": 45}'

# Cancel timer (discards elapsed)
POST /api/timer/cancel
```

---

## Time Audit

Track how time is actually spent with tagged entries and challenges.

### Challenges

A challenge is a time-audit session with defined start/end.

```bash
# Start a challenge
POST /api/time-audit/challenges
-d '{"startTime": "2026-06-12T09:00:00.000Z", "endTime": "2026-06-12T17:00:00.000Z"}'

# Get current challenge
GET /api/time-audit/challenges/current

# Update challenge status
PATCH /api/time-audit/challenges/{id}
-d '{"status": "PAUSED"}'
# Status: PAUSED, COMPLETED, ABANDONED
```

### Entries

```bash
# Log a time entry
POST /api/time-audit/entries
-d '{"intervalStart": "2026-06-12T09:00:00.000Z",
     "intervalEnd": "2026-06-12T09:45:00.000Z",
     "tags": ["deep-work", "coding"],
     "note": "Built the API integration",
     "taskId": "<task-id>"}'

# Get entries
GET /api/time-audit/entries
# Optional: ?startDate=2026-06-01&endDate=2026-06-12&tags=deep-work

# Update entry
PATCH /api/time-audit/entries/{id}
-d '{"tags": ["deep-work", "review"]}'

# Delete entry
DELETE /api/time-audit/entries/{id}'
```

### Summary

```bash
# Get time audit summary
GET /api/time-audit/summary
# Optional: ?startDate=...&endDate=...
```

---

## Calendar Events

Time blocking with calendar events linked to tasks.

```bash
# List events
GET /api/calendar/events
# Optional: ?start=...&end=...

# Create event
POST /api/calendar/events
-d '{"title": "Deep work session",
     "start": "2026-06-12T09:00:00.000Z",
     "end": "2026-06-12T11:00:00.000Z",
     "taskId": "<task-id>"}'

# Update event
PATCH /api/calendar/events/{id}

# Delete event
DELETE /api/calendar/events/{id}'
```
