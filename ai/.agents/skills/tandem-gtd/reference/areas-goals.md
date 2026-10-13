# Areas of Focus & Goals — Full Reference

Load this when you need: managing areas of focus, or goals with horizon-level targeting.

## Areas of Focus

Areas represent ongoing responsibilities (e.g., Health, Finances, Career). They provide a higher-level container for projects and goals.

### Endpoints

```bash
# List areas
GET /api/areas
# Optional: ?active=true

# Create area
POST /api/areas
-d '{"name": "Health", "description": "Exercise, nutrition, checkups", "isActive": true}'

# Get area
GET /api/areas/{id}

# Update area
PATCH /api/areas/{id} -d '{"description": "Updated"}'

# Delete area
DELETE /api/areas/{id}
```

### Linking

Projects and goals can reference an `areaId` to group them under an area of focus.

---

## Goals

Goals are linked to GTD Horizons of Focus levels.

### Horizon Levels

| Level | Scope | Timeframe |
|-------|-------|-----------|
| `RUNWAY` | Current actions/tasks | Now |
| `HORIZON_1` | Current projects | Weeks to months |
| `HORIZON_2` | Areas of focus & accountability | Ongoing |
| `HORIZON_3` | Goals | 1-2 years |
| `HORIZON_4` | Vision | 3-5 years |
| `HORIZON_5` | Purpose & principles | Lifetime |

### Endpoints

```bash
# List goals
GET /api/goals
# Optional: ?horizon=HORIZON_3&status=IN_PROGRESS

# Create goal
POST /api/goals
-d '{"title": "Run a marathon", "horizon": "HORIZON_3", "status": "IN_PROGRESS", "areaId": "<area-id>"}'

# Get goal
GET /api/goals/{id}

# Update goal (e.g., track progress)
PATCH /api/goals/{id} -d '{"progress": 50}'

# Delete goal
DELETE /api/goals/{id}
```
