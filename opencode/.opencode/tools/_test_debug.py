import re, sys
sys.path.insert(0, '.')
from _shared_runtime import request_text

DEFAULT_UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

urls = [
    ('MKBHD', 'https://www.youtube.com/@MKBHD/videos'),
    ('Linus', 'https://www.youtube.com/@LinusTechTips/videos'),
]

for name, url in urls:
    html, _ = request_text('GET', url, timeout=20, headers={'User-Agent': DEFAULT_UA}, proxy_mode='auto', provider='youtube', block_markers=['captcha', 'confirm'])
    vid_matches = list(re.finditer(r'"videoId":"([A-Za-z0-9_-]{11})"', html))
    print(f'{name}: videoId count={len(vid_matches)}')

    if vid_matches:
        m = vid_matches[0]
        chunk = html[m.end():m.end()+500]
        print(f'  First videoId: {m.group(1)}')
        print(f'  Chunk: {repr(chunk[:300])}')

        title_m2 = re.search(r'"title":\{"runs":\[\{"text":"([^"]+)"\}\]', chunk)
        print(f'  Simple title match: {title_m2.group(1) if title_m2 else None}')
    print()
