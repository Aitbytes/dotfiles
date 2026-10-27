---
name: youtube-research
description: "USE WHEN the answer lives in videos: product reviews, tutorials, tests, conference talks, interviews, 'ce qu'en disent les youtubeurs', transcripts de vidéos. Also USE WHEN listing une playlist, une chaîne, Watch Later (list=WL) ou abonnements en masse (yt-dlp --flat-playlist). Transcript-first: never summarize a video without its transcript (8-candidate budget, audit block). Cross-references retail-research and social-marketplace-research."
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

## Recettes éprouvées (2026-10)

### Listing playlist / chaîne fiable (Watch Later, abonnements)

```
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
  yt-dlp --cookies-from-browser brave --flat-playlist -J <url> > listing.json
```

- JSON natif `-J` **obligatoire** — jamais de parsing de texte délimité (`|`, CSV) : des titres
  contenant `|` ou des retours à la ligne ont déjà fait perdre 126 lignes.
- Quirk NixOS : `SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt` requis pour yt-dlp.
- Cookies navigateur > 90 jours → warning fréquent : préférer un re-login plutôt qu'itérer.
- Chaîne : préférer `youtube.py channel <url> --meta` (titres + dates en batch, voir ci-dessous).

### Transcripts anti-429 / IpBlocked

Quand `youtube-transcript-api` et yt-dlp retournent 429/IpBlocked (PO token), méthode UI+CDP
(testée 2026-10-25 : 6/9 vidéos extraites) :

```bash
# 1. Navigateur CDP — Chrome ≥136 REFUSE le debug remote sur le profil par défaut :
#    toujours un --user-data-dir dédié. setsid (pas nohup) pour survivre au shell.
setsid chromium --headless=new --user-data-dir=/tmp/chr-prof --remote-debugging-port=9222 \
  --no-first-run --no-default-browser-check --disable-sync --disable-gpu about:blank \
  >/tmp/chromium.log 2>&1 < /dev/null & disown
sleep 6 && curl -sm3 http://127.0.0.1:9222/json/version   # sanity check

# 2. Ouvrir la vidéo, cliquer « …Afficher la transcription », intercepter :
uv run --with websocket-client python /tmp/cdp_transcript.py VIDEO_ID
```

Squelette de `/tmp/cdp_transcript.py` (websocket-client ; `suppress_origin=True` OBLIGATOIRE,
sinon WS refusé) :

1. Créer l'onglet : `PUT http://127.0.0.1:9222/json/new` (PAS GET) → target ; puis
   `create_connection(tgt['webSocketDebuggerUrl'], timeout=150, suppress_origin=True)`.
2. `Network.enable` + `Page.enable` ; `Page.navigate` sur `watch?v=ID` ; sleep ~12 s.
3. Clic UI : `document.querySelector('#expand')?.click()` ; sleep 1,5 s ; puis
   `document.querySelector('ytd-video-description-transcript-section-renderer button')?.click()`.
4. Boucle `ws.recv()` ~50 s : sur `Network.requestWillBeSent`, garder le requestId si l'URL
   contient `get_panel` **OU** `get_transcript` — l'endpoint VARIE selon la version du client
   (double fallback d'interception) ; noter le status via `Network.responseReceived` ; puis
   `Network.getResponseBody {requestId}` → corps ~305KB (JSON).
5. Parser en parcours récursif : collecter les dicts `transcriptSegmentViewModel` dans l'ordre
   du document, extraire `snippet.simpleText` (ou `runs[].text`) + `startMs` → segments.
   Plus besoin de `timedtext` (souvent 429) : tout est dans `get_panel`.
6. Échecs : FAILED_PRECONDITION sur une vidéo = passer à la suivante, ne pas boucler ;
   IpBlocked persistant = basculer sur une **IP de sortie différente** (voir skill **steel-browser**).
   (Piège bash : `pkill -f` peut se tuer lui-même — matcher le pid, pas le pattern.)

### Boucle resolve avec retry

```bash
for id in $IDS; do
  out=$(uv run --with requests --with certifi \
    python3 ~/.opencode/tools/youtube.py resolve "$id" --format json)
  if echo "$out" | grep -q '"title": null'; then
    out=$(uv run --with requests --with certifi \
      python3 ~/.opencode/tools/youtube.py resolve "$id" --format json)  # retry ×1, pas plus
  fi
  echo "$out" > "resolve_$id.json"
done
```

Titre vide (`title: null` / `# YouTube Video: |`) = retry ×1 maximum, puis noter l'échec et passer
à la suite. Ne jamais re-resoudre une vidéo qui a déjà un titre.

### Rappel outil youtube.py (options corrigées 2026-10)

`~/.opencode/tools/youtube.py` reste le premier réflexe (search / resolve / channel / transcript) :

- `channel <url> --meta` — ajoute titres + dates de publication en batch (yt-dlp `--flat-playlist -J`,
  puis oEmbed par vidéo pour les titres manquants). Évite ~20 resolves individuels. `list` = alias.
- `transcript <id> --out FICHIER` — écrit le fichier avec la bonne extension (auto-correction
  `.json` → `.md` quand la sortie est markdown) : fini les JSONDecodeError + renames manuels.

### Coûts token

- Listing → sortie `-J` native (JSON), relire le fichier une seule fois.
- Transcripts → ne lire chaque fichier de transcript qu'**UNE fois** (pas de read → sed → re-read :
  c'est ~240KB de contexte économisés pour 8 transcripts).
- Métadonnées → résoudre en batch quand l'outil le permet (`channel --meta`) au lieu de N resolves.

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
