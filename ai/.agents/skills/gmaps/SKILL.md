---
name: gmaps
description: Google Maps Platform routing and geocoding. Use when the user asks for transit directions (metro, bus, train), real-time traffic-adjusted durations, or rich place search with ratings and opening hours. Requires GOOGLE_MAPS_API_KEY loaded via Vault (source ~/scripts/vault-env google-maps). Stdlib-only Python CLI.
---

# gmaps

Google Maps Platform-backed geocoding, place search and routing. This skill sits alongside the `maps` skill (OSM) and covers exactly what OSM cannot: **transit routing, traffic-aware durations, and Places API rich data**.

The CLI mirrors `maps` exactly — same sub-commands, same flags, same JSON shapes. An agent can call `gmaps directions "Paris" "Lyon" --mode transit` instead of `maps` when public transport matters.

## When to use this skill

- **Transit routing** (metro, bus, train) — the main reason to use `gmaps` over `maps`
- Real-time traffic-adjusted durations (`--departure-time now`)
- Rich place search with ratings, price level, opening hours
- Anything where Google Maps data quality is preferred over OSM

## How it's built

```
~/.agents/skills/gmaps/
├── SKILL.md          # this file
└── scripts/
    └── gmaps.py      # main CLI — pure stdlib, zero deps
```

`~/.local/bin/gmaps` is a 3-line bash wrapper.

## Prerequisites

**This skill requires a Google Maps Platform API key with billing enabled.** OSM (the `maps` skill) works without any setup; Google does not.

### Quick key check

```bash
gmaps provider
# { "api_key_configured": true, "api_key_prefix": "AIzaSy..." }
```

If `api_key_configured` is `false`, the key is not loaded. Source it from Vault:

```bash
source ~/scripts/vault-env google-maps
```

### One-time setup (vault)

After creating your API key in Google Cloud Console:

```bash
vault kv put kv-v2/cli-envs/google-maps GOOGLE_MAPS_API_KEY='AIza...'
```

Then load it in any session:

```bash
source ~/scripts/vault-env google-maps
```

The key is **never stored on disk** — it lives in Vault and is loaded into the shell's RAM on demand via `~/scripts/vault-env`.

### Google Cloud Console setup (one-time)

See the setup guide at the end of this file for a step-by-step walkthrough.

## Quick start

```bash
# All the same operations as `maps`, but with Google quality + transit mode
gmaps geocode "Tokyo Tower" --human --lang fr
gmaps reverse 35.6586 139.7454 --human --lang fr
gmaps search "ramen" --near "Shibuya, Tokyo" --human --lang ja
gmaps directions "Shibuya" "Shinjuku" --mode transit --human
gmaps directions "Paris" "Lyon" --mode driving --departure-time now --human
gmaps distance "Paris" --to "Lyon" "Marseille" --human
gmaps provider
```

## Multi-destination itineraries

```bash
# Road trip with true stopovers (per-leg breakdown + arrival times)
gmaps directions "Paris" "Marseille" --stops "Lyon" "Avignon" \
    --departure-time now --human --lang fr

# Let Google find the best stop order (TSP) — road modes only
gmaps directions "Paris" "Nice" --stops "Marseille" "Lyon" "Avignon" \
    --optimize --human --lang fr

# Full transit itinerary: one transit call per segment, chained automatically
# (--wait = minutes spent at each intermediate stop)
gmaps directions "Paris" "Marseille" --stops "Lyon" --mode transit \
    --wait 90 --human --lang fr
```

Three waypoint flavors on `directions`:

| Flag | Semantics |
|------|-----------|
| `--waypoints A B` | `via:` pass-through points — shape the route, **no stopover**, single leg |
| `--stops A B` | True stopovers — one leg per segment, per-leg distance/duration + arrival times |
| `--optimize` | Google reorders intermediate stops (TSP, road modes only). Requires stops; `--waypoints` are auto-promoted |
| `--wait MIN` | Dwell time at each intermediate stop — shifts the schedule and the next chained transit departure |

## Common flags

| Flag                | Effect                                                       |
|---------------------|--------------------------------------------------------------|
| `--human`           | Pretty-printed text summary instead of JSON                  |
| `--lang fr`         | Result language for display names (fr, en, ja, ...)          |
| `--timeout 30`      | HTTP timeout in seconds (default: 20)                        |

### Directions-specific flags

| Flag                          | Effect                                                       |
|-------------------------------|--------------------------------------------------------------|
| `--mode driving|walking|bicycling|transit` | Travel mode (default: driving)                |
| `--waypoints W1 W2 ...`       | Pass-through waypoints (`via:` — no stopover, single leg)      |
| `--stops S1 S2 ...`           | True stopovers — per-leg breakdown + arrival times             |
| `--optimize`                  | Google reorders intermediate stops (TSP; road modes only)      |
| `--wait MIN`                  | Minutes spent at each intermediate stop                        |
| `--alternatives`              | Return alternative routes                                    |
| `--departure-time now`        | Depart now (enables traffic data + required for transit)      |
| `--departure-time 1234567890` | Depart at specific Unix timestamp                            |

## What `gmaps` adds vs `maps`

| Capability                  | `maps` (OSM)     | `gmaps` (Google)   |
|-----------------------------|------------------|---------------------|
| Geocoding / reverse         | ✅               | ✅ (sometimes better in Asia) |
| Place search                | ✅ name + type  | ✅ name, type, **ratings, ★ reviews, price $$, opening status** |
| Driving / walking directions| ✅               | ✅ (+ traffic with `--departure-time`) |
| Cycling directions          | ✅               | ✅ (`--mode bicycling`) |
| **Transit directions**      | ❌               | ✅ (metro, bus, train, ferry) |
| Real-time traffic           | ❌               | ✅ (`--departure-time now`) |
| Distance matrix             | ✅               | ✅ |
| Free / offline              | ✅               | ❌ (API key + billing required) |

## Output shapes (match `maps` shapes)

```jsonc
// geocode / reverse — identical shape to maps
{
  "lat": 35.6586, "lng": 139.7454,
  "formatted_address": "4 Chome-2-8 Shibakoen, Minato City, Tokyo 105-0011, Japan",
  "place_id": "ChIJlTlj8z-LGGAROoav6aNsO9s",
  "type": "premise",
  "components": {"locality": "Tokyo", "country": "Japan", "postal_code": "105-0011"},
  "provider": "google"
}

// search — richer than maps (ratings, price, opening_hours)
[{
  "name": "Ichiran Shibuya",
  "lat": 35.659, "lng": 139.700,
  "formatted_address": "1-22-7 Jinnan, Shibuya City, Tokyo",
  "type": "restaurant",
  "types": ["restaurant", "food", "point_of_interest"],
  "rating": 4.3,
  "user_ratings_total": 5200,
  "price_level": 2,
  "business_status": "OPERATIONAL",
  "opening_hours": true,
  "provider": "google"
}]

// directions — same shape, with traffic + transit
{
  "provider": "google",
  "mode": "driving",
  "distance_m": 462500,
  "duration_s": 17400,
  "duration_in_traffic_s": 18600,   // null if no traffic data
  "summary": "A6 and A7",
  "origin_address": "Paris, France",
  "destination_address": "Lyon, France",
  "stops": [],                       // --stops (true stopovers)
  "optimized": false,                // true when --optimize applied
  "waypoint_order": null,            // [1,0,...] visiting order of stops (TSP)
  "departure_time_s": 1787996502,    // null unless --departure-time given
  "arrival_time_s": 1788015891,      // final arrival (schedule-aware)
  "chained": false,                  // true for multi-stop transit (API-chained legs)
  "legs": [/* per leg: distance, duration, steps, start/end address,
               departure_time_s, arrival_time_s */],
  "alternatives_available": 2,
  "warnings": [],
  "copyrights": "Map data ©2024",
  "geometry": {"points": "mof~Hqea...encoded polyline..."}
}

// distance — same 2D array shape as maps
{
  "provider": "google",
  "mode": "driving",
  "origins": ["Paris"],
  "destinations": ["Lyon", "Marseille"],
  "durations_s": [[17400, 29600]],
  "distances_m": [[462500, 773000]]
}
```

## How to use both skills together

```bash
# 1. Geocode with either (same output shape)
maps geocode "Tour Eiffel, Paris" --lang fr
gmaps geocode "Tour Eiffel, Paris" --lang fr

# 2. For driving/walking/cycling between French cities: use maps (free)
maps directions "Paris" "Lyon" --mode driving --human --lang fr

# 3. For transit routing: use gmaps (the only option)
gmaps directions "Gare de Lyon" "La Défense" --mode transit --human --lang fr

# 4. For traffic-adjusted duration:
gmaps directions "Paris" "Lyon" --departure-time now --human

# 5. For rich place search:
gmaps search "hôtel 4 étoiles" --near "Tour Eiffel, Paris" --human --lang fr
```

## Google Cloud Console setup

### 1. Create project
→ https://console.cloud.google.com/projectcreate

### 2. Enable billing
⚠ Maps Platform REQUIRES billing. Google gives $200/month free credit.
→ https://console.cloud.google.com/billing

### 3. Enable 4 APIs
For each, search in the library, click, **Enable**.
→ https://console.cloud.google.com/apis/library

| API | Needed for |
|-----|------------|
| **Geocoding API** | geocode / reverse |
| **Directions API** | directions (all modes including transit) |
| **Distance Matrix API** | distance |
| **Places API** | search (text search) |

### 4. Create API key
→ https://console.cloud.google.com/apis/credentials
→ Create credentials → API key
→ **Copy the key** (starts with `AIza...`)
→ Edit key → Restrict to: Geocoding, Directions, Distance Matrix, Places API
→ Save

### 5. Store key in Vault

```bash
vault kv put kv-v2/cli-envs/google-maps GOOGLE_MAPS_API_KEY='AIza...ta_clé...'
```

**Do NOT put this key in a file, config, or commit. Only in Vault.**

### 6. Test

```bash
source ~/scripts/vault-env google-maps
gmaps geocode "Tokyo" --human
# Must show: 📍 35.6762, 139.6503 / Tokyo, Japan / Provider: google
```

## Error handling for agents

| Error class | Trigger | Exit code | Agent should |
|---|---|---|---|
| `ApiKeyError` | Key missing, invalid, or billing not enabled | 3 | Tell user to check billing + key |
| `RateLimitError` | Quota exceeded | 4 | Wait 60s and retry once |
| `NotFoundError` | No result for this query | 1 | Tell user the place/route was not found |
| `MapsError` (other) | Network, parse, or API error | 2 | Report error message to user, try again once |

## Known quirks

1. **Billing is mandatory** — there is no "free tier without billing" for Maps Platform. Google requires a valid billing account and a credit card on record, even if you never exceed the $200 monthly credit.

2. **Transit requires `--departure-time`** — the skill auto-fills `departure_time=now` for transit mode, so `gmaps directions "A" "B" --mode transit` works without explicitly setting it.

3. **Transit + stops = chained API calls** — Google transit directions accept no waypoints, so `--stops` triggers one Directions call per segment (N stops ⇒ N+1 calls, N×Directions pricing). Each segment departs at the previous arrival (+ `--wait`). `duration_s` sums travel time only — waits excluded.

4. **`--optimize` (TSP)** uses Google's own `optimize:true`: origin and destination stay fixed, only intermediate stops are reordered. Result order in `waypoint_order` (indices into the stops list). Road modes only; max 25 stops per request.

5. **Place search is expensive** — Places Text Search costs $32 per 1000 queries (after the $200 credit). Use `maps search` (free OSM) for basic place discovery; use `gmaps search` only when you need ratings, opening hours, or price info.

6. **`--departure-time now` enables traffic** — without this flag, durations are free-flow estimates, identical to `maps`.

7. **Google polyline encoding** — the `geometry.points` field is an encoded polyline string. Use `polyline.decode()` from the `polyline` Python library to decode, or use it directly with Google's static maps API.

8. **Cycling mode** — Google uses `bicycling` (not `cycling`). The `--mode` flag accepts `bicycling` (native) and also `cycling` (aliased internally).

## Empirical evidence

| Query | Expected | Status |
|---|---|---|
| `gmaps geocode "Tokyo Tower"` | 35.6586, 139.7454 | Awaiting API key |
| `gmaps directions "Shibuya" "Shinjuku" --mode transit` | Metro route of ~20 min | Awaiting API key |
| `gmaps search "ramen" --near "Shibuya"` | Restaurants with ratings | Awaiting API key |

> Run these after setting up the API key and storing it in Vault.

## Resources

- `scripts/gmaps.py` — main CLI, stdlib-only
- `scripts/vault-env` — helper that loads secrets from Vault into the shell
- Google Maps Platform docs: <https://developers.google.com/maps/documentation>
- `maps` skill (OSM): `~/.agents/skills/maps/SKILL.md` — companion skill for free geocoding/routing