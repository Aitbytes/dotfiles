---
name: wger
description: Operate a wger workout & fitness manager instance via its REST API. Create/read/update/delete workout routines with days, slots, slot entries, progression configs (weight, reps, RIR, rest, sets), log workouts, manage weight entries, nutrition plans with meals, measurement categories & values, gallery images, exercise database, exercise translations, muscles, equipment, licenses, languages, user profiles, and trophies. Supports both legacy token auth and JWT.
---

# wger API Skill

Manage a [wger](https://github.com/wger-project/wger) workout and fitness manager instance via its REST API v2. wger is an open-source fitness application (Python/Django REST Framework) for creating workout routines with automatic weight progression rules, tracking body weight, nutrition plans, measurements, progress photos, and trophies.

## Prerequisites

- `WGER_URL` — base URL of the wger instance (required; no default)
- `WGER_USERNAME` and `WGER_PASSWORD` — admin credentials (required; obtain a token at runtime)
- Alternately: `WGER_TOKEN` — a pre-generated API token, or `WGER_JWT_ACCESS` — a JWT access token

If none are set, ask the user for the URL and credentials.

## References

This file is the index. Detailed instructions are in the references directory — load them on demand when working with specific domains:

- [Authentication & setup](references/auth.md) — Token auth, JWT, helper functions
- [Routines (workouts)](references/routines.md) — Routines, days, slots, slot entries, progression configs, workout sessions, workout logs
- [Weight tracking](references/weight.md) — Body weight entries
- [Nutrition plans](references/nutrition.md) — Nutrition plans, meals, meal items, nutritional values
- [Measurements & gallery](references/measurements.md) — Measurement categories & values, progress photo gallery
- [Exercise database](references/exercises.md) — Exercises, exerciseinfo, translations, categories, muscles, equipment, comments, aliases
- [User profile & utilities](references/profile.md) — Profile, trophies, languages, licenses, registration, permission checks
- [Python helper](references/python-helper.md) — Full `WgerClient` class with all methods

## Quick Start: Build a Routine from Scratch

```bash
TOKEN="<your-token>"
BASE="https://wger.example.com"

# 1. Find exercises
CHEST=$(curl -sk -H "Authorization: Token $TOKEN" "$BASE/api/v2/exercise/?search=bench+press&limit=1" | jq -r '.results[0].id')

# 2. Create routine
R=$(curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$BASE/api/v2/routine/" \
  -d '{"name":"My Routine","description":"A simple plan","start":"2025-06-01","end":"2025-08-31"}' | jq '.id')

# 3. Create day
D=$(curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$BASE/api/v2/day/" \
  -d "{\"routine\":$R,\"name\":\"Upper Body\",\"order\":1}" | jq '.id')

# 4. Create slot
S=$(curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$BASE/api/v2/slot/" \
  -d "{\"day\":$D,\"order\":1,\"comment\":\"Main lift\"}" | jq '.id')

# 5. Create slot entry
E=$(curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$BASE/api/v2/slot-entry/" \
  -d "{\"slot\":$S,\"exercise\":$CHEST,\"order\":1,\"repetition_unit\":1,\"weight_unit\":1}" | jq '.id')

# 6. Set starting weight
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$BASE/api/v2/weight-config/" \
  -d "{\"slot_entry\":$E,\"iteration\":\"1\",\"value\":\"60\",\"operation\":\"r\",\"step\":\"na\",\"repeat\":false}" | jq .

# 7. Add progression: +2.5kg each iteration
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$BASE/api/v2/weight-config/" \
  -d "{\"slot_entry\":$E,\"iteration\":\"2\",\"value\":\"2.5\",\"operation\":\"+\",\"step\":\"abs\",\"repeat\":true}" | jq .

# 8. Log a workout
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$BASE/api/v2/workoutlog/" \
  -d "{\"date\":\"2025-06-02T10:00:00Z\",\"exercise\":$CHEST,\"routine\":$R,\"slot_entry\":$E,\"iteration\":1,\"repetitions_unit\":1,\"repetitions\":\"10\",\"weight_unit\":1,\"weight\":\"60\",\"rir\":\"2\"}" | jq .

# 9. See the workout plan for today
curl -sk -H "Authorization: Token $TOKEN" "$BASE/api/v2/routine/$R/date-sequence-display/" | jq .
```

## Tips

1. **All user-owned data is scoped** — you can only see/edit data belonging to the authenticated user.
2. **SSL certs** — self-hosted instances often use self-signed certs. Always add `-k` / `verify=False`.
3. **Dates** — routine start/end use `YYYY-MM-DD`. Log dates use ISO datetime (`YYYY-MM-DDTHH:MM:SSZ`). Session dates use `YYYY-MM-DD`.
4. **Cascading deletes** — deleting a routine cascades to all days/slots/entries/configs/sessions/logs.
5. **Session auto-creation** — when you POST a workout log, a `WorkoutSession` is auto-created for that date+routine if one doesn't exist.
6. **Config iteration field is a string** — despite being numeric, pass `"iteration":"1"` as a string.
7. **Config replace vs arithmetic** — when `operation:"r"` (replace), set `step:"na"`. When `operation:"+"` or `"-"`, set `step:"abs"` or `step:"percent"`.
8. **User profile update** — use POST to the collection endpoint, not PATCH/PUT on detail.
9. **Pagination** — follows DRF conventions: `"next"`, `"previous"`, `"count"`, `"results"`.
10. **Resource hierarchy** — see [Routines](references/routines.md) for the full tree.
