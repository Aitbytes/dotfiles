#!/usr/bin/env python3
"""
maps (alternative implementation) — same operations as maps.py, but using
the third-party `requests` library instead of urllib.request.

This file is **not** invoked by the skill by default. It exists to make
the trade-off concrete and runnable for comparison.

Run with:  uv run --with requests python3 alternative-requests.py <args>
           # or
           python3 alternative-requests.py <args>   # if requests is installed

Key differences vs the stdlib version (maps.py):
  - Cleaner HTTP: requests.get() with raise_for_status=True
  - Session reuse: connection pooling across sub-commands
  - Retry hook: requests.adapters.HTTPAdapter with urllib3.util.retry.Retry
  - Less boilerplate around URL parsing / error decoding
  - 1 runtime dependency instead of zero
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = "pi-maps-skill/1.0 (+https://github.com/local/pi-maps)"
TIMEOUT = 20

# ---- shared session with retry / pooling --------------------------------

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
retry = Retry(total=3, backoff_factor=0.5,
              status_forcelist=(429, 500, 502, 503, 504),
              allowed_methods=frozenset(["GET"]))
session.mount("https://", HTTPAdapter(max_retries=retry, pool_connections=4,
                                       pool_maxsize=4))


def http_get_json(url: str, params: dict | None = None) -> Any:
    """GET a URL, return parsed JSON. Raises on HTTP/network error."""
    r = session.get(url, params=params, timeout=TIMEOUT)
    r.raise_for_status()  # HTTPError on 4xx/5xx with body attached
    return r.json()


# ---- minimal provider layer --------------------------------------------

class OSM:
    name = "osm"
    NOMINATIM = "https://nominatim.openstreetmap.org"
    OSRM = "https://router.project-osrm.org"

    def geocode(self, address: str, lang: str = "en") -> dict | None:
        r = http_get_json(f"{self.NOMINATIM}/search", {
            "q": address, "format": "json", "limit": 1,
            "addressdetails": 1, "accept-language": lang,
        })
        if not r:
            return None
        first = r[0]
        return {"lat": float(first["lat"]), "lng": float(first["lon"]),
                "formatted_address": first["display_name"],
                "provider": self.name}

    def reverse(self, lat: float, lng: float, lang: str = "en") -> dict | None:
        r = http_get_json(f"{self.NOMINATIM}/reverse", {
            "lat": lat, "lon": lng, "format": "json",
            "addressdetails": 1, "accept-language": lang, "zoom": 18,
        })
        if not r or "error" in r:
            return None
        return {"lat": float(r["lat"]), "lng": float(r["lon"]),
                "formatted_address": r["display_name"], "provider": self.name}

    def directions(self, o: str, d: str, *, mode="driving") -> dict:
        og, dg = self.geocode(o), self.geocode(d)
        coords = f"{og['lng']},{og['lat']};{dg['lng']},{dg['lat']}"
        r = http_get_json(
            f"{self.OSRM}/route/v1/{mode}/{coords}",
            {"overview": "full", "geometries": "geojson", "steps": "true"},
        )
        route = r["routes"][0]
        return {"provider": self.name, "mode": mode,
                "distance_m": route["distance"],
                "duration_s": route["duration"],
                "geometry": route["geometry"]}


# ---- CLI (kept short for the comparison) --------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="maps (requests-based comparison)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("geocode")
    sp.add_argument("address")

    sp = sub.add_parser("reverse")
    sp.add_argument("lat", type=float)
    sp.add_argument("lng", type=float)

    sp = sub.add_parser("directions")
    sp.add_argument("origin")
    sp.add_argument("destination")
    sp.add_argument("--mode", default="driving")

    args = ap.parse_args()
    osm = OSM()

    if args.cmd == "geocode":
        result = osm.geocode(args.address)
    elif args.cmd == "reverse":
        result = osm.reverse(args.lat, args.lng)
    elif args.cmd == "directions":
        result = osm.directions(args.origin, args.destination, mode=args.mode)
    else:
        ap.error("unknown command"); return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
