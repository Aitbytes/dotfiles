# Execution Budgets — editing master (P3)

> This file is the EDITING MASTER for humans. The canonical block below is pasted
> IDENTICALLY into: retail-research, social-marketplace-research, research-assistant,
> playwright-browser, youtube-research, reddit-research (standby; block present for
> reactivation). Drift-lint: agent-shared/drift_lint.py (byte-equality against this file's
> "CANONICAL BLOCK" section).

## Derivation (evidence, not vibes — recorded 2026-10-13)

| Tool | Observed legitimate max (session evidence) | Source | Cap |
|---|---|---|---|
| steel_cdp.py fetch | 40 fetches/task, 39 unique URLs, ~1 retry (canapé subagent 2026-08-21 — broad multi-retailer coverage, NOT a retry loop) | `sessions/--tmp--/01a0248e.../26180ed5` | **≤40/task, ≤2 attempts/URL** |
| youtube.py transcript | pre-budget era showed 58× (wasteful looping); youtube-research's own gating rule: 5 (light) / 8 (synthesis) candidates | youtube-research SKILL.md | **≤8 attempts/task** |
| youtube.py search | 36-48× in multi-topic subagents (2026-06-19 era, pre-budget); single-query discipline = ~12 | sessions 01a1320d-era | **≤12/task** |
| playwright-cli interactions | all-time totals: 106 snapshots / 53 opens / 30 clicks — per-task legit ~8-12 (vinted multi-page flows) | history aggregate | **≤20/task combined** |
| browser-use calls | 99× in one session = deviant outlier; legit flows (Gmail sign-in playbook) ~15-25 | steel-browser SKILL.md playbook | **≤30/task** |
| static fetches (curl/web_scraper/lbc_fetch) | lbc_fetch does 3 attempts/URL internally; typical tasks ≤10 URLs | design | **≤12 URLs, ≤3 attempts/URL** |
| vault/API scripts (fda_510k, patent_search, hcpcs, startup_data, eudamed) | typical ≤5 queries; 10 = generous headroom | usage history | **≤10/task** |

Rule: a cap hit means STOP that tool, log it in the Execution Audit, continue with other
evidence or report the gap. Caps are ceilings on waste, not targets to reach.

## CANONICAL BLOCK (paste-identical into the five executor skills)

```markdown
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
```

## Execution Audit block (retail & social — paste into their output formats)

```markdown
### Execution Audit
- Tool attempts: steel N, youtube N, playwright N, static N, api N
- Budget hits: [tool + cap] or none
- Walls hit: [site — wall_type — URL] or none
- Proposed sites.json rows: [site | status | wall_type | date] or none
- Gaps: [what wasn't covered and why]
```
