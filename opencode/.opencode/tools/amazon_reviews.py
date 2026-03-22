#!/usr/bin/env python3
"""
Amazon Reviews Scraper CLI - Extract product reviews from Amazon.

Uses requests + BeautifulSoup with rotating headers. Amazon actively blocks
scrapers, so results may be partial. For best results, provide a direct
product ASIN or URL.

Usage:
  python3 amazon_reviews.py --asin "B001234567"
  python3 amazon_reviews.py --url "https://www.amazon.com/dp/B001234567"
  python3 amazon_reviews.py --asin "B001234567" --pages 3 --stars 4
  python3 amazon_reviews.py --search "voice prosthesis" --limit 5

Options:
  --asin        Amazon product ASIN (e.g. B001234567)
  --url         Direct Amazon product URL
  --search      Search Amazon for a product (returns top result's reviews)
  --pages       Number of review pages to scrape (default: 1, max: 5)
  --stars       Filter by star rating: 1-5 or 'all' (default: all)
  --sort        Sort reviews: recent | helpful (default: helpful)
  --limit       Max reviews to return (default: 20)
  --format      Output format: md or json (default: md)
  --output      Output file path (default: stdout)

Note: Amazon may block requests. If scraping fails, try:
  - Using a VPN or proxy
  - Waiting and retrying
  - Using the Amazon Product Advertising API (requires AWS account)
"""

import sys
import json
import argparse
import time
import re
import random
import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

AMAZON_BASE = "https://www.amazon.com"


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
    })
    return session


def check_blocked(soup: BeautifulSoup) -> bool:
    """Detect if Amazon returned a CAPTCHA or block page."""
    title = soup.find("title")
    if title:
        t = title.get_text().lower()
        if "robot" in t or "captcha" in t or "sorry" in t or "automated" in t:
            return True
    if soup.find("form", {"action": "/errors/validateCaptcha"}):
        return True
    return False


def extract_asin_from_url(url: str) -> str | None:
    """Extract ASIN from an Amazon URL."""
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    match = re.search(r"/product/([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    match = re.search(r"asin=([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    return None


def get_product_info(session: requests.Session, asin: str) -> dict:
    """Fetch basic product info from the product page."""
    url = f"{AMAZON_BASE}/dp/{asin}"
    try:
        resp = session.get(url, timeout=30)
        soup = BeautifulSoup(resp.content, "lxml")
        if check_blocked(soup):
            return {"title": "N/A (blocked)", "rating": "N/A", "num_ratings": "N/A"}

        title_el = soup.find("span", {"id": "productTitle"})
        title = title_el.get_text(strip=True) if title_el else "N/A"

        rating_el = soup.find("span", {"class": "a-icon-alt"})
        rating = rating_el.get_text(strip=True) if rating_el else "N/A"

        num_el = soup.find("span", {"id": "acrCustomerReviewText"})
        num_ratings = num_el.get_text(strip=True) if num_el else "N/A"

        return {"title": title, "rating": rating, "num_ratings": num_ratings}
    except Exception as e:
        return {"title": "N/A", "rating": "N/A", "num_ratings": "N/A"}


def scrape_reviews_page(session: requests.Session, asin: str, page: int,
                        sort: str, stars: str) -> list[dict]:
    """Scrape a single page of Amazon reviews."""
    sort_map = {"helpful": "helpful", "recent": "recent"}
    sort_by = sort_map.get(sort, "helpful")

    params: dict = {
        "pageNumber": page,
        "sortBy": sort_by,
    }
    if stars != "all":
        params["filterByStar"] = f"{stars}_star"

    url = f"{AMAZON_BASE}/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page}"

    try:
        time.sleep(random.uniform(1.5, 3.0))  # Polite delay
        resp = session.get(url, params=params, timeout=30)
        soup = BeautifulSoup(resp.content, "lxml")

        if check_blocked(soup):
            print(f"  [amazon] blocked on page {page} — Amazon detected scraping", file=sys.stderr)
            return []

        reviews = []
        review_divs = soup.find_all("div", {"data-hook": "review"})

        for div in review_divs:
            # Rating
            rating_el = div.find("i", {"data-hook": "review-star-rating"})
            if not rating_el:
                rating_el = div.find("span", {"class": "a-icon-alt"})
            rating = rating_el.get_text(strip=True) if rating_el else "N/A"

            # Title
            title_el = div.find("span", {"data-hook": "review-title"})
            title = title_el.get_text(strip=True) if title_el else "N/A"

            # Body
            body_el = div.find("span", {"data-hook": "review-body"})
            body = body_el.get_text(strip=True) if body_el else "N/A"

            # Date
            date_el = div.find("span", {"data-hook": "review-date"})
            date = date_el.get_text(strip=True) if date_el else "N/A"

            # Helpful votes
            helpful_el = div.find("span", {"data-hook": "helpful-vote-statement"})
            helpful = helpful_el.get_text(strip=True) if helpful_el else ""

            # Verified purchase
            verified_el = div.find("span", {"data-hook": "avp-badge"})
            verified = bool(verified_el)

            reviews.append({
                "rating": rating,
                "title": title,
                "body": body[:1000],
                "date": date,
                "helpful": helpful,
                "verified_purchase": verified,
            })

        return reviews
    except Exception as e:
        print(f"  [amazon] page {page} error: {e}", file=sys.stderr)
        return []


def search_amazon(session: requests.Session, query: str) -> str | None:
    """Search Amazon and return the ASIN of the first result."""
    url = f"{AMAZON_BASE}/s"
    params = {"k": query, "ref": "nb_sb_noss"}

    try:
        time.sleep(random.uniform(1.0, 2.0))
        resp = session.get(url, params=params, timeout=30)
        soup = BeautifulSoup(resp.content, "lxml")

        if check_blocked(soup):
            print("  [amazon] blocked during search", file=sys.stderr)
            return None

        # Find first product result
        result = soup.find("div", {"data-asin": True, "data-component-type": "s-search-result"})
        if result:
            asin = result.get("data-asin")
            if asin:
                print(f"  Found ASIN: {asin}", file=sys.stderr)
                return asin

        return None
    except Exception as e:
        print(f"  [amazon search] error: {e}", file=sys.stderr)
        return None


def format_md(asin: str, product: dict, reviews: list[dict]) -> str:
    lines = [
        f"# Amazon Reviews — ASIN: {asin}",
        f"**Product**: {product.get('title', 'N/A')}  ",
        f"**Overall Rating**: {product.get('rating', 'N/A')}  ",
        f"**Total Ratings**: {product.get('num_ratings', 'N/A')}  ",
        f"**Reviews Collected**: {len(reviews)}",
        "",
    ]

    for i, r in enumerate(reviews, 1):
        lines.append(f"### Review {i}: {r.get('title', 'N/A')}")
        lines.append(f"- **Rating**: {r.get('rating', 'N/A')}")
        lines.append(f"- **Date**: {r.get('date', 'N/A')}")
        lines.append(f"- **Verified Purchase**: {'Yes' if r.get('verified_purchase') else 'No'}")
        if r.get("helpful"):
            lines.append(f"- **Helpful**: {r['helpful']}")
        lines.append(f"\n{r.get('body', 'N/A')}")
        lines.append("")

    lines.extend([
        "---",
        f"**Amazon Product URL**: {AMAZON_BASE}/dp/{asin}",
        f"**All Reviews**: {AMAZON_BASE}/product-reviews/{asin}",
        "",
        "> **Note**: Amazon actively blocks scrapers. If results are empty, try the URL directly.",
    ])

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Amazon reviews scraper.")
    p.add_argument("--asin", default=None, help="Amazon product ASIN")
    p.add_argument("--url", default=None, help="Amazon product URL")
    p.add_argument("--search", default=None, help="Search Amazon for a product")
    p.add_argument("--pages", type=int, default=1, help="Review pages to scrape (max 5)")
    p.add_argument("--stars", default="all", help="Filter by stars: 1-5 or all")
    p.add_argument("--sort", choices=["helpful", "recent"], default="helpful")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--output", default=None)
    args = p.parse_args()

    if not any([args.asin, args.url, args.search]):
        sys.exit("ERROR: Provide --asin, --url, or --search.")

    session = make_session()
    asin = args.asin

    if args.url and not asin:
        asin = extract_asin_from_url(args.url)
        if not asin:
            sys.exit(f"ERROR: Could not extract ASIN from URL: {args.url}")

    if args.search and not asin:
        print(f"Searching Amazon for: {args.search}", file=sys.stderr)
        asin = search_amazon(session, args.search)
        if not asin:
            sys.exit("ERROR: Could not find a product for that search query. Try --asin directly.")

    print(f"Amazon Reviews Scraper", file=sys.stderr)
    print(f"  ASIN  : {asin}", file=sys.stderr)
    print(f"  Pages : {min(args.pages, 5)}", file=sys.stderr)
    print(f"  Sort  : {args.sort}", file=sys.stderr)
    print(f"  Stars : {args.stars}", file=sys.stderr)

    print("  Fetching product info...", file=sys.stderr)
    product = get_product_info(session, asin)
    print(f"  Product: {product.get('title', 'N/A')[:60]}", file=sys.stderr)

    all_reviews: list[dict] = []
    for page in range(1, min(args.pages, 5) + 1):
        print(f"  Scraping page {page}...", file=sys.stderr)
        page_reviews = scrape_reviews_page(session, asin, page, args.sort, args.stars)
        all_reviews.extend(page_reviews)
        print(f"    -> {len(page_reviews)} reviews", file=sys.stderr)
        if len(all_reviews) >= args.limit:
            break

    all_reviews = all_reviews[: args.limit]
    print(f"  Total : {len(all_reviews)} reviews collected", file=sys.stderr)

    if not all_reviews:
        print(
            "\nNo reviews collected. Amazon may have blocked the request.\n"
            f"Try visiting directly: {AMAZON_BASE}/product-reviews/{asin}\n"
            "Or use the Reddit scraper for patient discussions instead.",
            file=sys.stderr,
        )

    if args.format == "json":
        output = json.dumps({"asin": asin, "product": product, "reviews": all_reviews}, indent=2)
    else:
        output = format_md(asin, product, all_reviews)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved -> {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
