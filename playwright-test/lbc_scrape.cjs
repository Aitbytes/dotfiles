// Leboncoin scraper — Playwright/Chromium, capture API adfinder + DOM
const { chromium } = require('playwright');
const fs = require('fs');

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36';

const QUERIES = [
  { tag: 'sommier_140x200', url: 'https://www.leboncoin.fr/recherche?text=sommier%20140x200&category=10&locations=Toulouse__43.6044_1.4442_10000' },
  { tag: 'sommier_140x190', url: 'https://www.leboncoin.fr/recherche?text=sommier%20140x190&category=10&locations=Toulouse__43.6044_1.4442_10000' },
];

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox', '--disable-dev-shm-usage'],
  });
  const ctx = await browser.newContext({
    userAgent: UA, locale: 'fr-FR', timezoneId: 'Europe/Paris',
    viewport: { width: 1440, height: 900 },
    extraHTTPHeaders: { 'Accept-Language': 'fr-FR,fr;q=0.9' },
  });
  await ctx.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['fr-FR', 'fr', 'en'] });
  });

  const apiHits = [];
  ctx.on('response', async (resp) => {
    const u = resp.url();
    if (/api\.leboncoin\.fr.*(adfinder|ads|search)/i.test(u) && resp.status() === 200) {
      try { const b = await resp.text(); if (b && b.length > 200 && b.startsWith('{')) apiHits.push({ url: u, body: b }); } catch {}
    }
  });

  const page = await ctx.newPage();
  // 1) page d'accueil pour cookies datadome
  try {
    await page.goto('https://www.leboncoin.fr/', { waitUntil: 'domcontentloaded', timeout: 45000 });
    for (let i = 0; i < 12; i++) {
      const inter = await page.evaluate(() => {
        const h = document.documentElement.innerHTML;
        return /captcha-delivery|ddv1|interstitial|Please enable JS/i.test(h);
      }).catch(() => false);
      if (!inter) break;
      await page.waitForTimeout(2500);
    }
    const title1 = await page.title().catch(() => '');
    console.log('HOME title:', title1.slice(0, 80));
  } catch (e) { console.log('HOME err', e.message.slice(0, 100)); }

  const results = {};
  for (const q of QUERIES) {
    try {
      await page.goto(q.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      let inter = true;
      for (let i = 0; i < 10; i++) {
        inter = await page.evaluate(() => /captcha-delivery|ddv1|interstitial|Please enable JS/i.test(document.documentElement.innerHTML)).catch(() => false);
        if (!inter) break;
        await page.waitForTimeout(2500);
      }
      await page.waitForTimeout(3000);
      await page.mouse.wheel(0, 1500).catch(() => {});
      await page.waitForTimeout(2000);
      const cards = await page.evaluate(() => {
        const out = [];
        document.querySelectorAll('a[href*="/ad/"]').forEach(a => {
          out.push({ href: a.href, text: (a.getAttribute('title') || a.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 300) });
        });
        return out;
      }).catch(() => []);
      results[q.tag] = {
        resolvedUrl: page.url(),
        blocked: inter,
        nLinks: cards.length,
        sample: cards.slice(0, 12),
      };
      console.log(`QUERY ${q.tag}: url=${page.url().slice(0, 120)} blocked=${inter} links=${cards.length}`);
    } catch (e) { console.log(`QUERY ${q.tag} err:`, e.message.slice(0, 120)); }
    await page.waitForTimeout(2500 + Math.random() * 2000);
  }
  fs.writeFileSync('/tmp/lbc_api_hits.json', JSON.stringify(apiHits, null, 1));
  fs.writeFileSync('/tmp/lbc_dom.json', JSON.stringify(results, null, 1));
  await ctx.storageState({ path: '/tmp/lbc_state.json' }).catch(() => {});
  await browser.close();
})();
