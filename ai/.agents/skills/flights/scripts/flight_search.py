#!/usr/bin/env python3
"""Flight search via Google Flights — TFS URL + Steel browser XHR capture + swoop decoder.

Pipeline (works from datacenter/LAN IPs where Google Flights' DOM never renders):
  1. Build the base64-protobuf TFS search URL (fast-flights query builder).
  2. Open it in the LAN Steel browser over CDP and watch network events.
  3. Capture the GetShoppingResults XHR body (the page always fires it, even
     when it stays stuck on "Loading results").
  4. De-chunk the batchexecute stream, parse with swoop's typed decoder.

Requires: fast-flights, swoop-flights, websocket-client (see skill venv).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
import urllib.request
from websocket import create_connection

from fast_flights import FlightQuery, Passengers, create_query
from swoop.decoder import decode_result

STEEL_CDP = "http://192.168.1.50:9223"
RPC_MARKER = "FlightsFrontendService/GetShoppingResults"


# --------------------------------------------------------------------------- TFS URL

def build_url(
    legs: list[tuple[str, str, str]],
    round_trip: bool,
    adults: int = 1,
    currency: str = "EUR",
    cabin: str = "economy",
) -> str:
    """legs = [(date, origin, destination), ...]; round-trip = 2 legs."""
    queries = [FlightQuery(date=d, from_airport=o, to_airport=t) for d, o, t in legs]
    q = create_query(
        flights=queries,
        trip="round-trip" if round_trip else "one-way",
        seat=cabin,  # type: ignore[arg-type]
        passengers=Passengers(adults=adults),
        language="en-US",
        currency=currency,
    )
    return q.url()


# --------------------------------------------------------------------------- CDP capture

def _new_tab(ws_http: str, url: str) -> dict:
    req = urllib.request.Request(f"{ws_http}/json/new?{url}", method="PUT")
    return json.loads(urllib.request.urlopen(req, timeout=15).read())


def capture_shopping_xhr(url: str, wait_s: int = 35, ws_http: str = STEEL_CDP) -> str:
    """Open url in Steel, return the raw GetShoppingResults response body."""
    tab = _new_tab(ws_http, url)
    ws = create_connection(tab["webSocketDebuggerUrl"], timeout=60)
    mid = 0

    def send(method: str, params: dict | None = None) -> int:
        nonlocal mid
        mid += 1
        ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        return mid

    send("Network.enable")
    rpc_ids: dict[str, str] = {}
    last_body = None
    ws.settimeout(0.5)
    deadline = time.time() + wait_s
    try:
        while time.time() < deadline:
            try:
                msg = json.loads(ws.recv())
            except Exception:
                continue
            m, p = msg.get("method", ""), msg.get("params", {})
            if m == "Network.requestWillBeSent" and RPC_MARKER in p["request"]["url"]:
                rpc_ids[p["requestId"]] = p["request"]["url"]
            elif m == "Network.loadingFinished" and p.get("requestId") in rpc_ids:
                rid = p["requestId"]
                call = send("Network.getResponseBody", {"requestId": rid})
                ws.settimeout(10)
                try:
                    while True:
                        m2 = json.loads(ws.recv())
                        if m2.get("id") == call:
                            body = (m2.get("result") or {}).get("body", "")
                            if len(body) > 1000:  # real payload, not an error envelope
                                last_body = body
                            break
                except Exception:
                    pass
                ws.settimeout(0.5)
            if last_body:
                break  # got what we came for
    finally:
        try:
            ws.close()
        except Exception:
            pass
        try:
            urllib.request.urlopen(f"{ws_http}/json/close/{tab['id']}", timeout=10)
        except Exception:
            pass
    return last_body


# --------------------------------------------------------------------------- parsing

def dechunk(raw: str) -> list[str]:
    """batchexecute `rt=c` streaming: )]}' prefix, then <len>\\n<chunk> frames."""
    body = raw[4:] if raw.startswith(")]}'") else raw
    out, i = [], 0
    while i < len(body):
        while i < len(body) and body[i] in "\r\n ":
            i += 1
        j = body.find("\n", i)
        if j == -1:
            break
        try:
            n = int(body[i:j].strip())
        except ValueError:
            break
        out.append(body[j + 1 : j + 1 + n])
        i = j + 1 + n
    return out


def parse_options(raw: str):
    """Return swoop Itinerary objects sorted by price (raises if Google rejected)."""
    chunks = dechunk(raw)
    if not chunks:
        raise RuntimeError("empty/invalid RPC response (blocked or stale page)")
    dec = json.JSONDecoder()
    err_status = None
    # the payload may live in any wrb.fr row of any chunk — scan until one decodes
    for chunk in chunks:
        try:
            outer, _ = dec.raw_decode(chunk)
        except json.JSONDecodeError:
            continue
        for row in outer:
            if not (isinstance(row, list) and len(row) > 2 and row[0] == "wrb.fr"):
                continue
            if isinstance(row[2], str) and row[2]:
                try:
                    result = decode_result(json.loads(row[2]))
                except Exception:
                    continue
                opts = result.best + result.other
                if opts:
                    return sorted(opts, key=lambda o: o.price_info.price)
            elif row[2] is None and len(row) > 4 and row[4]:
                err_status = row[4][0]
    if err_status is not None:
        hint = {3: "INVALID_ARGUMENT (date in the past? bad airports?)",
                8: "RESOURCE_EXHAUSTED (rate limited)",
                13: "INTERNAL (Google rejected the request)"}.get(
                    err_status, "upstream error")
        raise RuntimeError(f"Google returned gRPC status {err_status}: {hint}")
    raise RuntimeError("no itineraries in response (transient rejection — retry once; "
                       "if persistent, the route/date may genuinely have no data)")


# --------------------------------------------------------------------------- output

def hhmm(t) -> str:
    if isinstance(t, (tuple, list)) and len(t) >= 2:
        return f"{t[0]:02d}:{t[1]:02d}"
    if isinstance(t, str):
        return t
    return str(t)


def iso_date(d) -> str:
    if isinstance(d, (tuple, list)) and len(d) >= 3:
        return f"{d[0]:04d}-{d[1]:02d}-{d[2]:02d}"
    return str(d)


def print_table(opts, currency: str, limit: int) -> None:
    print(f"{'price':>10}  {'depart':>5}-{'arrive':<5}  {'dur':>5}  stops  itinerary")
    print("-" * 78)
    for o in opts[:limit]:
        segs = " + ".join(
            f"{s.flight_number} {s.departure_airport_code}-{s.arrival_airport_code}"
            for s in o.segments
        )
        dep, arr = hhmm(o.departure_time), hhmm(o.arrival_time)
        dur = f"{o.travel_time // 60}h{o.travel_time % 60:02d}"
        print(f"{o.price_info.price / 100:>9.2f}  {dep}-{arr:<5}  {dur:>5}  {o.stop_count:^5}  {segs}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Search Google Flights via Steel browser")
    ap.add_argument("origin", help="IATA origin (e.g. CDG, TLS, PAR)")
    ap.add_argument("destination", help="IATA destination")
    ap.add_argument("date", help="departure date YYYY-MM-DD")
    ap.add_argument("-r", "--return-date", help="return date YYYY-MM-DD (round trip)")
    ap.add_argument("-a", "--adults", type=int, default=1)
    ap.add_argument("-c", "--cabin", default="economy",
                    choices=["economy", "premium-economy", "business", "first"])
    ap.add_argument("--currency", default="EUR")
    ap.add_argument("-n", "--limit", type=int, default=15)
    ap.add_argument("--json", action="store_true", help="JSON output for agents")
    args = ap.parse_args()

    for name, d in (("date", args.date), ("return-date", args.return_date)):
        if d and d < str(datetime.date.today()):
            print(f"error: {name} {d} is in the past (Google returns INVALID_ARGUMENT)",
                  file=sys.stderr)
            return 2

    legs = [(args.date, args.origin.upper(), args.destination.upper())]
    if args.return_date:
        legs.append((args.return_date, args.destination.upper(), args.origin.upper()))
    url = build_url(legs, round_trip=bool(args.return_date),
                    adults=args.adults, currency=args.currency, cabin=args.cabin)

    try:
        raw = capture_shopping_xhr(url)
        if not raw:
            print("error: no shopping XHR captured (Steel up? try again — transient "
                  "error envelopes happen)", file=sys.stderr)
            return 1
        opts = parse_options(raw)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        out = []
        for o in opts:
            out.append({
                "price": o.price_info.price / 100,
                "currency": o.price_info.currency,
                "date": iso_date(o.departure_date),
                "depart": hhmm(o.departure_time),
                "arrive": hhmm(o.arrival_time),
                "duration_min": o.travel_time,
                "stops": o.stop_count,
                "airlines": o.airline_names,
                "segments": [f"{s.flight_number} {s.departure_airport_code}-{s.arrival_airport_code}"
                             for s in o.segments],
                "booking_token": o.booking_token,
            })
        print(json.dumps(out[: args.limit], indent=1))
    else:
        kind = "round trip" if args.return_date else "one way"
        print(f"{args.origin.upper()}->{args.destination.upper()} {kind} "
              f"{args.date}" + (f" / {args.return_date}" if args.return_date else "") +
              f" — {len(opts)} options\n")
        print_table(opts, args.currency, args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
