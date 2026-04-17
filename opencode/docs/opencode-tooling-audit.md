# OpenCode Tooling Audit

Phase 1: Inventory Freeze

## Scope

This audit freezes the current OpenCode tooling surface from these sources:

- `finding.md`
- `.config/opencode/opencode.json`
- `.config/opencode/agents/*.md`
- `.opencode/tools/*.ts`

The goal of this phase is descriptive, not corrective: list the current surface, map agent-visible names to actual implementations, identify overlaps and broken references, and define a before/after matrix for later refactor phases.

## Inventory Summary

- Custom tool entrypoints: 9 TypeScript wrappers in `.opencode/tools/`
- Backing custom scripts: 9 Python scripts, one per wrapper
- MCP server entries: 11 in `.config/opencode/opencode.json`
- Explicitly disabled MCP servers: 3 (`paperless`, `github`, `web-search`)
- Agent prompt files audited: 10 in `.config/opencode/agents/`
- Local skills present: 0 under `opencode/.config/opencode/skills/`
- Broken references confirmed in agent prompts: 3

Broken references confirmed in this phase:

- `web_scrape` is exposed by agents, but the actual custom tool filename is `web_scraper.ts`, so the callable tool name is `web_scraper`, not `web_scrape` (`.config/opencode/agents/research.md:20`, `.config/opencode/agents/retail-research.md:19`, `.config/opencode/agents/shopping-assistant.md:19`, `.opencode/tools/web_scraper.ts:4-50`).
- `reddit_scrape` is exposed by agents, but the actual custom tool filename is `reddit.ts`, so the callable tool name is `reddit`, not `reddit_scrape` (`.config/opencode/agents/reddit-research.md:19`, `.config/opencode/agents/retail-research.md:25`, `.config/opencode/agents/shopping-assistant.md:25`, `.opencode/tools/reddit.ts:4-42`).
- `retail-deep-research` is referenced by `deep-research`, but no corresponding agent file exists under `.config/opencode/agents/` (`.config/opencode/agents/deep-research.md:38-42`).

## Custom Tool Inventory

| Actual tool name | Wrapper entrypoint                  | Backing implementation              | Runtime path                                                           | Agent-visible name(s) today | Status                                                             |
| ---------------- | ----------------------------------- | ----------------------------------- | ---------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------ |
| `reddit`         | `.opencode/tools/reddit.ts`         | `.opencode/tools/reddit_scraper.py` | `uv run --with praw --with python-dotenv python3 ...`                  | `reddit_scrape`             | Broken alias in agents; tool filename and prompt name do not match |
| `web_scraper`    | `.opencode/tools/web_scraper.ts`    | `.opencode/tools/web_scraper.py`    | `uv run --with requests --with beautifulsoup4 --with lxml python3 ...` | `web_scrape`                | Broken alias in agents; tool filename and prompt name do not match |
| `youtube_search` | `.opencode/tools/youtube_search.ts` | `.opencode/tools/youtube_search.py` | `python3 ...`                                                          | `youtube_search`            | Name matches; direct script execution instead of `uv run`          |
| `amazon_reviews` | `.opencode/tools/amazon_reviews.ts` | `.opencode/tools/amazon_reviews.py` | `uv run --with requests --with beautifulsoup4 --with lxml python3 ...` | `amazon_reviews`            | Name matches                                                       |
| `fda_510k`       | `.opencode/tools/fda_510k.ts`       | `.opencode/tools/fda_510k.py`       | `uv run --with requests python3 ...`                                   | `fda_510k`                  | Name matches                                                       |
| `patent_search`  | `.opencode/tools/patent_search.ts`  | `.opencode/tools/patent_search.py`  | `uv run --with requests --with beautifulsoup4 --with lxml python3 ...` | `patent_search`             | Name matches                                                       |
| `hcpcs_lookup`   | `.opencode/tools/hcpcs_lookup.ts`   | `.opencode/tools/hcpcs_lookup.py`   | `uv run --with requests python3 ...`                                   | `hcpcs_lookup`              | Name matches                                                       |
| `startup_data`   | `.opencode/tools/startup_data.ts`   | `.opencode/tools/startup_data.py`   | `uv run --with requests python3 ...`                                   | `startup_data`              | Name matches                                                       |
| `eudamed_lookup` | `.opencode/tools/eudamed_lookup.ts` | `.opencode/tools/eudamed_lookup.py` | `uv run --with requests python3 ...`                                   | `eudamed_lookup`            | Name matches                                                       |

## MCP Inventory

Observed from `.config/opencode/opencode.json:51-134`.

| MCP server           | Enabled        | Implementation                                                        | Observed tool names in agent prompts                                                                                                                                                         | Notes                                                                                              |
| -------------------- | -------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `context7`           | Yes            | local `npx -y @upstash/context7-mcp`                                  | `context7_resolve-library-id`, `context7_query-docs`                                                                                                                                         | Used by `research` and `tutor`                                                                     |
| `ddg-search`         | **No**         | local `uvx duckduckgo-mcp-server`                                     | `ddg-search_search`, `ddg-search_fetch_content`                                                                                                                                              | Disabled — DuckDuckGo MCP triggers bot detection on this setup. Use `google-search` instead.       |
| `google-search`      | Yes            | local `npx -y @adenot/mcp-google-search`                              | `google-search_search`, `google-search_read_webpage`                                                                                                                                         | Used by `research`, `retail-research`, `shopping-assistant`, `youtube-research`, `reddit-research` |
| `paperless`          | No             | local `npx @nloui/paperless-mcp ...`                                  | none observed                                                                                                                                                                                | Disabled; not exposed in audited agents                                                            |
| `deepwiki`           | Yes            | remote `https://mcp.deepwiki.com/sse`                                 | none observed                                                                                                                                                                                | Enabled in config but not surfaced in audited agent tool lists                                     |
| `github`             | No             | local `npx -y @modelcontextprotocol/server-github`                    | none observed                                                                                                                                                                                | Disabled; not exposed in audited agents                                                            |
| `gh_grep`            | Implicitly yes | remote `https://mcp.grep.app`                                         | `gh_grep_searchGitHub`                                                                                                                                                                       | Used by `research`                                                                                 |
| `web-search`         | No             | remote `http://localhost:3002/mcp`                                    | none observed                                                                                                                                                                                | Disabled; not exposed in audited agents                                                            |
| `arxiv`              | Yes            | local `uv tool run arxiv-mcp-server --storage-path /tmp/arxiv-papers` | `arxiv_search_papers`, `arxiv_download_paper`, `arxiv_list_papers`, `arxiv_read_paper`                                                                                                       | Used by `research`                                                                                 |
| `youtube-transcript` | Yes            | local `npx -y @kimtaeyoon83/mcp-server-youtube-transcript`            | `youtube-transcript_get_transcript`                                                                                                                                                          | Used by `youtube-research`, `retail-research`, `shopping-assistant`                                |
| `pymupdf4llm`        | Yes            | local `uvx pymupdf4llm-mcp@latest stdio`                              | `pymupdf4llm_convert_pdf_to_markdown`                                                                                                                                                        | Used by `research`                                                                                 |
| `wikidata`           | Yes            | remote `https://wd-mcp.wmcloud.org/mcp/`                              | `wikidata_search_items`, `wikidata_search_properties`, `wikidata_get_statements`, `wikidata_get_statement_values`, `wikidata_get_instance_and_subclass_hierarchy`, `wikidata_execute_sparql` | Used by `research`                                                                                 |

## Agent-Exposed Capability Inventory

This section focuses on non-trivial capabilities: custom tools, MCP tools, and delegated subagent targets. Common built-ins like `read`, `glob`, and `grep` are omitted unless they materially affect routing.

| Agent                | Primary purpose                   | Direct custom tools exposed                                                                                   | Direct MCP tools exposed                                                                                          | Delegated capabilities                                                                                                | Notes                                                                                                                                                             |
| -------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `assistant`          | Personal assistant / orchestrator | none                                                                                                          | none                                                                                                              | `task` to `assistant-*` subagents                                                                                     | No direct external research surface                                                                                                                               |
| `chores`             | Docs, comments, git assistance    | none                                                                                                          | none                                                                                                              | generic `task`                                                                                                        | Mostly repo-local capability                                                                                                                                      |
| `tutor`              | Socratic tutoring                 | none                                                                                                          | `context7_*`                                                                                                      | generic `task`                                                                                                        | Prompt mentions `gh_grep_searchGitHub` and `google-search_search`, but they are not enabled in frontmatter (`.config/opencode/agents/tutor.md:17-19`, `:138-153`) |
| `research`           | General research                  | `web_scrape`, `fda_510k`, `patent_search`, `hcpcs_lookup`, `startup_data`, `eudamed_lookup`, `amazon_reviews` | `google-search_*`, `ddg-search_*`, `gh_grep_searchGitHub`, `context7_*`, `arxiv_*`, `pymupdf4llm_*`, `wikidata_*` | none                                                                                                                  | `web_scrape` is a broken alias                                                                                                                                    |
| `retail-research`    | Product and retailer research     | `web_scrape`, `amazon_reviews`, `youtube_search`, `reddit_scrape`                                             | `google-search_*`, `ddg-search_*`, `youtube-transcript_get_transcript`                                            | `youtube-research`, `reddit-research`, `playwright`                                                                   | Exposes both direct platform tools and specialist subagents                                                                                                       |
| `shopping-assistant` | Shopping orchestrator             | `web_scrape`, `amazon_reviews`, `youtube_search`, `reddit_scrape`                                             | `google-search_*`, `ddg-search_*`, `youtube-transcript_get_transcript`                                            | `retail-research`, `youtube-research`, `reddit-research`, `playwright`                                                | Same direct tool buffet as `retail-research`, despite being an orchestrator                                                                                       |
| `youtube-research`   | YouTube transcript-first research | `youtube_search`                                                                                              | `google-search_*`, `youtube-transcript_get_transcript`                                                            | generic `task`                                                                                                        | Prompt adds direct `uv` and `yt-dlp` fallback paths outside the declared tool surface                                                                             |
| `reddit-research`    | Reddit synthesis                  | `reddit_scrape`                                                                                               | `google-search_*`                                                                                                 | generic `task`                                                                                                        | `reddit_scrape` is a broken alias                                                                                                                                 |
| `playwright`         | Browser automation                | none                                                                                                          | none                                                                                                              | none                                                                                                                  | Capability is shell-driven Playwright CLI, plus optional `retail-playwright-search` skill                                                                         |
| `deep-research`      | Research orchestrator             | none                                                                                                          | none                                                                                                              | `research`, `youtube-research`, `reddit-research`, `retail-deep-research`, `retail-research`, `playwright`, `general` | `retail-deep-research` does not exist in the audited agent directory                                                                                              |

## Agent-Visible Name to Implementation Map

| Agent-visible name                             | Kind                  | Actual implementation                                                                                                 | Current state    |
| ---------------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `web_scrape`                                   | custom tool reference | No matching tool file. Nearest implementation is `.opencode/tools/web_scraper.ts` -> `.opencode/tools/web_scraper.py` | Broken reference |
| `reddit_scrape`                                | custom tool reference | No matching tool file. Nearest implementation is `.opencode/tools/reddit.ts` -> `.opencode/tools/reddit_scraper.py`   | Broken reference |
| `youtube_search`                               | custom tool reference | `.opencode/tools/youtube_search.ts` -> `.opencode/tools/youtube_search.py`                                            | Valid            |
| `amazon_reviews`                               | custom tool reference | `.opencode/tools/amazon_reviews.ts` -> `.opencode/tools/amazon_reviews.py`                                            | Valid            |
| `fda_510k`                                     | custom tool reference | `.opencode/tools/fda_510k.ts` -> `.opencode/tools/fda_510k.py`                                                        | Valid            |
| `patent_search`                                | custom tool reference | `.opencode/tools/patent_search.ts` -> `.opencode/tools/patent_search.py`                                              | Valid            |
| `hcpcs_lookup`                                 | custom tool reference | `.opencode/tools/hcpcs_lookup.ts` -> `.opencode/tools/hcpcs_lookup.py`                                                | Valid            |
| `startup_data`                                 | custom tool reference | `.opencode/tools/startup_data.ts` -> `.opencode/tools/startup_data.py`                                                | Valid            |
| `eudamed_lookup`                               | custom tool reference | `.opencode/tools/eudamed_lookup.ts` -> `.opencode/tools/eudamed_lookup.py`                                            | Valid            |
| `google-search_search`                         | MCP tool              | `google-search` MCP server in `.config/opencode/opencode.json:64-72`                                                  | Valid            |
| `google-search_read_webpage`                   | MCP tool              | `google-search` MCP server in `.config/opencode/opencode.json:64-72`                                                  | Valid            |
| `ddg-search_search`                            | MCP tool              | `ddg-search` MCP server in `.config/opencode/opencode.json:59-63`                                                     | **DISABLED** — bot detection                                                                      |
| `ddg-search_fetch_content`                     | MCP tool              | `ddg-search` MCP server in `.config/opencode/opencode.json:59-63`                                                     | **DISABLED** — bot detection                                                                      |
| `youtube-transcript_get_transcript`            | MCP tool              | `youtube-transcript` MCP server in `.config/opencode/opencode.json:119-123`                                           | Valid            |
| `gh_grep_searchGitHub`                         | MCP tool              | `gh_grep` MCP server in `.config/opencode/opencode.json:98-101`                                                       | Valid            |
| `context7_resolve-library-id`                  | MCP tool              | `context7` MCP server in `.config/opencode/opencode.json:52-58`                                                       | Valid            |
| `context7_query-docs`                          | MCP tool              | `context7` MCP server in `.config/opencode/opencode.json:52-58`                                                       | Valid            |
| `arxiv_search_papers`                          | MCP tool              | `arxiv` MCP server in `.config/opencode/opencode.json:107-118`                                                        | Valid            |
| `arxiv_download_paper`                         | MCP tool              | `arxiv` MCP server in `.config/opencode/opencode.json:107-118`                                                        | Valid            |
| `arxiv_list_papers`                            | MCP tool              | `arxiv` MCP server in `.config/opencode/opencode.json:107-118`                                                        | Valid            |
| `arxiv_read_paper`                             | MCP tool              | `arxiv` MCP server in `.config/opencode/opencode.json:107-118`                                                        | Valid            |
| `pymupdf4llm_convert_pdf_to_markdown`          | MCP tool              | `pymupdf4llm` MCP server in `.config/opencode/opencode.json:124-128`                                                  | Valid            |
| `wikidata_search_items`                        | MCP tool              | `wikidata` MCP server in `.config/opencode/opencode.json:129-133`                                                     | Valid            |
| `wikidata_search_properties`                   | MCP tool              | `wikidata` MCP server in `.config/opencode/opencode.json:129-133`                                                     | Valid            |
| `wikidata_get_statements`                      | MCP tool              | `wikidata` MCP server in `.config/opencode/opencode.json:129-133`                                                     | Valid            |
| `wikidata_get_statement_values`                | MCP tool              | `wikidata` MCP server in `.config/opencode/opencode.json:129-133`                                                     | Valid            |
| `wikidata_get_instance_and_subclass_hierarchy` | MCP tool              | `wikidata` MCP server in `.config/opencode/opencode.json:129-133`                                                     | Valid            |
| `wikidata_execute_sparql`                      | MCP tool              | `wikidata` MCP server in `.config/opencode/opencode.json:129-133`                                                     | Valid            |
| `retail-deep-research`                         | delegated subagent    | No file under `.config/opencode/agents/`                                                                              | Broken reference |

## Overlaps and Broken References

### Broken references

| Reference              | Where exposed                                              | Actual implementation     | Impact                                                                       |
| ---------------------- | ---------------------------------------------------------- | ------------------------- | ---------------------------------------------------------------------------- |
| `web_scrape`           | `research`, `retail-research`, `shopping-assistant`        | `web_scraper` custom tool | High; one of the primary generic fetch surfaces for those agents is misnamed |
| `reddit_scrape`        | `reddit-research`, `retail-research`, `shopping-assistant` | `reddit` custom tool      | High; the Reddit specialist agent's primary tool name does not resolve       |
| `retail-deep-research` | `deep-research` prompt prose                               | no agent file present     | Medium; orchestration plan references a nonexistent specialist agent         |

### Overlaps

| Capability area        | Current surfaces                                                                                                              | Why it overlaps                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Generic web discovery  | `google-search_*` (primary), `web_scraper` (fetch)                                                                              | DDG MCP disabled due to bot detection. Google MCP is primary search.                             |
| Generic page retrieval | `webfetch`, `google-search_read_webpage`, `ddg-search_fetch_content`, `web_scrape` / `web_scraper`                            | Four ways to read pages, with overlapping but not identical behavior                             |
| YouTube research       | `youtube_search`, `youtube-transcript_get_transcript`, prompt-level `youtube-transcript-api`, prompt-level `yt-dlp` + Whisper | Reliability logic is split across tool calls and prompt instructions                             |
| Shopping research      | `shopping-assistant` direct tools plus `retail-research`, `youtube-research`, `reddit-research`, and `playwright` subagents   | The orchestrator and executor layers both expose the same surfaces, increasing routing ambiguity |
| Reddit evidence        | Broken `reddit_scrape`, direct `webfetch` fallback, general search tools                                                      | Reddit-specific work is not cleanly isolated to one working tool boundary                        |

## Before / After Matrix

The "After" column is the target state implied by `finding.md`, not a change already present in the repo.

| Capability boundary         | Before (current state)                                                                                        | Main issue                                                       | After (target state)                                                                                               |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Reddit collection           | Agents call `reddit_scrape`; actual tool is `reddit`                                                          | Broken name; specialist agent cannot rely on its primary surface | One canonical Reddit tool name, ideally `reddit`, with prompts updated to match                                    |
| Generic web extraction      | Agents call `web_scrape`; actual tool is `web_scraper`                                                        | Broken name; generic scraping surface is miswired                | One canonical tool name, either rename file to `web_scrape` or update prompts to `web_scraper`                     |
| Web search and fetch        | `google-search_*`, `webfetch`, `web_scraper`                                                                | Overlap reduced after DDG MCP disabled. Clear roles: search → Google, fetch → web_scraper       | Keep Google MCP as primary search, web_scraper as page fetch, webfetch as lightweight fallback               |
| YouTube research            | `youtube_search` + `youtube-transcript_get_transcript` + ad hoc `uv` transcript fallback + `yt-dlp` + Whisper | Fallback tree lives in prompts, not in code                      | Collapse to one owned YouTube boundary that handles search, transcript retrieval, retries, and fallback internally |
| Retail orchestration        | `shopping-assistant` and `retail-research` both expose direct platform tools and subagents                    | Duplicated responsibility and routing ambiguity                  | Make `shopping-assistant` mostly orchestration-only; keep direct platform tools on executor agents                 |
| Specialist subagent routing | `deep-research` references `retail-deep-research` which does not exist                                        | Planner can route to a dead end                                  | Either add the missing agent or remove the reference and route to `retail-research`                                |
| Network/runtime policy      | Each wrapper chooses its own `uv run` / direct Python pattern                                                 | Inconsistent reliability and dependency behavior                 | Shared execution layer and consistent result envelope across all networked custom tools                            |

## Recommended Phase 2 Starting Points

Phase 1 establishes these concrete starting points for the next refactor phase:

1. Fix the three broken references first: `web_scrape`, `reddit_scrape`, and `retail-deep-research`.
2. Decide the canonical names for the two misaligned custom tools before changing any agent prompt text.
3. Freeze a reduced capability boundary for later work:
4. Keep one Reddit tool boundary.
5. Keep one YouTube tool boundary.
6. Keep one generic search surface and one generic fetch surface.
7. Keep domain-specific regulatory tools only where they materially outperform generic search/fetch.

## Appendix: Audited Files

- `finding.md`
- `.config/opencode/opencode.json`
- `.config/opencode/agents/assistant.md`
- `.config/opencode/agents/chores.md`
- `.config/opencode/agents/deep-research.md`
- `.config/opencode/agents/playwright.md`
- `.config/opencode/agents/reddit-research.md`
- `.config/opencode/agents/research.md`
- `.config/opencode/agents/retail-research.md`
- `.config/opencode/agents/shopping-assistant.md`
- `.config/opencode/agents/tutor.md`
- `.config/opencode/agents/youtube-research.md`
- `.opencode/tools/amazon_reviews.ts`
- `.opencode/tools/eudamed_lookup.ts`
- `.opencode/tools/fda_510k.ts`
- `.opencode/tools/hcpcs_lookup.ts`
- `.opencode/tools/patent_search.ts`
- `.opencode/tools/reddit.ts`
- `.opencode/tools/startup_data.ts`
- `.opencode/tools/web_scraper.ts`
- `.opencode/tools/youtube_search.ts`
