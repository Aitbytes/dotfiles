
# Findings
1. Primary agent workflows reference tool names that do not appear to exist, which likely breaks the agents' main execution paths.
   reddit-research enables reddit_scrape at .config/opencode/agents/reddit-research.md:19, and several agents enable web_scrape at .config/opencode/agents/research.md:20, .config/opencode/agents/shopping-assistant.md:19, and .config/opencode/agents/retail-research.md:19.
   The actual custom tool files are .opencode/tools/reddit.ts and .opencode/tools/web_scraper.ts, and OpenCode custom tools are named from filenames. That implies the tool names are reddit and web_scraper, not reddit_scrape and web_scrape.
   This is the highest-risk issue I found because those agents are written as if these are their primary tools.
2. Failure signaling is not machine-actionable, so agents cannot reliably distinguish "no data" from "tool failed".
   All the TypeScript wrappers collapse failures into plain strings like Error running ...: ${e.message} instead of structured errors: .opencode/tools/youtube_search.ts:25-29, .opencode/tools/reddit.ts:35-40, .opencode/tools/web_scraper.ts:42-48, .opencode/tools/amazon_reviews.ts:51-57, .opencode/tools/fda_510k.ts:44-49, .opencode/tools/patent_search.ts:44-49, .opencode/tools/hcpcs_lookup.ts:36-40, .opencode/tools/eudamed_lookup.ts:36-40, .opencode/tools/startup_data.ts:38-42.
   On the Python side, many transport failures are silently converted into empty result sets rather than typed failures: .opencode/tools/startup_data.py:73-75, .opencode/tools/startup_data.py:110-112, .opencode/tools/startup_data.py:177-179, .opencode/tools/patent_search.py:122-124, .opencode/tools/eudamed_lookup.py:91-93, .opencode/tools/eudamed_lookup.py:133-135, .opencode/tools/eudamed_lookup.py:166-168, .opencode/tools/amazon_reviews.py:137-139, .opencode/tools/amazon_reviews.py:181-183.
   That forces fallback logic into prompts because the agent cannot programmatically branch on a stable error contract.
3. Proxy behavior is implicit and inconsistent across the stack.
   You have an authenticated proxy config in ~/.config/proxy-conf:1-2.
   playwright explicitly documents that proxies must be unset because Chromium cannot automatically use the authenticated proxy: .config/opencode/agents/playwright.md:41-49.
   The other networked tools do not have any explicit proxy policy. They rely on default library behavior via urllib.request.urlopen(...) in .opencode/tools/youtube_search.py:19-21 and requests.get(...) / requests.Session() in .opencode/tools/web_scraper.py:36-49 and .opencode/tools/amazon_reviews.py:51-65.
   That means proxy behavior depends on ambient environment and library defaults, not on a shared reliability layer. In practice, that is exactly how you get "works in one agent, fails in another" behavior.
4. The YouTube workflow is split across too many surfaces, and most of the reliability logic lives in instructions instead of code.
   The current path spans a custom youtube_search tool, the youtube-transcript MCP, ad hoc uv run --with youtube-transcript-api, and finally yt-dlp plus Whisper, all spelled out in agent prose at .config/opencode/agents/youtube-research.md:31-32, .config/opencode/agents/youtube-research.md:89-93, .config/opencode/agents/youtube-research.md:123-166, and .config/opencode/agents/youtube-research.md:217-225.
   This makes success depend on the model correctly interpreting and executing a fallback tree, instead of calling one reliable tool that owns retries, proxy handling, rate limiting, and typed failure output.
   This is the clearest example of the architectural problem you described.
5. The tool surface is wider than needed, increasing routing ambiguity and context cost.
   shopping-assistant exposes direct web, search, Reddit, YouTube, transcript, Amazon, and task orchestration tools all at once: .config/opencode/agents/shopping-assistant.md:16-25.
   retail-research does the same: .config/opencode/agents/retail-research.md:16-25.
   research is broader still with generic web tools, GitHub search, regulatory tools, startup tools, OCR, arXiv, Wikidata, and more: .config/opencode/agents/research.md:16-43.
   OpenCode's own MCP docs warn that MCP servers add context and should be enabled carefully. The current setup is drifting toward overlap rather than a sharply separated tool contract.
6. The runtime contract is inconsistent between "direct script" and "tool wrapper" execution.
   I smoke-tested three scripts. youtube_search.py ran directly and returned results. fda_510k.py and web_scraper.py failed immediately with ModuleNotFoundError: No module named 'requests' when invoked directly, because they depend on wrapper-time uv run --with ....
   That is not inherently wrong, but it means execution reliability depends on calling the exact right wrapper. If agents are ever told "run the local script directly" for tools that need ephemeral deps, they will fail.
Assessment
Current inventory:
- 9 custom tools in .opencode/.opencode/tools
- 11 MCP server entries in .config/opencode/opencode.json, with 3 explicitly disabled
- 1 local skill in .config/opencode/skills/glm-ocr
- several specialized agent prompts carrying fallback logic that should live in code
The main problem is not "too many tools" by itself. The main problem is:
- overlapping tools
- inconsistent naming
- prompt-level fallback trees
- untyped failures
- no shared network/runtime policy
Skills vs Tools
Short answer: do not migrate reliability into skills.
What the docs and practitioner material converge on:
- OpenCode skills are reusable instructions loaded on demand, not deterministic executors.
- OpenCode custom tools are the actual callable functions.
- The Agent Skills ecosystem positions skills as folders of instructions, scripts, and resources.
- LlamaIndex's write-up draws the right line: MCP/tools are deterministic, schema-driven operations; skills are natural-language behavioral guidance and are easier for the model to misinterpret.
- Microsoft's skills repo also treats skills as focused activation context and warns against loading too many because of context rot.
- ClawHub is a registry/distribution layer for skills, not a runtime reliability solution.
The useful principle is:
- Skills orchestrate the how.
- Tools execute the what.
- Reliability belongs in tools, not in prompts and not in skills.
So if your goal is "minimal tool set with maximal programmatic reliability", the right move is:
- fewer, better tools
- thinner agent prompts
- optional skills for workflow guidance only
Recommended Target State
1. Build a shared execution layer for all networked tools.
   Put retries, timeout budgets, proxy loading, per-host overrides, jittered backoff, user-agent policy, rate-limit handling, and error normalization in one internal library.
   Every HTTP-facing tool should use that same layer.
2. Standardize one result envelope for every custom tool.
   Return JSON with a consistent shape, for example:
      {
     ok: false,
     stage: transcript_fetch,
     error: {
       kind: rate_limited,
       message: YouTube transcript endpoint returned 429,
       retriable: true,
       provider: youtube,
       http_status: 429
     },
     attempts: 3,
     proxy: configured,
     fallbacks_tried: [youtube-transcript, youtube-transcript-api]
   }
      No more plain-string wrapper failures.
   No more silent [] on transport errors.
3. Move fallback logic out of agent prompts and into the tool implementation.
   The YouTube case should become one tool boundary, not four.
   Suggested tool shape:
   - youtube with actions like search, transcript, resolve
   - or one youtube_fetch tool that accepts either query or url
   The tool should internally do:
   - discovery
   - transcript attempt order
   - retries
   - proxy policy
   - structured failure output
   Agents should not know the fallback tree.
4. Fix naming before anything else.
   Align agent configs with actual tool names.
   If you want names like reddit_scrape and web_scrape, rename the files.
   If you want to keep current filenames, update the agents.
   Right now this looks broken.
5. Reduce the surface by capability boundary, not by vendor/source count.
   My recommended minimal split:
   - youtube
   - reddit
   - web_scraper or just built-in webfetch plus one search tool, not three overlapping web surfaces
   - domain-specific regulatory tools only where they hit stable, structured APIs and materially outperform generic fetch/search
   Concretely:
   - web_scraper is probably redundant unless you really need selector extraction or table extraction beyond webfetch
   - keeping both Google Search and DDG is likely unnecessary unless you have a clear measured reason
   - shopping agents should preferably orchestrate specialist agents, not also carry the full direct tool buffet
6. Stop resolving Python deps at request time where possible.
   Right now most wrappers depend on uv run --with ... on each invocation.
   That is convenient, but it increases runtime variability and adds another failure domain.
   Better options:
   - one pinned tool runtime environment
   - or a local MCP server that owns the runtime once and exposes a stable interface
   If you keep uv run --with, at least centralize it and pin versions.
7. Add a real verification harness.
   At minimum:
   - unit tests for parsers using saved fixtures
   - smoke tests for each tool with expected success/failure envelopes
   - contract tests asserting that transient failures produce typed retriable errors, not empty results
   - proxy-mode smoke tests
   - offline fixtures for YouTube HTML, Amazon blocks, EUDAMED empty pages, etc.
Concrete Recommendation for YouTube
If I were narrowing this first, I would start here.
Replace this:
- youtube_search custom tool
- youtube-transcript MCP
- prompt fallback to youtube-transcript-api
- prompt fallback to yt-dlp plus Whisper
With this:
- one local youtube tool or local YouTube MCP server you own
That tool should:
- accept query and/or url
- handle search internally
- try transcript providers in a fixed order
- manage retries and proxy use automatically
- optionally support audio transcription behind a flag
- return structured results with exact failure stage and retryability
Then rewrite youtube-research.md to say roughly:
- use youtube
- do not manually fall back unless the tool explicitly reports an unrecoverable failure
- cite transcript source and confidence returned by the tool
That would remove most of the current mess in one pass.
Where Skills Help
Use skills for:
- deciding when to do transcript-first research
- evaluation rubrics
- reporting templates
- domain-specific heuristics
- audit/checklist workflows
Do not use skills for:
- retries
- proxy handling
- parser fallback trees
- rate-limit recovery
- auth recovery
- differentiating hard vs soft failure
ClawHub or Agent Skills could be useful later if you want:
- portable workflow packaging
- versioned distribution
- cross-agent reuse of research/reporting playbooks
They will not solve the runtime reliability problem you identified.
Suggested Sequence
1. Fix tool naming mismatches.
2. Define a shared tool result schema.
3. Build a shared network/runtime layer with proxy support.
4. Collapse YouTube into one owned tool boundary.
5. Remove overlapping search/fetch surfaces.
6. Rewrite agent prompts to depend on tool contracts instead of fallback prose.
7. Add contract tests.
If you want, I can take the next step and turn this review into a concrete refactor plan for the opencode config:
- proposed final tool inventory
- which tools to delete/merge/rename
- a youtube tool contract
- a shared Python runtime layout
- prompt simplifications for the affected agents
