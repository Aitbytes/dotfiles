---
name: social-marketplace-research
description: "USE WHEN second-hand (leboncoin, vinted), local services/providers, 'ce que la communaute pense de Z', user opinions via TikTok/Instagram/Facebook, occasion vs neuf price floors. leboncoin via lbc_fetch.py (verified unlock), vinted via playwright-cli, social lookups via steel. NOT for new-in-box retail (retail-research) or general research (research-assistant)."
---

## STATUS 2026-10-13 (full rewrite — ghost tools purged)

Previous primaries (CrotDalam, clinstagram, vinted-pp-cli, vinted-cli, Apify, HikerAPI,
ScrapeClaw, TikTok-Content-Scraper) are DEAD or UNINSTALLABLE — verified one by one on
2026-10-13. This version routes exclusively through tools verified live:

| Capability | Tool | Verified |
|---|---|---|
| leboncoin search (35 ads/query, prices) | `agent-shared/scripts/lbc_fetch.py` (curl_cffi + FR proxy) | **2026-10-13** |
| vinted.fr search | `playwright-cli` (no login needed) | **2026-10-13** |
| TikTok transcripts / explore / profiles | steel-browser extractors | 2026-08-16 |
| Instagram public profiles | steel-browser extractor | 2026-08-16 |
| Facebook public pages | steel-browser extractor | 2026-08-16 |
| Site status for ANY site | `steel-browser/sites.json` | maintained |

**Platform SEARCH is lookup-only on TikTok/IG/FB** (no query search without login).
To find handles/pages: web search first (DDG/Bing via web_scraper.py), then look up.

## Load before acting

1. Consult `~/.agents/skills/steel-browser/sites.json` status for target sites (absolute path).
2. Proxy policy: `~/.opencode/tools/env-guard.sh` (`proxy`, `proxy-fr`, `direct`).
3. This skill's escalation contract at the bottom is BINDING.

## Platform playbooks

### 1. Leboncoin — second-hand goods & services (FRANCE #1, UNLOCKED)

Primary: `agent-shared/scripts/lbc_fetch.py` (absolute path `~/dotfiles/ai/agent-shared/scripts/lbc_fetch.py`):

```bash
uv run --with curl_cffi python3 ~/dotfiles/ai/agent-shared/scripts/lbc_fetch.py \
  "canape convertible" --out /tmp/lbc.json     # 35 ads: title, price, city, url, date
```

- DataDome bypassed via curl_cffi (Chrome TLS impersonation) + iProyal FR-residential proxy.
- ~30% of attempts 403 — the script retries automatically. If it fails 3×, report, don't improvise.
- **NEVER scrape leboncoin from the home IP** (playwright/chrome direct flags it with DataDome).
- Zero-auth fallback: DDG `site:leboncoin.fr/ad` via web_scraper.py.

When to use: any French second-hand search (furniture, electronics, services, price floors).

### 2. Vinted — second-hand fashion/electronics

Primary: playwright-cli (unset proxy vars first — see env-guard direct):

```bash
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
npx @playwright/cli open "https://www.vinted.fr/vetements?search_text=<QUERY>"
npx @playwright/cli snapshot
```

- Listings + prices render without login (verified 2026-10-13).
- Filters via URL: `?search_text=X&price_to=200&sort=price_lowest&catalog[]=...`
- Do NOT reinstall vinted CLIs — both verified dead (upstream deleted / API 404).

### 3. TikTok — unfiltered user reviews, demos (lookup-only)

Primary: steel-browser (`transcript <video-url>`, `/@user` profiles, `/explore`).

- Transcripts work on ~1 in 5 videos (ASR captions only) — check `subtitle_tracks`.
- Find video URLs: web search `site:tiktok.com @handle <topic>`, then look up.
- Fallback: playwright-cli snapshot of profile/search pages (3-4s settle).

### 4. Instagram — visual reviews, local businesses (lookup-only)

Primary: steel-browser profile extractor (`instagram.com/<handle>/` → stats, bio, ~8 post links).

- Reels transcripts need login — don't attempt.
- Fallback: playwright-cli.

### 5. Facebook Groups/Pages — community advice, local recommendations (lookup-only)

Primary: steel-browser public-page extractor (`facebook.com/<page>/` → posts, author, rough timestamps).

- Marketplace/Groups require login — don't attempt.
- Find group/page names via web search, then look up public content.
- Fallback: playwright-cli (mobile viewport 375×812 renders simpler DOM).

## Query-type routing

| Query type | Order |
|---|---|
| Second-hand product (France) | Leboncoin (lbc_fetch) → Vinted (playwright) → Facebook Marketplace (skip: login) |
| User reviews / opinions | TikTok + Instagram lookups → YouTube (youtube-research skill) → Amazon reviews + Trustpilot + forums (steel extractors / playwright) → Reddit (STANDBY — see reddit-research) |
| Local service provider | Facebook public pages → Leboncoin Services (lbc_fetch, category=14) → web search |
| Price benchmark (new) | steel retail extractors (amazon.fr, aliexpress…) — see sites.json |

## Cross-referencing

- Any claim affecting a decision: verify across ≥2 platforms before High confidence.
- Second-hand price floors: leboncoin (demande set market) vs vinted (fashion/electronics).
- Report platform coverage table (worked / blocked / skipped + reason) — template below.

## Output: Unified Research Report

```
## Unified Research Report: [Query]
### 1. Platform Coverage — table: platform | tool used | results | status
### 2. Key Findings — synthesized, not per-platform silos
### 3. Top Results — with direct URLs + platform attribution
### 4. Cross-Platform Consensus — agreements and disagreements
### 5. Red Flags & Warnings — scams, unreliable sellers, complaints
### 6. Gaps & Limitations — unavailable platforms, empty searches
### 7. Verdict & Next Steps — clear recommendation + confidence

### Execution Audit
- Tool attempts: steel N, youtube N, playwright N, static N, api N
- Budget hits: [tool + cap] or none
- Walls hit: [site — wall_type — URL] or none
- Proposed sites.json rows: [site | status | wall_type | date] or none
- Gaps: [what wasn't covered and why]

```

## Skills Integration

| Skill | Relationship |
|---|---|
| `retail-research` | New-in-box pricing benchmarks; faithful-advisor format |
| `steel-browser` | Extractors for TikTok/IG/FB + retail sites; sites.json authority |
| `playwright-browser` | Fallback browser automation (direct connection only) |
| `youtube-research` | Long-form review depth |
| `reddit-research` | **STANDBY** — programmatic auth dead; use TheRedArchive (steel) for archived subs |

Do not dispatch to these skills yourself — reference in your report; the orchestrator routes.

## Plan Visibility (anti-stall)

Before ANY tool call, output a short plan message: the platform order and what each step will produce, in 3-6 lines. The user must see
where this is going within the first minute or he aborts the run (observed 2026-10-13,
session 01a13724: 3 min of silent tool-checking = aborted). Do NOT pre-verify every tool
exists; skill paths are maintained and doctor.sh covers health. Dispatch.

## User Preferences (distilled — editing master: ~/dotfiles/ai/agent-shared/user-preferences.md)

- Budget: a euro figure is REQUIRED (range or cap). Stretch above it only with a durability/wear argument. NEVER assume he buys everything: deliver a PRIORITY ORDER so he can budget.
- Decision driver: quality/price ratio. Compare BOTH new and second-hand (columns: neuf min/max, occasion min/max); hygiene risk can disqualify second-hand (mattresses, soft furniture). Repair-before-rebuy for electronics.
- Logistics profile (decision criteria, not trivia): Toulouse 31000 center, 42m2, 3rd floor no elevator, NO car, 20min walk from IKEA. Delivery window is a hard criterion; click-and-collect valued; include local stores (IKEA, Normal) alongside online.
- Output: comparison TABLES with linked prices, ONE link per cell. Google Sheet as decision tool on request (checklist columns, checkbox totals, shopping list). Priority-ranked shopping list, never an exhaustive assumed purchase.
- Division of labor: agent researches and drafts, HE buys and sends. No autonomous purchases; Gmail = draft only.
- Coverage: wide samples, multi-channel (official + Amazon reviews + YouTube + TikTok/IG + forums). Practitioner feedback outranks official pages. IKEA is the price/quality anchor to beat; seek budget-friendly alternatives, quality confirmed by reviews.
- Locale: France/Europe is the DEFAULT context: FR sources first (service-public.fr, ameli.fr, UFC-Que Choisir, FR comparators), FR consumer norms; US/global generalizations need explicit justification.
- Language: follow the message's language (FR dominant since 2026-09, EN for tech deliverables). NO m-dashes in deliverables. Tables over prose. Numbered options; he answers by numbers.
- Every claim carries its source. Final deliverable = structured synthesis with confidence levels, disagreements called out, recommended next step. NEVER a notes dump.

## Execution Budgets (canonical block — master: ~/dotfiles/ai/agent-shared/budgets.md)

Per subagent task:
- steel_cdp.py fetch: ≤40 (≤2 attempts/URL; --retry-wall counts as attempt 2)
- youtube.py: ≤12 searches, ≤8 transcript attempts (on failure, probe the NEXT candidate)
- playwright-cli: ≤20 interactions total (open/goto/snapshot/click/fill/press)
- browser-use: ≤30 tool calls (orchestrator-dispatched only)
- static fetches (curl / web_scraper.py / lbc_fetch.py): ≤12 URLs, ≤3 attempts/URL
- vault/API scripts (fda_510k, patent_search, hcpcs_lookup, startup_data, eudamed_lookup): ≤10 queries

A budget hit = stop that tool, note it in the Execution Audit block, continue with other
evidence or report the gap. Never loop past caps. Never silently degrade.

---

## Escalation & Reporting Contract (canonical, BINDING)

1. **Blocked site**: if the orchestrator's dispatch prompt marks a target site blocked → report immediately, zero attempts. Otherwise → at most 1 attempt per ladder level (static HTTP → Steel → playwright-cli), max 4 total, then report URL + error and stop. browser-use is orchestrator-dispatched only.
2. **Never self-route**: do not load other skills or re-dispatch subagents. Report; the orchestrator re-dispatches.
3. **Every wall/block/403 ends in a proposed status row** for `~/.agents/skills/steel-browser/sites.json` (site, status, wall_type, date) included in your report.
4. **Credential failures**: report the registry id (runbooks: `agent-shared/runbooks/`), not just error text.
5. **Budget hits**: stop and report; never silently degrade or improvise beyond the caps in rule 1.
6. **Output**: follow the output contract above; always include the Platform Coverage table.
