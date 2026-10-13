---
name: maps
description: Geocoding, place search and routing via OpenStreetMap. Lookup addresses/POIs, compute trajectories (driving, walking, cycling), get distance matrices. Stdlib-only Python CLI (urllib.request, json, argparse). No API key, no account, no third-party packages.
---

# maps

Geocoding, place search and routing for an AI agent. The CLI wraps OpenStreetMap (Nominatim for geocoding + OSRM for routing) and exposes a small set of commands the agent can run from any sandboxed shell.

```
maps geocode "Tour Eiffel, Paris"      # address → lat/lng
maps reverse 48.8584 2.2945            # lat/lng → address
maps search "café" --near "Paris"      # text search for places
maps directions "Paris" "Lyon" --mode driving
maps distance "Paris" --to "Lyon" "Marseille"
maps provider                          # show backend info
```

Always returns JSON by default; `--human` for a readable summary.

## When to use this skill

- "Find the coordinates of X"
- "What's the address at lat,lng?"
- "Find restaurants/hotels/stations near X"
- "How do I get from A to B by car/bike/walking?"
- "How long does it take between A and B?" (and the matrix variant with several origins/destinations)
- Any combination of the above in a single research trip

## How it's built

```
~/.agents/skills/maps/
├── SKILL.md                          # this file
└── scripts/
    ├── maps.py                       # main CLI — pure stdlib, zero deps
    └── alternative-requests.py       # same CLI using `requests` (for comparison)
```

`~/.local/bin/maps` is a 3-line bash wrapper around `maps.py`, so `maps <cmd>` works from anywhere.

## Backend: OpenStreetMap

| Service             | Used for                          | Endpoint                              |
|---------------------|-----------------------------------|----------------------------------------|
| Nominatim           | Geocoding, reverse, place search  | `nominatim.openstreetmap.org`          |
| OSRM demo           | Routing (route + table)           | `router.project-osrm.org`              |

**No API key, no billing, no account.** The cost is a strict 1 request/second rate limit on Nominatim (handled internally by the CLI).

### What OSM doesn't do (vs Google Maps)

- **Transit routing** (bus, metro, train) — OSM/OSRM only supports driving, walking, cycling. If the user asks for a metro trip, the skill will return a clear error and suggest using Google Maps directly.
- **Real-time traffic-adjusted durations** — durations are based on free-flow speed.
- **Places details** (ratings, opening hours, photos) — Nominatim returns type and classification but not Google Places rich data.

For everything else (geocoding, routing, distance matrices, search), OSM is excellent.

## Quick start

```bash
# Geocode an address
maps geocode "Tour Eiffel, Paris" --human --lang fr

# Reverse geocode coordinates (e.g. from a GPS reading)
maps reverse 48.8584 2.2945 --human --lang fr

# Search for POIs (text search with location bias)
maps search "café" --near "Paris" --human --lang fr

# Driving directions with optional waypoints and alternatives
maps directions "Paris" "Lyon" --mode driving --alternatives

# Walking or cycling
maps directions "Notre-Dame" "Sainte-Chapelle" --mode walking

# Distance/duration matrix
maps distance "Paris" "Lyon" --to "Marseille" "Nice"

# Always JSON-friendly for parsing
maps geocode "Tokyo Tower" | jq -r '.lat,.lng,.formatted_address'
```

## Common flags

| Flag           | Effect                                                       |
|----------------|--------------------------------------------------------------|
| `--human`      | Pretty-printed text summary instead of JSON                  |
| `--lang fr`    | Result language for display names (fr, en, de, es, ...)      |
| `--timeout 30` | HTTP timeout in seconds (default: 20)                        |

## Output shapes

```jsonc
// geocode / reverse — single object
{
  "lat": 48.8583, "lng": 2.2945,
  "formatted_address": "Tour Eiffel, 5 Avenue Anatole France, 75007 Paris, France",
  "place_id": "...",
  "type": "tower",
  "components": { "city": "Paris", "country": "France", "postcode": "75007" },
  "provider": "osm"
}

// search — array of objects
[ { "name": "...", "lat": ..., "lng": ..., "formatted_address": "...", "type": "...", "provider": "osm" }, ... ]

// directions — single object with legs and steps
{
  "provider": "osm",
  "mode": "driving",
  "distance_m": 462500,
  "duration_s": 17700,
  "summary": "via A6",
  "legs": [ { "distance_m": ..., "duration_s": ..., "steps": [ /* turn-by-turn */ ] } ],
  "alternatives_available": 1
}

// distance — single object
{
  "provider": "osm",
  "mode": "driving",
  "origins": ["Paris, France"],
  "destinations": ["Lyon, France", "Marseille, France"],
  "durations_s": [[17700, 29500]],
  "distances_m": [[462500, 773000]]
}
```

## Design choice: stdlib-only vs third-party

This skill ships with **two implementations** of the same CLI so the trade-off is concrete and runnable.

### Side-by-side: same operation, two ways

```python
# ── maps.py (default, stdlib only) ──────────────────────────────
import urllib.request, urllib.parse, json
from urllib.error import HTTPError, URLError

def http_get_json(url: str, params: dict, headers: dict | None = None):
    merged = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if headers:
        merged.update(headers)
    full = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(full, headers=merged)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        raise ProviderError(f"HTTP {e.code} {full}: {body}") from e
    except URLError as e:
        raise ProviderError(f"Network error for {full}: {e.reason}") from e
    except TimeoutError as e:
        raise ProviderError(f"Timeout after 20s: {full}") from e
    except json.JSONDecodeError as e:
        raise ProviderError(f"Non-JSON response from {full}: {e}") from e
```

```python
# ── alternative-requests.py (comparison) ───────────────────────
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
session.mount("https://", HTTPAdapter(
    max_retries=Retry(total=3, backoff_factor=0.5,
                      status_forcelist=(429, 500, 502, 503, 504),
                      allowed_methods=frozenset(["GET"])),
    pool_connections=4, pool_maxsize=4,
))

def http_get_json(url: str, params: dict, headers: dict | None = None):
    r = session.get(url, params=params, headers=headers, timeout=20)
    r.raise_for_status()  # HTTPError on 4xx/5xx with body attached
    return r.json()
```

### Trade-off summary

| Aspect                        | stdlib (`maps.py`)                                | `requests` (`alternative-requests.py`)            |
|-------------------------------|---------------------------------------------------|---------------------------------------------------|
| **Runtime dependencies**      | **0** — runs on a fresh Python install            | 1 (`requests`, which itself pulls `urllib3`, `certifi`, `charset-normalizer`, `idna`) |
| **Code size (this skill)**    | ~480 lines                                        | ~130 lines (~3.7× shorter)                        |
| **Connection pooling**        | Manual (`http.client` per call)                   | Automatic via `Session`                           |
| **Retries**                   | Manual try/except loop                            | Built-in `urllib3.util.retry.Retry`                |
| **Error body capture**        | Manual `e.read().decode()`                        | `r.raise_for_status()` then `r.text`              |
| **Streaming uploads**         | Awkward                                          | First-class (`files=`, `data=`, `json=`)          |
| **Async**                     | No                                                | No (use `httpx` if you need that)                 |
| **Header management**         | Manual merge dict                                 | `Session.headers.update(...)`                      |
| **JSON encoding**             | Manual `json.dumps()` + `.encode()`               | `json=` kwarg auto-handles                         |
| **Standardisation**           | PEP-style stdlib                                  | De facto industry standard                        |
| **Skill discoverability**     | Works in any sandboxed agent                      | Works wherever `requests` is installed             |

### When to use which

**Pick stdlib (`maps.py`)** when:
- The skill is shipped to many environments and you don't control dependencies
- The agent runs in a sandbox where installing packages is slow or blocked
- Operations are one-off or low-frequency (no need for connection pooling)
- You want the code to outlive the current Python ecosystem

**Pick `requests` (or `httpx`)** when:
- You're inside an existing project that already uses `requests`
- You need connection pooling, retries, or streaming
- You're doing high-volume batch geocoding and the per-call overhead matters
- You want clearer stack traces and a more "Pythonic" feel

The skill **does not ship `requests` as a runtime dep** — the alternative file is kept only as a reference and a benchmark. If you want to switch, install `requests` and replace `~/.local/bin/maps` with a wrapper that invokes `alternative-requests.py`:

```bash
# ~/.local/bin/maps (requests-based variant)
exec uv run --with requests --python 3.11 \
    python3 "$HOME/.agents/skills/maps/scripts/alternative-requests.py" "$@"
```

## Pitfalls and lessons learned

1. **Nominatim usage policy**: max 1 request per second, mandatory User-Agent identifying the application. The skill spaces requests by 1.1s and sets `User-Agent: pi-maps-skill/1.0`. Set `MAPS_NO_THROTTLE=1` only against your own Nominatim/OSRM instance.

2. **Nominatim bug** with `limit=1 + accept-language=en + addressdetails=1`: returns an empty array for many queries that should match (including "Paris"). Workaround baked into `maps.py`: use `limit=5` and take the first result. Don't be tempted to lower the limit to "be polite" — the bug triggers specifically at limit=1.

3. **Nominatim ambiguity**: queries like `Paris` can return results in Texas, Ontario, Île-de-France, etc. Prefer `Paris, France` or `Paris, Île-de-France`. The skill falls back to a simpler query if the first one fails, so `"Paris, France"` → `"Paris"` if needed.

4. **OSRM is routing-only, not transit**: `--mode transit` is not supported by this skill. Use Google Maps for transit routing (metro, bus, train).

5. **Static maps**: not implemented in this skill. For a static image URL, hit Google's `maps.googleapis.com/maps/api/staticmap` directly with the coords returned by `geocode`.

6. **Multiple legs**: when using `--waypoints`, the resulting `legs[]` array contains one entry per leg (origin→wp1, wp1→wp2, ..., last_wp→destination). Sum the distances/durations if you want the trip total.

7. **Rate-limit cooldown**: if you get many "Could not geocode" errors back-to-back on queries you know are valid (e.g. `Berlin`, `Tokyo`), wait 30–60 seconds. The OSM public servers are stricter than the documented 1 req/s after bursts.

8. **Language of results**: use `--lang fr` to get French display names. The Nominatim `accept-language` parameter accepts comma-separated fallbacks like `fr,en`.

9. **Self-hosted alternative**: for high-volume use, host your own Nominatim (https://github.com/mediagis/nominatim-docker) and OSRM (http://project-osrm.org) and override `Geocoder.NOMINATIM` / `Geocoder.OSRM` class attributes, or `MAPS_NO_THROTTLE=1` against your own instance.

## Empirical evidence

Verified end-to-end against the live OSM stack:

| Query                                      | Result                                            | Verdict          |
|--------------------------------------------|---------------------------------------------------|------------------|
| `maps geocode "Tour Eiffel, Paris"`        | 48.8583, 2.2945, "Tour Eiffel, 5 Avenue Anatole France, 75007 Paris, France" | ✅ matches Google |
| `maps reverse 48.8584 2.2945`              | "Avenue Gustave Eiffel, 75007 Paris, France"      | ✅ exact street  |
| `maps directions "Paris, France" "Lyon, France" --mode driving` | 462.5 km, 4h 55m via A6            | ✅ matches Google (≈463 km / 4h30–5h) |
| `maps distance "Paris" --to "Lyon" "Marseille"` | 462.5 km/4h55m, 773.0 km/8h14m              | ✅ within 1% of reference |
| `maps directions "Paris" "Marseille" --waypoints "Lyon"` | 776.5 km, 8h 23m                  | ✅ ≈ Paris→Lyon + Lyon→Marseille |
| `maps search "café" --near "Paris"`        | 10 Paris cafés returned                            | ✅ relevant      |
| `maps provider`                            | `{ "backend": "OpenStreetMap", "modes": [...] }`   | ✅               |
| `uv run --with requests python3 alternative-requests.py geocode "Berlin"` | 52.517, 13.395 (matches maps.py) | ✅ both impls agree |
| `maps directions "A" "B" --mode transit`   | error: "Transit routing is not supported by this skill" | ✅ clear error |

## Resources

- `scripts/maps.py` — main CLI, stdlib-only
- `scripts/alternative-requests.py` — same operations with `requests`, for reference
- Nominatim usage policy: <https://operations.osmfoundation.org/policies/nominatim/>
- OSRM demo server: <https://project-osrm.org>
- Nominatim self-host: <https://github.com/mediagis/nominatim-docker>
- OSRM self-host: <http://project-osrm.org>