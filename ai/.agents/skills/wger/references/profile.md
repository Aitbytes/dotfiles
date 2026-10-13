# User Profile & Utilities

User profile management, trophies, languages, licenses, registration, and utility endpoints.

## User Profile

The profile endpoint always returns the currently authenticated user's data.

```bash
# Get profile
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/userprofile/" | jq .

# Update profile (use POST, not PATCH/PUT — it always operates on the current user)
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/userprofile/" \
  -d '{
    "weight_rounding":"2.5",
    "height":180,
    "weight_unit":"kg",
    "gender":"1",
    "age":30,
    "calories":2800
  }' | jq .
```

**Profile fields:**

| Field | Type | Description |
|-------|------|-------------|
| `username` | string | Read-only |
| `email` | string | Must be unique |
| `email_verified` | bool | Read-only |
| `date_joined` | datetime | Read-only |
| `gym` | int | Gym ID the user belongs to |
| `is_trustworthy` | bool | Trusted contributor flag |
| `is_temporary` | bool | Temporary/demo account |
| `height` | int | Height in cm |
| `age` | int | Age in years |
| `birthdate` | date | Date of birth |
| `gender` | string | `"1"` = Male, `"2"` = Female |
| `weight_unit` | string | `"kg"` or `"lb"` |
| `weight_rounding` | decimal | How much to round weights (e.g. `"2.5"`) |
| `repetitions_rounding` | decimal | How much to round reps |
| `calories` | int | Daily calorie goal |
| `sleep_hours` | int | Hours of sleep |
| `work_hours` | int | Work hours per day |
| `work_intensity` | string | `"1"`=Low, `"2"`=Medium, `"3"`=High |
| `sport_hours` | int | Sport/exercise hours |
| `sport_intensity` | string | `"1"`/`"2"`/`"3"` |
| `freetime_hours` | int | Free time hours |
| `freetime_intensity` | string | `"1"`/`"2"`/`"3"` |
| `show_comments` | bool | Show exercise comments |
| `show_english_ingredients` | bool | Show ingredients in English |
| `ro_access` | bool | Read-only API access only |
| `num_days_weight_reminder` | int | Days between weight reminders (0=off) |
| `workout_reminder_active` | bool | Enable workout reminders |
| `workout_reminder` | int | Reminder interval in days |
| `workout_duration` | int | Expected workout time in minutes |
| `notification_language` | int | Language ID for notifications |

## Trophies

Wger includes a gamification system with 21 trophy types tracking workout streaks, volume, consistency, etc.

```bash
# All trophy definitions
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/trophy/" | jq .

# Trophy progress for current user (earned status, progress %, target values)
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/trophy/progress/" | jq .

# User's earned trophies
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/user-trophy/" | jq .

# User statistics (total weight lifted, workout count, streaks, etc.)
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/user-statistics/" | jq .
```

User statistics response:

```json
{
  "id": 1,
  "total_weight_lifted": "15000.00",
  "total_workouts": 42,
  "current_streak": 7,
  "longest_streak": 21,
  "last_workout_date": "2025-06-15",
  "earliest_workout_time": "05:30:00",
  "latest_workout_time": "22:00:00",
  "weekend_workout_streak": 3,
  "worked_out_jan_1": true,
  "last_updated": "2025-06-15T10:00:00+02:00"
}
```

## Languages

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/language/" | jq '.results'
```

Returns 20 languages with `id`, `short_name` (e.g. `"en"`, `"de"`), `full_name` (native), `full_name_en` (English name).

Common language IDs: 1=German, 2=English, 4=Spanish, 12=French, 13=Italian.

## Licenses

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/license/" | jq '.results'
```

| id | short_name | URL |
|----|-----------|-----|
| 1 | CC-BY-SA 3 | creativecommons.org |
| 2 | CC-BY-SA 4 | creativecommons.org |
| 3 | CC0 | creativecommons.org |
| 4 | CC-BY 4 | creativecommons.org |
| 5 | ODbL | opendatacommons.org |

## Registration

```bash
curl -sk -X POST -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/register/" \
  -d '{"username":"newuser","email":"user@example.com","password":"strongPass123"}' | jq .
```

Returns `{"message":"api user successfully registered","token":"..."}` on success, or `{"message":"Registration is not allowed on this instance"}` if disabled.

## Utility Endpoints

```bash
# Server version
curl -sk "$WGER_URL/api/v2/version/"
# Response: "2.6.0a2"

# Check if authenticated user has a specific Django permission
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/check-permission/?permission=exercises.add_exercise" | jq .
# Response: {"result": true} or {"result": false}

# Verify email address
curl -sk -X GET -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/userprofile/verify-email/" | jq .
# Response: {"status":"sent","message":"A verification email was sent to user@example.com"}

# Language detection for exercise descriptions
curl -sk -X POST -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/check-language/" \
  -d '{"language":2,"input":"This is an English exercise description for bench press"}' | jq .
# Response: {"result": true} or validation error with detected language
```
