---
name: research-extended-tools
description: Domain-specific research tools — FDA 510(k), patents, HCPCS, EUDAMED, startup data, arxiv, PDF extraction, Wikidata, RSS feeds, DuckDB
---

## When to Load This Skill

Load this skill when your research task involves ANY of:

### Cluster 1 — Regulated Industries & Structured Data

- Medical device FDA 510(k) clearance lookup
- Patent and intellectual property search (US, EP, WO, 100+ offices)
- HCPCS/CPT code lookup for medical procedures/devices
- Startup and funding data (SEC EDGAR, Crunchbase)
- EU medical device registry (EUDAMED)

### Cluster 2 — Academic Literature & Knowledge Graphs

- arXiv paper search, download, and reading
- PDF text extraction and conversion
- Wikidata entity search and SPARQL queries
- Academic paper search via OpenAlex

### Cluster 3 — Data Processing & Monitoring

- Structured data analysis (DuckDB)
- RSS feed parsing and monitoring
- Historical web archive access (Wayback Machine)

---

## Tool Invocation

All tools are standalone Python scripts at `~/.opencode/tools/`. Invoke them via `bash`
with `uv run` to provide dependencies. The **Tool Dependency Summary** at the bottom of
this file lists the correct `uv run --with ...` wrapper for each tool.

General pattern:
```bash
uv run --with <deps> python3 ~/.opencode/tools/<TOOL>.py <args> [--format md|json]
```

If `~/.config/proxy-conf` contains a dead proxy, strip proxy vars first:
```bash
HTTP_PROXY= HTTPS_PROXY= uv run --with <deps> python3 ~/.opencode/tools/<TOOL>.py ...
```

---

## Domain-Specific Tools

### Available as Scripts

| Tool | What it searches | Key params | Auth |
|------|-----------------|------------|------|
| `web_scraper` | Any public URL; modes: text/markdown/links/tables | `--url`, `--mode`, `--selector` | None |
| `fda_510k` | FDA 510(k) clearance DB (openFDA API) | `--query`, `--k-number`, `--applicant`, `--decision`, `--date-from` | None (set `OPENFDA_API_KEY` for higher rate limits) |
| `patent_search` | Google Patents — US, EP, WO, 100+ offices | `--query`, `--patent-number`, `--assignee`, `--country`, `--date-from` | None |
| `hcpcs_lookup` | HCPCS codes (NLM) + FDA device classification | `--code`, `--search`, `--source` (cms/fda/both) | None |
| `startup_data` | SEC EDGAR filings + optional Crunchbase | `--company`, `--query`, `--source` (edgar/crunchbase/both) | `CRUNCHBASE_API_KEY` for Crunchbase |
| `eudamed_lookup` | EU medical device registry (CE-marked, UDI, MDR) | `--query`, `--manufacturer`, `--udi` | None |

**Example invocations:**

```bash
# FDA 510(k) clearance search
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/fda_510k.py --query "blood glucose" --limit 20 --format md

# Patent search
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/patent_search.py --query "neural network" --country US --limit 10

# HCPCS code lookup
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/hcpcs_lookup.py --search "laryngectomy" --source both --format md

# EUDAMED device search
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/eudamed_lookup.py --query "implant" --limit 20 --format md

# Startup / SEC EDGAR data
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/startup_data.py --company "Tesla" --source edgar --format md

# Web scraping
uv run --with requests --with certifi --with beautifulsoup4 \
  python3 ~/.opencode/tools/web_scraper.py --url "https://example.com" --mode markdown
```

### One-off Inline Tools (via `uv run --with <pkg> python -c`)

These do not have standalone scripts. Invoke them as one-off Python snippets:

**arXiv papers:**
```bash
uv run --with arxiv python3 -c "
import arxiv
search = arxiv.Search(query='machine learning', max_results=10, sort_by=arxiv.SortCriterion.Relevance)
for result in arxiv.Client().results(search):
    print(result.title, result.entry_id, result.pdf_url)
"
```
Rate limit: add 3-second delay between requests.

**PDF text extraction (with PyMuPDF):**
```bash
uv run --with pymupdf python3 -c "
import fitz
doc = fitz.open('document.pdf')
print(''.join(page.get_text() for page in doc)[:2000])
"
```
**Alternative for tables:** `uv run --with pdfplumber python3 -c "..."`

**PDF to markdown (image extraction):** use `glm-ocr` skill for OCR on scanned PDFs. After OCR, `uv run --with pymupdf` for text extraction.

**DuckDB data analysis:**
```bash
uv run --with duckdb python3 -c "
import duckdb
print(duckdb.sql(\"SELECT * FROM 'data.csv' WHERE value > 100\").df())
"
```

**RSS feed parsing:**
```bash
uv run --with feedparser python3 -c "
import feedparser
feed = feedparser.parse('https://feeds.bbci.co.uk/news/rss.xml')
for e in feed.entries[:5]:
    print(e.get('title'), e.get('link'))
"
```

**OpenAlex academic search:**
```bash
uv run --with pyalex python3 -c "
from pyalex import Works
for w in Works().search('transformer architecture').get(per_page=10):
    print(w['title'], w['doi'])
"
```

**Wayback Machine check:**
```bash
uv run --with requests python3 -c "
import requests
r = requests.get('http://archive.org/wayback/available', params={'url': 'example.com'})
snap = r.json().get('archived_snapshots', {}).get('closest')
if snap:
    print(f\"Archived: {snap['url']} @ {snap['timestamp']}\")
"
```

**Wikidata SPARQL (no native tool — use the API directly):**
```bash
uv run --with requests python3 -c "
import requests, urllib.parse
query = '''
SELECT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q5 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". }
}
LIMIT 10
'''
url = 'https://query.wikidata.org/sparql?query=' + urllib.parse.quote(query)
r = requests.get(url, headers={'Accept': 'application/sparql-results+json'})
print(r.json())
"
```

Note: Wikidata QIDs and PIDs are not learnable — always use Wikidata search to discover relevant identifiers first.

**Audio transcription (faster-whisper):**
```bash
uv run --with faster-whisper python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('tiny', device='cpu', compute_type='int8')
segments, info = model.transcribe('audio.mp3', beam_size=5)
print(' '.join(s.text for s in segments))
"
```
**If that fails:** download audio via `uv run --with yt-dlp --with certifi yt-dlp -x --audio-format mp3 -o audio.%(ext)s "URL"`.

---

## Tool Dependency Summary

| Tool | `uv run --with ...` wrapper |
|------|------------------------------|
| `youtube.py` | `--with requests --with certifi --with youtube-transcript-api` |
| `web_scraper.py` | `--with requests --with certifi --with beautifulsoup4` |
| `fda_510k.py` | `--with requests --with certifi` |
| `patent_search.py` | `--with requests --with certifi` |
| `hcpcs_lookup.py` | `--with requests --with certifi` |
| `startup_data.py` | `--with requests --with certifi` |
| `eudamed_lookup.py` | `--with requests --with certifi` |
| `reddit_scraper.py` | `--with requests --with certifi --with praw --with python-dotenv` |

**Proxy workaround** (when `~/.config/proxy-conf` contains a dead proxy):
prefix all commands with `HTTP_PROXY= HTTPS_PROXY= ` to strip proxy vars.

---

## HCPCS Codes Pre-loaded for Laryngoscopy/Voice Restoration

- L8500: artificial larynx
- L8507: voice pros, patient-inserted
- L8509: MD-inserted voice prosthesis
- L8512/L8513: accessories
- A7520/A7521: tracheostomy tubes