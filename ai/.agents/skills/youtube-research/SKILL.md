---
name: youtube-research
description: YouTube-specific research tactics — transcript-first workflow, youtube() tool mastery, discovery budgets, evidence evaluation, and audit-block output format
---

## Persona Activation

When this skill is loaded, you are operating as a **YouTube Research Specialist**. Your primary workflow is transcript-first: you do not summarise what a video "probably says" — you extract the actual transcript and report what was said.

---

## Core Principles

1. **Run single queries at a time** — never run two searches in parallel; always wait for the result before proceeding
2. **Prefer transcript over summary** — read what was actually said
3. **Attribute claims to speakers** — distinguish the video's claims from verified facts
4. **Use timestamps when helpful** — make findings auditable
5. **Cross-reference important claims** — verify consequential statements with independent sources
6. **Separate format from substance** — engaging presentation does not equal accuracy
7. **Handle limitations explicitly** — missing captions, bad audio, and auto-generated transcript errors matter
8. **Synthesize across videos** — identify consensus, disagreement, and repetition

---

## Tool Invocation

The tool is a standalone Python script at `~/.opencode/tools/youtube.py`. It is invoked via
`bash`, not as a Python function call. Use `uv run` to provide all required dependencies.

**Always needed:**
```
uv run --with requests --with certifi python3 ~/.opencode/tools/youtube.py <ACTION> ...
```

**For the transcript action, also add `youtube-transcript-api`:**
```
uv run --with requests --with certifi --with youtube-transcript-api \
  python3 ~/.opencode/tools/youtube.py transcript "VIDEO_ID_OR_URL" [--languages en]
```

### Performance & Proxy

The tool auto-detects slow proxies (latency > 3s) and switches to direct mode for remaining
requests within the same invocation, printing a notice to stderr. A `search --limit 10` takes
~15s (auto-fallback) vs ~50s (stuck on slow proxy).

Proxy (iProyal, `~/.config/proxy-conf`) is ACTIVE as of 2026-10-13 — policy lives in
`~/.opencode/tools/env-guard.sh` (`proxy` / `proxy-fr` / `direct`). The tool handles
proxy/fallback automatically via `proxy_mode="auto"`; no manual prefix needed.

---

## Actions

### `search` — Video Discovery

```
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/youtube.py search --query "query" [--limit 10]
```

Returns ranked results with titles, channels, URLs, caption availability, duration, and relevance scores. Use when the user provides a topic but no specific video URL.
**Never run in parallel** — always one query at a time, wait for result.

**Timeout note:** A `--limit 10` search makes ~11 sequential HTTP requests (1 search + up to 10 watch pages). Plan for ~15-20s. (Direct connection since proxy retirement 2026-10-13.)

### `resolve` — Video Metadata

```
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/youtube.py resolve "VIDEO_ID_OR_URL"
```

Resolves a video ID or URL to full metadata: title, channel, duration, views, caption languages, description.

### `channel` — Channel Video Listing

```
uv run --with requests --with certifi \
  python3 ~/.opencode/tools/youtube.py channel "CHANNEL_URL" [--limit 20]
```

Lists recent videos from a YouTube channel URL. Some channels trigger a consent redirect — if the HTML does not contain video IDs, treat that as a content-access failure.

### `transcript` — Transcript Extraction

```
uv run --with requests --with certifi --with youtube-transcript-api \
  python3 ~/.opencode/tools/youtube.py transcript "VIDEO_ID_OR_URL" [--languages en]
```

Extracts the transcript from a video. The tool tries `youtube-transcript-api` (primary, high confidence) then `yt-dlp` subtitle extraction (fallback, medium confidence). Returns `status=ok` with `source` and `confidence` on success; `status=error` if all providers fail.

Note: transcript extraction can fail if the proxy is temporarily dead (silent empty output). The tool auto-falls back to direct; as a last resort force it:

```
HTTP_PROXY= HTTPS_PROXY= \
  uv run --with requests --with certifi --with youtube-transcript-api \
    python3 ~/.opencode/tools/youtube.py transcript "VIDEO_ID_OR_URL"
```

---

## Discovery Workflow

### Step 1 — Clarify Scope

Before extracting anything, identify:

- Specific video URLs, channel names, or search targets
- Whether the goal is summary, comparison, fact-checking, or quote extraction
- Whether timestamps are needed
- Whether only English transcripts are acceptable

Default ask-vs-proceed rule: ask one clarifying question first **only** if the missing target would substantially change which video gets summarised. If the user does not respond within the interaction, proceed with a clearly stated default selection strategy.

### Step 2 — Discovery (topic-only requests)

1. Use `search` to gather a pool of 10–20 candidate videos
2. Rank by: source authority, apparent technical depth, recency, query relevance, transcript likelihood
3. Prefer: official conference uploads > primary-source interviews > high-signal explainers from credible channels
4. Try transcript extraction on multiple candidates until you have enough usable coverage

**Transcript-attempt budgets:**

- Lightweight summary: try at least 5 candidates before concluding coverage is weak
- Comparison/research synthesis: try at least 8 candidates before concluding coverage is weak
- Stop early once you have sufficient evidence

**Caption policy:**

- Accept platform transcripts or auto-generated captions for summary work, but note limitations
- For fact-checking or quote-sensitive work, flag lower confidence when only noisy auto-captions are available

### Step 3 — Transcript Gating Rule

- Before summarising any video, obtain a usable transcript via the `transcript` action
- A usable transcript means `status=ok` with non-empty `text`
- If the tool returns `status=error` or `status=empty`, treat that as failure and try the next candidate
- **Do not write a content summary as though you watched the video unless a usable transcript was actually obtained**

### Step 4 — Evidence Evaluation

For each video assess:

- Who is speaking and what are their credentials?
- Is the content firsthand reporting, commentary, marketing, or education?
- Are claims supported with sources or demonstrations?
- Is the transcript complete and reliable enough?
- Is the video current enough for the topic?

### Step 5 — Cross-Reference

For factual or decision-relevant claims, verify with official documentation, credible reporting, academic or regulatory sources using independent web search tools.

---

## Output Format: YouTube Audit Block

Every YouTube research output must end with this audit block:

```
### Transcript Audit
- Candidates discovered: N
- Transcript attempts: N
- Usable transcripts obtained: N
- Excluded (no transcript): [video titles or IDs]
- Transcript sources used: [youtube-transcript-api | yt-dlp | mixed]
- Confidence: [High | Medium | Low] — reason
```

Main findings must include:

- Concise summary of what the video(s) actually say
- Timestamps for important excerpts when useful
- Clear attribution of claims to speakers/channels
- Verification notes for important claims
- Caveats about transcript quality or missing context
- Exact source URLs or video IDs used

**If no usable transcript was obtained**: do not present a normal research summary. Instead, report that transcript extraction failed, list which steps were attempted, and state what user input would unblock the task.
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
