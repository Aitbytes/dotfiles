#!/usr/bin/env python3
"""
Startup & Funding Data CLI

Sources:
  1. SEC EDGAR (free, no key) — Form D private placement filings via edgartools
  2. Crunchbase API (requires CRUNCHBASE_API_KEY) — company/funding data
  3. SEC EDGAR full-text search (free) — company filings search

Usage:
  python3 startup_data.py --company "Atos Medical"
  python3 startup_data.py --query "voice prosthesis" --source edgar
  python3 startup_data.py --company "InVivo Therapeutics" --source crunchbase
  python3 startup_data.py --query "laryngectomy startup" --limit 10

Options:
  --company     Company name to look up
  --query       Keyword search for companies/filings
  --source      Data source: edgar | crunchbase | both (default: edgar)
  --limit       Max results (default: 10)
  --format      Output format: md or json (default: md)
  --output      Output file path (default: stdout)

Environment variables:
  CRUNCHBASE_API_KEY  — Required for Crunchbase source
"""

import sys
import json
import argparse
import os
import requests


def search_edgar_full_text(query: str, limit: int) -> list[dict]:
    """Search SEC EDGAR full-text search API (free, no key)."""
    url = "https://efts.sec.gov/LATEST/search-index?q={}&dateRange=custom&startdt=2010-01-01&forms=D"
    # Use EDGAR EFTS full-text search
    search_url = "https://efts.sec.gov/LATEST/search-index"
    q_terms = " AND ".join(f'"{w}"' for w in query.split()) if " " in query else f'"{query}"'
    params = {
        "q": q_terms,
        "forms": "D,10-K,S-1",
        "dateRange": "custom",
        "startdt": "2010-01-01",
    }
    headers = {"User-Agent": "research-agent/1.0 (research@example.com)"}

    try:
        resp = requests.get(search_url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        hits = data.get("hits", {}).get("hits", [])[:limit]
        results = []
        for hit in hits:
            src = hit.get("_source", {})
            # display_names is a list like ["COMPANY NAME  (CIK 0000123456)"]
            display_names = src.get("display_names", [])
            company = display_names[0].split("(CIK")[0].strip() if display_names else "N/A"
            ciks = src.get("ciks", [])
            cik = ciks[0] if ciks else ""
            adsh = src.get("adsh", "")
            results.append({
                "source": "SEC EDGAR",
                "company": company,
                "form_type": src.get("form", src.get("root_forms", ["N/A"])[0] if src.get("root_forms") else "N/A"),
                "filed_at": src.get("file_date", "N/A"),
                "description": src.get("file_description", src.get("period_ending", "N/A")),
                "cik": cik,
                "filing_url": f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{adsh.replace('-','')}/{adsh}-index.htm" if adsh else f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=D&dateb=&owner=include&count=40",
            })
        return results
    except requests.exceptions.RequestException as e:
        print(f"  [EDGAR EFTS] error: {e}", file=sys.stderr)
        return []


def search_edgar_company(company: str, limit: int) -> list[dict]:
    """Search SEC EDGAR company search API (free, no key)."""
    url = "https://efts.sec.gov/LATEST/search-index"
    params = {
        "q": f'"{company}"',
        "forms": "D,10-K,S-1",
    }
    headers = {"User-Agent": "research-agent/1.0 (research@example.com)"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        hits = data.get("hits", {}).get("hits", [])[:limit]
        results = []
        for hit in hits:
            src = hit.get("_source", {})
            display_names = src.get("display_names", [])
            company = display_names[0].split("(CIK")[0].strip() if display_names else "N/A"
            ciks = src.get("ciks", [])
            cik = ciks[0] if ciks else ""
            adsh = src.get("adsh", "")
            results.append({
                "source": "SEC EDGAR",
                "company": company,
                "form_type": src.get("form", src.get("root_forms", ["N/A"])[0] if src.get("root_forms") else "N/A"),
                "filed_at": src.get("file_date", "N/A"),
                "cik": cik,
                "filing_url": f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{adsh.replace('-','')}/{adsh}-index.htm" if adsh else f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40",
                "description": src.get("file_description", src.get("period_ending", "")),
            })
        return results
    except requests.exceptions.RequestException as e:
        print(f"  [EDGAR company] error: {e}", file=sys.stderr)
        return []


def search_crunchbase(query: str, api_key: str, limit: int) -> list[dict]:
    """Search Crunchbase for companies (requires API key)."""
    url = "https://api.crunchbase.com/api/v4/searches/organizations"
    headers = {"X-cb-user-key": api_key, "Content-Type": "application/json"}
    payload = {
        "field_ids": [
            "identifier", "short_description", "founded_on",
            "funding_total", "last_funding_type", "last_funding_at",
            "num_funding_rounds", "investor_identifiers", "location_identifiers",
            "categories", "website_url",
        ],
        "query": [
            {
                "type": "predicate",
                "field_id": "facet_ids",
                "operator_id": "includes",
                "values": ["company"],
            }
        ],
        "limit": limit,
    }

    # Add name search if query provided
    if query:
        payload["query"].append({
            "type": "predicate",
            "field_id": "name",
            "operator_id": "contains",
            "values": [query],
        })

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 401:
            sys.exit("ERROR: CRUNCHBASE_API_KEY is invalid or expired.")
        if resp.status_code == 402:
            sys.exit("ERROR: Crunchbase API requires a paid plan for this endpoint.")
        resp.raise_for_status()
        data = resp.json()
        entities = data.get("entities", [])
        results = []
        for entity in entities:
            props = entity.get("properties", {})
            funding = props.get("funding_total", {})
            results.append({
                "source": "Crunchbase",
                "company": props.get("identifier", {}).get("value", "N/A"),
                "description": props.get("short_description", "N/A"),
                "founded": str(props.get("founded_on", {}).get("value", "N/A")),
                "total_funding_usd": funding.get("value_usd", "N/A") if funding else "N/A",
                "last_funding_type": props.get("last_funding_type", "N/A"),
                "last_funding_date": str(props.get("last_funding_at", "N/A")),
                "num_funding_rounds": props.get("num_funding_rounds", "N/A"),
                "location": ", ".join(
                    loc.get("value", "") for loc in props.get("location_identifiers", [])
                ),
                "website": props.get("website_url", "N/A"),
                "categories": ", ".join(
                    cat.get("value", "") for cat in props.get("categories", [])
                ),
            })
        return results
    except requests.exceptions.RequestException as e:
        print(f"  [Crunchbase] error: {e}", file=sys.stderr)
        return []


def format_md(results: list[dict], query: str) -> str:
    lines = [
        "# Startup & Funding Data",
        f"**Query**: `{query}`  ",
        f"**Results**: {len(results)}",
        "",
    ]

    for i, r in enumerate(results, 1):
        source = r.get("source", "")
        company = r.get("company", "N/A")
        lines.append(f"### {i}. {company}")
        lines.append(f"- **Source**: {source}")

        if source == "SEC EDGAR":
            lines.append(f"- **Form Type**: {r.get('form_type', 'N/A')}")
            lines.append(f"- **Filed**: {r.get('filed_at', 'N/A')}")
            lines.append(f"- **CIK**: {r.get('cik', 'N/A')}")
            lines.append(f"- **EDGAR URL**: {r.get('filing_url', r.get('url', 'N/A'))}")
        elif source == "Crunchbase":
            lines.append(f"- **Description**: {r.get('description', 'N/A')}")
            lines.append(f"- **Founded**: {r.get('founded', 'N/A')}")
            funding = r.get("total_funding_usd", "N/A")
            if funding != "N/A" and funding:
                lines.append(f"- **Total Funding**: ${int(funding):,}" if isinstance(funding, (int, float)) else f"- **Total Funding**: {funding}")
            lines.append(f"- **Last Funding Type**: {r.get('last_funding_type', 'N/A')}")
            lines.append(f"- **Last Funding Date**: {r.get('last_funding_date', 'N/A')}")
            lines.append(f"- **Funding Rounds**: {r.get('num_funding_rounds', 'N/A')}")
            lines.append(f"- **Location**: {r.get('location', 'N/A')}")
            lines.append(f"- **Categories**: {r.get('categories', 'N/A')}")
            lines.append(f"- **Website**: {r.get('website', 'N/A')}")

        lines.append("")

    lines.extend([
        "---",
        "**Resources**:",
        "- [SEC EDGAR Full-Text Search](https://efts.sec.gov/LATEST/search-index)",
        "- [SEC EDGAR Company Search](https://www.sec.gov/cgi-bin/browse-edgar)",
        "- [Crunchbase](https://www.crunchbase.com) (paid API)",
        "- [Form D Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=D)",
    ])

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Startup and funding data lookup.")
    p.add_argument("--company", default=None, help="Company name to look up")
    p.add_argument("--query", default=None, help="Keyword search")
    p.add_argument("--source", choices=["edgar", "crunchbase", "both"], default="edgar")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    if not args.company and not args.query:
        sys.exit("ERROR: Provide --company or --query.")

    query_label = args.company or args.query or ""
    crunchbase_key = os.getenv("CRUNCHBASE_API_KEY")

    if args.source in ("crunchbase", "both") and not crunchbase_key:
        sys.exit(
            "ERROR: CRUNCHBASE_API_KEY environment variable is not set.\n"
            "Set it to your Crunchbase API key, or use --source edgar for free SEC data."
        )

    print(f"Startup Data Lookup", file=sys.stderr)
    print(f"  Query : {query_label}", file=sys.stderr)
    print(f"  Source: {args.source}", file=sys.stderr)

    results: list[dict] = []

    if args.source in ("edgar", "both"):
        print("  Querying SEC EDGAR...", file=sys.stderr)
        if args.company:
            results.extend(search_edgar_company(args.company, args.limit))
        else:
            results.extend(search_edgar_full_text(args.query or "", args.limit))

    if args.source in ("crunchbase", "both") and crunchbase_key:
        print("  Querying Crunchbase...", file=sys.stderr)
        results.extend(search_crunchbase(args.company or args.query or "", crunchbase_key, args.limit))

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
