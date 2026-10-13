# Routines, Days, Slots & Workout Logging

## Resource Hierarchy

```
Routine (workout plan)
 └── Day (training day, ordered within routine)
      └── Slot (exercise group; multiple entries = superset)
           └── SlotEntry (one exercise + units + configs)
                ├── WeightConfig / MaxWeightConfig
                ├── RepetitionsConfig / MaxRepetitionsConfig
                ├── RiRConfig / MaxRiRConfig
                ├── RestConfig / MaxRestConfig
                └── SetsConfig / MaxSetsConfig

WorkoutSession (one session per date + routine)
 └── WorkoutLog (one log entry per exercise set)
```

## Routines

A Routine is a workout plan spanning a date range (max 120 days).

### CRUD

```bash
# List
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/" | jq .

# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/routine/" \
  -d '{"name":"Push Pull Legs","description":"3-day split","start":"2025-06-01","end":"2025-08-31"}' | jq .

# Update (PATCH)
curl -sk -X PATCH -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/routine/1/" \
  -d '{"description":"Updated plan"}' | jq .

# Delete (cascades to all children)
curl -sk -X DELETE -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/1/"
```

**Fields:** `name` (max 25 chars), `description` (max 1000), `start` (date), `end` (date, ≤120 days after start), `fit_in_week` (bool), `is_template` (bool), `is_public` (bool; requires `is_template=true`).

### Routine sub-actions

```bash
# Full structure: days → slots → entries → all configs recursively
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/1/structure/" | jq .

# Date sequence for display mode (merged same-exercise sets across slots)
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/1/date-sequence-display/" | jq .

# Date sequence for gym mode (separate slots as-is)
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/1/date-sequence-gym/" | jq .

# Workout logs grouped by session
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/1/logs/" | jq .

# Statistics: volume, intensity, sets by iteration/week/day/mesocycle
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/1/stats/" | jq .
```

The `date-sequence-*` endpoints return the full workout plan with calculated values (weight/reps/RIR/rest) mapped to each calendar date across the routine's duration.

The `stats` endpoint returns rich statistics:
- `intensity` — average intensity per exercise/muscle/body-region grouped by iteration, week, day, and mesocycle
- `volume` — total volume (weight × reps) grouped by the same dimensions
- `sets` — set count grouped by the same dimensions

### Templates & Publicoutines

```bash
# My templates
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/templates/" | jq .

# Public templates
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/public-templates/" | jq .

# Make a routine a template
curl -sk -X PATCH -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/routine/1/" -d '{"is_template":true}' | jq .
```

Templates are frozen routines you can copy. Set `is_public=true` to share with other users (requires `is_template=true`).

## Days

```bash
# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/day/" \
  -d '{"routine":1,"name":"Push Day","description":"Chest, Shoulders, Triceps","order":1}' | jq .

# Delete
curl -sk -X DELETE -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/day/1/"
```

**Fields:** `routine` (required), `order`, `name`, `description`, `is_rest` (bool — rest days have no exercises; setting this to true deletes all slots), `need_logs_to_advance` (bool — user must log a session before the next day in the sequence), `type` (one of: `custom`, `enom`, `amrap`, `hiit`, `tabata`, `edt`, `rft`, `afap`), `config` (JSON, nullable).

## Slots

A Slot groups one or more exercises together. Multiple entries in one slot = superset.

```bash
# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/slot/" \
  -d '{"day":1,"order":1,"comment":"Chest exercises"}' | jq .
```

**Fields:** `day` (required), `order`, `comment`, `config` (JSON, nullable).

## Slot Entries

A SlotEntry connects an exercise to a slot with weight/repetition unit settings and progression configs.

```bash
# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/slot-entry/" \
  -d '{
    "slot":1,
    "exercise":562,
    "order":1,
    "repetition_unit":1,
    "weight_unit":1,
    "type":"normal",
    "comment":"Flat bench press"
  }' | jq .
```

**Fields:** `slot` (required), `exercise` (required), `order`, `type` (exercise type, default `"normal"`):

| Type value | Meaning |
|------------|---------|
| `normal` | Standard set |
| `warmup` | Warm-up set |
| `dropset` | Drop set |
| `myo` | Myo-reps |
| `partial` | Partial reps |
| `forced` | Forced reps |
| `tut` | Time Under Tension |
| `iso` | Iso-hold |
| `jump` | Jump set |

`repetition_unit`, `repetition_rounding`, `weight_unit`, `weight_rounding`, `comment`, `config` (JSON), `class_name` (custom python progression class name, overrides all other configs).

## Progression Configs

Each SlotEntry can have up to 10 config types (5 base + 5 max variants). Configs define how weight, reps, RIR, rest, and sets change across iterations.

### Config endpoints

| Endpoint | Purpose |
|----------|---------|
| `/api/v2/weight-config/` | Target weight per iteration |
| `/api/v2/max-weight-config/` | Max weight cap per iteration |
| `/api/v2/repetitions-config/` | Target reps per iteration |
| `/api/v2/max-repetitions-config/` | Max reps cap per iteration |
| `/api/v2/rir-config/` | Target RIR per iteration |
| `/api/v2/max-rir-config/` | Max RIR per iteration |
| `/api/v2/rest-config/` | Target rest (seconds) per iteration |
| `/api/v2/max-rest-config/` | Max rest per iteration |
| `/api/v2/sets-config/` | Target sets per iteration |
| `/api/v2/max-sets-config/` | Max sets per iteration |

### Common config fields

| Field | Type | Description |
|-------|------|-------------|
| `slot_entry` | int | Required. References a slot entry |
| `iteration` | string | When this config activates (e.g. `"1"`, `"2"`, `"3"`) |
| `value` | string | The value as a decimal string (e.g. `"40.00"`, `"2.5"`) |
| `operation` | string | `"+"` = add, `"-"` = subtract, `"r"` = replace |
| `step` | string | `"abs"` = absolute amount, `"percent"` = % of current, `"na"` = N/A (use with replace) |
| `repeat` | bool | If true, repeats this config on all subsequent iterations |
| `requirements` | JSON | Min values logs must meet for this iteration to activate (see below) |

**Critical rule:** When `operation` is `"r"` (replace), always use `"step":"na"`. When `operation` is `"+"` or `"-"`, use `"step":"abs"` (add/subtract fixed amount) or `"step":"percent"` (add/subtract percentage of current value).

### Creating configs

```bash
# Set starting weight to 60kg at iteration 1 (replace)
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/weight-config/" \
  -d '{"slot_entry":1,"iteration":"1","value":"60","operation":"r","step":"na","repeat":false}' | jq .

# Add 2 reps at iteration 2
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/repetitions-config/" \
  -d '{"slot_entry":1,"iteration":"2","value":"2","operation":"+","step":"abs","repeat":false}' | jq .

# Add 5% weight every subsequent iteration from 3 onward
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/weight-config/" \
  -d '{"slot_entry":1,"iteration":"3","value":"5","operation":"+","step":"percent","repeat":true}' | jq .

# Set RIR to 3 at iteration 1
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/rir-config/" \
  -d '{"slot_entry":1,"iteration":"1","value":"3","operation":"r","step":"na","repeat":false}' | jq .
```

### Requirements

The `requirements` field enables conditional progression — configs only activate when previous logs meet minimum values. Pass a JSON object like:

```json
{
  "rules": {
    "weight": true
  }
}
```

This means: "only activate this config if the weight logged in the previous iteration meets or exceeds the target weight." Multiple rules can be combined.

### Progression logic

The system evaluates configs iteration by iteration:
1. For each iteration, it checks which configs apply (based on `iteration` field + `repeat`).
2. If a config has `requirements`, it checks if the previous iteration's logs meet them.
3. If requirements are met (or none exist), the config is applied.
4. Configs are applied in sequence: replace first, then add/subtract.

## Workout Sessions

Sessions are auto-created when logs reference a new date+routine combination. You can also create them explicitly:

```bash
# Create session with notes and timing
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/workoutsession/" \
  -d '{
    "routine":1,
    "day":1,
    "date":"2025-06-15",
    "notes":"Felt strong today",
    "impression":"3",
    "time_start":"09:00",
    "time_end":"10:15"
  }' | jq .
```

**Fields:** `routine`, `day` (optional), `date` (YYYY-MM-DD), `notes`, `impression` (`"1"`=Bad, `"2"`=Neutral, `"3"`=Good), `time_start`, `time_end` (HH:MM).

**Note about date format:** Sessions use `YYYY-MM-DD`, not ISO datetime. Using ISO datetime will return a validation error.

## Workout Logs

Log each individual set of an exercise. A session is auto-created for the date+routine combination if none exists.

```bash
# Log a set
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/workoutlog/" \
  -d '{
    "date":"2025-06-15T09:30:00Z",
    "exercise":562,
    "routine":1,
    "slot_entry":1,
    "iteration":1,
    "repetitions_unit":1,
    "repetitions":"10",
    "weight_unit":1,
    "weight":"60",
    "rir":"2",
    "rest":90
  }' | jq .
```

**Fields:** `date` (ISO datetime), `exercise`, `routine`, `session` (read-only, auto-set), `slot_entry`, `iteration`, `repetitions_unit`, `repetitions`, `repetitions_target`, `weight_unit`, `weight`, `weight_target`, `rir` (0–9.9), `rir_target`, `rest` (seconds), `rest_target`, `next_log` (chain another log for drop-sets/myo-reps).

**Constraint:** At least one of `repetitions` or `weight` must be non-null. The `iteration` field ties logs to routine day iterations and drives progression calculations.

## Listing & Filtering

Most endpoints support standard Django filter fields. Examples:

```bash
# Filter routines by name
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/routine/?name=Push" | jq .

# Filter workout logs by session
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/workoutlog/?session=1" | jq .

# Filter days by routine
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/day/?routine=1" | jq .
```

Use `?limit=N` to control page size (default varies by endpoint).
