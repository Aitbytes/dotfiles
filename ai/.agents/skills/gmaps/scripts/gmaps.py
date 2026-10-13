#!/usr/bin/env python3
"""
gmaps — geocoding, place search and routing (Google Maps Platform).

Pure Python standard-library implementation. Backend: Google Maps Platform
(Geocoding, Directions, Distance Matrix, Places APIs). Requires a valid
GOOGLE_MAPS_API_KEY env var (loaded via Vault — see SKILL.md).

Sub-commands
------------
    gmaps geocode    <address>                       -> {lat,lng,address,...}
    gmaps reverse    <lat> <lng>                     -> {lat,lng,address,...}
    gmaps search     <query> [--near <place>]        -> [place, place, ...]
    gmaps directions <origin> <destination>          -> {distance,duration,steps,...}
                        [--mode driving|walking|bicycling|transit]
                        [--waypoints W1 W2 ...]      (via: pass-through, one leg)
                        [--stops S1 S2 ...]          (true stopovers, per-leg)
                        [--optimize]                 (Google reorders stops, TSP)
                        [--wait MIN]                 (dwell time per stop)
                        [--alternatives]
                        [--departure-time now|<unix_ts>]
    gmaps distance   <origin1> <origin2> ... --to D1 D2 ...
                                                    -> matrix
    gmaps provider                                  -> backend info

Common flags
------------
    --human      Human-readable output instead of JSON.
    --lang fr|en Result language (default: en).
    --timeout N  HTTP timeout in seconds (default: 20).

Requires:  GOOGLE_MAPS_API_KEY  env var (store in Vault, never on disk).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENT = "pi-gmaps-skill/1.0 (+https://github.com/local/pi-gmaps)"
DEFAULT_TIMEOUT = 20
BASE_URL = "https://maps.googleapis.com/maps/api"
VALID_MODES = ("driving", "walking", "bicycling", "transit")
GOOGLE_MODE_MAP = {"driving": "driving", "walking": "walking",
                   "cycling": "bicycling", "bicycling": "bicycling",
                   "transit": "transit"}


# ---------------------------------------------------------------------------
# API key
# ---------------------------------------------------------------------------


def _get_api_key() -> str:
    key = os.environ.get("GOOGLE_MAPS_API_KEY") or os.environ.get("GMAPS_API_KEY")
    if not key:
        raise MapsError(
            "GOOGLE_MAPS_API_KEY is not set. Load it via:\n"
            "  source ~/scripts/vault-env google-maps\n"
            "See SKILL.md for Google Cloud Console setup instructions.")
    return key


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class MapsError(Exception):
    """Base error for the gmaps skill."""


class NotFoundError(MapsError):
    """The backend returned no result."""


class ApiKeyError(MapsError):
    """API key is missing, invalid, or billing is not enabled."""


class RateLimitError(MapsError):
    """Quota exceeded."""


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------


def http_get_json(url: str, params: dict,
                  timeout: float | None = None) -> Any:
    """GET a Google Maps API endpoint and return the parsed JSON body.

    Raises the appropriate MapsError subclass on failure.
    """
    if timeout is None:
        timeout = DEFAULT_TIMEOUT
    params = {**params, "key": _get_api_key()}
    full = f"{url}?{urllib.parse.urlencode(params)}"
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    req = urllib.request.Request(full, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise RateLimitError(f"Quota exceeded for {url}")
        body = e.read().decode("utf-8", errors="replace")[:300]
        raise MapsError(f"HTTP {e.code} {url}: {body}") from e
    except urllib.error.URLError as e:
        raise MapsError(f"Network error for {url}: {e.reason}") from e
    except TimeoutError as e:
        raise MapsError(f"Timeout after {timeout}s: {url}") from e
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise MapsError(f"Non-JSON response from {url}: {e}") from e
    status = data.get("status", "")
    if status == "OK":
        return data
    if status == "ZERO_RESULTS":
        return data  # caller checks data["results"] / data["routes"]
    if status == "REQUEST_DENIED":
        msg = data.get("error_message", "Request denied")
        if "billing" in msg.lower() or ("not enabled" in msg.lower()):
            raise ApiKeyError(
                f"Billing not enabled for this project: {msg}\n"
                "Enable billing at https://console.cloud.google.com/billing")
        raise ApiKeyError(f"API key denied: {msg}")
    if status == "OVER_QUERY_LIMIT":
        raise RateLimitError("Quota exceeded. Wait and retry, or check "
                             "Google Cloud Console quotas.")
    if status == "INVALID_REQUEST":
        raise MapsError(f"Invalid request: {data.get('error_message', status)}")
    # UNKNOWN_ERROR, NOT_FOUND (Places), etc.
    raise MapsError(f"Google API error: {status} — "
                    f"{data.get('error_message', 'no details')}")


# ---------------------------------------------------------------------------
# Google Maps Geocoder
# ---------------------------------------------------------------------------


class Geocoder:
    """Google Maps Platform-backed geocoder and router."""

    @staticmethod
    def _normalize_geocode(r: dict) -> dict:
        comps = {}
        for c in r.get("address_components", []):
            for t in c.get("types", []):
                comps[t] = c["long_name"]
        return {
            "lat": r["geometry"]["location"]["lat"],
            "lng": r["geometry"]["location"]["lng"],
            "formatted_address": r.get("formatted_address"),
            "place_id": r.get("place_id"),
            "type": (r.get("types") or [""])[0],
            "components": comps,
            "provider": "google",
        }

    # -- geocoding -----------------------------------------------------------

    def geocode(self, address: str, lang: str = "en") -> dict | None:
        data = http_get_json(f"{BASE_URL}/geocode/json", {
            "address": address, "language": lang,
        })
        results = data.get("results", [])
        return self._normalize_geocode(results[0]) if results else None

    def reverse(self, lat: float, lng: float, lang: str = "en") -> dict | None:
        data = http_get_json(f"{BASE_URL}/geocode/json", {
            "latlng": f"{lat},{lng}", "language": lang,
        })
        results = data.get("results", [])
        return self._normalize_geocode(results[0]) if results else None

    def search(self, query: str, near: str | None = None,
               lang: str = "en") -> list[dict]:
        params: dict[str, str] = {"query": query, "language": lang}
        if near:
            # Bias results near a location — try geocoding 'near' first
            try:
                g = self.geocode(near, lang=lang)
                if g:
                    params["location"] = f"{g['lat']},{g['lng']}"
                    params["radius"] = "5000"
            except MapsError:
                pass  # location bias is best-effort; search proceeds anyway
        data = http_get_json(f"{BASE_URL}/place/textsearch/json", params)
        out = []
        for r in data.get("results", []):
            out.append({
                "name": r.get("name"),
                "lat": r["geometry"]["location"]["lat"],
                "lng": r["geometry"]["location"]["lng"],
                "formatted_address": r.get("formatted_address"),
                "type": (r.get("types") or [""])[0],
                "types": r.get("types", []),
                "rating": r.get("rating"),
                "user_ratings_total": r.get("user_ratings_total"),
                "price_level": r.get("price_level"),
                "business_status": r.get("business_status"),
                "opening_hours": r.get("opening_hours", {}).get("open_now"),
                "place_id": r.get("place_id"),
                "provider": "google",
            })
        return out

    # -- routing -------------------------------------------------------------

    def directions(self, origin: str, destination: str, *,
                   mode: str = "driving",
                   waypoints: list[str] | None = None,
                   stops: list[str] | None = None,
                   optimize: bool = False,
                   alternatives: bool = False,
                   departure_time: str | None = None,
                   lang: str = "en",
                   wait_min: int = 0) -> dict:
        google_mode = GOOGLE_MODE_MAP.get(mode)
        if not google_mode:
            raise MapsError(
                f"Unknown mode {mode!r}. "
                f"Supported: {', '.join(VALID_MODES)}")
        waypoints = waypoints or []
        stops = stops or []
        if waypoints and stops:
            raise MapsError(
                "Use either --waypoints (via, pass-through) or --stops "
                "(true stopovers), not both.")
        if optimize:
            if waypoints:  # TSP needs stopovers — promote via-points to stops
                stops, waypoints = waypoints, []
            if not stops:
                raise MapsError(
                    "--optimize needs intermediate stops "
                    "(pass --stops; --waypoints are promoted automatically).")
            if google_mode == "transit":
                raise MapsError(
                    "--optimize is not available in transit mode "
                    "(Google optimizes road routes only).")
        if len(stops) > 25:
            raise MapsError(
                f"Too many stops ({len(stops)}); Google Directions accepts "
                "at most 25 intermediate waypoints per request.")
        if google_mode == "transit" and (stops or waypoints):
            # Google transit directions accept no waypoints at all —
            # chain one transit call per segment instead.
            chain_stops = stops + waypoints
            result = self._itinerary_transit(
                [origin, *chain_stops, destination],
                departure_time=departure_time, lang=lang, wait_min=wait_min)
            if waypoints:
                result["warnings"].insert(
                    0, "transit mode: via-waypoints unsupported by Google; "
                       "treated as stopovers")
            return result
        params: dict = {
            "origin": origin,
            "destination": destination,
            "mode": google_mode,
            "language": lang,
            "alternatives": "true" if alternatives else "false",
        }
        if waypoints:
            params["waypoints"] = "via:" + "|via:".join(waypoints)
        if stops:
            wp = ["optimize:true", *stops] if optimize else list(stops)
            params["waypoints"] = "|".join(wp)
        if departure_time:
            if departure_time == "now":
                import time
                params["departure_time"] = str(int(time.time()))
            else:
                params["departure_time"] = departure_time
        # transit mode needs departure_time or arrival_time
        if google_mode == "transit" and "departure_time" not in params:
            import time
            params["departure_time"] = str(int(time.time()))
        data = http_get_json(f"{BASE_URL}/directions/json", params)
        routes = data.get("routes", [])
        if not routes:
            raise NotFoundError("No route found between these locations.")
        route = routes[0]
        legs_out = []
        for leg in route["legs"]:
            steps = []
            for s in leg.get("steps", []):
                instr = (s.get("html_instructions", "")
                         .replace("<b>", "").replace("</b>", "")
                         .replace('div style="font-size:0.9em"', "span")
                         .replace("</div>", "</span>"))
                steps.append({
                    "instruction": instr,
                    "name": s.get("name", ""),
                    "maneuver": s.get("maneuver", ""),
                    "travel_mode": s.get("travel_mode", ""),
                    "distance_m": s.get("distance", {}).get("value", 0),
                    "duration_s": s.get("duration", {}).get("value", 0),
                    "transit_details": s.get("transit_details"),
                    "start_location": [
                        s.get("start_location", {}).get("lng"),
                        s.get("start_location", {}).get("lat"),
                    ],
                })
            legs_out.append({
                "distance_m": leg["distance"]["value"],
                "duration_s": leg["duration"]["value"],
                "duration_in_traffic_s": (
                    leg["duration_in_traffic"]["value"]
                    if "duration_in_traffic" in leg else None
                ),
                "start_address": leg.get("start_address"),
                "end_address": leg.get("end_address"),
                "departure_time_s": (leg.get("departure_time") or {}).get("value"),
                "arrival_time_s": (leg.get("arrival_time") or {}).get("value"),
                "steps": steps,
            })
        # Schedule: derive per-leg departure/arrival times when the request
        # carries a departure_time (or transit, which auto-fills one).
        dep0 = int(params["departure_time"]) if "departure_time" in params else None
        arrival_total = None
        if dep0 is not None and legs_out:
            cum = dep0
            for i, leg in enumerate(legs_out):
                if leg["departure_time_s"] is None:
                    leg["departure_time_s"] = cum
                if leg["arrival_time_s"] is None:
                    dur = leg["duration_in_traffic_s"] or leg["duration_s"]
                    leg["arrival_time_s"] = leg["departure_time_s"] + dur
                cum = leg["arrival_time_s"]
                if i < len(legs_out) - 1 and wait_min:
                    cum += wait_min * 60  # dwell at each intermediate stop
            arrival_total = legs_out[-1]["arrival_time_s"]
        return {
            "provider": "google",
            "mode": mode,
            "origin_address": legs_out[0]["start_address"] if legs_out else None,
            "destination_address": (legs_out[-1]["end_address"]
                                     if legs_out else None),
            "waypoints": waypoints,
            "stops": stops,
            "optimized": bool(optimize),
            "waypoint_order": route.get("waypoint_order") if optimize else None,
            "departure_time_s": dep0,
            "arrival_time_s": arrival_total,
            "chained": False,
            "wait_min": wait_min or None,
            "distance_m": sum(l["distance_m"] for l in legs_out),
            "duration_s": sum(l["duration_s"] for l in legs_out),
            "duration_in_traffic_s": sum(
                l["duration_in_traffic_s"] or 0 for l in legs_out
            ) or None,
            "summary": route.get("summary", ""),
            "copyrights": route.get("copyrights", ""),
            "warnings": route.get("warnings", []),
            "geometry": route.get("overview_polyline", {}),
            "legs": legs_out,
            "alternatives_available": max(0, len(routes) - 1)
                if alternatives else 0,
        }

    def _itinerary_transit(self, points: list[str], *,
                           departure_time: str | None = None,
                           lang: str = "en", wait_min: int = 0) -> dict:
        """Chain one transit directions call per segment.

        Google transit directions accept no waypoints, so a multi-stop
        transit itinerary is built by calling directions() for each
        consecutive pair, feeding each segment's arrival time (plus the
        dwell time) into the next segment's departure. Returns the same
        shape as directions() with all legs concatenated.
        """
        import time as _time
        if departure_time in (None, "now"):
            dep = int(_time.time())
        else:
            try:
                dep = int(departure_time)
            except ValueError:
                raise MapsError(f"Invalid departure time: {departure_time!r}")
        legs_all: list[dict] = []
        warnings: list[str] = []
        segments: list[str] = []
        copyrights = ""
        for a, b in zip(points, points[1:]):
            res = self.directions(a, b, mode="transit",
                                  departure_time=str(dep), lang=lang)
            legs_all.extend(res["legs"])
            for w in res.get("warnings", []):
                if w not in warnings:
                    warnings.append(w)
            segments.append(res.get("geometry", {}).get("points", ""))
            copyrights = res.get("copyrights", copyrights)
            last = res["legs"][-1]
            arr = last.get("arrival_time_s")
            if arr is None:
                arr = dep + last["duration_s"]
            dep = arr + wait_min * 60
        if not legs_all:
            raise NotFoundError("No transit route found along this itinerary.")
        return {
            "provider": "google",
            "mode": "transit",
            "origin_address": legs_all[0].get("start_address"),
            "destination_address": legs_all[-1].get("end_address"),
            "waypoints": [],
            "stops": points[1:-1],
            "optimized": False,
            "waypoint_order": None,
            "departure_time_s": legs_all[0].get("departure_time_s"),
            "arrival_time_s": legs_all[-1].get("arrival_time_s"),
            "chained": True,
            "wait_min": wait_min or None,
            "distance_m": sum(l["distance_m"] for l in legs_all),
            "duration_s": sum(l["duration_s"] for l in legs_all),
            "duration_in_traffic_s": None,
            "summary": f"transit × {len(points) - 1} segment(s)",
            "copyrights": copyrights,
            "warnings": warnings,
            "geometry": {"points": "".join(segments), "segments": segments},
            "legs": legs_all,
            "alternatives_available": 0,
        }

    def distance_matrix(self, origins: list[str], destinations: list[str],
                        *, mode: str = "driving", lang: str = "en") -> dict:
        google_mode = GOOGLE_MODE_MAP.get(mode, "driving")
        data = http_get_json(f"{BASE_URL}/distancematrix/json", {
            "origins": "|".join(origins),
            "destinations": "|".join(destinations),
            "mode": google_mode,
            "language": lang,
        })
        durations = []
        distances = []
        for row in data.get("rows", []):
            dur_row, dist_row = [], []
            for el in row.get("elements", []):
                status = el.get("status")
                if status == "OK":
                    dur_row.append(el.get("duration", {}).get("value"))
                    dist_row.append(el.get("distance", {}).get("value"))
                else:
                    dur_row.append(None)
                    dist_row.append(None)
            durations.append(dur_row)
            distances.append(dist_row)
        return {
            "provider": "google",
            "mode": mode,
            "origins": origins,
            "destinations": destinations,
            "durations_s": durations,
            "distances_m": distances,
        }


# ---------------------------------------------------------------------------
# Human-readable formatting
# ---------------------------------------------------------------------------


def fmt_distance(m: float | None) -> str:
    if m is None:
        return "—"
    if m < 1000:
        return f"{m:.0f} m"
    return f"{m / 1000:.1f} km"


def fmt_duration(s: float | None) -> str:
    if s is None:
        return "—"
    s = int(s)
    if s < 60:
        return f"{s}s"
    h, m = divmod(s, 3600)
    m //= 60
    if h:
        return f"{h}h {m:02d}m"
    return f"{m}m"


def fmt_time(ts: float | None) -> str:
    """Unix timestamp -> HH:MM (system-local timezone)."""
    if ts is None:
        return "—"
    import time
    return time.strftime("%H:%M", time.localtime(ts))


def print_human_geocode(r: dict | None) -> None:
    if not r:
        print("No result found.", file=sys.stderr)
        return
    print(f"📍 {r['lat']:.4f}, {r['lng']:.4f}")
    print(f"   {r.get('formatted_address', '')}")
    print(f"   Type: {r.get('type', '?')} | Provider: {r.get('provider', '?')}")
    if r.get("components"):
        bits = []
        c = r["components"]
        for k in ("locality", "city", "town", "village",
                  "administrative_area_level_1",
                  "country", "postal_code"):
            if k in c:
                bits.append(c[k])
        if bits:
            print(f"   ↳ {', '.join(bits)}")


def print_human_search(results: list[dict]) -> None:
    if not results:
        print("No results.", file=sys.stderr)
        return
    for i, r in enumerate(results, 1):
        marker = "⭐" if r.get("rating") else "📍"
        name = r.get("name", "?")
        print(f"{marker} {i}. {name}")
        if r.get("rating"):
            stars = "★" * int(r.get("rating", 0))
            print(f"   {stars} {r['rating']:.1f} ({r.get('user_ratings_total', 0)} reviews)"
                  f"{' ⋅ Open' if r.get('opening_hours') else ''}"
                  f"{' ⋅ $' * r.get('price_level', 0) if r.get('price_level') else ''}")
        print(f"   {r.get('formatted_address', '')}")


def print_human_directions(r: dict) -> None:
    icons = {"driving": "🚗", "walking": "🚶", "bicycling": "🚴", "cycling": "🚴",
             "transit": "🚌"}
    icon = icons.get(r.get("mode", ""), "🧭")
    stops = r.get("stops") or []
    legs = r.get("legs", [])
    multi = bool(stops) or len(legs) > 1
    title = (f"{r.get('origin_address', '?')} → "
             f"{r.get('destination_address', '?')}")
    if stops:
        title += f"  ({len(stops)} stop{'s' if len(stops) > 1 else ''})"
    if r.get("chained"):
        title += "  [chained transit]"
    print(f"{icon} {title}")
    print(f"   Distance: {fmt_distance(r['distance_m'])}")
    if r.get("duration_in_traffic_s"):
        print(f"   Duration (free-flow): {fmt_duration(r['duration_s'])}  |  "
              f"with traffic: {fmt_duration(r['duration_in_traffic_s'])}")
    else:
        print(f"   Duration: {fmt_duration(r['duration_s'])}")
    if r.get("arrival_time_s"):
        dep = (r.get("departure_time_s")
               or (legs[0].get("departure_time_s") if legs else None))
        wait = (f"  (+{r['wait_min']} min at each stop)"
                if r.get("wait_min") else "")
        print(f"   Departure: {fmt_time(dep)}  |  "
              f"Arrival: {fmt_time(r['arrival_time_s'])}{wait}")
    if r.get("summary"):
        print(f"   Via: {r['summary']}")
    if r.get("optimized") and r.get("waypoint_order") is not None:
        ordered = [stops[i] for i in r["waypoint_order"] if 0 <= i < len(stops)]
        print(f"   Optimized order: {' → '.join(ordered)}")
    elif stops:
        print(f"   Stops: {', '.join(stops)}")
    if r.get("waypoints"):
        print(f"   Waypoints (via): {', '.join(r['waypoints'])}")
    if r.get("alternatives_available"):
        print(f"   Alternatives: {r['alternatives_available']} more route(s)")
    for w in r.get("warnings", []):
        print(f"   ⚠ {w}")
    print()
    steps_total = sum(len(leg["steps"]) for leg in legs)
    for i, leg in enumerate(legs, 1):
        line = (f"   Leg {i}: {fmt_distance(leg['distance_m'])} — "
                f"{fmt_duration(leg['duration_s'])}")
        arr_t = leg.get("arrival_time_s")
        if arr_t is not None:
            line += f"  ({fmt_time(leg.get('departure_time_s'))} → {fmt_time(arr_t)})"
        print(line)
        if leg.get("duration_in_traffic_s"):
            print(f"      with traffic: {fmt_duration(leg['duration_in_traffic_s'])}")
        if multi and leg.get("end_address"):
            print(f"      → {leg['end_address']}")
    print(f"\n   {steps_total} step(s) total. Use --json for full instructions.")


def print_human_matrix(r: dict) -> None:
    env = "🚗" if r["mode"] == "driving" else "🚶" if r["mode"] == "walking" else "🚴"
    mode_label = f"{env} {r['mode']} (Google Maps)"
    print(f"Origin → Destination matrix — {mode_label}:")
    cols = r["destinations"]
    header = " " * 24 + "".join(f"{c[:14]:>15}" for c in cols)
    print(header)
    print("-" * len(header))
    for i, o in enumerate(r["origins"]):
        dur_row = r.get("durations_s") and r["durations_s"][i]
        dist_row = r.get("distances_m") and r["distances_m"][i]
        print(f"{o[:23]:24}" + "".join(
            f"{fmt_duration(d):>15}" if d is not None else f"{'—':>15}"
            for d in (dur_row or [])
        ))
        print(f"{'  distance:':24}" + "".join(
            f"{fmt_distance(d):>15}" if d is not None else f"{'—':>15}"
            for d in (dist_row or [])
        ))


# ---------------------------------------------------------------------------
# Sub-command dispatchers
# ---------------------------------------------------------------------------


def cmd_geocode(args, geo: Geocoder) -> int:
    result = geo.geocode(" ".join(args.address), lang=args.lang)
    if args.human:
        print_human_geocode(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result else 1


def cmd_reverse(args, geo: Geocoder) -> int:
    try:
        lat, lng = float(args.lat), float(args.lng)
    except ValueError:
        raise MapsError(f"Invalid coordinates: {args.lat} {args.lng}")
    result = geo.reverse(lat, lng, lang=args.lang)
    if args.human:
        print_human_geocode(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result else 1


def cmd_search(args, geo: Geocoder) -> int:
    results = geo.search(args.query, near=args.near, lang=args.lang)
    if args.human:
        print_human_search(results)
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if results else 1


def cmd_directions(args, geo: Geocoder) -> int:
    kwargs = {}
    if getattr(args, "departure_time", None):
        kwargs["departure_time"] = args.departure_time
    result = geo.directions(
        args.origin, args.destination,
        mode=args.mode, waypoints=args.waypoints,
        stops=getattr(args, "stops", None) or None,
        optimize=getattr(args, "optimize", False),
        wait_min=getattr(args, "wait", 0) or 0,
        alternatives=args.alternatives, lang=args.lang,
        **kwargs,
    )
    if args.human:
        print_human_directions(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_distance(args, geo: Geocoder) -> int:
    if not args.origins:
        raise MapsError("distance needs at least one origin")
    if not args.to:
        raise MapsError("distance needs --to <dest1> [<dest2> ...]")
    result = geo.distance_matrix(
        args.origins, args.to, mode=args.mode, lang=args.lang)
    if args.human:
        print_human_matrix(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_provider(args, geo: Geocoder) -> int:
    key = os.environ.get("GOOGLE_MAPS_API_KEY") or os.environ.get("GMAPS_API_KEY")
    info = {
        "backend": "Google Maps Platform",
        "services": [
            "Geocoding API",
            "Directions API",
            "Distance Matrix API",
            "Places API (Text Search)",
        ],
        "modes": list(VALID_MODES),
        "supports_transit": True,
        "api_key_configured": bool(key),
        "api_key_prefix": f"{key[:8]}..." if key else "not set",
        "traffic": True,
        "rich_places": True,
    }
    print(json.dumps(info, indent=2))
    return 0


# ---------------------------------------------------------------------------
# CLI plumbing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--human", action="store_true",
                        help="Human-readable output (default: JSON)")
    common.add_argument("--lang", default="en",
                        help="Result language: fr, en, de, es, ... (default: en)")
    common.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT})")

    p = argparse.ArgumentParser(
        prog="gmaps",
        description="Geocoding, place search and routing (Google Maps Platform).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
        epilog="Requires GOOGLE_MAPS_API_KEY. See SKILL.md for setup.",
    )
    sub = p.add_subparsers(dest="cmd", required=True, metavar="COMMAND")

    sp = sub.add_parser("geocode", help="Address → coordinates", parents=[common])
    sp.add_argument("address", nargs="+")
    sp.set_defaults(func=cmd_geocode)

    sp = sub.add_parser("reverse", help="Coordinates → address", parents=[common])
    sp.add_argument("lat")
    sp.add_argument("lng")
    sp.set_defaults(func=cmd_reverse)

    sp = sub.add_parser("search", help="Text search for places/POIs", parents=[common])
    sp.add_argument("query")
    sp.add_argument("--near", help="Bias results near a place/address")
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("directions", help="Compute a route A → B", parents=[common])
    sp.add_argument("origin")
    sp.add_argument("destination")
    sp.add_argument("--mode", choices=VALID_MODES, default="driving")
    sp.add_argument("--waypoints", nargs="+", default=[],
                    help="Pass-through waypoints (via: shape the route, single leg)")
    sp.add_argument("--stops", nargs="+", default=[],
                    help="True stopovers: per-leg breakdown + arrival times; "
                         "transit segments are chained automatically")
    sp.add_argument("--optimize", action="store_true",
                    help="Let Google reorder intermediate stops (TSP; road modes; "
                         "implies --stops with --waypoints)")
    sp.add_argument("--wait", type=int, default=0, metavar="MIN",
                    help="Minutes spent at each intermediate stop "
                         "(schedule + transit chaining)")
    sp.add_argument("--alternatives", action="store_true")
    sp.add_argument("--departure-time",
                    help="Departure time: 'now' or Unix timestamp (enables traffic + transit)")
    sp.set_defaults(func=cmd_directions)

    sp = sub.add_parser("distance",
                        help="Distance/duration matrix (origins --to destinations)",
                        parents=[common])
    sp.add_argument("origins", nargs="+")
    sp.add_argument("--to", nargs="+", dest="to", default=[])
    sp.add_argument("--mode", choices=VALID_MODES, default="driving")
    sp.set_defaults(func=cmd_distance)

    sp = sub.add_parser("provider", help="Show backend info & API key status",
                        parents=[common])
    sp.set_defaults(func=cmd_provider)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    global DEFAULT_TIMEOUT
    DEFAULT_TIMEOUT = args.timeout

    try:
        geo = Geocoder()
        return args.func(args, geo)
    except ApiKeyError as e:
        print(f"API KEY: {e}", file=sys.stderr)
        return 3
    except RateLimitError as e:
        print(f"RATE LIMIT: {e}", file=sys.stderr)
        return 4
    except MapsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())