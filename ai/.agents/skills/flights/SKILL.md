---
name: flights
description: "Search real flight prices via Google Flights' internal RPC — works headless from LAN/datacenter IPs where Skyscanner/Kayak/Google-Flights-DOM are all blocked. CLI + JSON output for agents."
version: 1.0.0
license: MIT
platforms: [linux]
metadata:
  tags: [flights, travel, google-flights, steel, cdp, scraping]
---

# Flights Skill

Search Google Flights programmatically and get real prices, airlines, times and
stops — no API key, no paid service.

## When to Use
- "find me flights X→Y on date", price checks, round-trip totals, comparing
  routes/cabin classes, price monitoring loops
- Output is agent-friendly (`--json`)

## How It Works (the hard-won part — read before improvising)
Google Flights is hostile to automation, and every "obvious" route is blocked
from this environment (verified 2026-09-13):

| Route | Status |
|---|---|
| Skyscanner web | PerimeterX captcha wall, hard-blocked from this IP. Their API is partner-only (closed). |
| Kayak / Momondo web | Server-side `errorOccurred=true` redirect on direct search URLs, even with session cookies. |
| Google Flights DOM in Steel | Results XHR fires, but the page never renders (`li[aria-label]` stays 0; "Loading results" forever). |
| `fast-flights` direct fetch | Gets consent page unless you inject `SOCS` cookie; even then `script[ds:1]` no longer exists. |
| `swoop` direct RPC | Gets gRPC `[13]` INTERNAL (its request lacks the page's session context). |
| **What works** | **Open the TFS results URL in Steel, capture the page's own `GetShoppingResults` XHR via CDP, de-chunk + decode with swoop's decoder.** |

The XHR response arrives as `)]}'` + HTTP-chunked `<len>\n<json>` frames; the
`wrb.fr` data row is NOT always the first row — scan all rows of all chunks.

## Usage

```bash
P=~/.agents/skills/flights/.venv/bin/python
S=~/.agents/skills/flights/scripts/flight_search.py

# One way
$P $S CDG JFK 2026-10-28

# Round trip, 2 adults, business
$P $S TLS OPO 2026-11-12 -r 2026-11-19 -a 2 -c business

# Agent consumption
$P $S TLS NCE 2026-10-13 --json -n 10

# Filter-ish: increase -n to see more (initial XHR returns ~15-60 options)
$P $S PAR NYC 2026-10-28 -n 30
```

Options: `origin destination date [-r return_date] [-a adults]
[-c economy|premium-economy|business|first] [--currency EUR] [-n limit]
[--json]`. Airports are IATA codes; city codes (PAR, NYC) work.

Output prices are **decimal currency units** (the RPC sends cents).
`booking_token` in JSON output can be used later for `GetBookingResults` fare
detail queries (swoop's `price_selector`/`check_price` build those).

## Procedure
1. Steel health: `$HOME/.agents/skills/steel-browser/.venv/bin/python
   ~/.agents/skills/steel-browser/scripts/steel_cdp.py health`
2. Run the search (takes ~10-30s: tab open + results XHR + close).
3. Parse `--json` output or the printed table.

## Pitfalls
- **Past dates → gRPC status 3** (INVALID_ARGUMENT). The script pre-checks.
- **Transient rejections**: Google intermittently answers valid searches with
  an HTTP-200 error envelope (known upstream issue for all scrapers). If you
  get "no itineraries in response", **retry once** — usually succeeds.
- Initial XHR ≈ 15-60 itineraries (Google's "best + first batch"). More load
  on scroll in a real browser; not captured. Enough for price discovery.
- Dates in output tuples: script formats them; if you reuse `swoop.decoder`
  directly, `departure_date` is a `(y, m, d)` tuple, times are `(h, m)`.
- The DOM never renders in headless Steel even when data flows — never wait
  for `li[aria-label]` selectors; capture the XHR instead.
- TFS URL building: use the script / `fast_flights.create_query`. Round-trip =
  **two** `FlightQuery` entries (outbound + return) with `trip="round-trip"`.
- Google consent: Steel's shared profile already carries the `SOCS` cookie
  (set once via CDP "Reject all" click). If consent ever reappears, click it
  via `browser-use` with `BU_CDP_URL=http://192.168.1.50:9223`.
- Payment/booking is out of scope: this finds and prices flights.

## Setup / Rebuild

```bash
cd ~/.agents/skills/flights && python3 -m venv .venv \
  && .venv/bin/pip install fast-flights swoop-flights websocket-client typing_extensions
```
(`typing_extensions` is needed because fast-flights' own deps are incomplete.)

## Verification
- `flight_search.py TLS NCE <future-date>` → ≥5 options, cheapest ~€49 nonstop
- `flight_search.py CDG JFK <future-date>` → ~23 options, cheapest ~€500 1-stop
- `flight_search.py TLS OPO <d> -r <d+7> --json` → round-trip totals, ~€60+
- Past date → clean pre-check error, no browser round-trip

## Related
- `steel-browser` skill (CDP plumbing, health check, wall detection)
- `browser-use` skill (fallback interactive control: consent clicks)
- Libraries: `fast-flights` (TFS/protobuf URL builder only), `swoop-flights`
  (response decoder only) — both used as libraries here, not for fetching.
