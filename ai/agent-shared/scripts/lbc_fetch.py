#!/usr/bin/env python3
"""lbc_fetch.py — leboncoin search via iProyal FR-residential proxy + curl_cffi.

The DataDome unlock for leboncoin.fr (verified live 2026-10-13, from session
01a1320d). Plain curl gets a 774-byte 403 (TLS fingerprint); curl_cffi with
impersonate="chrome" through the FR-geo proxy passes and returns the SSR page
with a __NEXT_DATA__ JSON blob containing every listing.

Usage:
    lbc_fetch.py "canape convertible" [--pages 1] [--out /tmp/lbc.json]

- Proxy read from ~/.config/proxy-conf (never hardcoded).
- Geo goes on the PASSWORD: <pass>_country-fr. Port 12321.
- ~30% of attempts 403 (DataDome) — this script retries automatically.
- Output: JSON list of ads: subject, price_cents, location.city, url, list_id.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

PROXY_CONF = Path.home() / ".config/proxy-conf"
SEARCH_URL = "https://www.leboncoin.fr/recherche?text={q}"
NEXT_DATA = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S)


def load_proxy(country: str = "fr") -> str:
    """Parse ~/.config/proxy-conf -> http://user:<pass>_<country>@host:port"""
    text = PROXY_CONF.read_text()
    m = re.search(r'http://([^:]+):([^@]*)@([^:/"]+):(\d+)', text)
    if not m:
        sys.exit(f"error: no proxy URL found in {PROXY_CONF}")
    user, pw, host, port = m.groups()
    return f"http://{user}:{pw}_{country}@{host}:{port}"


def fetch(query: str, proxy: str, timeout: int = 60, attempts: int = 3) -> str:
    from urllib.parse import quote
    from curl_cffi import requests  # uv run --with curl_cffi
    last = "no attempts"
    url = SEARCH_URL.format(q=quote(query))
    for i in range(1, attempts + 1):
        r = requests.get(url, impersonate="chrome",
                         proxies={"http": proxy, "https": proxy},
                         headers={"Accept-Language": "fr-FR,fr;q=0.9"}, timeout=timeout)
        if r.status_code == 200 and "__NEXT_DATA__" in r.text:
            return r.text
        last = f"HTTP {r.status_code} size {len(r.text)}"
        print(f"attempt {i}: {last} — retrying", file=sys.stderr)
        time.sleep(3 + 2 * i)
    sys.exit(f"error: leboncoin blocked after {attempts} attempts ({last})")


def parse(html: str) -> list[dict]:
    m = NEXT_DATA.search(html)
    if not m:
        sys.exit("error: 200 page but no __NEXT_DATA__ (layout change — re-check)")
    data = json.loads(m.group(1))
    ads = data.get("props", {}).get("pageProps", {}).get("searchData", {}).get("ads", [])
    out = []
    for a in ads:
        loc = a.get("location") or {}
        out.append({
            "id": a.get("list_id"),
            "title": a.get("subject"),
            "price_eur": (a["price_cents"] / 100) if a.get("price_cents") else None,
            "city": loc.get("city"),
            "url": a.get("url"),
            "date": a.get("first_publication_date"),
        })
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--pages", type=int, default=1, help="search-result pages (offset pagination)")
    ap.add_argument("--out", default=None, help="write JSON here (default: stdout)")
    args = ap.parse_args()
    if args.pages > 1:
        sys.exit("error: --pages>1 not implemented; use offset param in SEARCH_URL")

    proxy = load_proxy()
    all_ads: list[dict] = []
    for page in range(1, args.pages + 1):
        html = fetch(args.query, proxy)
        all_ads.extend(parse(html))
    seen, dedup = set(), []
    for a in all_ads:
        if a["id"] and a["id"] not in seen:
            seen.add(a["id"])
            dedup.append(a)
    result = json.dumps(dedup, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(result)
        print(f"{len(dedup)} ads -> {args.out}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
