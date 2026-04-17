#!/usr/bin/env python3
"""
EUDAMED Lookup CLI - Search the European Database on Medical Devices.

Uses the unofficial EUDAMED REST API (documented at openregulatory.github.io/eudamed-api).
No API key required. Data is publicly accessible.

Usage:
  python3 eudamed_lookup.py --query "voice prosthesis"
  python3 eudamed_lookup.py --query "laryngectomy" --limit 20
  python3 eudamed_lookup.py --manufacturer "Atos Medical" --limit 10
  python3 eudamed_lookup.py --udi "00380740123456"
  python3 eudamed_lookup.py --query "tracheoesophageal" --format json

Options:
  --query         Keyword search for devices
  --manufacturer  Filter by manufacturer/actor name
  --udi           Look up a specific UDI (Unique Device Identifier)
  --limit         Max results (default: 20)
  --format        Output format: md or json (default: md)
  --output        Output file path (default: stdout)

API: https://ec.europa.eu/tools/eudamed/ (unofficial REST endpoints)
Docs: https://openregulatory.github.io/eudamed-api/
"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shared_runtime import ToolRuntimeError, format_error, request_json

EUDAMED_BASE = "https://ec.europa.eu/tools/eudamed/api"

HEADERS = {
    "User-Agent": "research-agent/1.0",
    "Accept": "application/json",
    "Accept-Language": "en",
}


def search_devices(query: str | None, manufacturer: str | None, limit: int) -> list[dict]:
    url = f"{EUDAMED_BASE}/devices/udiDiData"
    params: dict = {
        "lang": "en",
        "pageSize": min(limit, 50),
        "pageNumber": 1,
    }
    if query:
        params["keyword"] = query
    if manufacturer:
        params["actorName"] = manufacturer

    try:
        data, _ = request_json("GET", url, params=params, headers=HEADERS, provider="eudamed")
        items = data.get("content", data.get("data", []))
        if not isinstance(items, list):
            items = []

        results = []
        for item in items[:limit]:
            risk_class_raw = item.get("riskClass", {})
            risk_class = risk_class_raw.get("code", "N/A").replace("refdata.risk-class.", "") if isinstance(risk_class_raw, dict) else str(risk_class_raw)
            status_raw = item.get("deviceStatusType", {})
            status = status_raw.get("code", "N/A").replace("refdata.device-model-status.", "") if isinstance(status_raw, dict) else str(status_raw)
            results.append({
                "source": "EUDAMED",
                "udi_di": item.get("primaryDi", item.get("basicUdi", "N/A")),
                "device_name": item.get("tradeName", item.get("deviceName", "N/A")),
                "manufacturer": item.get("manufacturerName", item.get("actorName", "N/A")),
                "model": item.get("deviceModel", item.get("modelNumber", "N/A")),
                "catalogue_number": item.get("catalogueNumber", "N/A"),
                "device_type": item.get("deviceType", "N/A"),
                "risk_class": risk_class,
                "mdr_article": item.get("mdrArticle", item.get("applicableLegislation", "N/A")),
                "status": status,
                "country": item.get("countryCode", "N/A"),
                "authorised_rep": item.get("authorisedRepresentativeName", "N/A"),
                "url": f"https://ec.europa.eu/tools/eudamed/#/screen/search-device?lang=en&keyword={query or ''}",
            })
        return results
    except ToolRuntimeError:
        raise


def search_actors(manufacturer: str, limit: int) -> list[dict]:
    url = f"{EUDAMED_BASE}/actors"
    params: dict = {
        "lang": "en",
        "pageSize": min(limit, 50),
        "pageNumber": 1,
        "actorName": manufacturer,
    }

    try:
        data, _ = request_json("GET", url, params=params, headers=HEADERS, provider="eudamed")
        items = data.get("content", data.get("data", []))
        if not isinstance(items, list):
            items = []

        results = []
        for item in items[:limit]:
            results.append({
                "source": "EUDAMED Actors",
                "actor_id": item.get("actorId", item.get("id", "N/A")),
                "name": item.get("actorName", item.get("name", "N/A")),
                "role": item.get("actorType", item.get("role", "N/A")),
                "country": item.get("countryCode", "N/A"),
                "registration_number": item.get("registrationNumber", "N/A"),
                "status": item.get("status", "N/A"),
            })
        return results
    except ToolRuntimeError:
        raise


def lookup_udi(udi: str) -> list[dict]:
    url = f"{EUDAMED_BASE}/devices/udiDiData/{udi}"
    params = {"lang": "en"}

    try:
        data, _ = request_json("GET", url, params=params, headers=HEADERS, provider="eudamed")
        risk_class_raw = data.get("riskClass", {})
        risk_class = risk_class_raw.get("code", "N/A").replace("refdata.risk-class.", "") if isinstance(risk_class_raw, dict) else str(risk_class_raw)
        status_raw = data.get("deviceStatusType", {})
        status = status_raw.get("code", "N/A").replace("refdata.device-model-status.", "") if isinstance(status_raw, dict) else str(status_raw)
        return [{
            "source": "EUDAMED",
            "udi_di": data.get("primaryDi", data.get("basicUdi", udi)),
            "device_name": data.get("tradeName", data.get("deviceName", "N/A")),
            "manufacturer": data.get("manufacturerName", data.get("actorName", "N/A")),
            "model": data.get("deviceModel", data.get("modelNumber", "N/A")),
            "catalogue_number": data.get("catalogueNumber", "N/A"),
            "device_type": data.get("deviceType", "N/A"),
            "risk_class": risk_class,
            "status": status,
            "country": data.get("countryCode", "N/A"),
            "authorised_rep": data.get("authorisedRepresentativeName", "N/A"),
        }]
    except ToolRuntimeError:
        raise


def format_md(results: list[dict], query: str) -> str:
    lines = [
        "# EUDAMED — European Medical Device Database",
        f"**Query**: `{query}`  ",
        f"**Results**: {len(results)}",
        "",
        "> Data from EUDAMED (European Database on Medical Devices), EU MDR/IVDR registry.",
        "",
    ]

    for i, r in enumerate(results, 1):
        source = r.get("source", "EUDAMED")
        if source == "EUDAMED Actors":
            lines.append(f"### {i}. {r.get('name', 'N/A')} *(Actor/Manufacturer)*")
            lines.append(f"- **Source**: {source}")
            lines.append(f"- **Actor ID**: {r.get('actor_id', 'N/A')}")
            lines.append(f"- **Role**: {r.get('role', 'N/A')}")
            lines.append(f"- **Country**: {r.get('country', 'N/A')}")
            lines.append(f"- **Registration Number**: {r.get('registration_number', 'N/A')}")
            lines.append(f"- **Status**: {r.get('status', 'N/A')}")
        else:
            lines.append(f"### {i}. {r.get('device_name', 'N/A')}")
            lines.append(f"- **Source**: {source}")
            lines.append(f"- **UDI-DI**: {r.get('udi_di', 'N/A')}")
            lines.append(f"- **Manufacturer**: {r.get('manufacturer', 'N/A')}")
            lines.append(f"- **Model**: {r.get('model', 'N/A')}")
            lines.append(f"- **Catalogue Number**: {r.get('catalogue_number', 'N/A')}")
            lines.append(f"- **Device Type**: {r.get('device_type', 'N/A')}")
            lines.append(f"- **Risk Class**: {r.get('risk_class', 'N/A')}")
            lines.append(f"- **MDR Article**: {r.get('mdr_article', 'N/A')}")
            lines.append(f"- **Status**: {r.get('status', 'N/A')}")
            lines.append(f"- **Country**: {r.get('country', 'N/A')}")
            lines.append(f"- **Authorised Rep (EU)**: {r.get('authorised_rep', 'N/A')}")
            if r.get("url"):
                lines.append(f"- **EUDAMED URL**: {r['url']}")

        lines.append("")

    lines.extend([
        "---",
        "**Resources**:",
        "- [EUDAMED Search](https://ec.europa.eu/tools/eudamed/#/screen/search-device)",
        "- [BEUDAMED (better search UI)](https://beudamed.com)",
        "- [EUDAMED API Docs (unofficial)](https://openregulatory.github.io/eudamed-api/)",
        "- [EU MDR Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017R0745)",
    ])

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="EUDAMED EU medical device database lookup.")
    p.add_argument("--query", default=None, help="Keyword search for devices")
    p.add_argument("--manufacturer", default=None, help="Manufacturer/actor name")
    p.add_argument("--udi", default=None, help="Specific UDI-DI to look up")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    if not any([args.query, args.manufacturer, args.udi]):
        sys.exit("ERROR: Provide at least one of --query, --manufacturer, or --udi.")

    query_label = args.udi or args.query or args.manufacturer or ""

    print(f"EUDAMED Lookup", file=sys.stderr)
    print(f"  Query : {query_label}", file=sys.stderr)

    results: list[dict] = []

    try:
        if args.udi:
            print("  Looking up UDI...", file=sys.stderr)
            results = lookup_udi(args.udi)
        else:
            print("  Searching devices...", file=sys.stderr)
            results.extend(search_devices(args.query, args.manufacturer, args.limit))
            if args.manufacturer:
                print("  Searching actors...", file=sys.stderr)
                results.extend(search_actors(args.manufacturer, args.limit))
    except ToolRuntimeError as e:
        sys.exit(format_error(e))

    print(f"  Found : {len(results)} results", file=sys.stderr)

    if not results:
        print(
            "\nNo results found. EUDAMED data may be limited — try the web UI at:\n"
            "https://ec.europa.eu/tools/eudamed/#/screen/search-device\n"
            "or BEUDAMED at https://beudamed.com"
        )
        return

    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:
        output = format_md(results, query_label)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved -> {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
