#!/usr/bin/env python3
"""
Reddit Scraper CLI - Collect Reddit posts and comments for research.

Usage:
  python3 reddit_scraper.py --niche "chronic pain" --subreddits "chronicpain+fibromyalgia" --output pain_data.md
  python3 reddit_scraper.py --niche "freelancing" --terms "burnout,clients,payment" --limit 30 --min-score 10

Options:
  --niche         Topic/keyword to search for (required)
  --subreddits    Plus-separated list of subreddits (default: auto-derived from niche)
  --terms         Comma-separated list of additional search terms (optional)
  --limit         Max posts per search term (default: 20)
  --max-posts     Hard cap on total unique posts collected across all terms (default: 50)
  --min-score     Minimum post score to include (default: 10)
  --comments      Number of top comments to fetch per post (default: 10)
  --min-comment-score  Minimum comment score to include (default: 1)
  --output        Output file path (default: <niche>_reddit_data.md)
  --format        Output format: md or json (default: md)
  --sort          Reddit sort: relevance, new, top, comments (default: top)

Notes:
  - Posts are written to the output file progressively as they are collected.
  - Use --max-posts to avoid runaway collection when many --terms are provided.
  - Environment: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
"""

import os
import sys
import time
import json
import argparse
import praw
import praw.exceptions
import requests.exceptions
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Rate-limiting helpers
# ---------------------------------------------------------------------------

REQUEST_DELAY = 1.0
MAX_RETRIES = 5
TIMEOUT_RETRY_DELAY = 5
MAX_BACKOFF = 60


def _sleep(seconds: float, reason: str = ""):
    if reason:
        print(f"  [rate-limit] sleeping {seconds:.1f}s — {reason}")
    time.sleep(seconds)


def with_backoff(fn, *args, **kwargs):
    delay = 1.0
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = fn(*args, **kwargs)
            _sleep(REQUEST_DELAY)
            return result
        except praw.exceptions.RedditAPIException as e:
            print(f"  [reddit-api] attempt {attempt}/{MAX_RETRIES}: {e}")
            if attempt == MAX_RETRIES:
                raise
            _sleep(min(delay, MAX_BACKOFF), "Reddit API error – backoff")
            delay *= 2
        except requests.exceptions.Timeout:
            print(f"  [timeout]    attempt {attempt}/{MAX_RETRIES}")
            if attempt == MAX_RETRIES:
                raise
            _sleep(TIMEOUT_RETRY_DELAY, "timeout – retrying")
        except requests.exceptions.RequestException as e:
            print(f"  [network]    attempt {attempt}/{MAX_RETRIES}: {e}")
            if attempt == MAX_RETRIES:
                raise
            _sleep(min(delay, MAX_BACKOFF), "network error – backoff")
            delay *= 2
    return None


def init_reddit() -> praw.Reddit:
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "research-agent/1.0 (by /u/researcher)")

    if not client_id or not client_secret:
        sys.exit(
            "ERROR: REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET not set.\n"
            "Set these in your environment or .env file."
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )


def fetch_comments(post, max_comments: int, min_score: int) -> list[dict]:
    def _load():
        post.comments.replace_more(limit=0)
        return post.comments.list()

    try:
        all_comments = with_backoff(_load)
    except Exception as e:
        print(f"  [comments] failed to load comments: {e}")
        return []

    results = []
    for comment in (all_comments or []):
        if len(results) >= max_comments:
            break
        if not hasattr(comment, "body") or not comment.body:
            continue
        if comment.score < min_score:
            continue
        results.append({"body": comment.body[:500], "score": comment.score})

    return results


def search_posts(reddit: praw.Reddit, subreddits: str, term: str, limit: int, min_score: int, sort: str) -> list:
    def _search():
        return list(reddit.subreddit(subreddits).search(term, sort=sort, limit=limit))

    try:
        posts = with_backoff(_search) or []
    except Exception as e:
        print(f"  [search] error for '{term}': {e}")
        return []

    return [p for p in posts if p.score >= min_score]


def post_to_markdown(post: dict, index: int) -> str:
    lines = [
        f"### Post {index}: {post['title']}",
        f"- Score: {post['score']}, Comments: {post['num_comments']}",
        f"- Subreddit: r/{post['subreddit']}",
        f"- URL: {post['url']}",
    ]
    if post["body"]:
        lines.append(f"- Body: {post['body']}\n")
    if post["comments"]:
        lines.append("#### Top Comments:\n")
        for j, c in enumerate(post["comments"], 1):
            lines.append(f"**Comment {j}** (score: {c['score']}): {c['body']}\n")
    lines.append("---\n")
    return "\n".join(lines)


def scrape(reddit: praw.Reddit, niche: str, subreddits: str, terms: list[str], limit: int,
           max_posts: int, min_score: int, n_comments: int, min_comment_score: int,
           sort: str, output_path: str, fmt: str) -> list[dict]:
    seen_ids: set[str] = set()
    all_posts: list[dict] = []

    if fmt == "md":
        out_f = open(output_path, "w", encoding="utf-8")
        out_f.write(f"# Reddit Data - {niche}\n\n")
        out_f.write("## Collected Posts and Comments\n\n")
        out_f.flush()
    else:
        out_f = None

    try:
        for term in terms:
            if len(all_posts) >= max_posts:
                print(f"\n[max-posts] reached {max_posts} posts — stopping early.")
                break

            print(f"\nSearching: '{term}' in r/{subreddits}  (sort={sort}, limit={limit})")
            posts = search_posts(reddit, subreddits, term, limit, min_score, sort)
            print(f"  -> {len(posts)} posts pass min-score={min_score}")

            for post in posts:
                if len(all_posts) >= max_posts:
                    break
                if post.id in seen_ids:
                    continue
                seen_ids.add(post.id)

                print(f"  [{len(all_posts)+1}/{max_posts}] Fetching comments: {post.title[:60]}...")
                comments = fetch_comments(post, n_comments, min_comment_score)

                record = {
                    "id": post.id,
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "subreddit": str(post.subreddit),
                    "url": f"https://reddit.com{post.permalink}",
                    "body": (post.selftext or "")[:1500],
                    "comments": comments,
                }
                all_posts.append(record)

                if fmt == "md" and out_f:
                    out_f.write(post_to_markdown(record, len(all_posts)))
                    out_f.flush()

    finally:
        if fmt == "md" and out_f:
            out_f.close()

    return all_posts


def build_default_subreddits(niche: str) -> str:
    slug = niche.lower().replace(" ", "")
    return f"{slug}+AskReddit"


def main():
    p = argparse.ArgumentParser(description="Reddit scraper for research.")
    p.add_argument("--niche", required=True, help="Primary topic / niche to research")
    p.add_argument("--subreddits", default=None, help="Plus-separated subreddit list")
    p.add_argument("--terms", default=None, help="Comma-separated extra search terms")
    p.add_argument("--limit", type=int, default=20, help="Max posts per search term")
    p.add_argument("--max-posts", type=int, default=50, help="Hard cap on total unique posts")
    p.add_argument("--min-score", type=int, default=10, help="Minimum post score")
    p.add_argument("--comments", type=int, default=10, help="Top comments per post")
    p.add_argument("--min-comment-score", type=int, default=1, help="Minimum comment score")
    p.add_argument("--output", default=None, help="Output file path")
    p.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    p.add_argument("--sort", choices=["relevance", "new", "top", "comments"], default="top", help="Reddit sort order")
    args = p.parse_args()

    niche = args.niche
    subreddits = args.subreddits or build_default_subreddits(niche)
    extra_terms = [t.strip() for t in args.terms.split(",")] if args.terms else []
    terms = [niche] + extra_terms
    output_path = args.output or f"{niche.lower().replace(' ', '_')}_reddit_data.{args.format}"

    print(f"Reddit Scraper")
    print(f"  Niche     : {niche}")
    print(f"  Subreddits: {subreddits}")
    print(f"  Terms     : {terms}")
    print(f"  Limit     : {args.limit} posts/term, min-score={args.min_score}")
    print(f"  Comments  : {args.comments} per post, min-score={args.min_comment_score}")
    print(f"  Sort      : {args.sort}")
    print(f"  Output    : {output_path} ({args.format})")
    print()

    reddit = init_reddit()

    posts = scrape(
        reddit=reddit, niche=niche, subreddits=subreddits, terms=terms,
        limit=args.limit, max_posts=args.max_posts, min_score=args.min_score,
        n_comments=args.comments, min_comment_score=args.min_comment_score,
        sort=args.sort, output_path=output_path, fmt=args.format,
    )

    print(f"\nTotal unique posts collected: {len(posts)}")

    if args.format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"Saved -> {output_path}")


if __name__ == "__main__":
    main()
