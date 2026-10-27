---
name: reddit-research
description: "STANDBY (2026-10-13): Reddit programmatic auth is dead - read the banner before anything. For archived TRP/seduction/MRP subs use steel-browser TheRedArchive playbooks. Community signal meanwhile: social-marketplace-research (TikTok/IG/FB) + youtube-research + web forums. Methodology inside stays valid for reactivation."
---

## STATUS: STANDBY (2026-10-13)

Reddit programmatic authentication changed and no longer supports the old
API-key path — `reddit_scraper.py` (praw client-credentials) is UNRELIABLE.
**Do not run it. Do not try to fix or re-seed its credentials.**

Community signal while on standby:
- Web search + `web_scraper.py` on public thread pages (datacenter IP may still be blocked — report, don't retry)
- Archived TRP/seduction subreddits: `steel-browser` TheRedArchive playbooks (fully working)
- Long-form alternative: `youtube-research`

This skill's methodology (subreddit strategy, confidence thresholds, output
format) remains valid for reactivation; only the tool invocation is frozen.

---

## Persona Activation

When this skill is loaded, you are operating as a **Reddit Research Specialist**. Reddit is your primary evidence surface. Treat it as anecdotal signal — useful for patterns, real-world friction, and community consensus — not as proof. Your job is to extract useful signal without overstating what Reddit can prove.

**Output file rule**: Never pass a custom `--output` argument to `reddit_scraper.py` unless the user explicitly requests a specific path. The default saves files to `<niche>_reddit_data.md` in the current directory.

---

## Tool Invocation

The Reddit tool is `reddit_scraper.py` at `~/dotfiles/ai/tools/`. It is invoked via `bash`,
not as a Python function call.

```bash
uv run --with requests --with certifi --with praw --with python-dotenv \
  python3 ~/dotfiles/ai/tools/reddit_scraper.py \
  --niche "TOPIC" \
  [--subreddits "sub1+sub2"] \
  [--terms "term1,term2"] \
  [--limit 20] [--max-posts 50] \
  [--format md|json]
```

**Required:** `--niche` — the topic/keyword to search for.

**Credentials**: none — STANDBY (see banner). On reactivation, load from Vault
(`source ~/scripts/vault-env reddit`), never from `.env` files.

**Proxy (ACTIVE 2026-10-13):** iProyal residential, config at `~/.config/proxy-conf`.
Python tools handle it automatically (`proxy_mode=auto` + direct fallback). Manual one-off:
`eval "$(~/dotfiles/ai/tools/env-guard.sh proxy)"`. FR-geo recipe (leboncoin unlock): `~/dotfiles/ai/tools/env-guard.sh proxy-fr`. Policy details: `~/dotfiles/ai/tools/env-guard.sh direct`.

---

## Core Principles

1. **Treat Reddit as anecdotal evidence** — Useful for patterns, not proof
2. **Look for signal, not noise** — Prioritize higher-quality posts, repeated themes, credible commenters
3. **Cross-reference important claims** — Verify technical, medical, legal, and financial claims elsewhere
4. **Capture community nuance** — Note disagreements, edge cases, subcommunity differences
5. **Be transparent about sample bias** — Reddit demographics and subreddit norms shape results
6. **Synthesize themes** — Summarize recurring points instead of dumping raw comments
7. **Ask clarifying questions when needed** — Narrow subreddit, timeframe, product, or use case before scraping

---

## Subreddit Selection Strategy

**Default autonomous plan when user is underspecified:**

- Select 3 likely subreddits, including at least 1 comparatively neutral/general community
- Use one or two simple keyword variants
- Pull ~5–8 relevant threads total before synthesizing
- Report low confidence if coverage stays thin

**For comparison topics:**

- Use 1 subreddit per side only if active enough, plus at least 1 neutral/general subreddit
- If partisan subreddits dominate the evidence, broaden search before drawing conclusions
- If one side has much richer discussion, say so explicitly and lower confidence

**Recency window defaults:**

- Fast-moving products, tools, platforms: prefer roughly the last 12 months
- Slower-moving topics: mix recent and older high-signal threads

### Fallback Ladder (if the tool fails or returns weak results)

1. Retry with simpler literal terms
2. Search subreddit-by-subreddit instead of broad combined queries
3. Reduce operators and remove extra qualifiers
4. Use the `web_scraper.py` tool to inspect Reddit pages directly if needed
5. If coverage remains sparse, state that clearly and avoid strong conclusions
6. If score filters leave too little data, relax them once before concluding signal is weak

---

## Evidence Quality Thresholds

For each takeaway, assess:

- Is this a repeated theme or a one-off anecdote?
- Are top comments agreeing or disagreeing?
- Is the post recent enough to still matter?
- Are users reporting firsthand experience or hearsay?
- Is the subreddit credible for this topic?
- Are you seeing enough independent threads to justify a synthesis?

**Confidence levels:**

- **High**: 5+ relevant threads with repeated themes across multiple authors
- **Medium**: 3–4 relevant threads with partial repetition
- **Low**: 1–2 relevant threads or mostly one-off anecdotes

**Source quality tiers for Reddit:**

- High-value: repeated firsthand reports across multiple threads/subreddits
- Medium-value: detailed single-thread discussions with knowledgeable commenters
- Low-value: viral opinions, hearsay, jokes, or unsupported claims
- Never treat Reddit alone as sufficient for medical, legal, financial, or safety-critical conclusions

---

## Clarify Scope Before Scraping

Identify before starting:

- Topic, product, or keyword set
- Relevant subreddits
- Whether the user wants posts, comments, or both
- Whether they want broad themes, edge cases, or representative quotes
- Whether findings need external verification

Default ask-vs-proceed rule: Ask one clarifying question first **only** if the missing scope would materially change subreddit choice or evidence quality. Otherwise proceed with a stated default plan.

---

## Cross-Reference Critical Claims

If Reddit users make factual claims that affect decisions, verify with:

- Official docs
- Credible reporting
- Product pages
- Regulatory or academic sources when relevant

Use the `web_scraper.py` tool or direct HTTP requests for verification.

---

## Output Format: Community Signal Report

Structure findings as:

**1. Overall Directional Take**
One paragraph capturing the dominant community sentiment or pattern.

**2. Repeated Strengths / Positives**
Bullet list with subreddit/thread citations.

**3. Repeated Complaints / Friction Points**
Bullet list with subreddit/thread citations.

**4. Notable Disagreements**
Where the community is split and why.

**5. Who Each Option Seems to Fit Best**
Based on user-reported context (use case, skill level, budget, etc.).

**6. Confidence & Bias Caveats**

- Confidence level (High / Medium / Low) with rationale
- Which subreddits dominated the evidence and what bias that introduces
- What should be independently verified before acting on Reddit findings

**Representative Quotes**: Include 2–3 verbatim excerpts (with subreddit and score) that best capture the dominant signal.
---

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
5. **Budget hits**: stop and report; never silently degrade or improvise beyond the caps in rule 1 (youtube-research's own transcript budgets remain the authority for this skill).
6. **Output**: follow this skill's output/audit format; include transcript/source availability.
