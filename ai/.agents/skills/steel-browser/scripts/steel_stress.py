"""steel_stress.py — re-usable stress harness for the Steel browser.

Batches: fingerprint | batch1 (baseline) | batch2 (moderate) | batch3 (hard walls) | concurrency N
Results appended to steel-stress-results.jsonl in cwd.
Edit BATCH lists to suit the target site mix. Requires steel_cdp.py in same dir.

Usage: python steel_stress.py batch1   (or: fingerprint / batch2 / batch3 / concurrency 5)
"""
import json, time, sys, base64, threading
import urllib.request
import websocket

CDP_HTTP = "http://192.168.1.50:9223"
RESULTS = "steel-stress-results.jsonl"
NAV_TIMEOUT = 40

EXTRACT_JS = """
(() => {
  const nav = performance.getEntriesByType('navigation')[0] || {};
  return {
    url: location.href,
    title: document.title,
    readyState: document.readyState,
    status: nav.responseStatus !== undefined ? nav.responseStatus : null,
    text: (document.body ? document.body.innerText : '').replace(/\\s+/g, ' ').slice(0, 1500),
    html: document.documentElement.outerHTML.slice(0, 40000),
    ua: navigator.userAgent
  };
})()
"""

WALLS = {
    "cloudflare_challenge": ["just a moment", "checking your browser", "cf-chl", "attention required! | cloudflare", "enable javascript and cookies to continue", "verify you are human", "un instant"],
    "datadome": ["datadome", "captcha-delivery.com"],
    "perimeterx": ["press & hold", "perimeterx", "px-captcha"],
    "akamai": ["reference #"],
    "recaptcha": ["g-recaptcha", "are you a robot", "unusual traffic", "prove you are human", "security check"],
    "hcaptcha": ["hcaptcha.com", "h-captcha"],
    "login_wall": ["sign in to continue", "log in to continue", "authwall", "sign up to continue", "login to continue", "keep up with what's happening"],
    "geo_block": ["not available in your country", "not available in your region"],
    "blocked_403": ["access denied", "you don't have permission to access", "request blocked", "403 forbidden"],
    "consent_wall": ["we value your privacy", "cookie preferences", "manage cookies", "accept all cookies"],
    "paywall": ["subscribe to continue", "subscription required", "already a subscriber"],
}
# markers that only count when visible in title/body text (not buried in script tags)
TEXT_ONLY = {"recaptcha", "hcaptcha", "datadome", "perimeterx", "akamai"}

BATCH1 = ["https://example.com", "https://www.wikipedia.org", "https://github.com",
          "https://stackoverflow.com", "https://news.ycombinator.com", "https://www.reddit.com"]
BATCH2 = ["https://www.bing.com/search?q=test", "https://duckduckgo.com/?q=test", "https://www.amazon.com",
          "https://www.ebay.com", "https://www.cnn.com", "https://www.medium.com"]
BATCH3 = ["https://www.x.com", "https://www.linkedin.com", "https://www.facebook.com",
          "https://www.instagram.com", "https://www.tiktok.com/explore",
          "https://www.ikea.com/fr/fr/search/?q=bureau", "https://www.cloudflare.com",
          "https://arstechnica.com", "https://www.nytimes.com"]


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


def detect_walls(d):
    title_text = " ".join([(d.get("title") or "").lower(), (d.get("text") or "").lower()[:800]])
    blob = title_text + " " + (d.get("html") or "").lower()[:20000]
    hits = []
    for wall, markers in WALLS.items():
        hay = title_text if wall in TEXT_ONLY else blob
        if any(mk in hay for mk in markers):
            hits.append(wall)
    return hits


def judge(d, err=None):
    if err:
        if "timeout" in str(err).lower():
            return "timeout", [f"nav_error:{str(err)[:80]}"]
        return "error", [f"nav_error:{str(err)[:120]}"]
    status = d.get("status")
    hits = detect_walls(d)
    title = (d.get("title") or "").strip()
    text_len = len(d.get("text") or "")
    hard = {"cloudflare_challenge", "datadome", "perimeterx", "recaptcha", "hcaptcha", "blocked_403", "geo_block"}
    if status and status >= 400:
        return "hard_wall", hits + [f"http_{status}"]
    if any(h in hard for h in hits):
        return "hard_wall", hits
    if {"login_wall", "consent_wall", "paywall"} & set(hits):
        return "soft_wall", hits
    if not title and text_len < 60:
        return "blank", hits
    if text_len > 200:
        return "ok", hits
    return "suspicious", hits


def test_site(cdp, url, nav_timeout=NAV_TIMEOUT):
    rec = {"url": url, "ts": time.strftime("%H:%M:%S")}
    target_id = None
    t0 = time.time()
    try:
        target_id = cdp.call("Target.createTarget", {"url": "about:blank"})["targetId"]
        sess = cdp.call("Target.attachToTarget", {"targetId": target_id, "flatten": True})["sessionId"]
        cdp.call("Page.enable", sessionId=sess)
        cdp.call("Page.navigate", {"url": url}, sessionId=sess)
        deadline = time.time() + nav_timeout
        while time.time() < deadline:
            time.sleep(1.0)
            try:
                r = cdp.call("Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True},
                             sessionId=sess, timeout=8)
                if r.get("result", {}).get("value", "") == "complete":
                    break
            except Exception:
                pass
        time.sleep(2.0)
        r = cdp.call("Runtime.evaluate", {"expression": EXTRACT_JS, "returnByValue": True},
                     sessionId=sess, timeout=20)
        d = r.get("result", {}).get("value") or {}
        verdict, hits = judge(d)
        shot = 0
        try:
            shot_b64 = cdp.call("Page.captureScreenshot", {"format": "jpeg", "quality": 40}, sessionId=sess, timeout=15)["data"]
            shot = len(base64.b64decode(shot_b64))
        except Exception:
            pass
        rec.update({"verdict": verdict, "walls": hits, "final_url": d.get("url"),
                    "title": (d.get("title") or "")[:80], "http_status": d.get("status"),
                    "nav_ms": int((time.time() - t0) * 1000), "text_len": len(d.get("text") or ""),
                    "screenshot_bytes": shot})
    except Exception as e:
        verdict, hits = judge({}, err=str(e))
        rec.update({"verdict": verdict, "walls": hits, "nav_ms": int((time.time() - t0) * 1000)})
    finally:
        if target_id:
            try:
                cdp.call("Target.closeTarget", {"targetId": target_id}, timeout=10)
            except Exception:
                pass
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(f"{rec.get('verdict','?').upper():<10} {url[:48]:<48} {(rec.get('title') or '')[:38]:<38} {rec.get('nav_ms',0)}ms walls={','.join(rec.get('walls', [])[:3])}", flush=True)
    return rec


def connect():
    return CDP(http_json(f"{CDP_HTTP}/json/version")["webSocketDebuggerUrl"])


def run_concurrency(n=5):
    sites = ["https://example.com", "https://www.wikipedia.org", "https://github.com",
             "https://news.ycombinator.com", "https://stackoverflow.com"]
    urls = [sites[i % len(sites)] for i in range(n)]
    results = [None] * n

    def worker(i):
        try:
            cdp = connect()
            results[i] = test_site(cdp, urls[i], nav_timeout=45)
            cdp.close()
        except Exception as e:
            results[i] = {"url": urls[i], "verdict": "error", "walls": [f"thread:{e}"[:100]]}
            print(f"ERROR      {urls[i]}: {e}", flush=True)

    t0 = time.time()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    ok = sum(1 for r in results if r and r.get("verdict") == "ok")
    print(f"CONCURRENCY: {ok}/{n} ok in {time.time()-t0:.0f}s")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "batch1"
    if mode == "concurrency":
        run_concurrency(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
        return
    sites = {"batch1": BATCH1, "batch2": BATCH2, "batch3": BATCH3}.get(mode)
    if not sites:
        print(__doc__)
        return 2
    cdp = connect()
    for url in sites:
        test_site(cdp, url)
    cdp.close()
    print(f"{mode} DONE")


if __name__ == "__main__":
    main()
