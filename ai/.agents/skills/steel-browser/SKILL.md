---
name: steel-browser
description: "Fetch and extract web data via LAN Steel browser over CDP."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [steel, cdp, browser, scraping, extraction]
    related_skills: []
---

# Steel Browser Skill

Drive the self-hosted Steel browser (Docker stack `steel` on `admin@192.168.1.50`) over raw CDP to fetch pages, extract structured data, and take screenshots — including JS-heavy sites that plain HTTP fetches cannot handle.

## When to Use
- Fetching/extracting from JS-rendered sites (SPAs, infinite scroll, meta tags behind JS)
- Site playbooks: Facebook public pages, Instagram profiles, TikTok explore + transcripts, IKEA product search
- Screenshotting pages; wall detection (Cloudflare/DataDome/login)
- Re-testing site accessibility after Steel/Chrome updates (`scripts/steel_stress.py`)
- Don't use for: plain static HTML (use `web_extract`); Google search (blocked, use DDG/Bing); leboncoin (DataDome hard-blocked); anything requiring login credentials (exception: Devoteam corporate Gmail — playbook below)

## Prerequisites
- Steel stack healthy: `curl -s http://192.168.1.50:3000/v1/health` → `{"status":"ok"}`
- Python deps: `websocket-client`, pre-installed in the skill venv — run scripts with `~/.agents/skills/steel-browser/.venv/bin/python` (rebuild if needed: `python3 -m venv .venv && .venv/bin/pip install websocket-client`)
- Scripts live in this skill dir; run with the session python

## How to Run
All through the `terminal` tool, from any cwd (scripts resolve their own path):

    python=~/.agents/skills/steel-browser/.venv/bin/python
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py health
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch https://example.com
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch https://www.ikea.com/fr/fr/search/?q=bureau --site ikea --out /tmp/ikea.json
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch https://www.instagram.com/nasa/ --site auto
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch https://www.amazon.fr/s?k=bureau --site auto
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch https://fr.aliexpress.com/w/wholesale-bureau.html --site auto
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://www.action.com/fr-fr/search/?q=bureau" --site auto --retry-wall
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://www.but.fr/Common/Search/SearchProductsList?KeyWords=bureau" --site auto --timeout 80
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://www.conforama.fr/recherche-conforama/bureau" --site auto --retry-wall --timeout 80
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://www.manomano.fr/recherche/bureau" --site auto --retry-wall --timeout 80
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://www.vidaxl.fr/catalogsearch/result/?q=bureau" --site auto
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://www.miliboo.com/recherche.html?search=bureau" --site auto
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://www.kavehome.com/fr/fr/o/canapes" --site auto
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch "https://theredarchive.com/search?s=daygame+session" --site theredarchive
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch https://theredarchive.com/r/seduction/going-out-with-the-sole-intention-of-meeting-women.1283290 --site theredarchive
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py fetch https://www.quora.com --retry-wall
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py transcript https://www.tiktok.com/@user/video/123
    $python ~/.agents/skills/steel-browser/scripts/steel_cdp.py shot https://example.com /tmp/x.jpg

`--site` selects an extractor: `auto` (match by URL), `facebook`, `instagram`, `tiktok`, `ikea`, `amazon`, `aliexpress`, `action`, `but`, `conforama`, `manomano`, `vidaxl`, `miliboo`, `kavehome`, `theredarchive`, or `none`. Output is JSON on stdout (or `--out` file). `--settle F` overrides the post-load wait (seconds).

## Quick Reference
- Steel REST API: `http://192.168.1.50:3000/v1` (health, POST /sessions)
- CDP endpoint: `http://192.168.1.50:9223` (`/json/version`, `/json/list`, per-target ws)
- Server ops: `sshpass`+ssh `admin@192.168.1.50`, stack at `/data/docker/compose/steel`, logs `docker logs steel`
- Concurrency: keep ≤5 parallel tabs (10 works but stragglers hit ~50s)

## Procedure
1. Check health (`health` subcommand). If down: `ssh admin@192.168.1.50 'cd /data/docker/compose/steel && docker compose up -d'`.
2. `fetch <url>` with `--site auto` when the URL matches a playbook site.
3. Inspect the JSON `verdict` field: `ok` → use `data`; wall fields list what blocked us.
4. Cloudflare interstitial (`walls: ["cloudflare_challenge"]`)? Re-run with `--retry-wall` — one retry after 5s often clears it (verified on quora.com).
5. Need a screenshot too? `shot` subcommand, jpeg ~80KB.

## Site Playbooks (retail verified 2026-08-21, social verified 2026-08-16)
### TheRedArchive (theredarchive.com) — banned-subreddit research
- **Search** (`theredarchive.com/search?s=<query>`): results server-rendered → `{kind: theredarchive_search, items: [{sub, title, path}]}`. **CRITICAL: the query param is `s`, NOT `q`** — `?q=` silently renders the empty search landing page (the form submits `s`). Results ranked by relevance across all archived subreddits (askTRP, TheRedPill, seduction, MRP…). DuckDuckGo hits a bot challenge and Bing drops `site:` — use this native search instead.
- **Thread** (`/r/<sub>/<slug>.<id>`): OP + full comment tree parsed from in-page JSON-LD (`@graph` → DiscussionForumPosting + nested Comments) → `{kind: theredarchive_thread, title, author, date, op, commentCount, comments: top 20 sorted by upvoteCount}`.
- **Subreddit index** (`/r/<sub>`): Top Posts table → `{kind: theredarchive_index, items: [{title, path}]}` (50/page).
- No walls, no login, no JS needed (plain HTTP works too) — the whole archive is server-rendered.

### E-commerce / retail extractors
- **Amazon FR** (`amazon.fr/s?k=<query>`): results via `[data-component-type="s-search-result"]` — name, clean price (`89,99€`), ASIN, rating. EN titles common (browser locale → `/-/en/` paths) — fine for extraction. No wall.
- **AliExpress** (`fr.aliexpress.com/w/wholesale-<query>.html`): cards `.search-item-card-wrapper-gallery` — class-agnostic price/promo/sold/rating parse from card text lines (hashed classnames change; text-line regex is stable). 24–60 items. No wall.
- **Action** (`action.com/<locale>/search/?q=<query>` — param is **q**, NOT query): product links `/p/<itemnr>/<slug>/` — name, `X,XX €/pce` price. Cloudflare challenge on first load → **use `--retry-wall`**. Beware: wrong param (`query=`) silently falls back to homepage carousels.
- **BUT** (`but.fr/Common/Search/SearchProductsList?KeyWords=<query>` — found via their `/Api/Rest/SearchEngine/Suggestions` API): cards `/produits/<ean>/<slug>.html` — name, price+promo (`149,99€179,99€-16%`). SPA slow: auto-settle 12s + JS polls for link/price hydration (`--timeout 80`). Note: generic queries redirect to category pages (`/index-cXXXXX.html`) — extractor works on both. Intermittent DataDome tag present; only a real captcha-delivery interstitial means blocked.
- **Conforama** (`conforama.fr/recherche-conforama/<query>` — from their robots.txt): tiles `article[data-component-id="product-tile"]` + `data-objectid`, price via `.price` (`Vendu X €`). **Prices lazy-hydrate per-tile on visibility** — extractor polls for the first price, then scrolls in waves and merges. Cloudflare managed on domain → **`--retry-wall`**. `--timeout 80`.
- **ManoMano** (`manomano.fr/recherche/<query>`): links `a[href^="/p/"]`, price parsed from card text lines. Cloudflare challenge → **`--retry-wall`**. **CRITICAL: the grid is virtualized — NEVER scroll and parse IMMEDIATELY** (scrolling removes cards from the DOM; waiting dehydrates prices). Each product has 2-3 anchors (image/title) — dedup AFTER the price filter, or you keep the image anchor with no price. Sponsored cards in front never carry prices.
- **VidaXL** (`vidaxl.fr/catalogsearch/result/?q=<query>` — Magento): tiles `.product-tile` + `data-pid`, links `/e/<slug>/<id>.html`, price from `[class*="price"]` (normalize "70 99 €" → "70,99 €"). No wall.
- **Miliboo** (`miliboo.com/recherche.html?search=<query>` — param is **search**, from their homepage form): cards `.product-teaser` / `.card.product`, price `.product-price`. Category pages (`/<slug>.html`) extract too. No wall.
- **Kave Home** (`www.kavehome.com/fr/fr/o/<category-slug>` — e.g. `canapes`, `chaises`, `tables` — search is a JS overlay, NOT URL-addressable): cards `[class*="productBox"]`, links `/fr/fr/p/<slug>`, price from card `[class*="price"]`. `fr.kavehome.com` is NXDOMAIN — use `www.`.
- **IKEA search** (`ikea.com/<locale>/search/?q=`): products via `.plp-price-module` — name `.plp-price-module__product-name`, price `.plp-price__sr-text` (strip "Prix"), link `a[href*="/p/"]`. ~12+ items per page.

### Blocked retail (datacenter IP / anti-bot, do not retry)
- **Temu**: "Security verification" + login-gated search (`Temu | Login`), `window.rawData` keys deliberately obfuscated. Hard-blocked.
- **Maisons du Monde** (correct domain: `www.maisonsdumonde.com`, the hyphenated one is NXDOMAIN): DataDome interstitial. Hard-blocked.
- **Leroy Merlin**: DataDome. Hard-blocked.
- **Decathlon**: Cloudflare managed challenge, retry does NOT clear. Blocked.
- **Cdiscount**: "Accès bloqué" (WAF/IP). Blocked.
- **La Redoute**: "WAF Block/IP Block" on homepage. Blocked.
- **Fly** (`fly-meubles.fr`): domain dead (NXDOMAIN).

### Partial (page loads, no extractor yet)
- none currently — all explored retail sites are either extracted or documented as blocked

### Social (verified 2026-08-16)
- **TikTok transcripts**: `transcript <video-url>` — reads `__UNIVERSAL_DATA_FOR_REHYDRATION__` JSON → `video.subtitleInfos` → fetches the WebVTT (via page-context fetch; needs TikTok referer). Works only when TikTok's ASR generated captions (~1 in 5 videos; `subtitle_tracks` field shows what exists). Timestamps stripped to plain text.
- **Facebook public pages** (`facebook.com/<page>/`): posts via `div[role="article"]` — text, author, rough timestamp. Login form is present but public page content still renders. Marketplace: requires login, don't bother. Video transcripts: not available logged-out (login required).
- **Instagram profiles** (`instagram.com/<handle>/`): handle, follower/following stats, bio, up to ~8 post links (`a[href*="/p/"]`). No login wall for profile pages. Reels: video plays logged-out (blob: src) but no caption/transcript data in DOM — transcripts need login.
- **TikTok explore** (`tiktok.com/explore`): video links + view counts (captions only render on hover — not in DOM). Profile pages (`/@user`): grid is lazy-loaded — scroll or treat explore as the entry.
- **IKEA search** (`ikea.com/<locale>/search/?q=`): products via `.plp-price-module` — name `.plp-price-module__product-name`, price `.plp-price__sr-text` (strip "Prix"), link `a[href*="/p/"]`. ~12+ items per page.
- **leboncoin**: DataDome captcha iframe (`geo.captcha-delivery.com`) — hard-blocked headless, retry does NOT clear. Skip.

### Devoteam corporate Gmail sign-in (verified 2026-09-08)
Google Workspace account `mohamed.ait.taleb@devoteam.com` — full login flow driven over Steel CDP via browser-use, incl. password fallback + 2FA phone prompt. Result: signed-in session persists in Steel's shared Chrome profile (future tabs/fetches authenticated, no re-login until logout/expiry).
- **Credentials**: Vault `kv-v2/Perso` → fields `Devoteam-mail`, `Devoteam-pswd`. Load into env in-memory only (never print, never write to disk):
  `export VAULT_ADDR='https://hashi-vault.aitbytes.fyi'; J=$(vault kv get -format=json kv-v2/Perso); export M=$(echo "$J" | jq -r '.data.data["Devoteam-mail"]'); export P=$(echo "$J" | jq -r '.data.data["Devoteam-pswd"]')`
- **Harness**: `BU_CDP_URL=http://192.168.1.50:9223 browser-use <<'PY' ...` — helpers `new_tab`, `page_info()`, `js()`, `cdp()`, `click_at_xy(x,y)`, `wait_for_load()`. First call of a flow: `new_tab(url)`.
- **Flow** (GAIA v3, English UI):
  1. `new_tab("https://mail.google.com")` → lands on `accounts.google.com/v3/signin/identifier`
  2. Email: `input#identifierId` (type=**text**, NOT type=email — `input[type=email]` matches nothing). Focus with `click_at_xy` at its center, then `cdp("Input.insertText", text=...)`, click Next
  3. Passkey challenge screen ("Complete sign-in using your passkey") → DOM-click **Try another way** → chooser lists **Enter your password** → select it
  4. Password: `input[name="Passwd"]` (an earlier hidden `input[name=hiddenPassword]` exists — ignore it) → type + Next
  5. 2FA chooser (`/challenge/selection`): options = Use your passkey / one-time security code / **Tap Yes on your phone or tablet** / phone offline code / **Google Authenticator code** / SMS at •• •• •• •• 34
  6. Phone prompt (user's Galaxy S23 FE): number-match — user taps Yes then the shown 2-digit number; number re-issues on "Resend it"; expires ~2-3 min. Poll `page_info()` until URL = `https://mail.google.com/mail/u/0/#inbox`
- **CRITICAL gotchas**:
  - Sign-in options are `DIV[role="link"]` / `DIV[role="button"]`, NOT `<button>` — selector lists like `div[role=button]` miss them and clicks "don't register". Always match `[role="link"], [role="button"], button` filtered by `innerText`, then DOM `.click()` on the element carrying the role (els[0] must be the interactive element, not a text wrapper)
  - Coordinate clicks are often swallowed while the page still shows "Loading" (pre-hydration); DOM `.click()` on the right element is reliable there
  - `Runtime.evaluate` / IPC timeouts mid-flow are benign (page navigating) — just re-check state in a fresh call
  - "Already signed in?" check first: `page_info().url` starts with `https://mail.google.com/mail/u/0/` → skip the whole flow
  - After a valid password, corporate policy still forces 2FA — that is the expected happy path, not an error

## Pitfalls
- **Google search → HTTP 429 + captcha**, persistent (datacenter IP). Use DuckDuckGo or Bing instead — both extract fine.
- **DataDome walls never clear** by retry (unlike Cloudflare's JS challenge which often clears on 2nd load).
- **DataDome false positives**: some sites (BUT) embed the DataDome SDK tag without triggering it — wall detection keys on `captcha-delivery.com` (real interstitial), never on a bare "datadome" substring.
- **Lazy price hydration** (BUT skeletons, Conforama per-tile intersection observer): extractors must scroll and poll — a single post-load snapshot gets empty prices.
- **Virtualized grids (ManoMano)**: scrolling REMOVES earlier cards from the DOM, and cards dehydrate over time — parse immediately without scrolling. Multi-anchor products: dedup after filtering (image anchors carry no price).
- **Cloudflare auto-resolution**: non-interactive challenges often self-resolve in 5-15s via auto-redirect — `--retry-wall` now polls patiently BEFORE reloading (reloading mid-challenge can leave SPAs in a bad state, e.g. ManoMano without prices).
- **Wrong search param = silent homepage**: action.com needs `?q=` not `?query=` — the page loads "fine" but shows homepage carousels. Always sanity-check item names against the query.
- Fingerprint tells that remain: `plugins.length=0`, SwiftShader WebGL, `pdfViewerEnabled=false`. Hardened bot-fingerprinting (Cloudflare managed challenge e.g. nowsecure.nl, G2 403) will block; most sites don't.
- Tail latency: ~4-8s per page typical; leave nav_timeout 40s+ for slow SPAs.
- One shared Chrome per Steel instance: tabs are isolated but the browser profile (cookies) is shared — a Cloudflare clearance gained on one tab helps others on the same domain.
- `Target.closeTarget` after every tab or the browser accumulates targets.
- Login walls (X/Twitter full content, FB marketplace, IG stories) are not solvable without credentials — never attempt logins, except the sanctioned Devoteam Gmail playbook above.

## Verification
- `health` prints browser version + session API status
- `fetch https://example.com --site none` returns verdict `ok`, title "Example Domain"
- `fetch https://www.ikea.com/fr/fr/search/?q=bureau --site ikea` returns ≥8 items with prices
- `fetch https://www.amazon.fr/s?k=bureau --site auto` returns `amazon_search` ≥20 items with prices
- `fetch https://fr.aliexpress.com/w/wholesale-bureau.html --site auto` returns `aliexpress_search` ≥24 items with prices
- `fetch "https://www.action.com/fr-fr/search/?q=bureau" --site auto --retry-wall` returns `action_products` ~24 items (verify names match the query, not homepage carousels — if all items are "Semaine d'Action" promos, the URL param is wrong)
- `fetch "https://www.but.fr/Common/Search/SearchProductsList?KeyWords=bureau" --site auto --timeout 80` returns `but_products` ~50 items, all with prices
- `fetch "https://www.conforama.fr/recherche-conforama/table-basse" --site auto --retry-wall --timeout 80` returns `conforama_products` ~60 items with prices (price hydration is lazy — occasional slow runs; retry once if 0 priced)
- `fetch "https://www.manomano.fr/recherche/etagere" --site auto --retry-wall --timeout 80` returns `manomano_products` ≥10 items with prices
- `fetch "https://www.vidaxl.fr/catalogsearch/result/?q=bureau" --site auto` returns `vidaxl_products` ~20-40 items with prices
- `fetch "https://www.miliboo.com/recherche.html?search=bureau" --site auto` returns `miliboo_products` ~24 items with prices
- `fetch "https://www.kavehome.com/fr/fr/o/chaises" --site auto` returns `kavehome_products` ~40-60 items with prices
- `fetch "https://theredarchive.com/search?s=daygame+session" --site theredarchive` returns `theredarchive_search` with 25+ titled result items
- `fetch https://theredarchive.com/r/TheRedPill/yes-you-can-approach-women-in-the-gym.1513022 --site theredarchive` returns `theredarchive_thread` with title, author, `op` and 8+ scored comments
- Re-testing wall behavior after any Chrome/Steel update: `python scripts/steel_stress.py batch1|batch2|batch3|concurrency 5` (harness shipped in `scripts/`; results JSONL in cwd)
