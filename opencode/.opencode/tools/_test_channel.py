#!/usr/bin/env python3
import re, sys
sys.path.insert(0, '.')
from _shared_runtime import request_text

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

def parse_channel_page(html: str) -> list[dict]:
    results = []
    for m in re.finditer(r'"videoId":"([A-Za-z0-9_-]{11})"', html):
        vid = m.group(1)
        chunk = html[m.end():m.end()+1500]

        title_m = re.search(r'"title":\{"runs":\[\{"text":"([^"]+)"\}\]', chunk)
        desc_m = re.search(r'"descriptionSnippet":\{"runs":\[\{"text":"([^"]+)"\}\]', chunk)
        date_m = re.search(r'"publishedTimeText":\{"simpleText":"([^"]+)"\}', chunk)
        length_m = re.search(r'"lengthText":\{.*?"simpleText":"([^"]+)"', chunk)
        views_m = re.search(r'"viewCountText":\{"simpleText":"([^"]+)"\}', chunk)

        results.append({
            'video_id': vid,
            'title': title_m.group(1) if title_m else None,
            'description': desc_m.group(1)[:100] if desc_m else None,
            'published': date_m.group(1) if date_m else None,
            'duration': length_m.group(1) if length_m else None,
            'views': views_m.group(1) if views_m else None,
            'url': f'https://www.youtube.com/watch?v={vid}'
        })
    return results


channels = [
    ("MKBHD", "https://www.youtube.com/@MKBHD/videos"),
    ("Linus Tech Tips", "https://www.youtube.com/@LinusTechTips/videos"),
]

for name, url in channels:
    html, _ = request_text('GET', url, timeout=20,
        headers={'User-Agent': DEFAULT_USER_AGENT},
        proxy_mode='auto', provider='youtube',
        block_markers=['captcha', 'confirm'])

    videos = parse_channel_page(html)
    print(f"=== {name}: {len(videos)} videos ===")
    for v in videos[:3]:
        print(f"  {v['video_id']}: {v['title']} | {v['views']} | {v['published']}")
    print()
