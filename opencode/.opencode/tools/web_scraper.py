#!/usr/bin/env python3
"""
Web Scraper CLI - Fetch and extract text/data from any public URL.

Usage:
  python3 web_scraper.py --url "https://example.com"
  python3 web_scraper.py --url "https://example.com" --selector "h1,p,table"
  python3 web_scraper.py --url "https://example.com" --mode text --output result.md

Options:
  --url         URL to fetch (required)
  --selector    CSS selector(s) to extract (comma-separated, default: body text)
  --mode        Output mode: text | html | markdown | links | tables (default: text)
  --output      Output file path (default: stdout)
  --timeout     Request timeout in seconds (default: 30)
  --user-agent  Custom User-Agent string
  --headers     Extra headers as JSON string (e.g. '{"Accept-Language": "en"}')
  --max-chars   Max characters to return (default: 50000)
  --follow      Follow redirects (default: true)
"""

import sys
import os
import json
import argparse
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _shared_runtime import ToolRuntimeError, format_error, request_with_retries

from bs4 import BeautifulSoup

DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def fetch(url: str, timeout: int, user_agent: str, extra_headers: dict, follow: bool):
    headers = {"User-Agent": user_agent, **extra_headers}
    result = request_with_retries(
        "GET", url,
        headers=headers,
        timeout=timeout,
        allow_redirects=follow,
        provider="web_scraper",
    )
    return result.response


def extract_text(soup: BeautifulSoup, selector: str | None) -> str:
    if selector:
        elements = []
        for sel in selector.split(","):
            elements.extend(soup.select(sel.strip()))
        return "\n\n".join(el.get_text(separator="\n", strip=True) for el in elements)
    for tag in soup(["script", "style", "noscript", "nav", "footer", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def extract_links(soup: BeautifulSoup, base_url: str) -> str:
    from urllib.parse import urljoin
    links = []
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        text = a.get_text(strip=True) or href
        links.append(f"- [{text}]({href})")
    return "\n".join(links) if links else "(no links found)"


def extract_tables(soup: BeautifulSoup) -> str:
    tables = soup.find_all("table")
    if not tables:
        return "(no tables found)"
    results = []
    for i, table in enumerate(tables, 1):
        rows = table.find_all("tr")
        table_lines = [f"### Table {i}"]
        for row in rows:
            cells = [c.get_text(strip=True) for c in row.find_all(["th", "td"])]
            table_lines.append(" | ".join(cells))
        results.append("\n".join(table_lines))
    return "\n\n".join(results)


def html_to_markdown(soup: BeautifulSoup, selector: str | None) -> str:
    if selector:
        elements = []
        for sel in selector.split(","):
            elements.extend(soup.select(sel.strip()))
        root = BeautifulSoup("<div></div>", "lxml")
        container = root.find("div")
        for el in elements:
            container.append(el)
        soup = root

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    lines = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "a", "strong", "em", "code", "pre", "blockquote", "table", "tr", "td", "th"]):
        name = el.name
        text = el.get_text(strip=True)
        if not text:
            continue
        if name in ("h1",):
            lines.append(f"# {text}")
        elif name in ("h2",):
            lines.append(f"## {text}")
        elif name in ("h3",):
            lines.append(f"### {text}")
        elif name in ("h4", "h5", "h6"):
            lines.append(f"#### {text}")
        elif name == "p":
            lines.append(text)
        elif name == "li":
            lines.append(f"- {text}")
        elif name in ("td", "th"):
            pass
        elif name == "blockquote":
            lines.append(f"> {text}")
        elif name == "pre":
            lines.append(f"```\n{text}\n```")

    deduped = []
    prev = None
    for line in lines:
        if line != prev:
            deduped.append(line)
        prev = line

    return "\n\n".join(deduped)


def clean_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    p = argparse.ArgumentParser(description="Web scraper for research.")
    p.add_argument("--url", required=True, help="URL to fetch")
    p.add_argument("--selector", default=None, help="CSS selector(s), comma-separated")
    p.add_argument("--mode", choices=["text", "html", "markdown", "links", "tables"], default="text")
    p.add_argument("--output", default=None, help="Output file path (default: stdout)")
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--user-agent", default=DEFAULT_UA)
    p.add_argument("--headers", default=None, help="Extra headers as JSON string")
    p.add_argument("--max-chars", type=int, default=50000)
    p.add_argument("--follow", type=lambda x: x.lower() != "false", default=True)
    args = p.parse_args()

    extra_headers = {}
    if args.headers:
        try:
            extra_headers = json.loads(args.headers)
        except json.JSONDecodeError as e:
            sys.exit(f"ERROR: --headers is not valid JSON: {e}")

    print(f"Fetching: {args.url}", file=sys.stderr)
    try:
        resp = fetch(args.url, args.timeout, args.user_agent, extra_headers, args.follow)
    except ToolRuntimeError as e:
        sys.exit(format_error(e))

    content_type = resp.headers.get("Content-Type", "")
    if "html" not in content_type and args.mode not in ("html",):
        result = resp.text[: args.max_chars]
    else:
        soup = BeautifulSoup(resp.content, "lxml")

        if args.mode == "text":
            result = clean_text(extract_text(soup, args.selector))
        elif args.mode == "html":
            result = resp.text
        elif args.mode == "markdown":
            result = clean_text(html_to_markdown(soup, args.selector))
        elif args.mode == "links":
            result = extract_links(soup, args.url)
        elif args.mode == "tables":
            result = extract_tables(soup)
        else:
            result = clean_text(extract_text(soup, args.selector))

    result = result[: args.max_chars]

    header = f"# Scraped: {args.url}\n\n"
    output = header + result

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved -> {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
