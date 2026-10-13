#!/usr/bin/env python3
"""
maps — geocoding, place search and routing CLI.

Pure Python standard-library implementation. Backend: OpenStreetMap
(Nominatim for geocoding + OSRM for routing). No API key, no third-party
packages, no account required.

Sub-commands
------------
    maps geocode    <address>                       -> {lat,lng,address,...}
    maps reverse    <lat> <lng>                     -> {lat,lng,address,...}
    maps search     <query> [--near <place>]        -> [place, place, ...]
    maps directions <origin> <destination>          -> {distance,duration,steps,...}
                        [--mode driving|walking|cycling]
                        [--waypoints W1 W2 ...]
                        [--alternatives]
    maps distance   <origin1> <origin2> ... --to D1 D2 ...
                                                    -> matrix
    maps provider                                  -> backend info

Common flags
------------
    --human      Human-readable output instead of JSON.
    --lang fr|en Result language (default: en).
    --timeout N  HTTP timeout in seconds (default: 20).

Not supported (use Google Maps for these):
    - Transit routing (bus, metro, train)
    - Real-time traffic-adjusted durations

Stdlib-only: uses urllib.request, json, argparse, urllib.parse, time,
os, sys. No third-party packages required.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENT = "pi-maps-skill/1.0 (+https://github.com/local/pi-maps)"
DEFAULT_TIMEOUT = 20
OSM_MIN_INTERVAL = 1.1  # OSM usage policy: max 1 req/s. We space to 1.1s.
# Set MAPS_NO_THROTTLE=1 only against your own Nominatim/OSRM instance.
if os.environ.get("MAPS_NO_THROTTLE"):
    OSM_MIN_INTERVAL = 0.0

VALID_MODES = ("driving", "walking", "cycling")
OSRM_PROFILES = {"driving": "driving", "walking": "foot", "cycling": "bike"}


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class MapsError(Exception):
    """Base error for the maps skill."""


class NotFoundError(MapsError):
    """The backend returned no result."""


class ProviderError(MapsError):
    """The backend returned an error response (bad input, rate limit, etc.)."""


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------


def http_get_json(url: str, headers: dict | None = None,
                  timeout: float = DEFAULT_TIMEOUT) -> Any:
    """GET a URL and return the parsed JSON body.

    Raises MapsError on transport failure, HTTP error or non-JSON body.
    """
    merged = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if headers:
        merged.update(headers)
    req = urllib.request.Request(url, headers=merged)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        raise ProviderError(f"HTTP {e.code} {url}: {body}") from e
    except urllib.error.URLError as e:
        raise ProviderError(f"Network error for {url}: {e.reason}") from e
    except TimeoutError as e:
        raise ProviderError(f"Timeout after {timeout}s: {url}") from e
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise ProviderError(f"Non-JSON response from {url}: {e}") from e


# ---------------------------------------------------------------------------
# OSM-backed geocoder/router (single class, single backend)
# ---------------------------------------------------------------------------


class Geocoder:
    """OpenStreetMap-backed geocoder and router.

    Wraps two public services:
      - Nominatim  https://nominatim.openstreetmap.org  (search/reverse)
      - OSRM       https://router.project-osrm.org     (route/table)
    """

    NOMINATIM = "https://nominatim.openstreetmap.org"
    OSRM = "https://router.project-osrm.org"

    def __init__(self) -> None:
        self._last = 0.0  # monotonic time of last request (for throttle)

    # -- polite throttle -----------------------------------------------------

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last
        if elapsed < OSM_MIN_INTERVAL:
            time.sleep(OSM_MIN_INTERVAL - elapsed)
        self._last = time.monotonic()

    # -- low-level nominatim/osrm wrappers ----------------------------------

    def _nominatim(self, path: str, params: dict) -> Any:
        self._throttle()
        url = f"{self.NOMINATIM}{path}?{urllib.parse.urlencode(params)}"
        return http_get_json(url)

    def _osrm(self, path: str) -> Any:
        self._throttle()
        return http_get_json(f"{self.OSRM}{path}")

    # -- public API: geocoding ------------------------------------------------

    def geocode(self, address: str, lang: str = "en") -> dict | None:
        # Nominatim quirk: limit=1 + accept-language=en + addressdetails=1
        # returns 0 results for many queries. Use limit=5 and pick first.
        data = self._nominatim("/search", {
            "q": address,
            "format": "json",
            "addressdetails": "1",
            "limit": "5",
            "accept-language": lang,
        })
        if not data:
            return None
        r = data[0]
        return {
            "lat": float(r["lat"]),
            "lng": float(r["lon"]),
            "formatted_address": r.get("display_name"),
            "place_id": str(r.get("place_id")),
            "type": r.get("type"),
            "components": r.get("address", {}),
            "provider": "osm",
        }

    def reverse(self, lat: float, lng: float, lang: str = "en") -> dict | None:
        data = self._nominatim("/reverse", {
            "lat": str(lat),
            "lon": str(lng),
            "format": "json",
            "addressdetails": "1",
            "accept-language": lang,
            "zoom": "18",
            "limit": "1",
        })
        if not data or data.get("error"):
            return None
        return {
            "lat": float(data["lat"]),
            "lng": float(data["lon"]),
            "formatted_address": data.get("display_name"),
            "place_id": str(data.get("place_id")),
            "type": data.get("type"),
            "components": data.get("address", {}),
            "provider": "osm",
        }

    def search(self, query: str, near: str | None = None,
               lang: str = "en") -> list[dict]:
        q = query if not near else f"{query} {near}"
        data = self._nominatim("/search", {
            "q": q,
            "format": "json",
            "addressdetails": "1",
            "limit": "10",
            "accept-language": lang,
            "dedupe": "1",
        })
        out = []
        for r in data:
            out.append({
                "name": (r.get("display_name") or "").split(",", 1)[0].strip(),
                "lat": float(r["lat"]),
                "lng": float(r["lon"]),
                "formatted_address": r.get("display_name"),
                "type": r.get("type"),
                "class": r.get("class"),
                "provider": "osm",
            })
        return out

    # -- public API: routing --------------------------------------------------

    def _resolve(self, address: str) -> dict:
        """Geocode an address or pass through 'lat,lng' shorthand.

        Tries the query as-is, then progressively simpler variants if
        Nominatim returns empty (which often happens with ambiguous or
        already-resolved queries when the caller is rate-limited):
          "Paris, France" -> "Paris"
        """
        if "," in address and all(p.replace(".", "").replace("-", "").isdigit()
                                   for p in address.split(",")):
            lat_s, lng_s = [p.strip() for p in address.split(",", 1)]
            return {"lat": float(lat_s), "lng": float(lng_s),
                    "formatted_address": address}
        variants = [address]
        if "," in address:
            first = address.split(",", 1)[0].strip()
            if first and first != address:
                variants.append(first)
        for q in variants:
            g = self.geocode(q)
            if g:
                return g
        raise NotFoundError(
            f"Could not geocode: {address!r}. "
            f"Tried: {variants}. "
            f"Try a more specific query, simpler wording, or wait a few seconds "
            f"if you have been issuing many requests (Nominatim throttles ~1 req/s).")

    @staticmethod
    def _step_normalize(s: dict) -> dict:
        m = s.get("maneuver", {})
        return {
            "instruction": m.get("instruction") or s.get("name", ""),
            "name": s.get("name", ""),
            "maneuver": m.get("type", ""),
            "modifier": m.get("modifier", ""),
            "distance_m": s.get("distance", 0),
            "duration_s": s.get("duration", 0),
            "location": m.get("location"),
        }

    def directions(self, origin: str, destination: str, *,
                   mode: str = "driving",
                   waypoints: list[str] | None = None,
                   alternatives: bool = False,
                   lang: str = "en") -> dict:
        if mode not in VALID_MODES:
            raise MapsError(
                f"Unsupported mode {mode!r}. Supported: {', '.join(VALID_MODES)}. "
                f"Transit routing is not supported by this skill.")
        o = self._resolve(origin)
        d = self._resolve(destination)
        coords: list[str] = [f"{o['lng']},{o['lat']}"]
        if waypoints:
            for w in waypoints:
                wp = self._resolve(w)
                coords.append(f"{wp['lng']},{wp['lat']}")
        coords.append(f"{d['lng']},{d['lat']}")

        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "true",
            "alternatives": "true" if alternatives else "false",
            "annotations": "false",
        }
        path = (f"/route/v1/{OSRM_PROFILES[mode]}/"
                f"{';'.join(coords)}?{urllib.parse.urlencode(params)}")
        data = self._osrm(path)
        if data.get("code") != "Ok":
            raise ProviderError(
                f"OSRM routing failed: {data.get('code')} — {data.get('message')}")
        route = data["routes"][0]
        legs_out = []
        for leg in route["legs"]:
            legs_out.append({
                "distance_m": leg["distance"],
                "duration_s": leg["duration"],
                "summary": leg.get("summary", ""),
                "steps": [self._step_normalize(s) for s in leg["steps"]],
            })
        return {
            "provider": "osm",
            "mode": mode,
            "origin": o,
            "destination": d,
            "waypoints": waypoints or [],
            "distance_m": route["distance"],
            "duration_s": route["duration"],
            "summary": route.get("legs", [{}])[0].get("summary", ""),
            "geometry": route["geometry"],
            "legs": legs_out,
            "alternatives_available": max(0, len(data.get("routes", [])) - 1)
                if alternatives else 0,
        }

    def distance_matrix(self, origins: list[str], destinations: list[str],
                        *, mode: str = "driving", lang: str = "en") -> dict:
        if mode not in VALID_MODES:
            raise MapsError(f"Unsupported mode {mode!r}")
        o_pts = [self._resolve(o) for o in origins]
        d_pts = [self._resolve(d) for d in destinations]
        all_pts = o_pts + d_pts
        coords = ";".join(f"{p['lng']},{p['lat']}" for p in all_pts)
        n_o, n_d = len(o_pts), len(d_pts)
        sources = ";".join(str(i) for i in range(n_o))
        dests = ";".join(str(i) for i in range(n_o, n_o + n_d))
        path = (f"/table/v1/{OSRM_PROFILES[mode]}/{coords}?"
                f"sources={sources}&destinations={dests}"
                f"&annotations=duration,distance")
        data = self._osrm(path)
        if data.get("code") != "Ok":
            raise ProviderError(f"OSRM table failed: {data.get('code')}")
        return {
            "provider": "osm",
            "mode": mode,
            "origins": origins,
            "destinations": destinations,
            "durations_s": data.get("durations"),
            "distances_m": data.get("distances"),
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


def print_human_geocode(r: dict | None) -> None:
    if not r:
        print("No result found.", file=sys.stderr)
        return
    print(f"📍 {r['lat']:.4f}, {r['lng']:.4f}")
    print(f"   {r.get('formatted_address', '')}")
    print(f"   Type: {r.get('type', '?')} | Provider: {r['provider']}")
    if r.get("components"):
        bits = []
        c = r["components"]
        for k in ("city", "town", "village", "state", "country", "postcode"):
            if k in c:
                bits.append(c[k])
        if bits:
            print(f"   ↳ {', '.join(bits)}")


def print_human_search(results: list[dict]) -> None:
    if not results:
        print("No results.", file=sys.stderr)
        return
    for i, r in enumerate(results, 1):
        name = r.get("name") or r.get("formatted_address", "")
        print(f"📍 {i}. {name}")
        print(f"   {r['lat']:.4f}, {r['lng']:.4f}")
        if r.get("formatted_address"):
            print(f"   {r['formatted_address']}")
        if r.get("type"):
            print(f"   type: {r['type']}")


def print_human_directions(r: dict) -> None:
    icons = {"driving": "🚗", "walking": "🚶", "cycling": "🚴"}
    icon = icons.get(r.get("mode", ""), "🧭")
    print(f"{icon} {r.get('origin', {}).get('formatted_address', '?')}"
          f" → {r.get('destination', {}).get('formatted_address', '?')}")
    print(f"   Distance: {fmt_distance(r['distance_m'])}")
    print(f"   Duration: {fmt_duration(r['duration_s'])}")
    if r.get("summary"):
        print(f"   Via: {r['summary']}")
    if r.get("alternatives_available"):
        print(f"   Alternatives: {r['alternatives_available']} more route(s) available")
    if r.get("waypoints"):
        print(f"   Waypoints: {', '.join(r['waypoints'])}")
    print()
    steps_total = sum(len(leg["steps"]) for leg in r.get("legs", []))
    print(f"   {steps_total} step(s) total. Use --json for full instructions.")


def print_human_matrix(r: dict) -> None:
    print(f"Origin → Destination matrix ({r['mode']}):")
    cols = r["destinations"]
    header = " " * 24 + "".join(f"{c[:14]:>15}" for c in cols)
    print(header)
    print("-" * len(header))
    for i, o in enumerate(r["origins"]):
        row_dur = r.get("durations_s") and r["durations_s"][i]
        row_dist = r.get("distances_m") and r["distances_m"][i]
        print(f"{o[:23]:24}" + "".join(
            f"{fmt_duration(d):>15}" if d is not None else f"{'—':>15}"
            for d in (row_dur or [])
        ))
        print(f"{'  distance:':24}" + "".join(
            f"{fmt_distance(d):>15}" if d is not None else f"{'—':>15}"
            for d in (row_dist or [])
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
    result = geo.directions(
        args.origin, args.destination,
        mode=args.mode, waypoints=args.waypoints,
        alternatives=args.alternatives, lang=args.lang,
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
    info = {
        "backend": "OpenStreetMap",
        "services": ["Nominatim (geocoding)", "OSRM (routing)"],
        "modes": list(VALID_MODES),
        "supports_transit": False,
        "api_key_required": False,
        "rate_limit": "1 request/second (Nominatim public servers)",
    }
    print(json.dumps(info, indent=2))
    return 0


# ---------------------------------------------------------------------------
# CLI plumbing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    # Global flags that work either BEFORE or AFTER the subcommand.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--human", action="store_true",
                        help="Human-readable output (default: JSON)")
    common.add_argument("--lang", default="en",
                        help="Result language: fr, en, de, es, ... (default: en)")
    common.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT})")

    p = argparse.ArgumentParser(
        prog="maps",
        description="Geocoding, place search and routing (OpenStreetMap).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
        epilog="Stdlib-only. OpenStreetMap backend (Nominatim + OSRM).",
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
    sp.add_argument("--waypoints", nargs="+", default=[])
    sp.add_argument("--alternatives", action="store_true")
    sp.set_defaults(func=cmd_directions)

    sp = sub.add_parser("distance",
                        help="Distance/duration matrix (origins --to destinations)",
                        parents=[common])
    sp.add_argument("origins", nargs="+")
    sp.add_argument("--to", nargs="+", dest="to", default=[])
    sp.add_argument("--mode", choices=VALID_MODES, default="driving")
    sp.set_defaults(func=cmd_distance)

    sp = sub.add_parser("provider", help="Show backend info", parents=[common])
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
    except MapsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())