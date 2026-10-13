---
name: mealie
description: Interact with the self-hosted Mealie instance (recipes.aitbytes.dev) — search/import recipes, manage on-hand pantry foods, get SuperCook-style recipe suggestions from what you have, manage shopping lists and meal plans. Stdlib-only Python CLI. Auth via Vault (source ~/scripts/vault-env mealie).
---

# mealie

CLI for the self-hosted Mealie instance at `https://recipes.aitbytes.dev`. Wraps the Mealie REST API for an AI agent.

```
source ~/scripts/vault-env mealie      # loads MEALIE_URL + MEALIE_API_KEY (Vault kv-v2/cli-envs/mealie)

mealie whoami                          # identity + household check
mealie suggest --human                 # ⭐ "qu'est-ce que je peux cuisiner ?" (SuperCook-style)
mealie on-hand                         # list on-hand foods (the pantry)
mealie on-hand add tomate oeufs riz    # mark foods as on-hand (created if missing)
mealie on-hand remove tomate
mealie import-url https://...          # scrape + import a recipe from any recipe website
mealie search "bolognaise"             # search recipes
mealie get <slug>                      # full recipe (ingredients + steps)
mealie create --name "X" --ingredients "a|b|c" --steps "1|2"
mealie lists                           # shopping lists
mealie list-add-recipe courses <slug>  # add a recipe's ingredients to the list
mealie list-add courses "sel" "huile"
mealie list-items courses
mealie mealplan --days 7               # this week's meal plan
```

## When to use this skill

- "Qu'est-ce que je peux cuisiner avec ce que j'ai ?" → `mealie suggest --human` (the SuperCook replacement)
- "Ajoute des courgettes et des œufs à mon placard" → `mealie on-hand add courgettes oeufs`
- "Enregistre cette recette" + URL → `mealie import-url <url>` (scrapes schema.org Recipe JSON-LD)
- "Ajoute les ingrédients de la recette X à la liste de courses" → `mealie list-add-recipe courses <slug>`
- "Quel est le plan de repas de la semaine ?" → `mealie mealplan`
- Nutrition/macro questions about a recipe → `mealie get <slug> --raw` (has nutrition when scraped) or cross-check with the `wger` skill

## Architecture

```
~/.agents/skills/mealie/
├── SKILL.md                    # this file
└── scripts/mealie.py           # main CLI — pure stdlib, zero deps
~/.local/bin/mealie             # 3-line bash wrapper → mealie.py
```

## Deployment facts

| What | Value |
|---|---|
| Instance | Mealie `v2.8.0` on **blithe-main** (standalone Docker, behind Traefik/nginx) — NOT on Dokploy |
| URL | `https://mealie.aitbytes.fyi` |
| Admin | `admin` — creds in Vault `kv-v2/blithe/debian003/mealie` (`admin_password`, `agent_api_token`, `seeded_password`) |
| Skill auth | `source ~/scripts/vault-env mealie` loads `kv-v2/cli-envs/mealie` (kept in sync with the path above) |
| Old Dokploy instance | deleted (was recipes.aitbytes.dev, volume mealie-data removed) |

## API notes (learned the hard way)

- Auth: `Authorization: Bearer <api-key>` (long-lived token via `POST /api/users/api-tokens`). Works on both v2 and v3.
- v3 only: **login is form-encoded** (JSON body returns 401). v2.8 accepts JSON login too — the CLI uses the API key, so it doesn't care.
- **Suggestions** = `GET /api/recipes/suggestions?limit&maxMissingFoods&includeFoodsOnHand=true&useHouseholdFoods=true`
  → `items[] {recipe, missingFoods[], missingTools[]}`. Only recipes from **your** library are suggested
  (Mealie ≠ big recipe database: import recipes first, or invent with the LLM and `mealie create`).
- "On hand" foods are **household-scoped** (slug `family`): `PUT /api/foods/{id}` with
  `households_with_ingredient_food: ["family"]`. There is no `onHand` field on foods (same on v2.8 and v3).
- URL import = `POST /api/recipes/create/url` body `{"url": ...}` on BOTH v2.8 and v3 (the old `/create-url`
  path is gone) — can take 10-60s. AI-assisted import exists: `POST /api/recipes/create/ai` (v3).
- Shopping list "add recipe": `POST /api/households/shopping/lists/{id}/recipe` with a **list** body
  `[{"recipeId": ..., "recipeIncrementQuantity": 1, "recipeIngredients": null}]`. Foods marked on-hand
  are skipped unless `recipeIngredients` is provided. Read items via the detail endpoint
  `GET /lists/{id}` — the paginated `GET /lists` returns empty `listItems`.
- Most list endpoints are paginated: `?page=N&perPage=M` → `{items, totalPages}`.
