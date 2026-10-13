# Nutrition Plans

Manage nutrition plans with meals, meal items, and nutritional value calculations.

## Resource Hierarchy

```
NutritionPlan
 └── Meal (breakfast, lunch, etc.)
      └── MealItem (ingredient + amount + weight unit)

NutritionDiary (log item — consumed ingredient on a date)
```

## Nutrition Plans

```bash
# List
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/nutritionplan/" | jq .

# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/nutritionplan/" \
  -d '{
    "description":"Cutting Plan",
    "goal_energy":2000,
    "goal_protein":160,
    "goal_carbohydrates":150,
    "goal_fat":55,
    "goal_fiber":25
  }' | jq .

# Update (PATCH)
curl -sk -X PATCH -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/nutritionplan/1/" \
  -d '{"goal_energy":2200}' | jq .

# Delete
curl -sk -X DELETE -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/nutritionplan/1/"
```

**Fields:** `description`, `start` (date), `end` (date or null for ongoing), `only_logging` (bool — just log food without structured meals), `goal_energy` (kcal), `goal_protein` (g), `goal_carbohydrates` (g), `goal_fat` (g), `goal_fiber` (g).

### Nutrition Plan Info

Returns the full plan with nested meals, meal items, and nutritional values:

```bash
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/nutritionplaninfo/" | jq .
```

### Nutritional Values

```bash
# Total for the full plan
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/nutritionplan/1/nutritional_values/" | jq .

# Total for a single meal
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/meal/1/nutritional_values/" | jq .
```

Response format for nutritional values:

```json
{
  "energy": 450.0,
  "protein": 35.0,
  "carbohydrates": 50.0,
  "carbohydrates_sugar": null,
  "fat": 12.0,
  "fat_saturated": null,
  "fiber": null,
  "sodium": null
}
```

## Meals

```bash
# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/meal/" \
  -d '{"plan":1,"time":"08:00","name":"Breakfast"}' | jq .

# Update
curl -sk -X PATCH -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/meal/1/" \
  -d '{"name":"Big Breakfast","time":"07:30"}' | jq .

# Delete
curl -sk -X DELETE -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/meal/1/"
```

**Fields:** `plan` (required), `time` (HH:MM:SS), `name`, `order` (auto-assigned).

## Meal Items

Add an ingredient to a meal:

```bash
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/mealitem/" \
  -d '{"meal":1,"ingredient":123,"amount":200,"weight_unit":null}' | jq .
```

**Fields:** `meal` (required), `ingredient` (required — must be a valid ingredient ID from the database), `amount` (grams or scaled by weight_unit), `weight_unit` (ingredient weight unit ID, or null for default 100g). `order` is auto-assigned.

**Critical:** The `ingredient` ID must exist in the instance's ingredient database. If the instance has no ingredients loaded (fresh install without Open Food Facts ingestion), this will fail with `"Invalid pk \"...\" - object does not exist."`.

### Nutritional Values for a Meal Item

```bash
curl -sk -H "Authorization: Token $TOKEN" \
  "$WGER_URL/api/v2/mealitem/1/nutritional_values/" | jq .
```

## Nutrition Diary (Log Items)

Log consumed food/ingredients on specific dates:

```bash
# List
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/nutritiondiary/" | jq .

# Create
curl -sk -X POST -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" \
  "$WGER_URL/api/v2/nutritiondiary/" \
  -d '{"plan":1,"meal":1,"datetime":"2025-06-15T12:00:00Z","amount":150,"ingredient":123}' | jq .
```

## Ingredient Database

```bash
# List ingredients (may be empty on fresh installs)
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/ingredient/?limit=10" | jq .

# Detailed info (nested weight units, images, etc.)
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/ingredientinfo/?limit=10" | jq .

# Ingredient weight units
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/ingredientweightunit/" | jq .

# Ingredient images
curl -sk -H "Authorization: Token $TOKEN" "$WGER_URL/api/v2/ingredient-image/" | jq .
```

The ingredient database is typically populated from Open Food Facts. On a fresh install with no ingredients, nutrition plan functionality (meal items, diary) will be limited to plans and meals only.