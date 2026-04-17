import re, sys
sys.path.insert(0, '.')
from _shared_runtime import request_text

DEFAULT_UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

# Test MKBHD page content
url = 'https://www.youtube.com/@MKBHD/videos'
html, _ = request_text('GET', url, timeout=20, headers={'User-Agent': DEFAULT_UA}, proxy_mode='auto', provider='youtube', block_markers=['captcha', 'confirm'])

print(f'HTML length: {len(html)}')

# Check for key markers
for marker in ['videoId', 'richItemRenderer', 'videoRenderer', 'ytInitialData', 'Country', 'restricted', 'login']:
    count = html.count(marker)
    print(f'  "{marker}": {count} occurrences')

# Search for videoId with escaped quotes
print()
print('Searching for videoId patterns...')
patterns = [
    r'"videoId":"([A-Za-z0-9_-]{11})"',
    r'videoId%3A%22([A-Za-z0-9_-]{11})',
    r'\\"videoId\\":\\"([A-Za-z0-9_-]{11})\\"',
]
for p in patterns:
    m = re.search(p, html)
    if m:
        print(f'  Pattern matched: {p[:40]} -> {m.group(1)}')
    else:
        print(f'  No match: {p[:40]}')

# Show first 500 chars of HTML
print()
print('First 500 chars of HTML:')
print(repr(html[:500]))
