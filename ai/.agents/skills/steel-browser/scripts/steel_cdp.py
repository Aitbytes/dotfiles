#!/usr/bin/env python
"""steel_cdp.py — drive the LAN Steel browser (Chrome) over raw CDP.

Subcommands:
  health                          — check Steel API + CDP endpoint
  fetch <url> [--site X] [--out F] [--retry-wall] [--timeout N] [--settle F]
  transcript <tiktok-video-url> [--out F]
  shot <url> <out.jpg>            — screenshot to jpeg file
Extractors: auto|none|facebook|instagram|tiktok|ikea|amazon|aliexpress|action|but|conforama|manomano|vidaxl|miliboo|kavehome|theredarchive (auto matches by URL)
Output: single JSON object on stdout.
"""
import base64
import json
import re
import sys
import time
import urllib.request

import websocket

API = "http://192.168.1.50:3000/v1"
CDP_HTTP = "http://192.168.1.50:9223"
DEFAULT_TIMEOUT = 45

# ---------- CDP client ----------

class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=90)
        self.next_id = 0

    def send(self, method, params=None, sessionId=None):
        self.next_id += 1
        msg = {"id": self.next_id, "method": method, "params": params or {}}
        if sessionId:
            msg["sessionId"] = sessionId
        self.ws.send(json.dumps(msg))
        return self.next_id

    def recv_until(self, want_id, timeout=60):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                self.ws.settimeout(max(1, deadline - time.time()))
                m = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                break
            if m.get("id") == want_id:
                if "error" in m:
                    raise RuntimeError(f"CDP error: {m['error']}")
                return m.get("result", {})
        raise TimeoutError(f"no response for id {want_id}")

    def call(self, method, params=None, sessionId=None, timeout=60):
        return self.recv_until(self.send(method, params, sessionId), timeout=timeout)

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def http_json(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.load(r)


def connect():
    return CDP(http_json(f"{CDP_HTTP}/json/version")["webSocketDebuggerUrl"])


# ---------- navigation with wall detection ----------

WALLS = {
    "cloudflare_challenge": ["just a moment", "checking your browser", "attention required! | cloudflare", "verify you are human", "un instant", "performing security verification"],
    "datadome": ["captcha-delivery.com"],
    "login_wall": ["sign in to continue", "log in to continue", "authwall", "sign up to continue", "login to continue", "keep up with what's happening"],
    "recaptcha": ["g-recaptcha", "are you a robot", "unusual traffic", "prove you are human"],
    "consent_wall": ["we value your privacy", "manage cookies", "accept all cookies", "consent to cookies"],
    "blocked": ["access denied", "you don't have permission to access", "403 forbidden", "request blocked", "accès bloqué", "error reason : waf", "dns_probe_finished"],
}
TEXT_ONLY = {"recaptcha", "consent_wall"}


def detect_walls(title, text, html):
    t = f"{title or ''} {text or ''}".lower()[:1200]
    h = (html or "").lower()[:20000]
    hits = []
    for wall, markers in WALLS.items():
        hay = t if wall in TEXT_ONLY else t + " " + h
        if any(mk in hay for mk in markers):
            hits.append(wall)
    return hits


EXTRACT_COMMON = """
(() => ({
  url: location.href,
  title: document.title,
  text: document.body ? document.body.innerText.replace(/\\s+/g, ' ').slice(0, 2500) : '',
  html: document.documentElement.outerHTML.slice(0, 60000)
}))()
"""


def navigate(cdp, url, nav_timeout=DEFAULT_TIMEOUT, settle=3.0):
    """Open a tab, navigate, wait for load. Returns (sessionId, targetId)."""
    tid = cdp.call("Target.createTarget", {"url": "about:blank"})["targetId"]
    s = cdp.call("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
    cdp.call("Page.enable", sessionId=s)
    cdp.call("Page.navigate", {"url": url}, sessionId=s)
    deadline = time.time() + nav_timeout
    while time.time() < deadline:
        time.sleep(1.0)
        try:
            st = cdp.call("Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True},
                          sessionId=s, timeout=8)["result"].get("value", "")
            if st == "complete":
                break
        except Exception:
            pass
    time.sleep(settle)
    return s, tid


def page_state(cdp, s):
    r = cdp.call("Runtime.evaluate", {"expression": EXTRACT_COMMON, "returnByValue": True},
                 sessionId=s, timeout=25)["result"].get("value") or {}
    return r


# ---------- site extractors ----------

def extract_facebook(js_eval):
    return js_eval(r"""
(() => {
  const posts = [...document.querySelectorAll('div[role="article"]')].slice(0, 10).map(a => a.innerText.replace(/\\s+/g, ' ').slice(0, 300));
  const uniq = [];
  const seen = new Set();
  for (const p of posts) { const k = p.slice(0, 80); if (!seen.has(k) && p.length > 40) { seen.add(k); uniq.push(p); } }
  return {kind: 'facebook_page', posts: uniq.slice(0, 6),
          loginForm: !!document.querySelector('form[action*="login"], input[name="email"]')};
})()
""")


def extract_instagram(js_eval):
    return js_eval(r"""
(() => {
  const links = [...new Set([...document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]')].map(a => a.getAttribute('href')))];
  const header = document.querySelector('header') || document;
  const stats = [...header.querySelectorAll('a, li')].map(e => e.textContent.trim()).filter(t => /\\d/.test(t) && t.length < 30).slice(0, 6);
  const handle = header.querySelector('h2, h1')?.textContent?.trim() || '';
  const bio = [...header.querySelectorAll('[dir="auto"]')].map(e => e.textContent.trim()).filter(t => t && t !== handle && !/\\d/.test(t.slice(0,3))).slice(0, 3);
  return {kind: 'instagram_profile', handle, stats, bio, postLinks: links.slice(0, 10),
          loginWall: !!document.querySelector('input[name="username"]')};
})()
""")


def extract_tiktok(js_eval):
    return js_eval(r"""
(() => {
  const items = [...document.querySelectorAll('a[href*="/video/"]')].slice(0, 20).map(a => {
    const card = a.closest('[data-e2e], div');
    const cap = (card?.querySelector('[data-e2e="video-desc"], p, div[class*="Caption"]')?.textContent || a.textContent || '').trim().slice(0, 140);
    const views = card?.querySelector('[data-e2e="video-views"], [data-e2e="like-count"]')?.textContent?.trim() || '';
    if (/^[\\d.,]+\\s*[KMB]?$/i.test(cap)) return {caption: '', views: cap, href: a.getAttribute('href')};
    return {caption: cap, views, href: a.getAttribute('href')};
  });
  const seen = new Set(); const uniq = [];
  for (const it of items) { if (it.href && !seen.has(it.href)) { seen.add(it.href); uniq.push(it); } }
  return {kind: 'tiktok_list', items: uniq.slice(0, 10),
          loggedIn: !!document.querySelector('[data-e2e="top-upload-button"], [data-e2e="nav-upload"]')};
})()
""")


def extract_ikea(js_eval):
    return js_eval(r"""
(() => {
  const items = [];
  const modules = [...document.querySelectorAll('.plp-price-module')];
  for (const m of modules.slice(0, 60)) {
    const name = m.querySelector('.plp-price-module__product-name')?.textContent?.trim() || '';
    const a = m.querySelector('a[href*="/p/"]');
    const price = m.querySelector('.plp-price__sr-text')?.textContent?.replace(/^\\s*Prix\\s*/, '').trim() || '';
    const desc = [...m.querySelectorAll('.plp-text')].map(e => e.textContent.trim()).find(t => t && !t.startsWith('Prix')) || '';
    if (name && a) items.push({name, desc: desc.slice(0, 80), price, path: new URL(a.href).pathname});
  }
  const seen = new Set(); const uniq = [];
  for (const it of items) { if (!seen.has(it.path)) { seen.add(it.path); uniq.push(it); } }
  return {kind: 'ikea_products', count: uniq.length, items: uniq.slice(0, 20)};
})()
""")


def extract_amazon(js_eval):
    return js_eval(r"""
(() => {
  const results = [...document.querySelectorAll('[data-component-type="s-search-result"]')];
  const items = results.slice(0, 40).map(r => {
    const a = r.querySelector('h2 a, h2 span a, [data-cy="title-recipe"] a');
    const whole = r.querySelector('.a-price-whole')?.textContent?.replace(/[,\.\s]+$/, '').trim() || '';
    const frac = r.querySelector('.a-price-fraction')?.textContent?.trim() || '';
    const sym = r.querySelector('.a-price-symbol')?.textContent?.trim() || '€';
    const rating = r.querySelector('.a-icon-alt')?.textContent?.split(' ')[0] || '';
    return {asin: r.getAttribute('data-asin'), name: (a?.textContent || '').trim().slice(0, 120),
            price: whole ? (frac ? whole + ',' + frac : whole) + sym : '', path: a ? new URL(a.href).pathname : '',
            rating};
  }).filter(x => x.name && x.path);
  return {kind: 'amazon_search', count: items.length, items: items.slice(0, 20)};
})()
""")


def extract_aliexpress(js_eval):
    return js_eval(r"""
(async () => {
  for (let i = 0; i < 3; i++) { window.scrollBy(0, 1200); await new Promise(r => setTimeout(r, 600)); }
  const cards = [...document.querySelectorAll('.search-item-card-wrapper-gallery')].slice(0, 60);
  const items = cards.map(c => {
    const a = c.querySelector('a[href*="/item/"]');
    const href = a ? a.getAttribute('href').split('?')[0].replace(/^\/\//, '') : '';
    const tEl = [...c.querySelectorAll('[title]')].find(e => (e.getAttribute('title') || '').length > 30);
    const title = tEl?.getAttribute('title') || c.querySelector('img[alt]')?.getAttribute('alt') || '';
    const lines = (c.innerText || '').split('\\n').map(s => s.trim()).filter(Boolean);
    const price = lines.find(l => /^\d[\d\s.,]*\s*€$/.test(l)) || '';
    const oldIdx = lines.indexOf(price);
    const old = lines.find((l, i) => i > oldIdx && oldIdx >= 0 && /^\d[\d\s.,]*\s*€$/.test(l)) || '';
    const disc = lines.find(l => /^-\d+%$/.test(l)) || '';
    const sold = lines.find(l => /\d+\s*(vendus?|sold|bought)/i.test(l)) || '';
    const rating = lines.find(l => /^\d[.,]\d$/.test(l)) || '';
    return {name: title.slice(0, 120), price, old: old !== price ? old : '', disc, sold, rating, path: href};
  }).filter(x => x.path && x.name);
  const seen = new Set(); const uniq = [];
  for (const it of items) { if (!seen.has(it.path)) { seen.add(it.path); uniq.push(it); } }
  return {kind: 'aliexpress_search', count: uniq.length, items: uniq.slice(0, 20)};
})()
""")


def extract_action(js_eval):
    return js_eval(r"""
(async () => {
  for (let i = 0; i < 3; i++) { window.scrollBy(0, 1200); await new Promise(r => setTimeout(r, 600)); }
  const tiles = [...document.querySelectorAll('a[href*="/p/"]')];
  const seen = new Set(); const items = [];
  for (const a of tiles.slice(0, 150)) {
    const href = a.getAttribute('href').split('?')[0];
    if (seen.has(href)) continue;
    seen.add(href);
    const card = a.closest('article, li, div');
    const name = (a.getAttribute('aria-label') || card?.querySelector('h2, h3, [class*="title"]')?.textContent || a.textContent || '').trim().replace(/\s+/g, ' ');
    const price = card?.querySelector('[class*="price" i], [data-testid*="price" i]')?.textContent?.trim().replace(/\s+/g, ' ').slice(0, 25) || '';
    items.push({name: name.slice(0, 100), price, path: href});
  }
  return {kind: 'action_products', count: items.length, items: items.slice(0, 20)};
})()
""")


def extract_but(js_eval):
    return js_eval(r"""
(async () => {
  const realPrice = () => !!document.querySelector('[class*="product-card__price"]:not([class*="skeleton"]), [class*="price"]:not([class*="skeleton"])');
  for (let i = 0; i < 12 && !realPrice(); i++) await new Promise(r => setTimeout(r, 2000));
  window.scrollBy(0, 1500);
  await new Promise(r => setTimeout(r, 1200));
  const links = [...document.querySelectorAll('a[href*="/produits/"], a[href*="product"], a[href*="index-p"]')].slice(0, 80);
  const seen = new Set(); const items = [];
  for (const a of links) {
    const href = a.getAttribute('href').split('?')[0];
    if (!href || seen.has(href) || !/\/produits\/|product/i.test(href)) continue;
    seen.add(href);
    let card = a;
    for (let i = 0; i < 5; i++) {
      const p = card.parentElement;
      if (p && p.querySelectorAll('a[href]').length <= 3) card = p; else break;
    }
    const name = (a.getAttribute('title') || a.getAttribute('aria-label') || card.querySelector('h2, h3, [class*="title"], [class*="name"]')?.textContent || '').trim().replace(/\s+/g, ' ');
    const priceEl = card.querySelector('[class*="price"]:not([class*="skeleton"])');
    const price = priceEl?.textContent?.trim().replace(/\s+/g, ' ') || '';
    const promo = (price.match(/-\d+%/) || [''])[0];
    items.push({name: name.slice(0, 100), price: price.slice(0, 40), promo, path: href});
  }
  return {kind: 'but_products', count: items.length, items: items.slice(0, 20)};
})()
""")


def extract_conforama(js_eval):
    return js_eval(r"""
(async () => {
  // let price hydration start before scrolling: poll for the first numeric price
  const priceReady = () => { const t = document.querySelector('article[data-component-id="product-tile"] .price'); return !!(t && /\d/.test(t.textContent || '')); };
  for (let i = 0; i < 6 && !priceReady(); i++) await new Promise(r => setTimeout(r, 1300));
  // prices hydrate per-tile via intersection observer: scroll in waves, merge results
  const grab = () => {
    const out = {};
    for (const t of document.querySelectorAll('article[data-component-id="product-tile"]')) {
      const a = t.querySelector('a[href*="/p/"]');
      if (!a) continue;
      const path = new URL(a.href).pathname;
      const priceTxt = t.querySelector('.price')?.textContent?.replace(/\s+/g, ' ').trim() || '';
      const m = priceTxt.match(/Vendu\s*([\d\s]+,?\d*)\s*€/) || priceTxt.match(/^([\d\s]+,?\d*)\s*€/);      const name = (t.getAttribute('aria-label') || '').replace(/^Voir le produit\s*/i, '').replace(/<[^>]+>/g, '').trim();
      if (!out[path] || (m && !out[path].price))
        out[path] = {id: t.getAttribute('data-objectid') || '', name: name.slice(0, 120),
                     price: m ? m[1].trim() : (out[path] ? out[path].price : ''), path};
    }
    return out;
  };
  let acc = {};
  for (let round = 0; round < 5; round++) {
    acc = Object.assign(acc, grab());
    window.scrollBy(0, 1600);
    await new Promise(r => setTimeout(r, 1600));
  }
  acc = Object.assign(acc, grab());
  const items = Object.values(acc).slice(0, 60);
  return {kind: 'conforama_products', count: items.length, items: items.slice(0, 20)};
})()
""")


def extract_manomano(js_eval):
    return js_eval(r"""
(async () => {
  // CAUTION: ManoMano virtualizes its grid — scrolling REMOVES cards from the DOM,
  // and cards dehydrate over time. Parse IMMEDIATELY (no scroll, no long poll);
  // only wait if the grid itself hasn't mounted yet.
  const hasGrid = () => document.querySelectorAll('a[href^="/p/"]').length > 5;
  for (let i = 0; i < 10 && !hasGrid(); i++) await new Promise(r => setTimeout(r, 1500));
  const anchors = [...document.querySelectorAll('a[href^="/p/"]')].slice(0, 80);
  const raw = [];
  for (const a of anchors) {
    const href = a.getAttribute('href').split('?')[0];
    let card = a;
    for (let i = 0; i < 6; i++) { const p = card.parentElement; if (p && [...p.querySelectorAll('a[href^="/p/"]')].length <= 2) card = p; else break; }
    const name = (a.getAttribute('aria-label') || a.textContent || card.querySelector('[class*="title" i], h3, h2')?.textContent || '').trim().replace(/\s+/g, ' ');
    const lines = (card.innerText || '').split('\\n').map(s => s.trim());
    const price = lines.find(l => /^\d[\d\s]*,\d{2}\s*€$/.test(l)) || '';
    const rating = lines.find(l => /^\d[.,]\d$/.test(l)) || '';
    const reviews = lines.find(l => /\(\d+\)/.test(l)) || '';
    if (name.length > 8 && price) raw.push({name: name.slice(0, 120), price, rating, reviews, path: href});
  }
  // dedup AFTER the price filter: each product has several anchors (image/title),
  // only the title anchor carries the price — deduping first would keep the image one
  const seen = new Set(); const items = [];
  for (const it of raw) { if (!seen.has(it.path)) { seen.add(it.path); items.push(it); } }
  return {kind: 'manomano_products', count: items.length, items: items.slice(0, 20)};
})()
""")


def extract_vidaxl(js_eval):
    return js_eval(r"""
(async () => {
  for (let i = 0; i < 3; i++) { window.scrollBy(0, 1400); await new Promise(r => setTimeout(r, 700)); }
  const tiles = [...document.querySelectorAll('.product-tile')].slice(0, 60);
  const items = tiles.map(t => {
    const a = t.querySelector('a[href*="/e/"]');
    const name = t.querySelector('img[alt]')?.getAttribute('alt') || (a?.textContent || '').trim();
    const priceRaw = t.querySelector('[class*="price" i]')?.textContent?.replace(/\s+/g, ' ').trim() || '';
    const m = priceRaw.match(/(\d+)\s+(\d+)\s*€/);
    const price = m ? m[1] + ',' + m[2] + ' €' : (priceRaw.match(/[\d.,]+\s*€/) || [''])[0];
    return {pid: t.getAttribute('data-pid') || '', name: name.replace(/\s+/g, ' ').slice(0, 120), price,
            path: a ? new URL(a.href, location.origin).pathname : ''};
  }).filter(x => x.path && x.name);
  const seen = new Set(); const uniq = [];
  for (const it of items) { if (!seen.has(it.path)) { seen.add(it.path); uniq.push(it); } }
  return {kind: 'vidaxl_products', count: uniq.length, items: uniq.slice(0, 20)};
})()
""")


def extract_miliboo(js_eval):
    return js_eval(r"""
(() => {
  const cards = [...document.querySelectorAll('.product-teaser, .card.product')].slice(0, 60);
  const items = cards.map(c => {
    const a = c.querySelector('a[href*=".html"]');
    const name = c.querySelector('[class*="title" i], .card-title, h3, h2')?.textContent
      || (a?.getAttribute('title') || a?.textContent || '');
    const price = c.querySelector('.product-price')?.textContent?.trim().replace(/\s+/g, ' ').slice(0, 30) || '';
    return {name: name.trim().replace(/\s+/g, ' ').slice(0, 120), price,
            path: a ? new URL(a.href, location.origin).pathname : ''};
  }).filter(x => x.path && x.name && x.price);
  const seen = new Set(); const uniq = [];
  for (const it of items) { if (!seen.has(it.path)) { seen.add(it.path); uniq.push(it); } }
  return {kind: 'miliboo_products', count: uniq.length, items: uniq.slice(0, 20)};
})()
""")


def extract_kavehome(js_eval):
    return js_eval(r"""
(async () => {
  for (let i = 0; i < 4; i++) { window.scrollBy(0, 1600); await new Promise(r => setTimeout(r, 800)); }
  const links = [...new Set([...document.querySelectorAll('a[href*="/p/"]')].map(a => a.getAttribute('href').split('?')[0]))];
  const items = links.slice(0, 60).map(href => {
    const a = document.querySelector('a[href="' + href + '"]');
    const card = a?.closest('[class*="productBox"]') || a?.closest('article, li, div');
    const name = (a?.getAttribute('aria-label') || a?.getAttribute('title') || card?.querySelector('h2, h3, [class*="title"]')?.textContent || a?.textContent || '').trim().replace(/\s+/g, ' ');
    const price = card?.querySelector('[class*="price" i]')?.textContent?.trim().replace(/\s+/g, ' ').slice(0, 30) || '';
    return {name: name.slice(0, 120), price, path: href};
  }).filter(x => x.name.length > 5);
  return {kind: 'kavehome_products', count: items.length, items: items.slice(0, 20)};
})()
""")


def extract_theredarchive(js_eval):
    """TheRedArchive.com — subreddit archive. Detects page type by URL:
    - /search?s=<q>  -> search results (NOTE: param is `s`, `q` renders an empty landing page)
    - /r/<sub>/<slug>.<id> -> thread (OP + comments from JSON-LD, sorted by upvotes)
    - /r/<sub>       -> subreddit index (Top Posts table)
    All pages are server-rendered; no walls, no login."""
    return js_eval(r"""
(() => {
  const path = location.pathname;
  const clean = (t) => (t || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  // ---- thread page ----
  if (/^\/r\/[^/]+\/.+\.\d+/.test(path)) {
    const el = document.querySelector('script[type="application/ld+json"]');
    if (!el) return {kind: 'theredarchive_thread', error: 'no JSON-LD'};
    let raw = el.textContent.replace(/&(quot|amp|lt|gt|#39|apos);/g, s =>
      ({'&quot;':'"','&amp;':'&','&lt;':'<','&gt;':'>','&#39;':"'",'&apos;':"'"}[s]));
    let data;
    try { data = JSON.parse(raw); } catch (e) { return {kind: 'theredarchive_thread', error: 'json: ' + e.message}; }
    const nodes = Array.isArray(data) ? data : (data['@graph'] || [data]);
    const post = nodes.find(n => n && (n['@type'] === 'DiscussionForumPosting' || n['@type'] === 'Article'));
    if (!post) return {kind: 'theredarchive_thread', error: 'no posting node', types: nodes.map(n => n && n['@type'])};
    const comments = [];
    const walk = c => {
      if (Array.isArray(c)) { c.forEach(walk); return; }
      if (c && typeof c === 'object') {
        if (c['@type'] === 'Comment') comments.push(c);
        walk(c.comment || []);
      }
    };
    walk(post.comment || []);
    comments.sort((a, b) => (b.upvoteCount || 0) - (a.upvoteCount || 0));
    return {
      kind: 'theredarchive_thread',
      title: clean(post.headline || post.title || ''),
      author: (post.author || {}).name || '',
      score: post.upvoteCount,
      date: post.datePublished || '',
      op: clean(post.articleBody || post.text || '').slice(0, 1500),
      commentCount: comments.length,
      comments: comments.slice(0, 20).map(c => ({
        score: c.upvoteCount || 0,
        author: (c.author || {}).name || '',
        date: c.datePublished || '',
        text: clean(c.text).slice(0, 800)
      }))
    };
  }
  // ---- search page ----
  if (path === '/search' || path.startsWith('/search/')) {
    const seen = new Set(); const items = [];
    for (const a of document.querySelectorAll('a[href*="/r/"]')) {
      const href = (a.getAttribute('href') || '').split('?')[0];
      const m = href.match(/^\/r\/([^/]+)\/(.+)\.(\d+)$/);
      if (!m) continue;
      const title = clean(a.textContent);
      if (title.length < 8) continue;
      if (seen.has(href)) continue;
      seen.add(href);
      items.push({sub: m[1], title: title.slice(0, 200), path: href});
    }
    return {kind: 'theredarchive_search', count: items.length, items: items.slice(0, 30)};
  }
  // ---- subreddit index ----
  if (/^\/r\/[^/]+\/?$/.test(path)) {
    const seen = new Set(); const items = [];
    for (const a of document.querySelectorAll('a[href*="/r/"]')) {
      const href = (a.getAttribute('href') || '').split('?')[0];
      if (!/^\/r\/[^/]+\/.+\.\d+$/.test(href)) continue;
      const title = clean(a.textContent);
      if (title.length < 8 || seen.has(href)) continue;
      seen.add(href);
      items.push({title: title.slice(0, 200), path: href});
    }
    return {kind: 'theredarchive_index', subreddit: path.replace(/^\/r\//, '').replace(/\/$/, ''),
            count: items.length, items: items.slice(0, 30)};
  }
  return {kind: 'theredarchive_other', path};
})()
""")


SITE_MATCH = [
    ("facebook", re.compile(r"facebook\.com/")),
    ("instagram", re.compile(r"instagram\.com/")),
    ("tiktok", re.compile(r"tiktok\.com/")),
    ("ikea", re.compile(r"ikea\.com/")),
    ("amazon", re.compile(r"amazon\.[a-z.]+/")),
    ("aliexpress", re.compile(r"aliexpress\.com/")),
    ("action", re.compile(r"action\.com/")),
    ("but", re.compile(r"but\.fr/")),
    ("conforama", re.compile(r"conforama\.fr/")),
    ("manomano", re.compile(r"manomano\.[a-z.]+/")),
    ("vidaxl", re.compile(r"vidaxl\.[a-z.]+/")),
    ("miliboo", re.compile(r"miliboo\.com/")),
    ("kavehome", re.compile(r"kavehome\.com/")),
    ("theredarchive", re.compile(r"theredarchive\.com/")),
]

EXTRACTORS = {
    "facebook": extract_facebook,
    "instagram": extract_instagram,
    "tiktok": extract_tiktok,
    "ikea": extract_ikea,
    "amazon": extract_amazon,
    "aliexpress": extract_aliexpress,
    "action": extract_action,
    "but": extract_but,
    "conforama": extract_conforama,
    "manomano": extract_manomano,
    "vidaxl": extract_vidaxl,
    "miliboo": extract_miliboo,
    "kavehome": extract_kavehome,
    "theredarchive": extract_theredarchive,
}


def site_for(url):
    for name, rx in SITE_MATCH:
        if rx.search(url):
            return name
    return "none"


# ---------- commands ----------

def cmd_health():
    out = {}
    try:
        out["api"] = http_json(f"{API}/health", timeout=5)
    except Exception as e:
        out["api"] = f"DOWN: {e}"
    try:
        v = http_json(f"{CDP_HTTP}/json/version", timeout=5)
        out["cdp_browser"] = v.get("Browser")
        out["cdp"] = "ok"
    except Exception as e:
        out["cdp"] = f"DOWN: {e}"
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if isinstance(out.get("api"), dict) and out.get("cdp") == "ok" else 1


def cmd_fetch(url, site="auto", out_file=None, retry_wall=False, nav_timeout=DEFAULT_TIMEOUT, settle=3.0):
    if site == "auto":
        site = site_for(url)
    # sites needing longer settle for lazy hydration
    if settle == 3.0 and site == "but":
        settle = 12.0
    elif settle == 3.0 and site in ("conforama", "aliexpress", "manomano", "vidaxl", "miliboo", "kavehome"):
        settle = 8.0
    cdp = connect()
    result = {"url": url, "site": site}
    try:
        s, tid = navigate(cdp, url, nav_timeout=nav_timeout, settle=settle)
        state = page_state(cdp, s)
        walls = detect_walls(state.get("title"), state.get("text"), state.get("html"))
        # Cloudflare-style interstitial: the non-interactive challenge often
        # self-resolves in 5-15s (no reload needed) — poll patiently first
        if retry_wall and any(w in ("cloudflare_challenge", "datadome") for w in walls):
            for _ in range(5):
                time.sleep(3)
                state = page_state(cdp, s)
                walls = detect_walls(state.get("title"), state.get("text"), state.get("html"))
                if not any(w in ("cloudflare_challenge", "datadome") for w in walls):
                    break
            if any(w in ("cloudflare_challenge", "datadome") for w in walls):
                cdp.call("Page.reload", {}, sessionId=s, timeout=30)
                time.sleep(6)
                state = page_state(cdp, s)
                walls = detect_walls(state.get("title"), state.get("text"), state.get("html"))
            result["retried"] = True
        result["final_url"] = state.get("url")
        result["title"] = state.get("title")
        result["walls"] = walls
        result["text"] = (state.get("text") or "")[:6500]
        blocked = any(w in ("cloudflare_challenge", "datadome", "blocked") for w in walls)
        result["verdict"] = "blocked" if blocked else "ok"
        if not blocked and site in EXTRACTORS:
            def js_eval(js):
                try:
                    return cdp.call("Runtime.evaluate", {"expression": js, "returnByValue": True,
                                                        "awaitPromise": True},
                                    sessionId=s, timeout=45)["result"].get("value")
                except Exception as e:
                    return {"error": str(e)[:150]}
            result["data"] = EXTRACTORS[site](js_eval)
        try:
            cdp.call("Target.closeTarget", {"targetId": tid}, timeout=10)
        except Exception:
            pass
    except Exception as e:
        result["verdict"] = "error"
        result["error"] = str(e)[:200]
    finally:
        cdp.close()
    payload = json.dumps(result, ensure_ascii=False, indent=1)
    if out_file:
        with open(out_file, "w") as f:
            f.write(payload)
        print(json.dumps({"out": out_file, "verdict": result.get("verdict"), "walls": result.get("walls")}))
    else:
        print(payload)
    return 0


def cmd_shot(url, out_path, nav_timeout=DEFAULT_TIMEOUT):
    cdp = connect()
    try:
        s, tid = navigate(cdp, url, nav_timeout=nav_timeout)
        b64 = cdp.call("Page.captureScreenshot", {"format": "jpeg", "quality": 60}, sessionId=s, timeout=20)["data"]
        data = base64.b64decode(b64)
        with open(out_path, "wb") as f:
            f.write(data)
        try:
            cdp.call("Target.closeTarget", {"targetId": tid}, timeout=10)
        except Exception:
            pass
        print(json.dumps({"out": out_path, "bytes": len(data)}))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e)[:200]}))
        return 1
    finally:
        cdp.close()


def cmd_transcript(url, out_file=None):
    """TikTok video -> transcript via hydration JSON subtitleInfos -> WebVTT."""
    if "tiktok.com" not in url:
        print(json.dumps({"error": "transcript currently supports tiktok.com video URLs only"}))
        return 1
    cdp = connect()
    try:
        s, tid = navigate(cdp, url, nav_timeout=45, settle=6.0)
        def js(expr, await_promise=False):
            return cdp.call("Runtime.evaluate",
                            {"expression": expr, "returnByValue": True, "awaitPromise": await_promise},
                            sessionId=s, timeout=30)["result"].get("value")
        info = js("""
(() => {
  const el = document.getElementById('__UNIVERSAL_DATA_FOR_REHYDRATION__');
  if (!el) return {err: 'no hydration node'};
  const data = JSON.parse(el.textContent);
  const detail = (data['__DEFAULT_SCOPE__'] || {})['webapp.video-detail'];
  if (!detail) return {err: 'no video-detail scope'};
  if (detail.statusCode && detail.statusCode !== 0) return {err: 'status ' + detail.statusCode + ' ' + (detail.statusMsg || '')};
  const item = detail.itemInfo && detail.itemInfo.itemStruct;
  if (!item) return {err: 'no itemStruct'};
  const subs = (item.video && item.video.subtitleInfos) || [];
  return {desc: item.desc || '', author: item.author ? item.author.uniqueId : '',
          duration: item.video ? item.video.duration : null,
          subs: subs.map(x => ({lang: x.LanguageCodeName, source: x.Source, url: x.Url}))};
})()
""")
        if not info or info.get("err"):
            print(json.dumps({"url": url, "verdict": "error", "error": (info or {}).get("err", "no data")}))
            return 1
        result = {"url": url, "verdict": "ok", "author": info.get("author"),
                  "desc": (info.get("desc") or "")[:200], "duration_s": info.get("duration"),
                  "subtitle_tracks": [(x["lang"], x["source"]) for x in info.get("subs", [])]}
        if not info.get("subs"):
            result["transcript"] = None
            result["note"] = "no ASR subtitle track on this video (TikTok only adds them when ASR ran; ~1 in 5 videos)"
        else:
            vtt = next((x for x in info["subs"] if (x.get("url") or "").find("webvtt") >= 0 or x.get("source") == "ASR"),
                       info["subs"][0])
            vtt_url = vtt["url"].replace("\u002F", "/").replace("'", "\\'")
            body = js(f"fetch('{vtt_url}').then(r => r.text()).catch(e => 'FETCH_ERR: ' + e.message)",
                      await_promise=True) or ""
            if body.startswith("FETCH_ERR"):
                result["verdict"] = "error"
                result["error"] = body[:150]
            else:
                # WebVTT -> plain text lines
                lines = []
                for ln in body.splitlines():
                    ln = ln.strip()
                    if (not ln or ln == "WEBVTT" or "-->" in ln
                            or ln.startswith(("Kind:", "Language:", "NOTE"))
                            or ln.isdigit()):  # cue identifier lines
                        continue
                    lines.append(ln)
                # dedupe consecutive repeats
                text = []
                for ln in lines:
                    if not text or text[-1] != ln:
                        text.append(ln)
                result["transcript_lang"] = vtt["lang"]
                result["transcript_source"] = vtt["source"]
                result["transcript"] = " ".join(text)[:4000]
                result["vtt_raw_chars"] = len(body)
        try:
            cdp.call("Target.closeTarget", {"targetId": tid}, timeout=10)
        except Exception:
            pass
        payload = json.dumps(result, ensure_ascii=False, indent=1)
        if out_file:
            with open(out_file, "w") as f:
                f.write(payload)
            print(json.dumps({"out": out_file, "verdict": result.get("verdict"), "lang": result.get("transcript_lang")}))
        else:
            print(payload)
        return 0
    finally:
        cdp.close()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "health":
        return cmd_health()
    if cmd == "fetch":
        url = sys.argv[2]
        site, out_file, retry_wall, nav_timeout, settle = "auto", None, False, DEFAULT_TIMEOUT, 3.0
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--site":
                site = args[i + 1]; i += 2
            elif args[i] == "--out":
                out_file = args[i + 1]; i += 2
            elif args[i] == "--retry-wall":
                retry_wall = True; i += 1
            elif args[i] == "--timeout":
                nav_timeout = int(args[i + 1]); i += 2
            elif args[i] == "--settle":
                settle = float(args[i + 1]); i += 2
            else:
                i += 1
        return cmd_fetch(url, site=site, out_file=out_file, retry_wall=retry_wall,
                         nav_timeout=nav_timeout, settle=settle)
    if cmd == "transcript":
        url = sys.argv[2]
        out_file = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--out" else None
        return cmd_transcript(url, out_file=out_file)
    if cmd == "shot":
        return cmd_shot(sys.argv[2], sys.argv[3])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
