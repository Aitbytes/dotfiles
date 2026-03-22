#!/usr/bin/env python3
"""
FDA 510(k) Lookup CLI - Query the openFDA Device 510(k) Clearances API.

Usage:
  python3 fda_510k.py --query "laryngectomy"
  python3 fda_510k.py --query "voice prosthesis" --limit 20 --format md
  python3 fda_510k.py --k-number "K201234"
  python3 fda_510k.py --applicant "Atos Medical" --limit 10

Options:
  --query       Free-text search across all 510(k) fields
  --k-number    Specific 510(k) number (e.g. K201234)
  --applicant   Filter by applicant/company name
  --device-name Filter by device name
  --decision    Filter by decision: SESE (Substantially Equivalent), NSUB, etc.
  --date-from   Filter by decision date from (YYYYMMDD)
  --date-to     Filter by decision date to (YYYYMMDD)
  --limit       Max results to return (default: 10, max: 100)
  --format      Output format: md or json (default: md)
  --output      Output file path (default: stdout)
  --api-key     openFDA API key (optional, increases rate limit)

API: https://api.fda.gov/device/510k.json (no key required for basic use)
Docs: https://open.fda.gov/apis/device/510k/
"""

import sys
import json
import argparse
import os
import requests

BASE_URL = "https://api.fda.gov/device/510k.json"


def build_search(args) -> str:
    """Build the openFDA search query string."""
    parts = []

    if args.k_number:
        parts.append(f'k_number:"{args.k_number}"')
    if args.applicant:
        parts.append(f'applicant:"{args.applicant}"')
    if args.device_name:
        parts.append(f'device_name:"{args.device_name}"')
    if args.decision:
        parts.append(f'decision_code:"{args.decision}"')
    if args.date_from or args.date_to:
        date_from = args.date_from or "19760101"
        date_to = args.date_to or "20991231"
        parts.append(f"decision_date:[{date_from}+TO+{date_to}]")
    if args.query and not args.k_number:
        # Free-text search across multiple fields
        parts.append(args.query)

    return "+AND+".join(parts) if parts else ""


def fetch_510k(search: str, limit: int, api_key: str | None) -> dict:
    params: dict = {"limit": min(limit, 100)}
    if search:
        params["search"] = search
    if api_key:
        params["api_key"] = api_key

    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        if resp.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        sys.exit(f"ERROR: HTTP {e.response.status_code} from openFDA — {e.response.text[:300]}")
    except requests.exceptions.RequestException as e:
        sys.exit(f"ERROR: {e}")


def format_result_md(r: dict, index: int) -> str:
    lines = [
        f"### {index}. {r.get('device_name', 'Unknown Device')}",
        f"- **510(k) Number**: {r.get('k_number', 'N/A')}",
        f"- **Applicant**: {r.get('applicant', 'N/A')}",
        f"- **Decision**: {r.get('decision_description', r.get('decision_code', 'N/A'))}",
        f"- **Decision Date**: {r.get('decision_date', 'N/A')}",
        f"- **Product Code**: {r.get('product_code', 'N/A')}",
        f"- **Advisory Committee**: {r.get('advisory_committee_description', r.get('advisory_committee', 'N/A'))}",
        f"- **Regulation Number**: {r.get('regulation_number', 'N/A')}",
        f"- **Statement**: {r.get('statement_or_summary', 'N/A')[:300]}",
    ]

    # Predicate devices
    predicates = r.get("openfda", {})
    if predicates:
        lines.append(f"- **OpenFDA Data**: {json.dumps(predicates)[:200]}")

    lines.append("")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="FDA 510(k) lookup via openFDA API.")
    p.add_argument("--query", default=None, help="Free-text search query")
    p.add_argument("--k-number", default=None, help="Specific 510(k) number")
    p.add_argument("--applicant", default=None, help="Applicant/company name")
    p.add_argument("--device-name", default=None, help="Device name filter")
    p.add_argument("--decision", default=None, help="Decision code (e.g. SESE)")
    p.add_argument("--date-from", default=None, help="Decision date from YYYYMMDD")
    p.add_argument("--date-to", default=None, help="Decision date to YYYYMMDD")
    p.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--output", default=None, help="Output file path")
    p.add_argument("--api-key", default=os.getenv("OPENFDA_API_KEY"), help="openFDA API key")
    args = p.parse_args()

    if not any([args.query, args.k_number, args.applicant, args.device_name]):
        sys.exit("ERROR: Provide at least one of --query, --k-number, --applicant, or --device-name.")

    search = build_search(args)
    print(f"Querying openFDA 510(k) API...", file=sys.stderr)
    print(f"  Search: {search or '(all)'}", file=sys.stderr)
    print(f"  Limit : {args.limit}", file=sys.stderr)

    data = fetch_510k(search, args.limit, args.api_key)
    results = data.get("results", [])
    total = data.get("meta", {}).get("results", {}).get("total", len(results))

    print(f"  Found : {total} total records, returning {len(results)}", file=sys.stderr)

    if args.format == "json":
        output = json.dumps(data, indent=2)
    else:
        lines = [
            f"# FDA 510(k) Search Results",
            f"**Query**: `{search or '(all)'}`  ",
            f"**Total records**: {total}  ",
            f"**Showing**: {len(results)}",
            "",
        ]
        for i, r in enumerate(results, 1):
            lines.append(format_result_md(r, i))
        output = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved -> {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
