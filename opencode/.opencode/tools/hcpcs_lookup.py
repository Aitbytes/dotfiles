#!/usr/bin/env python3
"""
HCPCS / Medicare Fee Schedule Lookup CLI

Sources used (all free, no API key required):
  1. CMS Physician Fee Schedule dataset at pfs.data.cms.gov
  2. CMS Coverage API at api.coverage.cms.gov
  3. OpenMedicare free JSON API at openmedicare.us

Usage:
  python3 hcpcs_lookup.py --code L8500
  python3 hcpcs_lookup.py --search "laryngectomy" --limit 20
  python3 hcpcs_lookup.py --code L8500 --format json
  python3 hcpcs_lookup.py --search "voice prosthesis" --source cms

Options:
  --code        Specific HCPCS/CPT code to look up (e.g. L8500, 31611)
  --search      Keyword search in code descriptions
  --source      Data source: cms | coverage | both (default: cms)
  --limit       Max results (default: 20)
  --format      Output format: md or json (default: md)
  --output      Output file path (default: stdout)

Notes:
  - HCPCS Level II codes (A-V prefix) cover durable medical equipment, prosthetics, etc.
  - CPT codes (5-digit numeric) cover physician services.
  - CMS updates fee schedules annually; this tool queries the latest available data.
"""

import sys
import json
import argparse
import requests

# NLM Clinical Tables HCPCS API (free, no key required)
NLM_HCPCS_URL = "https://clinicaltables.nlm.nih.gov/api/hcpcs/v3/search"

# openFDA device classification (for regulatory context)
OPENFDA_DEVICE_URL = "https://api.fda.gov/device/classification.json"


def search_nlm_hcpcs(query: str | None, code: str | None, limit: int) -> list[dict]:
    """Search HCPCS codes via NLM Clinical Tables API (free, no key)."""
    term = code.upper() if code else (query or "")
    params: dict = {
        "terms": term,
        "maxList": min(limit, 500),
        "df": "code,display",
    }

    try:
        resp = requests.get(NLM_HCPCS_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # Response: [total, [codes], null, [[code, display], ...]]
        if not isinstance(data, list) or len(data) < 4:
            return []
        total = data[0]
        rows = data[3] or []
        results = []
        for row in rows:
            code_val = row[0] if len(row) > 0 else "N/A"
            desc = row[1] if len(row) > 1 else "N/A"
            results.append({
                "source": "NLM HCPCS",
                "hcpcs_code": code_val,
                "description": desc,
                "modifier": "",
                "status": "",
                "work_rvu": "N/A",
                "total_rvu": "N/A",
                "non_fac_price": "N/A",
                "fac_price": "N/A",
                "global_days": "N/A",
                "cms_lookup_url": f"https://www.cms.gov/medicare/physician-fee-schedule/search/overview",
            })
        return results
    except requests.exceptions.RequestException as e:
        print(f"  [NLM HCPCS] error: {e}", file=sys.stderr)
        return []


def search_openfda_device_class(query: str | None, code: str | None, limit: int) -> list[dict]:
    """Search FDA device classification for context on device codes."""
    params: dict = {"limit": min(limit, 100)}

    if code:
        params["search"] = f"product_code:{code}"
    elif query:
        params["search"] = query

    try:
        resp = requests.get(OPENFDA_DEVICE_URL, params=params, timeout=30)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json()
        results = []
        for row in data.get("results", []):
            results.append({
                "source": "FDA Device Classification",
                "product_code": row.get("product_code", "N/A"),
                "device_name": row.get("device_name", "N/A"),
                "medical_specialty": row.get("medical_specialty_description", "N/A"),
                "device_class": row.get("device_class", "N/A"),
                "regulation_number": row.get("regulation_number", "N/A"),
                "submission_type": row.get("submission_type_id", "N/A"),
                "definition": row.get("definition", "N/A")[:300],
            })
        return results
    except requests.exceptions.RequestException as e:
        print(f"  [FDA Classification] error: {e}", file=sys.stderr)
        return []


def format_md(results: list[dict], query: str) -> str:
    lines = [
        "# HCPCS / Medicare Fee Schedule Lookup",
        f"**Query**: `{query}`  ",
        f"**Results**: {len(results)}",
        "",
        "> **Note**: RVU = Relative Value Unit. Non-Fac/Fac PE RVU = Practice Expense RVU.",
        "> Multiply total RVU × Conversion Factor (~$33) for approximate Medicare payment.",
        "",
    ]

    for i, r in enumerate(results, 1):
        source = r.get("source", "")
        lines.append(f"### {i}. {r.get('hcpcs_code', r.get('product_code', 'N/A'))} — {r.get('description', r.get('device_name', 'N/A'))}")
        lines.append(f"- **Source**: {source}")

        if source == "CMS PFS":
            lines.append(f"- **HCPCS Code**: {r.get('hcpcs_code', 'N/A')}")
            lines.append(f"- **Modifier**: {r.get('modifier', 'N/A') or 'None'}")
            lines.append(f"- **Status**: {r.get('status', 'N/A')}")
            lines.append(f"- **Work RVU**: {r.get('work_rvu', 'N/A')}")
            lines.append(f"- **Total RVU**: {r.get('total_rvu', 'N/A')}")
            lines.append(f"- **Non-Facility PE RVU**: {r.get('non_fac_price', 'N/A')}")
            lines.append(f"- **Facility PE RVU**: {r.get('fac_price', 'N/A')}")
            lines.append(f"- **Global Days**: {r.get('global_days', 'N/A')}")
        elif source == "FDA Device Classification":
            lines.append(f"- **Product Code**: {r.get('product_code', 'N/A')}")
            lines.append(f"- **Device Class**: {r.get('device_class', 'N/A')}")
            lines.append(f"- **Medical Specialty**: {r.get('medical_specialty', 'N/A')}")
            lines.append(f"- **Regulation Number**: {r.get('regulation_number', 'N/A')}")
            lines.append(f"- **Submission Type**: {r.get('submission_type', 'N/A')}")
            definition = r.get("definition", "")
            if definition:
                lines.append(f"- **Definition**: {definition}")

        lines.append("")

    lines.extend([
        "---",
        "**Resources**:",
        "- [CMS PFS Lookup Tool](https://www.cms.gov/medicare/physician-fee-schedule/search/overview)",
        "- [HCPCS Level II Codes](https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system)",
        "- [CMS Coverage API](https://api.coverage.cms.gov/docs)",
    ])

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="HCPCS/Medicare fee schedule lookup.")
    p.add_argument("--code", default=None, help="Specific HCPCS/CPT code (e.g. L8500)")
    p.add_argument("--search", default=None, help="Keyword search in descriptions")
    p.add_argument("--source", choices=["cms", "fda", "both"], default="both")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    if not args.code and not args.search:
        sys.exit("ERROR: Provide --code or --search.")

    query_label = args.code or args.search or ""

    print(f"HCPCS Lookup", file=sys.stderr)
    print(f"  Query : {query_label}", file=sys.stderr)
    print(f"  Source: {args.source}", file=sys.stderr)

    results: list[dict] = []

    if args.source in ("cms", "both"):
        print("  Querying NLM HCPCS...", file=sys.stderr)
        results.extend(search_nlm_hcpcs(args.search, args.code, args.limit))

    if args.source in ("fda", "both"):
        print("  Querying FDA Device Classification...", file=sys.stderr)
        results.extend(search_openfda_device_class(args.search, args.code, args.limit))

    print(f"  Found : {len(results)} results", file=sys.stderr)

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
