#!/usr/bin/env python3
"""mealie — CLI for a self-hosted Mealie instance.

Recipes, on-hand pantry, SuperCook-style suggestions, shopping lists.
Pure stdlib (urllib, json, argparse). No third-party deps.

Auth: MEALIE_URL + MEALIE_API_KEY env vars — load with: source ~/scripts/vault-env mealie
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("MEALIE_URL", "").rstrip("/")
KEY = os.environ.get("MEALIE_API_KEY", "")


def _req(method, path, body=None, params=None, timeout=90):
    if not BASE or not KEY:
        sys.exit("MEALIE_URL / MEALIE_API_KEY not set — run: source ~/scripts/vault-env mealie")
    url = f"{BASE}/api{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:300]
        sys.exit(f"HTTP {e.code} on {method} {path}: {detail}")


def _paginate(path, extra=None, per_page=100):
    items, page = [], 1
    while True:
        data = _req("GET", path, params={"perPage": per_page, "page": page, **(extra or {})})
        items += data.get("items", [])
        if page >= data.get("totalPages", 1):
            return items
        page += 1


def _household_slug():
    return _req("GET", "/households/self")["slug"]


# ── whoami ────────────────────────────────────────────────────────────────
def cmd_whoami(_):
    user = _req("GET", "/users/self")
    hh = _req("GET", "/households/self")
    print(json.dumps({"user": user.get("username"), "admin": user.get("admin"),
                      "household": hh.get("name"), "slug": hh.get("slug"), "url": BASE}))


# ── recipes ───────────────────────────────────────────────────────────────
def cmd_search(args):
    items = _paginate("/recipes", {"search": args.query}) if args.query else _paginate("/recipes")
    items = items[:args.limit]
    print(json.dumps([{"slug": r["slug"], "name": r["name"], "tags": [t["name"] for t in r.get("tags", [])]}
                      for r in items], indent=2, ensure_ascii=False))


def cmd_get(args):
    recipe = _req("GET", f"/recipes/{urllib.parse.quote(args.slug)}")
    if args.raw:
        print(json.dumps(recipe, indent=2, ensure_ascii=False))
        return
    out = {
        "slug": recipe.get("slug"),
        "name": recipe.get("name"),
        "servings": recipe.get("recipeServings"),
        "totalTime": recipe.get("totalTime"),
        "ingredients": [{"quantity": i.get("quantity"), "unit": (i.get("unit") or {}).get("name"),
                         "food": (i.get("food") or {}).get("name"), "note": i.get("note")}
                        for i in recipe.get("recipeIngredient", [])],
        "steps": [s.get("text") for s in recipe.get("recipeInstructions", [])],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


def cmd_import_url(args):
    slug = _req("POST", "/recipes/create/url", {"url": args.url}, timeout=120)
    print(json.dumps({"imported": True, "slug": slug}))
    if args.show:
        cmd_get(argparse.Namespace(slug=slug if isinstance(slug, str) else slug.get("slug"), raw=False))


def cmd_create(args):
    body = {"name": args.name}
    if args.ingredients:
        body["recipeIngredient"] = [{"note": line} for line in args.ingredients.split("|")]
    if args.steps:
        body["recipeInstructions"] = [{"text": s} for s in args.steps.split("|")]
    slug = _req("POST", "/recipes", body)
    print(json.dumps({"created": True, "slug": slug}))


# ── on-hand pantry ────────────────────────────────────────────────────────
def _find_food(name):
    name = name.strip().lower()
    foods = _paginate("/foods")
    for f in foods:
        if f.get("name", "").strip().lower() == name:
            return f
    return None


def _set_on_hand(food, on_hand):
    hh = _household_slug()
    households = [hh] if on_hand else []
    body = {"id": food["id"], "name": food["name"], "households_with_ingredient_food": households}
    return _req("PUT", f"/foods/{food['id']}", body)


def cmd_on_hand(args):
    if args.action in ("list", None):
        hh = _household_slug()
        on_hand = [f["name"] for f in _paginate("/foods")
                   if hh in (f.get("householdsWithIngredientFood") or [])]
        print(json.dumps({"onHand": sorted(on_hand)}, indent=2, ensure_ascii=False))
        return
    results = []
    for name in args.names:
        food = _find_food(name)
        if not food:
            food = _req("POST", "/foods", {"name": name.strip()})
        updated = _set_on_hand(food, args.action == "add")
        results.append({"food": updated.get("name"), "onHand": args.action == "add"})
    print(json.dumps(results, indent=2, ensure_ascii=False))


# ── suggestions (SuperCook-style) ─────────────────────────────────────────
def cmd_suggest(args):
    data = _req("GET", "/recipes/suggestions", params={
        "limit": args.limit, "maxMissingFoods": args.max_missing,
        "includeFoodsOnHand": "true", "useHouseholdFoods": "true",
    })
    out = [{"slug": it["recipe"]["slug"], "name": it["recipe"]["name"],
            "missing": [f["name"] for f in it.get("missingFoods", [])],
            "missingTools": [t["name"] for t in it.get("missingTools", [])]}
           for it in data.get("items", [])]
    if args.human:
        for i, r in enumerate(out, 1):
            missing = f"  (manque: {', '.join(r['missing'])})" if r["missing"] else "  ✔ tout est là"
            print(f"{i}. {r['name']}{missing}")
        if not out:
            print("Aucune suggestion — ajoute des aliments: mealie on-hand add tomate oeufs riz")
    else:
        print(json.dumps(out, indent=2, ensure_ascii=False))


# ── shopping lists ────────────────────────────────────────────────────────
def _resolve_list(ref):
    lists = _paginate("/households/shopping/lists")
    for l in lists:
        if l["id"] == ref or l.get("name", "").lower() == ref.lower():
            return l
    if lists:
        return lists[0]
    return _req("POST", "/households/shopping/lists", {"name": ref})


def cmd_lists(_):
    print(json.dumps([{"id": l["id"], "name": l["name"]}
                      for l in _paginate("/households/shopping/lists")], indent=2, ensure_ascii=False))


def cmd_list_items(args):
    l = _resolve_list(args.list)
    full = _req("GET", f"/households/shopping/lists/{l['id']}")
    print(json.dumps({"list": full["name"], "items": [
        {"note": i.get("note") or (i.get("food") or {}).get("name"), "checked": i.get("checked"),
         "quantity": i.get("quantity")} for i in (full.get("listItems") or [])]}, indent=2, ensure_ascii=False))


def cmd_list_add(args):
    l = _resolve_list(args.list)
    items = [{"shoppingListId": l["id"], "note": n, "checked": False} for n in args.items]
    _req("POST", "/households/shopping/items/create-many", {"items": items})
    print(json.dumps({"added": len(items), "list": l["name"]}))


def cmd_list_add_recipe(args):
    l = _resolve_list(args.list)
    recipe = _req("GET", f"/recipes/{urllib.parse.quote(args.slug)}")
    _req("POST", f"/households/shopping/lists/{l['id']}/recipe",
         [{"recipeId": recipe["id"], "recipeIncrementQuantity": 1, "recipeIngredients": None}])
    print(json.dumps({"added": recipe["name"], "list": l["name"]}))


# ── mealplan ──────────────────────────────────────────────────────────────
def cmd_mealplan(args):
    data = _req("GET", "/households/mealplans", params={"start": args.start, "limit": args.days})
    print(json.dumps([{"date": m.get("date"), "mealType": m.get("entryType"),
                       "slug": (m.get("recipe") or {}).get("slug")}
                      for m in (data if isinstance(data, list) else data.get("items", []))],
                     indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(prog="mealie", description="Self-hosted Mealie CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami").set_defaults(fn=cmd_whoami)

    p = sub.add_parser("search", help="search recipes")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("get", help="full recipe by slug")
    p.add_argument("slug")
    p.add_argument("--raw", action="store_true")
    p.set_defaults(fn=cmd_get)

    p = sub.add_parser("import-url", help="scrape + import a recipe from a website")
    p.add_argument("url")
    p.add_argument("--show", action="store_true")
    p.set_defaults(fn=cmd_import_url)

    p = sub.add_parser("create", help="create a recipe manually")
    p.add_argument("--name", required=True)
    p.add_argument("--ingredients", help="pipe-separated notes")
    p.add_argument("--steps", help="pipe-separated steps")
    p.set_defaults(fn=cmd_create)

    p = sub.add_parser("on-hand", help="list/add/remove on-hand foods")
    p.add_argument("action", nargs="?", choices=["list", "add", "remove"], default="list")
    p.add_argument("names", nargs="*")
    p.set_defaults(fn=cmd_on_hand)

    p = sub.add_parser("suggest", help="recipes from what you have (SuperCook-style)")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--max-missing", type=int, default=5)
    p.add_argument("--human", action="store_true")
    p.set_defaults(fn=cmd_suggest)

    sub.add_parser("lists").set_defaults(fn=cmd_lists)
    p = sub.add_parser("list-items")
    p.add_argument("list", help="list id or name (defaults to first list)")
    p.set_defaults(fn=cmd_list_items)
    p = sub.add_parser("list-add")
    p.add_argument("list")
    p.add_argument("items", nargs="+")
    p.set_defaults(fn=cmd_list_add)
    p = sub.add_parser("list-add-recipe")
    p.add_argument("list")
    p.add_argument("slug")
    p.set_defaults(fn=cmd_list_add_recipe)

    p = sub.add_parser("mealplan")
    p.add_argument("--start", default="")
    p.add_argument("--days", type=int, default=7)
    p.set_defaults(fn=cmd_mealplan)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
