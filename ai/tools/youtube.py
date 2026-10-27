#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Any

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _shared_runtime import (
    ToolRuntimeError,
    create_error,
    format_error,
    request_text,
    load_proxy_config,
    request_with_retries,
)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query={q}"
YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={vid}"

TRANSCRIPT_SOURCE_YT_API = "youtube-transcript-api"
TRANSCRIPT_SOURCE_YTDLP = "yt-dlp"
TRANSCRIPT_SOURCE_NONE = "none"

CONFIDENCE_HIGH = "high"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_LOW = "low"


def normalize_query_variants(query: str) -> list[str]:
    base = query.strip()
    variants = [base]
    lowered = base.lower()
    if "youtube" not in lowered:
        variants.append(f"{base} youtube")
    deduped: list[str] = []
    for item in variants:
        if item not in deduped:
            deduped.append(item)
    return deduped


def parse_channel_page(html: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for m in re.finditer(r'"videoId":"([A-Za-z0-9_-]{11})"', html):
        vid = m.group(1)
        if vid in seen_ids:
            continue
        seen_ids.add(vid)
        chunk = html[m.end():m.end() + 1500]

        title_m = re.search(r'"title":\{"runs":\[\{"text":"([^"]+)"', chunk)
        desc_m = re.search(r'"descriptionSnippet":\{"runs":\[\{"text":"([^"]+)"', chunk)
        date_m = re.search(r'"publishedTimeText":\{"simpleText":"([^"]+)"\}', chunk)
        length_m = re.search(r'"lengthText":\{.*?"simpleText":"([^"]+)"', chunk)
        views_m = re.search(r'"viewCountText":\{"simpleText":"([^"]+)"\}', chunk)

        results.append({
            "video_id": vid,
            "title": title_m.group(1) if title_m else None,
            "description": desc_m.group(1)[:200] if desc_m else None,
            "published": date_m.group(1) if date_m else None,
            "duration": length_m.group(1) if length_m else None,
            "views": views_m.group(1) if views_m else None,
            "url": YOUTUBE_WATCH_URL.format(vid=vid),
        })
    return results


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

    has_captions = "captionTracks" in html
    caption_langs: list[str] = []
    if has_captions:
        caption_langs = re.findall(r'"languageCode":"([a-z]{2}(?:-[A-Z]{2})?)"', html)

    return {
        "video_id": video_id,
        "url": YOUTUBE_WATCH_URL.format(vid=video_id),
        "title": title,
        "channel": channel,
        "has_captions": has_captions,
        "caption_languages": sorted(set(caption_langs)),
        "duration_seconds": int(length_match.group(1)) if length_match else None,
        "view_count": int(views_match.group(1)) if views_match else None,
        "publish_date": publish_match.group(1) if publish_match else None,
        "description_preview": description[:280] if description else None,
    }


def rank_result(result: dict[str, Any], query: str, index: int) -> float:
    score = 0.0
    title = (result.get("title") or "").lower()
    channel = (result.get("channel") or "").lower()
    q_words = [w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2]

    score += max(0, 20 - index)
    score += 8 if result.get("has_captions") else 0

    for word in q_words:
        if word in title:
            score += 3
        if word in channel:
            score += 1

    if "shorts" in title:
        score -= 5

    return score


def search(query: str, limit: int = 10, attempts: int = 4, timeout: int = 20, proxy_mode: str = "auto") -> dict[str, Any]:
    variants = normalize_query_variants(query)[:attempts]
    candidates: dict[str, dict[str, Any]] = {}
    debug_queries: list[dict[str, Any]] = []

    for variant in variants:
        search_url = YOUTUBE_SEARCH_URL.format(q=urllib.parse.quote_plus(variant))
        try:
            html, _ = request_text(
                "GET", search_url, timeout=timeout,
                headers={"User-Agent": DEFAULT_USER_AGENT},
                proxy_mode=proxy_mode, provider="youtube",
                block_markers=["captcha", "confirm you're not a robot"],
            )
        except ToolRuntimeError as exc:
            debug_queries.append({"query": variant, "error": format_error(exc)})
            continue

        ids = extract_video_ids(html)
        debug_queries.append({"query": variant, "video_ids_found": ids[:10], "html_length": len(html)})

        for index, video_id in enumerate(ids):
            entry = candidates.setdefault(video_id, {"video_id": video_id, "best_index": index})
            entry["best_index"] = min(entry["best_index"], index)

    ordered_ids = sorted(candidates.keys(), key=lambda vid: candidates[vid]["best_index"])
    results: list[dict[str, Any]] = []

    for video_id in ordered_ids:
        if len(results) >= limit:
            break
        watch_url = YOUTUBE_WATCH_URL.format(vid=video_id)
        try:
            html, _ = request_text(
                "GET", watch_url, timeout=timeout,
                headers={"User-Agent": DEFAULT_USER_AGENT},
                proxy_mode=proxy_mode, provider="youtube",
                block_markers=["captcha", "confirm you're not a robot"],
            )
        except ToolRuntimeError as exc:
            results.append({
                "video_id": video_id,
                "url": watch_url,
                "error": format_error(exc),
            })
            continue

        metadata = parse_watch_metadata(video_id, html)
        metadata["rank_score"] = rank_result(metadata, query, candidates[video_id]["best_index"])
        results.append(metadata)
        time.sleep(0.1)

    results.sort(key=lambda item: item.get("rank_score", 0), reverse=True)
    return {
        "status": "ok",
        "query": query,
        "query_variants": variants,
        "results": results[:limit],
        "debug": debug_queries,
    }


def resolve(video_id_or_url: str, timeout: int = 20, proxy_mode: str = "auto") -> dict[str, Any]:
    video_id = video_id_or_url.strip()
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", video_id)
    if match:
        video_id = match.group(1)
    if not re.match(r"^[A-Za-z0-9_-]{11}$", video_id):
        return {
            "status": "error",
            "error": {"kind": "invalid_input", "message": f"Invalid video ID or URL: {video_id_or_url}"},
        }

    watch_url = YOUTUBE_WATCH_URL.format(vid=video_id)
    try:
        html, _ = request_text(
            "GET", watch_url, timeout=timeout,
            headers={"User-Agent": DEFAULT_USER_AGENT},
            proxy_mode=proxy_mode, provider="youtube",
            block_markers=["captcha", "confirm you're not a robot"],
        )
    except ToolRuntimeError as exc:
        return {
            "status": "error",
            "error": {"kind": exc.kind, "message": exc.message},
        }

    metadata = parse_watch_metadata(video_id, html)
    return {"status": "ok", **metadata}


def _oembed_meta(video_id: str, timeout: int = 10, proxy_mode: str = "auto") -> dict[str, Any] | None:
    """Resolve title (+author) for one video via the oEmbed API (no dates there)."""
    oembed_url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode(
        {"url": YOUTUBE_WATCH_URL.format(vid=video_id), "format": "json"}
    )
    try:
        text, _ = request_text(
            "GET", oembed_url, timeout=timeout,
            headers={"User-Agent": DEFAULT_USER_AGENT},
            proxy_mode=proxy_mode, provider="youtube",
        )
        data = json.loads(text)
        return data if isinstance(data, dict) else None
    except (ToolRuntimeError, json.JSONDecodeError, ValueError):
        return None


def _ytdlp_flat_entries(channel_url: str, playlist_end: int = 30, timeout: int = 120) -> dict[str, dict[str, Any]] | None:
    """One yt-dlp --flat-playlist -J pass over a channel/playlist.

    Native JSON with titles + timestamps — never parse delimited text (titles
    containing '|' have already cost 126 lost lines in a past session).
    """
    # Channel root ("@handle") = home tab: no dates, few entries. The /videos
    # tab is what recent-video listings need.
    if re.search(r"youtube\.com/@[^/]+/?$", channel_url):
        channel_url = channel_url.rstrip("/") + "/videos"
    # Proxy can be slow/flaky; retry yt-dlp without proxy if the proxied run fails.
    for attempt_pm in ("auto", "direct"):
        entries = _ytdlp_flat_entries_attempt(channel_url, playlist_end, timeout, attempt_pm)
        if entries:
            return entries
    return None


def _ytdlp_flat_entries_attempt(channel_url: str, playlist_end: int, timeout: int, attempt_pm: str) -> dict[str, dict[str, Any]] | None:
    env = _build_proxy_env(attempt_pm)
    # NixOS quirk: yt-dlp needs an explicit CA bundle.
    env.setdefault("SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt")
    try:
        result = subprocess.run(
            ["uv", "run", "--with", "yt-dlp", "--with", "certifi",
             "yt-dlp", "--flat-playlist", "-J",
             "--playlist-end", str(max(1, playlist_end)),
             "--extractor-args", "youtubetab:approximate_date",
             "--socket-timeout", "20",
             channel_url],
            capture_output=True, text=True, timeout=timeout, env=env,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    entries: dict[str, dict[str, Any]] = {}
    for entry in data.get("entries") or []:
        vid = entry.get("id")
        if not vid:
            continue
        ts = entry.get("timestamp") or entry.get("release_timestamp")
        published = None
        if ts:
            try:
                published = datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat()
            except (ValueError, OverflowError, OSError):
                published = None
        entries[vid] = {"title": entry.get("title"), "published": published}
    return entries or None


def _enrich_channel_meta(payload: dict[str, Any], timeout: int, proxy_mode: str) -> None:
    """Add titles + publish dates in batch (avoids ~20 individual resolves).

    Strategy: one yt-dlp --flat-playlist -J pass (titles + dates), then one
    oEmbed call per video whose title is still missing (oEmbed has no dates).
    """
    results = payload.get("results", [])
    flat = _ytdlp_flat_entries(
        payload.get("channel_url", ""), playlist_end=max(len(results), 1) + 10,
        timeout=max(60, timeout),
    )
    if not results and flat:
        # Channel HTML was consent-walled / empty: rebuild the listing from
        # yt-dlp flat-playlist (the SKILL.md "listing fiable" recipe).
        payload["results"] = [
            {
                "video_id": vid,
                "title": entry.get("title"),
                "published": entry.get("published"),
                "meta_source": "yt-dlp",
                "url": YOUTUBE_WATCH_URL.format(vid=vid),
            }
            for vid, entry in list(flat.items())
        ]
        results = payload["results"]
    if not results:
        return
    touched_ytdlp = 0
    if flat:
        for item in results:
            entry = flat.get(item.get("video_id"))
            if not entry:
                continue
            changed = False
            if not item.get("title") and entry.get("title"):
                item["title"] = entry["title"]
                changed = True
            if not item.get("published") and entry.get("published"):
                item["published"] = entry["published"]
                changed = True
            if changed:
                item["meta_source"] = "yt-dlp"
                touched_ytdlp += 1
    touched_oembed = 0
    for item in results:
        if item.get("title"):
            continue
        meta = _oembed_meta(item.get("video_id", ""), timeout=timeout, proxy_mode=proxy_mode)
        if meta and meta.get("title"):
            item["title"] = meta["title"]
            if meta.get("author_name"):
                item["channel"] = meta["author_name"]
            item["meta_source"] = "oembed"
            touched_oembed += 1
    payload["meta_enriched"] = {
        "yt_dlp_entries": touched_ytdlp,
        "oembed_titles": touched_oembed,
        "still_missing_titles": sum(1 for i in results if not i.get("title")),
    }


def _write_output_file(path: str, content: str, fmt: str) -> str:
    """Write output to a file, auto-correcting .json -> .md when the content is
    markdown (prevents JSONDecodeError + manual renames when re-read later)."""
    if fmt == "md" and path.lower().endswith(".json"):
        corrected = path[:-5] + ".md"
        print(f"[youtube-tool] format is markdown: extension auto-corrected {path} -> {corrected}", file=sys.stderr)
        path = corrected
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def channel_videos(channel_url: str, limit: int = 20, timeout: int = 20, proxy_mode: str = "auto", meta: bool = False) -> dict[str, Any]:
    # Normalize shorthand inputs ("@handle", "@handle/videos", bare handle) —
    # requests raises MissingSchema on scheme-less URLs (was surfaced as a mute
    # "Unexpected request failure").
    if not channel_url.lower().startswith(("http://", "https://")):
        channel_url = "https://www.youtube.com/" + channel_url.lstrip("/")
    def _fetch(html: str) -> list[dict[str, Any]]:
        return parse_channel_page(html)

    try:
        html, _ = request_text(
            "GET", channel_url, timeout=timeout,
            headers={"User-Agent": DEFAULT_USER_AGENT},
            proxy_mode=proxy_mode, provider="youtube",
            block_markers=["captcha", "confirm you're not a robot"],
        )
    except ToolRuntimeError as exc:
        return {
            "status": "error",
            "error": {"kind": exc.kind, "message": exc.message, "details": exc.details},
        }

    videos = _fetch(html)

    if not videos and proxy_mode == "auto":
        html_direct, _ = request_text(
            "GET", channel_url, timeout=timeout,
            headers={"User-Agent": DEFAULT_USER_AGENT},
            proxy_mode="direct", provider="youtube",
            block_markers=["captcha", "confirm you're not a robot"],
        )
        videos = _fetch(html_direct)

    payload = {
        "status": "ok",
        "channel_url": channel_url,
        "results": videos[:limit],
    }
    if meta:
        _enrich_channel_meta(payload, timeout=timeout, proxy_mode=proxy_mode)
    return payload


def _build_proxy_env(proxy_mode: str = "auto") -> dict[str, str]:
    env = dict(os.environ)
    if proxy_mode in {"direct", "disabled"}:
        for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            env.pop(k, None)
        return env
    cfg = load_proxy_config()
    if cfg.enabled:
        if cfg.http:
            env["HTTP_PROXY"] = cfg.http
            env["http_proxy"] = cfg.http
        if cfg.https:
            env["HTTPS_PROXY"] = cfg.https
            env["https_proxy"] = cfg.https
    return env


def _stderr_hint(stderr: str) -> str:
    """Extract an actionable hint from a failing provider's stderr."""
    markers = ("IpBlocked", "RequestBlocked", "TooManyRequests", "429", "PO Token", "PO token",
               "TranscriptsDisabled", "NoTranscriptFound", "VideoUnavailable")
    for marker in markers:
        if marker in stderr:
            return marker
    lines = [l for l in stderr.strip().splitlines() if l.strip()]
    return lines[-1][:160] if lines else "unknown error"


def _try_transcript_api(video_id: str, languages: list[str] | None = None, proxy_mode: str = "auto") -> dict[str, Any]:
    # youtube-transcript-api is not installed in system Python; use uv run subprocess only.
    # The new API requires instance: YouTubeTranscriptApi().fetch(), not static .fetch().
    # Proxy can cause IpBlocked from YouTube; retry without proxy on failure.
    last_hint = "youtube-transcript-api failed"
    for attempt_pm in [proxy_mode, "direct"]:
        sub_env = _build_proxy_env(attempt_pm)
        try:
            code = (
                "from youtube_transcript_api import YouTubeTranscriptApi; "
                f"t = YouTubeTranscriptApi().fetch('{video_id}'"
            )
            if languages:
                code += f", languages={languages}"
            code += "); "
            code += "import json; print(json.dumps([{'text': s.text, 'start': s.start, 'duration': s.duration} for s in t]))"

            result = subprocess.run(
                ["uv", "run", "--with", "youtube-transcript-api", "python3", "-c", code],
                capture_output=True, text=True, timeout=60,
                env=sub_env,
            )
            if result.returncode == 0 and result.stdout.strip():
                try:
                    entries = json.loads(result.stdout.strip())
                    if entries:
                        snippets = [
                            {"text": e["text"], "start": e.get("start", 0), "duration": e.get("duration", 0)}
                            for e in entries
                        ]
                        full_text = " ".join(s["text"] for s in snippets)
                        return {
                            "source": TRANSCRIPT_SOURCE_YT_API,
                            "confidence": CONFIDENCE_HIGH,
                            "language": languages[0] if languages else "unknown",
                            "snippet_count": len(snippets),
                            "text": full_text,
                            "snippets": snippets,
                        }
                except json.JSONDecodeError:
                    pass
            else:
                last_hint = _stderr_hint(result.stderr or "")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    return {"source": TRANSCRIPT_SOURCE_NONE, "confidence": CONFIDENCE_LOW, "error": f"youtube-transcript-api failed: {last_hint}"}


def _try_ytdlp_transcript(video_id: str, proxy_mode: str = "auto") -> dict[str, Any]:
    # Retry without proxy if first attempt fails (prevents IP block)
    import glob as glob_mod
    import os
    for attempt_pm in [proxy_mode, "direct"]:
        sub_env = _build_proxy_env(attempt_pm)
        try:
            result = subprocess.run(
                ["uv", "run", "--with", "yt-dlp", "--with", "certifi",
                 "yt-dlp", "--write-auto-sub", "--sub-lang", "en,en-.*,.*",
                 "--skip-download", "--output", f"/tmp/yt_{video_id}",
                 f"https://www.youtube.com/watch?v={video_id}"],
                capture_output=True, text=True, timeout=120,
                env=sub_env
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

        subtitle_files = glob_mod.glob(f"/tmp/yt_{video_id}.*.vtt") + glob_mod.glob(f"/tmp/yt_{video_id}.*.srt")
        if not subtitle_files:
            continue

        for sf in subtitle_files:
            try:
                with open(sf, encoding="utf-8") as f:
                    content = f.read()
                snippets = []
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("WEBVTT") or line.startswith("NOTE") or "-->" in line or line.isdigit():
                        continue
                    snippets.append(line)
                if snippets:
                    full_text = " ".join(snippets)
                    for cleanup_sf in glob_mod.glob(f"/tmp/yt_{video_id}.*"):
                        try:
                            os.unlink(cleanup_sf)
                        except OSError:
                            pass
                    return {
                        "source": TRANSCRIPT_SOURCE_YTDLP,
                        "confidence": CONFIDENCE_MEDIUM,
                        "language": "en",
                        "snippet_count": len(snippets),
                        "text": full_text,
                        "snippets": [{"text": s, "start": 0, "duration": 0} for s in snippets],
                    }
            except (OSError, UnicodeDecodeError):
                continue

    for cleanup_sf in glob_mod.glob(f"/tmp/yt_{video_id}.*"):
        try:
            os.unlink(cleanup_sf)
        except OSError:
            pass
    return {"source": TRANSCRIPT_SOURCE_NONE, "confidence": CONFIDENCE_LOW, "error": "Could not parse subtitle files from yt-dlp"}


def transcript(
    video_id_or_url: str,
    languages: list[str] | None = None,
    include_fallback: bool = True,
    timeout: int = 20,
    proxy_mode: str = "auto",
) -> dict[str, Any]:
    video_id = video_id_or_url.strip()
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", video_id)
    if match:
        video_id = match.group(1)
    if not re.match(r"^[A-Za-z0-9_-]{11}$", video_id):
        return {
            "status": "error",
            "error": {"kind": "invalid_input", "message": f"Invalid video ID or URL: {video_id_or_url}"},
        }

    if languages is None:
        languages = ["en"]

    attempts: list[dict[str, Any]] = []

    primary = _try_transcript_api(video_id, languages, proxy_mode=proxy_mode)
    attempts.append({"source": TRANSCRIPT_SOURCE_YT_API, "succeeded": primary["source"] != TRANSCRIPT_SOURCE_NONE})
    if primary["source"] != TRANSCRIPT_SOURCE_NONE:
        primary["video_id"] = video_id
        primary["url"] = YOUTUBE_WATCH_URL.format(vid=video_id)
        primary["attempts"] = attempts
        primary["status"] = "ok"
        return primary

    if not include_fallback:
        return {
            "status": "empty",
            "video_id": video_id,
            "url": YOUTUBE_WATCH_URL.format(vid=video_id),
            "source": TRANSCRIPT_SOURCE_NONE,
            "confidence": CONFIDENCE_LOW,
            "error": "Primary transcript source (youtube-transcript-api) returned no data",
            "attempts": attempts,
        }

    fallback = _try_ytdlp_transcript(video_id,proxy_mode=proxy_mode)
    attempts.append({"source": TRANSCRIPT_SOURCE_YTDLP, "succeeded": fallback["source"] != TRANSCRIPT_SOURCE_NONE})
    if fallback["source"] != TRANSCRIPT_SOURCE_NONE:
        fallback["video_id"] = video_id
        fallback["url"] = YOUTUBE_WATCH_URL.format(vid=video_id)
        fallback["attempts"] = attempts
        fallback["status"] = "ok"
        return fallback

    final_error = "All transcript sources failed"
    primary_err = str(primary.get("error", ""))
    blocked_markers = ("IpBlocked", "RequestBlocked", "TooManyRequests", "429", "PO Token", "PO token")
    if any(m in primary_err for m in blocked_markers):
        final_error = (
            f"All transcript sources failed ({primary_err}). YouTube is blocking this exit IP. "
            "Fallback: use the UI+CDP recipe in the youtube-research SKILL.md — open the video in a "
            "CDP-driven browser, click \"…Afficher la transcription\", intercept the get_panel OR "
            "get_transcript response, parse transcriptSegmentViewModel. If still blocked, switch exit "
            "IP (see steel-browser skill). FAILED_PRECONDITION on a video = move to the next one."
        )
    return {
        "status": "error",
        "video_id": video_id,
        "url": YOUTUBE_WATCH_URL.format(vid=video_id),
        "source": TRANSCRIPT_SOURCE_NONE,
        "confidence": CONFIDENCE_LOW,
        "error": final_error,
        "provider_errors": {
            "youtube-transcript-api": primary.get("error"),
            "yt-dlp": fallback.get("error"),
        },
        "attempts": attempts,
    }


def render_search_md(payload: dict[str, Any]) -> str:
    lines = [f"# YouTube Search Results - {payload['query']}", ""]
    lines.append("## Results")
    lines.append("")
    for idx, item in enumerate(payload.get("results", []), 1):
        lines.append(f"### {idx}. {item.get('title') or item.get('video_id', 'Unknown')}")
        lines.append(f"- URL: {item.get('url', '')}")
        if item.get("channel"):
            lines.append(f"- Channel: {item['channel']}")
        lines.append(f"- Video ID: {item.get('video_id', '')}")
        lines.append(f"- Has caption tracks: {item.get('has_captions', False)}")
        if item.get("caption_languages"):
            lines.append(f"- Caption languages: {', '.join(item['caption_languages'])}")
        if item.get("publish_date"):
            lines.append(f"- Publish date: {item['publish_date']}")
        if item.get("duration_seconds") is not None:
            lines.append(f"- Duration seconds: {item['duration_seconds']}")
        if item.get("rank_score") is not None:
            lines.append(f"- Rank score: {item['rank_score']:.1f}")
        if item.get("description_preview"):
            lines.append(f"- Description preview: {item['description_preview']}")
        if item.get("error"):
            lines.append(f"- Error: {item['error']}")
        lines.append("")

    lines.append("## Debug")
    lines.append("")
    for dbg in payload.get("debug", []):
        if dbg.get("error"):
            lines.append(f"- `{dbg['query']}` -> error: {dbg['error']}")
        else:
            ids = ", ".join(dbg.get("video_ids_found", []))
            lines.append(f"- `{dbg['query']}` -> IDs: {ids}")
    return "\n".join(lines).strip() + "\n"


def render_resolve_md(payload: dict[str, Any]) -> str:
    if payload.get("status") == "error":
        return f"# Error\n\n{payload['error']['message']}\n"

    lines = [f"# YouTube Video: {payload.get('title', payload.get('video_id', 'Unknown'))}", ""]
    lines.append(f"- **URL**: {payload.get('url', '')}")
    lines.append(f"- **Video ID**: {payload.get('video_id', '')}")
    if payload.get("channel"):
        lines.append(f"- **Channel**: {payload['channel']}")
    lines.append(f"- **Has captions**: {payload.get('has_captions', False)}")
    if payload.get("caption_languages"):
        lines.append(f"- **Caption languages**: {', '.join(payload['caption_languages'])}")
    if payload.get("duration_seconds") is not None:
        lines.append(f"- **Duration**: {payload['duration_seconds']}s")
    if payload.get("view_count") is not None:
        lines.append(f"- **Views**: {payload['view_count']:,}")
    if payload.get("publish_date"):
        lines.append(f"- **Published**: {payload['publish_date']}")
    if payload.get("description_preview"):
        lines.append(f"- **Description**: {payload['description_preview']}")
    return "\n".join(lines).strip() + "\n"


def render_transcript_md(payload: dict[str, Any]) -> str:
    if payload.get("status") == "error":
        return f"# Transcript Error\n\nFailed to get transcript for {payload.get('video_id', 'unknown')}\n\nError: {payload.get('error', 'Unknown error')}\n"

    vid = payload.get("video_id", "unknown")
    lines = [
        f"# Transcript: {vid}",
        "- **Format**: markdown",
        f"- **Source**: {payload.get('source', 'unknown')}",
        f"- **Confidence**: {payload.get('confidence', 'unknown')}",
        f"- **Language**: {payload.get('language', 'unknown')}",
        f"- **Snippet count**: {payload.get('snippet_count', 0)}",
        "",
    ]

    if payload.get("attempts"):
        lines.append("## Transcript Attempts")
        for attempt in payload["attempts"]:
            status = "succeeded" if attempt["succeeded"] else "failed"
            lines.append(f"- {attempt['source']}: {status}")
        lines.append("")

    lines.append("## Full Text")
    lines.append("")
    lines.append(payload.get("text", ""))

    if payload.get("snippets") and len(payload["snippets"]) <= 200:
        lines.append("")
        lines.append("## Timestamped Segments")
        lines.append("")
        for s in payload["snippets"]:
            start = s.get("start", 0)
            mins, secs = divmod(int(start), 60)
            lines.append(f"[{mins:02d}:{secs:02d}] {s['text']}")

    return "\n".join(lines).strip() + "\n"



def render_channel_md(payload: dict[str, Any]) -> str:
    if payload.get("status") == "error":
        return f"# Channel Error\n\n{payload['error']['message']}\n"

    lines = [f"# Channel Videos", ""]
    lines.append(f"- **Channel URL**: {payload.get('channel_url', '')}")
    lines.append(f"- **Video count**: {len(payload.get('results', []))}")
    if payload.get("meta_enriched"):
        me = payload["meta_enriched"]
        lines.append(
            f"- **Meta enrichment**: yt-dlp entries: {me.get('yt_dlp_entries', 0)}, "
            f"oEmbed titles: {me.get('oembed_titles', 0)}, "
            f"titles still missing: {me.get('still_missing_titles', 0)}"
        )
    lines.append("")
    lines.append("## Videos")
    lines.append("")
    for idx, item in enumerate(payload.get("results", []), 1):
        lines.append(f"### {idx}. {item.get('title') or item.get('video_id', 'Unknown')}")
        lines.append(f"- URL: {item.get('url', '')}")
        if item.get("meta_source"):
            lines.append(f"- Meta source: {item['meta_source']}")
        if item.get("published"):
            lines.append(f"- Published: {item['published']}")
        if item.get("views"):
            lines.append(f"- Views: {item['views']}")
        if item.get("duration"):
            lines.append(f"- Duration: {item['duration']}")
        if item.get("description"):
            lines.append(f"- Description: {item['description'][:120]}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="YouTube tool: search, resolve, and extract transcripts.")
    sub = parser.add_subparsers(dest="action", required=True)

    search_p = sub.add_parser("search", help="Search YouTube for videos")
    search_p.add_argument("--query", required=True, help="Search query")
    search_p.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    search_p.add_argument("--attempts", type=int, default=4, help="Query variant attempts (default: 4)")
    search_p.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds")
    search_p.add_argument("--format", choices=["md", "json"], default="md")
    search_p.add_argument("--proxy-mode", choices=["auto", "direct", "required", "disabled"], default="auto")

    resolve_p = sub.add_parser("resolve", help="Resolve a video URL/ID to metadata")
    resolve_p.add_argument("video_id_or_url", help="YouTube video ID or URL")
    resolve_p.add_argument("--timeout", type=int, default=20)
    resolve_p.add_argument("--format", choices=["md", "json"], default="md")
    resolve_p.add_argument("--proxy-mode", choices=["auto", "direct", "required", "disabled"], default="auto")

    transcript_p = sub.add_parser("transcript", help="Extract transcript from a video")
    transcript_p.add_argument("video_id_or_url", help="YouTube video ID or URL")
    transcript_p.add_argument("--languages", nargs="+", default=["en"], help="Preferred languages (default: en)")
    transcript_p.add_argument("--no-fallback", action="store_true", help="Skip yt-dlp fallback")
    transcript_p.add_argument("--out", default=None,
                              help="Write output to file; auto-corrects .json -> .md when format is markdown")
    transcript_p.add_argument("--timeout", type=int, default=20)
    transcript_p.add_argument("--format", choices=["md", "json"], default="md")
    transcript_p.add_argument("--proxy-mode", choices=["auto", "direct", "required", "disabled"], default="auto")

    channel_p = sub.add_parser("channel", aliases=["list"], help="List videos from a channel")
    channel_p.add_argument("channel_url", help="YouTube channel URL (e.g. https://www.youtube.com/@MKBHD/videos)")
    channel_p.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    channel_p.add_argument("--meta", action="store_true",
                           help="Add titles + publish dates in batch (yt-dlp flat-playlist, oEmbed fallback)")
    channel_p.add_argument("--timeout", type=int, default=20)
    channel_p.add_argument("--format", choices=["md", "json"], default="md")
    channel_p.add_argument("--proxy-mode", choices=["auto", "direct", "required", "disabled"], default="auto")

    args = parser.parse_args()

    try:
        if args.action == "search":
            payload = search(
                query=args.query,
                limit=max(1, args.limit),
                attempts=max(1, args.attempts),
                timeout=max(1, args.timeout),
                proxy_mode=args.proxy_mode,
            )
            output = render_search_md(payload) if args.format == "md" else json.dumps(payload, indent=2, ensure_ascii=False)
        elif args.action == "resolve":
            payload = resolve(
                video_id_or_url=args.video_id_or_url,
                timeout=max(1, args.timeout),
                proxy_mode=args.proxy_mode,
            )
            output = render_resolve_md(payload) if args.format == "md" else json.dumps(payload, indent=2, ensure_ascii=False)
        elif args.action == "transcript":
            payload = transcript(
                video_id_or_url=args.video_id_or_url,
                languages=args.languages,
                include_fallback=not args.no_fallback,
                timeout=max(1, args.timeout),
                proxy_mode=args.proxy_mode,
            )
            output = render_transcript_md(payload) if args.format == "md" else json.dumps(payload, indent=2, ensure_ascii=False)
            if args.out:
                written = _write_output_file(args.out, output, args.format)
                print(json.dumps({"status": "ok", "written_to": written, "format": args.format,
                                  "bytes": len(output.encode("utf-8"))}))
                return 0
        elif args.action in ("channel", "list"):
            payload = channel_videos(
                channel_url=args.channel_url,
                limit=max(1, args.limit),
                timeout=max(1, args.timeout),
                proxy_mode=args.proxy_mode,
                meta=args.meta,
            )
            output = render_channel_md(payload) if args.format == "md" else json.dumps(payload, indent=2, ensure_ascii=False)
        else:
            print(f"Unknown action: {args.action}", file=sys.stderr)
            return 1

        print(output)
        return 0
    except ToolRuntimeError as exc:
        print(json.dumps({"status": "error", "error": exc.to_dict()}, indent=2), file=sys.stderr)
        return 1
    except Exception as exc:
        print(json.dumps({"status": "error", "error": {"kind": "internal", "message": str(exc)}}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
