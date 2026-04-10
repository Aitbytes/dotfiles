#!/usr/bin/env python3

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


def fetch(url: str, timeout: int, user_agent: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "ignore")


def normalize_query_variants(query: str) -> list[str]:
    base = query.strip()
    variants = [base]

    lowered = base.lower()
    if "youtube" not in lowered:
        variants.append(f"{base} youtube")
    if "beginner" in lowered and "mobility" not in lowered:
        variants.append(f"{base} mobility")
    if "desk" in lowered and "posture" not in lowered:
        variants.append(f"{base} posture")
    if "calisthenics" in lowered and "bodyweight" not in lowered:
        variants.append(f"{base} bodyweight")

    deduped: list[str] = []
    for item in variants:
        if item not in deduped:
            deduped.append(item)
    return deduped


def extract_video_ids(html: str) -> list[str]:
    ids = re.findall(r"watch\?v=([A-Za-z0-9_-]{11})", html)
    seen: set[str] = set()
    ordered: list[str] = []
    for vid in ids:
        if vid not in seen:
            seen.add(vid)
            ordered.append(vid)
    return ordered


def parse_watch_metadata(video_id: str, html: str) -> dict[str, Any]:
    title_match = re.search(r"<title>(.*?)</title>", html, re.S)
    channel_match = re.search(r'"ownerChannelName":"(.*?)"', html)
    length_match = re.search(r'"lengthSeconds":"(\d+)"', html)
    views_match = re.search(r'"viewCount":"(\d+)"', html)
    publish_match = re.search(r'"publishDate":"([^"]+)"', html)
    desc_match = re.search(r'"shortDescription":"(.*?)","isCrawlable"', html, re.S)

    title = title_match.group(1).replace(" - YouTube", "").strip() if title_match else None
    channel = channel_match.group(1) if channel_match else None
    description = None
    if desc_match:
        description = desc_match.group(1)
        description = description.encode("utf-8", "ignore").decode("unicode_escape", "ignore")
        description = description.replace("\\n", " ").strip()

    return {
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": title,
        "channel": channel,
        "has_caption_tracks": "captionTracks" in html,
        "duration_seconds": int(length_match.group(1)) if length_match else None,
        "view_count": int(views_match.group(1)) if views_match else None,
        "publish_date": publish_match.group(1) if publish_match else None,
        "description_preview": description[:280] if description else None,
    }


def rank_result(result: dict[str, Any], query: str, query_variant: str, index: int) -> float:
    score = 0.0
    title = (result.get("title") or "").lower()
    channel = (result.get("channel") or "").lower()
    q_words = [w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2]

    score += max(0, 20 - index)
    score += 8 if result.get("has_caption_tracks") else 0

    for word in q_words:
        if word in title:
            score += 3
        if word in channel:
            score += 1

    authority_channels = [
        "ted",
        "stanford",
        "mit",
        "google",
        "hybrid calisthenics",
        "fitnessfaqs",
        "calimove",
        "tom merrick",
    ]
    if any(name in channel for name in authority_channels):
        score += 6

    if "shorts" in title:
        score -= 5
    if query_variant.lower() != query.lower():
        score -= 0.2

    return score


def search_youtube(query: str, limit: int, attempts: int, timeout: int, user_agent: str) -> dict[str, Any]:
    variants = normalize_query_variants(query)[:attempts]
    candidates: dict[str, dict[str, Any]] = {}
    debug_queries: list[dict[str, Any]] = []

    for variant in variants:
        search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(variant)
        try:
            html = fetch(search_url, timeout=timeout, user_agent=user_agent)
        except Exception as exc:
            debug_queries.append({"query": variant, "error": str(exc)})
            continue

        ids = extract_video_ids(html)
        debug_queries.append({"query": variant, "video_ids_found": ids[:10], "html_length": len(html)})

        for index, video_id in enumerate(ids):
            entry = candidates.setdefault(video_id, {"video_id": video_id, "query_hits": [], "best_index": index})
            entry["query_hits"].append({"query": variant, "index": index})
            entry["best_index"] = min(entry["best_index"], index)

    ordered_ids = sorted(candidates.keys(), key=lambda vid: candidates[vid]["best_index"])
    results: list[dict[str, Any]] = []

    for video_id in ordered_ids:
        if len(results) >= limit:
            break
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            html = fetch(watch_url, timeout=timeout, user_agent=user_agent)
        except Exception as exc:
            results.append(
                {
                    "video_id": video_id,
                    "url": watch_url,
                    "error": str(exc),
                    "query_hits": candidates[video_id]["query_hits"],
                }
            )
            continue

        metadata = parse_watch_metadata(video_id, html)
        metadata["query_hits"] = candidates[video_id]["query_hits"]
        metadata["rank_score"] = rank_result(metadata, query, metadata["query_hits"][0]["query"], candidates[video_id]["best_index"])
        results.append(metadata)
        time.sleep(0.1)

    results.sort(key=lambda item: item.get("rank_score", 0), reverse=True)
    return {
        "query": query,
        "query_variants": variants,
        "results": results[:limit],
        "debug": debug_queries,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [f"# YouTube Search Results - {payload['query']}", ""]
    lines.append("## Results")
    lines.append("")
    for idx, item in enumerate(payload["results"], 1):
        lines.append(f"### {idx}. {item.get('title') or item['video_id']}")
        lines.append(f"- URL: {item['url']}")
        if item.get("channel"):
            lines.append(f"- Channel: {item['channel']}")
        lines.append(f"- Video ID: {item['video_id']}")
        lines.append(f"- Has caption tracks: {item.get('has_caption_tracks')}")
        if item.get("publish_date"):
            lines.append(f"- Publish date: {item['publish_date']}")
        if item.get("duration_seconds") is not None:
            lines.append(f"- Duration seconds: {item['duration_seconds']}")
        if item.get("rank_score") is not None:
            lines.append(f"- Rank score: {item['rank_score']:.1f}")
        if item.get("description_preview"):
            lines.append(f"- Description preview: {item['description_preview']}")
        query_hits = item.get("query_hits") or []
        if query_hits:
            hits = ", ".join(f"{hit['query']} (#{hit['index'] + 1})" for hit in query_hits[:4])
            lines.append(f"- Query hits: {hits}")
        if item.get("error"):
            lines.append(f"- Error: {item['error']}")
        lines.append("")

    lines.append("## Debug")
    lines.append("")
    for dbg in payload["debug"]:
        if dbg.get("error"):
            lines.append(f"- `{dbg['query']}` -> error: {dbg['error']}")
        else:
            ids = ", ".join(dbg.get("video_ids_found", []))
            lines.append(f"- `{dbg['query']}` -> IDs: {ids}")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Search YouTube videos from raw HTML and return metadata.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--attempts", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--format", choices=["json", "md"], default="md")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    args = parser.parse_args()

    try:
        payload = search_youtube(
            query=args.query,
            limit=max(1, args.limit),
            attempts=max(1, args.attempts),
            timeout=max(1, args.timeout),
            user_agent=args.user_agent,
        )
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        return 1

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
