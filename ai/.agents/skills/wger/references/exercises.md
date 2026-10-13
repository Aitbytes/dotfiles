# Exercise Database

The wger exercise database is read-only via the API (write access requires special permissions). It contains exercises with multilingual translations, muscle targeting, equipment requirements, images, videos, and community comments.

## Exercise Categories

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercisecategory/" | jq '.results'
```

Common categories (may vary by instance):

| id | Name      |
|----|-----------|
| 10 | Abs       |
| 8  | Arms      |
| 12 | Back      |
| 14 | Calves    |
| 11 | Chest     |
| 9  | Legs      |
| 13 | Shoulders |
| 15 | Trunk     |

## Muscles

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/muscle/" | jq '.results'
```

Returns muscle objects with `id`, `name`, `name_en`, `is_front` (bool), and SVG image URLs (`image_url_main`, `image_url_secondary`). 16 muscles total.

## Equipment

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/equipment/" | jq '.results'
```

Common equipment IDs: 1=Barbell, 8=Bench, 10=None (bodyweight), etc. 11 types total.

## Exercises

```bash
# List all (paginated, ~846 exercises on a typical instance)
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercise/?limit=20" | jq .

# Filter by category
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercise/?category=10&limit=10" | jq .

# Filter by muscles
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercise/?muscles=2" | jq .

# Filter by equipment
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercise/?equipment=1" | jq .

# Search by name
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercise/?search=squat&limit=5" | jq .

# Combine filters: chest exercises with barbell
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/exercise/?category=11&equipment=1&limit=10" | jq .
```

Exercise response includes `id`, `uuid`, `created`, `last_update`, `category`, `muscles` (array), `muscles_secondary` (array), `equipment` (array), `variation_group`, `license_author`.

## ExerciseInfo (detailed view)

Returns nested data with translations, muscles (with SVG URLs), images, videos, comments, and aliases:

```bash
# List
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exerciseinfo/?limit=10" | jq .

# Single
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exerciseinfo/562/" | jq .

# Search
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/exerciseinfo/?search=bench+press&limit=3" | jq .

# Filter by category (with nesting)
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/exerciseinfo/?category=10&limit=5" | jq .
```

The info response includes:
- `category`: nested `{id, name}`
- `muscles` / `muscles_secondary`: arrays with `{id, name, name_en, is_front, image_url_main, image_url_secondary}`
- `equipment`: array of `{id, name}`
- `license`: `{id, full_name, short_name, url}`
- `translations`: array of `{id, uuid, name, description, language, aliases, notes}`
- `images`: array of image objects
- `videos`: array of `{id, uuid, url, is_main, exercise, size}`
- `author_history`: array of author names

## Exercise Translations

Translations provide names and descriptions in different languages:

```bash
# List
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercise-translation/?limit=10" | jq .

# Search by name
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/exercise-translation/?search=bench+press&limit=3" | jq .
```

**Fields:** `id`, `uuid`, `name`, `description`, `exercise`, `language`, `created`, `license`, `license_author`, `aliases`, `notes`.

## Exercise Images

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exerciseimage/?limit=10" | jq .
```

## Exercise Videos

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/video/?limit=10" | jq .
```

## Exercise Comments

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercisecomment/?limit=10" | jq .
```

## Exercise Aliases

Alternative names for exercises (e.g. "Military Press" for "Shoulder Press"):

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/exercisealias/?limit=10" | jq .
```