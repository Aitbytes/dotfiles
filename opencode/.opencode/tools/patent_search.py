#!/usr/bin/env python3
"""
Patent Search CLI - Search patents via Google Patents and USPTO.

Uses the Google Patents CSV export endpoint (no API key required) and
optionally the USPTO Open Data Portal (requires PATENT_CLIENT_ODP_API_KEY).

Usage:
  python3 patent_search.py --query "voice prosthesis laryngectomy"
  python3 patent_search.py --query "tracheoesophageal" --assignee "Atos Medical"
  python3 patent_search.py --query "electrolarynx" --date-from 2015 --limit 20
  python3 patent_search.py --patent-number "US10413399B2"
  python3 patent_search.py --query "voice prosthesis" --country US --limit 10

Options:
  --query         Keyword search query (required unless --patent-number given)
  --patent-number Fetch a specific patent by number (opens Google Patents URL)
  --assignee      Filter by assignee/company name
  --inventor      Filter by inventor name
  --country       Country code filter: US, EP, WO, DE, etc. (default: all)
  --date-from     Filter by priority date year from (e.g. 2015)
  --date-to       Filter by priority date year to (e.g. 2024)
  --limit         Max results (default: 10, max: 100)
  --format        Output format: md or json (default: md)
  --output        Output file path (default: stdout)

Data source: Google Patents CSV export (patents.google.com)
No API key required.
"""

import sys
import os
import json
import argparse
import csv
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shared_runtime import ToolRuntimeError, format_error, request_text

GOOGLE_PATENTS_XHR = "https://patents.google.com/xhr/query"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://patents.google.com/",
}


def build_google_patents_url(query: str, assignee: str | None, inventor: str | None,
                              country: str | None, date_from: str | None,
                              date_to: str | None, limit: int) -> str:
    parts = []
    if query:
        parts.append(query)
    if assignee:
        parts.append(f'assignee:"{assignee}"')
    if inventor:
        parts.append(f'inventor:"{inventor}"')

    q = "+".join(p.replace(" ", "+") for p in parts)
    url_parts = [f"q={q}"]

    if date_from:
        url_parts.append(f"after=priority:{date_from}0101")
    if date_to:
        url_parts.append(f"before=priority:{date_to}1231")
    if country:
        url_parts.append(f"country={country.upper()}")

    return "&".join(url_parts)


def search_google_patents(query: str, assignee: str | None, inventor: str | None,
                           country: str | None, date_from: str | None,
                           date_to: str | None, limit: int) -> list[dict]:
    url_params = build_google_patents_url(query, assignee, inventor, country, date_from, date_to, limit)
    params = {
        "url": url_params,
        "exp": "",
        "download": "false",
    }

    try:
        text, _ = request_text("GET", GOOGLE_PATENTS_XHR, params=params, headers=HEADERS, provider="patent_search", proxy_mode="direct")
        lines = text.strip().splitlines()
        csv_lines = []
        for line in lines:
            if line.startswith("search URL:,"):
                continue
            csv_lines.append(line)

        if not csv_lines:
            return []

        reader = csv.DictReader(io.StringIO("\n".join(csv_lines)))
        results = []
        for i, row in enumerate(reader):
            if i >= limit:
                break
            results.append({
                "source": "Google Patents",
                "patent_number": row.get("id", "N/A"),
                "title": row.get("title", "N/A"),
                "assignee": row.get("assignee", "N/A"),
                "inventor": row.get("inventor/author", "N/A"),
                "priority_date": row.get("priority date", "N/A"),
                "filing_date": row.get("filing/creation date", "N/A"),
                "publication_date": row.get("publication date", "N/A"),
                "grant_date": row.get("grant date", "N/A"),
                "url": row.get("result link", "N/A"),
            })
        return results
    except ToolRuntimeError:
        raise


def fetch_patent_by_number(patent_number: str) -> list[dict]:
    pn_clean = patent_number.replace("-", "")
    url = f"https://patents.google.com/patent/{pn_clean}/en"

    try:
        text, _ = request_text("GET", url, headers=HEADERS, provider="patent_search", proxy_mode="direct")
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text, "lxml")

        title_el = soup.find("span", {"itemprop": "title"})
        title = title_el.get_text(strip=True) if title_el else "N/A"

        abstract_el = soup.find("div", {"class": "abstract"})
        if not abstract_el:
            abstract_el = soup.find("section", {"itemprop": "description"})
        abstract = abstract_el.get_text(strip=True)[:500] if abstract_el else "N/A"

        return [{
            "source": "Google Patents",
            "patent_number": patent_number,
            "title": title,
            "abstract": abstract,
            "url": url,
        }]
    except ToolRuntimeError:
        raise


def format_md(results: list[dict], query: str) -> str:
    lines = [
        "# Patent Search Results",
        f"**Query**: `{query}`  ",
        f"**Results**: {len(results)}",
        f"**Source**: Google Patents",
        "",
    ]

    for i, r in enumerate(results, 1):
        lines.append(f"### {i}. {r.get('title', 'N/A')}")
        lines.append(f"- **Patent Number**: {r.get('patent_number', 'N/A')}")
        lines.append(f"- **Assignee**: {r.get('assignee', 'N/A')}")
        lines.append(f"- **Inventor**: {r.get('inventor', 'N/A')}")
        lines.append(f"- **Priority Date**: {r.get('priority_date', 'N/A')}")
        lines.append(f"- **Filing Date**: {r.get('filing_date', 'N/A')}")
        lines.append(f"- **Publication Date**: {r.get('publication_date', 'N/A')}")
        lines.append(f"- **Grant Date**: {r.get('grant_date', 'N/A')}")
        if r.get("abstract"):
            lines.append(f"- **Abstract**: {r['abstract'][:300]}...")
        lines.append(f"- **URL**: {r.get('url', 'N/A')}")
        lines.append("")

    lines.extend([
        "---",
        "**Resources**:",
        "- [Google Patents](https://patents.google.com)",
        "- [USPTO Patent Public Search](https://ppubs.uspto.gov/pubwebapp/static/pages/ppubsbasic.html)",
        "- [Espacenet (EPO)](https://worldwide.espacenet.com)",
        "- [WIPO PatentScope](https://patentscope.wipo.int)",
    ])

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Patent search via Google Patents.")
    p.add_argument("--query", default=None, help="Keyword search query")
    p.add_argument("--patent-number", default=None, help="Specific patent number")
    p.add_argument("--assignee", default=None, help="Assignee/company name")
    p.add_argument("--inventor", default=None, help="Inventor name")
    p.add_argument("--country", default=None, help="Country code (US, EP, WO, DE, etc.)")
    p.add_argument("--date-from", default=None, help="Priority date year from (e.g. 2015)")
    p.add_argument("--date-to", default=None, help="Priority date year to (e.g. 2024)")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    if not any([args.query, args.patent_number, args.assignee, args.inventor]):
        sys.exit("ERROR: Provide at least one of --query, --patent-number, --assignee, or --inventor.")

    query_label = args.patent_number or args.query or args.assignee or args.inventor or ""

    print(f"Patent Search", file=sys.stderr)
    print(f"  Query : {query_label}", file=sys.stderr)
    print(f"  Limit : {args.limit}", file=sys.stderr)

    results: list[dict] = []

    try:
        if args.patent_number:
            print("  Fetching specific patent...", file=sys.stderr)
            results = fetch_patent_by_number(args.patent_number)
        else:
            print("  Searching Google Patents...", file=sys.stderr)
            results = search_google_patents(
                args.query or "",
                args.assignee,
                args.inventor,
                args.country,
                args.date_from,
                args.date_to,
                args.limit,
            )
    except ToolRuntimeError as e:
        sys.exit(format_error(e))

    print(f"  Found : {len(results)} results", file=sys.stderr)

    if args.format == "json":
        output = json.dumps(results, indent=2, default=str)
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
