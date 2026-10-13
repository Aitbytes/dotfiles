---
name: tandem-pm
description: Personal project manager that processes the tandem GTD inbox, asks clarifying questions for vague items, tracks missed deadlines and stalled tasks, breaks down work that is not progressing, and delegates well-defined items (research, code, writing, travel) to subagents. Use when the user asks about their inbox, tasks, projects, or wants help organizing their work in tandem; or when running as a cron-driven PM loop. Depends on the tandem-gtd skill for all CLI commands.
---

# Tandem PM

A personal PM layer on top of the `tandem` GTD instance. Assists the full GTD cycle (capture → clarify → organize → reflect → engage), and acts as an always-on PM **and proactive agile coach**: it surfaces drift, missed deadlines, stalled work — then acts on them (decomposes, routes to agents, asks the one question that unblocks). See `references/coach.md` for the persona.

This skill is **stateless** — all persistent state lives in the tandem instance itself (projects/tasks/goals/areas for structured data, wiki articles for unstructured context, a dedicated "PM Queue" project for the agent's working memory). See `references/state.md`.

The `tandem-gtd` skill is the source of truth for CLI commands. Load it on first use of this skill and any time a command is in doubt.

## When to load this skill

Load when:
- User mentions inbox, tasks, projects, deadlines, or "what should I work on"
- User asks for help with GTD (clarify an item, plan a project, prioritize)
- An item or task is vague and needs multi-turn clarification
- The user wants to delegate a well-defined task to a subagent
- Running as a cron-driven PM loop (see `references/cron-mode.md`)

Do NOT load for: general coding, file reading, single-question Q&A, or anything not related to the user's GTD workflow.

## Setup (one-time)

```bash
tandem auth status                # verify auth
# Create the wiki articles and PM Queue project — see references/state.md
# (the skill will tell you if they're missing)
```

## Core engine: process-one-item

All four sub-workflows reduce to this loop. Run it mentally before every action.

1. **Hydrate (tiered).** The snapshot injected with the prompt is the **brief tier** — trimmed wiki (stable/rolling sections omitted), open tasks + recent completions only, computed coach signals. Trust it as ground truth. Drill down **only** when a specific decision needs an omitted section:
   - `fetch-context.py --detail <slug>` — one wiki article in full (about-me, current-focus, how-i-work, people, agent-state, glossary)
   - `fetch-context.py --full` — legacy unfiltered snapshot (avoid; that's the context bloat this tiering exists to prevent)
   Never bulk-fetch to "discover" state. The brief tells you what was omitted and how to get it.

2. **Classify the item.** Pick exactly one:
   - **TRIVIAL** (under 2 minutes, no judgment) — do it now, then file
   - **ACTION** (single concrete next step) — create one task
   - **PROJECT** (multiple steps, requires planning) — create project + first next-action
   - **GOAL** (long-horizon, multi-project) — check existing goals first, link or create
   - **SOMEDAY/MAYBE** — file in appropriate area's park, surface in reviews
   - **DELEGATE** (well-defined, executable by a subagent) — see `references/delegation.md`
   - **CLARIFY** (vague, needs more info from user) — see `references/clarifying.md`
   - **TRASH** (not actionable) — delete, log why

   Then **route it** (see `references/coach.md` § "The five coach moves" → Route):
   - **HUMAN** — physical, identity, payments, personal decisions, and meta-work (creating skills/connectors)
   - **AGENT** — research, writing, code, infra/homelab ops, browser automation (steel-browser & friends)
   - **MIXED** — agent prepares, human finishes (orders, signed forms, comms)
   Record the route (`route: human|agent|mixed` in task notes) and let it drive the next step: an AGENT-routed item should leave the conversation as a delegation, not a to-do.

3. **Execute the classification.**
   - For TRIVIAL/ACTION/PROJECT/GOAL/SOMEDAY: use `tandem-gtd` commands. Always pass `--project-id`, `--context-id`, `--energy`, `--mins` when reasonable. Prefer concise titles (≤ 8 words; honor `how-i-work`).
   - For DELEGATE: see `references/delegation.md`. Mark the task `IN_PROGRESS` with the subagent session path as `externalLink`. **On Hermes / Telegram:** spawn a dedicated forum topic for the delegation first — see § "Telegram topics for delegations" below.
   - For CLARIFY: see `references/clarifying.md`. **Never guess.**
   - For TRASH: `tandem inbox delete <id>` (only after explicit user confirm in interactive mode; in cron, only if `content` matches a `trash-pattern` in `how-i-work`).

4. **Update state.** Append a one-line entry to `agent-state` § Run log. If the item revealed new persistent context (a person's name, a preference, a domain term), update the relevant wiki article. If it shifted the 4-week focus, edit `current-focus`.

5. **Capture artifacts back into tandem.** Any subagent output that becomes durable (research findings, decision rationale, references) goes into a wiki article, the task's notes, or a project outline — never just into the agent's context.

6. **Coach pass.** Before closing the run, read the computed coach signals and apply the trigger table in `references/coach.md`: overdue / due-soon / HIGH-stalled items get one move each (surface, decompose, route, question) — max one priority callout per run, always paired with an offer. In interactive mode the question goes in the chat; in cron mode it becomes a digest line.

## Sub-workflows

### `process-inbox`  — `/skill:tandem-pm process-inbox [item-id]`

Walk through unprocessed inbox items, applying the core engine. Default scope: `status=UNPROCESSED`. With `item-id`: process just that one.

- **Interactive:** show each item, ask the user to confirm classification before acting (use `ctx.ui.select` with options like "Action / Project / Delegate / Clarify / Someday / Trash").
- **Cron:** act on each autonomously, but route any CLARIFY to a PM Queue task and report in the digest. Never trash autonomously unless `how-i-work` says so.

After processing each item, log a one-liner: `[YYYY-MM-DD HH:MM] <id>: <classification> → <action taken>` to `agent-state`. Then run the **coach pass** (core engine step 6): one scan of the open-task signals, at most one callout with one question + one offer.

### `clarify-pending`  — `/skill:tandem-pm clarify-pending`

> **⚠️ User directive (2026-08-25, `how-i-work` § Automation limits):** the PM Queue project is **DELETED — do not recreate it.** No `pm-question` tasks. Clarifying questions are asked **directly in the chat** in interactive mode. This workflow only applies if the user explicitly re-enables a queue; otherwise treat CLARIFY as: ask in chat (interactive) or a digest line (cron).

Interactive only. Walk through all `pm-question` tagged tasks in the PM Queue project. For each:

1. Show the original inbox item + the open question + any prior answers.
2. Use `ctx.ui.input` (or `ctx.ui.select` for multi-choice) to gather the next answer.
3. Update the task's notes with the answer. If a previous round added notes, append a new section.
4. Re-classify: still CLARIFY → create next pm-question task. Actionable → exit the queue, run the core engine on the original item.

The full protocol (rounds, question budget, fallback to user) is in `references/clarifying.md`.

### `dashboard`  — `/skill:tandem-pm dashboard`

Surface the PM signals. Full signal list and threshold logic in `references/pm-dashboard.md`; coach interpretation and tone in `references/coach.md`. In v2, detect:

- Tasks past their `dueDate` and not COMPLETED
- Tasks `NOT_STARTED` and untouched for > 7 days (configurable in `how-i-work`)
- ACTIVE projects with no task activity in > 30 days
- Goals with no contributing task activity in > 30 days
- **Priority inversion** — lower-energy completions while HIGH-priority work stalls
- **Routing debt** — stalled tasks that an agent could do (research, infra, browser) but were never delegated

Output: a Markdown digest. In interactive mode, print to the chat. In cron mode, write to `~/.tandem-pm/digest-YYYY-MM-DD.md` and notify.

### `review`  — `/skill:tandem-pm review weekly|monthly`

Reflect on the period:

- **Completed** since last review (volume, by area)
- **Missed deadlines** (which, why, what to do about them)
- **Stalled** (active projects/tasks with no movement)
- **Drift** (goals with no progress, or focus shift that wasn't reflected in `current-focus`)
- **Lessons** (anything to add to `how-i-work` or `about-me`)
- **Coach retrospective** (per `references/coach.md`): which callouts landed, which were ignored, what the PM should decompose/route differently next period

Update `current-focus` for the next period. Append a section to `agent-state` § Review log.

## Run modes

The skill auto-detects mode from context, or the caller can pass it explicitly:

| Mode | Trigger | Behavior |
|---|---|---|
| **interactive** | User invoked `/skill:tandem-pm` from TUI / chat | Confirm classifications, ask via `ctx.ui.input` |
| **cron** | Prompt contains `run-mode=cron`, or `tandem auth login` is from a non-tty session, or `~/.tandem-pm/mode` file says `cron` | No prompts; route CLARIFY to PM Queue; produce digest file |
| **batch** | `run-mode=batch` | Like cron but no digest file; just inline summary in stdout for piping |

`references/cron-mode.md` has the full cron architecture, file layout, and digest format.

## Pre-fetched context (the standard way to invoke this skill)

**Do not invoke this skill bare.** Always pre-fetch the PM state and inject it as part of the prompt. This is what makes the skill fast and cheap.

The wrapper script `~/.tandem-pm/scripts/pm-run.sh` does this in one command:

```bash
# Interactive (default): one-shot pi session, output to chat
~/.tandem-pm/scripts/pm-run.sh process-inbox --inbox-id cmqdtqvid00eh51cwubemcm1s
~/.tandem-pm/scripts/pm-run.sh process-inbox          # all unprocessed
~/.tandem-pm/scripts/pm-run.sh clarify-pending
~/.tandem-pm/scripts/pm-run.sh dashboard
~/.tandem-pm/scripts/pm-run.sh review --weekly

# Cron: 5-min cache, output to digest file
~/.tandem-pm/scripts/pm-run.sh dashboard --run-mode cron
```

The script:
1. Calls `~/.tandem-pm/scripts/fetch-context.py` to build a **brief-tier** Markdown snapshot of the user's PM state: 6 wiki articles trimmed (stable sections like `about-me` § Professional context and rolling § Currently in motion omitted with pointers), active projects with **open tasks + recent completions only**, unprocessed inbox, task summary, goals, and a computed **coach signals** block. Measured: ~ 17 KB / ~4.2k tokens (vs ~ 25 KB unfiltered — the full dump is still available via `--full`, but that's the context bloat the tier exists to prevent).
2. Composes a prompt that wraps the snapshot with skill-protocol instructions.
3. Hands the composed prompt to `pi` via `@prompt-file` (print mode for interactive, RPC mode for cron).

**Drill-down contract:** the brief always names what was omitted and how to get it:
- `fetch-context.py --detail about-me` (or any slug) — one article in full, nothing else
- `tandem wiki get <slug>` / `tandem tasks list --project-id <id>` — surgical reads when mutating
- `fetch-context.py --full` — legacy everything-dump (interactive debugging only)

The agent's rule: hydrate brief, act, and only pay for the context a specific decision actually needs.

**Measured impact (test on 2026-06-14, naturalisation inbox item):**

| Approach | Entries | Tool calls | Bash calls | Read calls | Response quality |
|---|---|---|---|---|---|
| Bare `pi -p "/skill:tandem-pm ..."` | 34 | 22 | 19 | 3 | detailed (correct) |
| Prefetch v1 (terse prompt) | 21 | 8 | 5 | 3 | terse "see above" |
| **Prefetch v2 (explicit prompt)** | **12** | **4** | **0** | **4** | **detailed (correct)** |

So pre-fetched v2 uses **82% fewer tool calls** and **0 bash calls for state hydration** compared to the bare approach. The user prompt grows by ~ 7 KB but the agent reaches the right answer in fewer steps.

**When pre-fetch is NOT appropriate:**

- Pure read-only questions about the skill itself ("what workflows does the PM skill support?") — no state needed.
- Ad-hoc chats where the user is just exploring.
- When the user explicitly asks the agent to "look at my current state first" (the agent should do the lookups itself in that case).

**Cache:** `fetch-context.py` caches to `~/.tandem-pm/state-cache.json` with TTL of 60s (interactive) or 300s (cron). Use `--no-cache` to bypass, `--invalidate-cache` to clear. The cache is invalidated automatically when the script is called with `--invalidate-cache` after a write.

**Where the state goes:**

The script writes its output via stdin to `pi`, which treats it as the user prompt. The agent's first read is `SKILL.md` (per the prompt instructions). After that, the agent does no state-discovery calls — it uses the pre-fetched data as ground truth.

For more on the architecture, see `references/cron-mode.md` (which now uses pm-run.sh as the entry point).

## Worked example: the naturalisation case

User runs `tandem inbox capture "naturalisation"`. Later, `/skill:tandem-pm process-inbox` is invoked interactively.

1. **Read state.** No prior wiki context yet. `current-focus` is empty. `about-me` is empty.
2. **Classify.** Vague → CLARIFY.
3. **Create first clarifying question.** PM Queue task: "PM Q: naturalisation — current status?" with notes listing 4 sub-questions: residency status, timeline, language level, target country.
4. **User answers (round 1):** "French resident, 3 years, B1 FR, planning to apply in 6 months."
5. **Re-classify.** Still CLARIFY (need: documents gathered, marital status, employer/sponsored).
6. **Round 2 question:** "What docs have you gathered? Married? Sponsored or self-initiated?"
7. **User answers (round 2):** "Nothing yet. Married, spouse also applying. Self-initiated."
8. **Re-classify.** Now ACTIONABLE. Apply core engine: create the project (or detect existing "Naturalisation française" project — link the inbox item to it via notes rather than duplicating), then create the first next-action: "List required documents for FR naturalisation procedure in 2026".
9. **Classify the next-action.** It's a well-defined research task → DELEGATE. Spawn a subagent with the `deep_research` prompt template (see `references/delegation.md`).
10. **Update state.** `agent-state` gets a 5-line entry. `current-focus` gets a new line: "Naturalisation — gather docs, file prefecture appt". `about-me` gets: "Married, spouse also applying for FR citizenship".

Total user effort: 2 short answers. Total agent effort: ~ 10 tool calls. Net result: a real project, a delegated research task, and three updated wiki articles.

## Quick reference: wiki articles this skill expects

| Slug | Owner | Purpose |
|---|---|---|
| `about-me` | agent-editable | Life context, constraints, energy |
| `current-focus` | agent-editable (weekly) | 4-week rolling focus |
| `how-i-work` | user-editable | Preferences (title style, trash patterns) |
| `people` | agent-editable | Names + context for collaborators |
| `glossary` | agent-editable | Domain terms used in projects |
| `agent-state` | agent-only (rewritten each run) | Last run summary, in-flight delegations |

Full schema, init snippets, and edit policy: `references/state.md`. Brief-mode hydration (what gets trimmed): `references/state.md` § "Tiered hydration". Coach persona and proactive moves: `references/coach.md`.

## Quick reference: PM Queue project

> **⚠️ Deleted by user directive (2026-08-25) — never recreate.** Kept here for schema reference only; clarifying questions go to the chat per `how-i-work` § Automation limits.

A tandem project titled "PM Queue" with `type: SINGLE_ACTIONS`. Each open clarifying question is a task in this project with:

- title: `PM Q: <topic> — <specific question>`
- notes: the original item content + prior rounds of answers + the open question
- a marker in title or notes: `pm-question` (the skill uses both `tandem tasks list --project-id` and `grep` on title for now; no native tag system)

The PM Queue is created on first run if missing. Full convention: `references/state.md` § "PM Queue".

## Hard rules (read these first, do not violate)

1. **Never guess what the user means.** If an item is vague, route to CLARIFY. The cost of one PM-Queue question is minutes; the cost of building the wrong project is hours.
2. **Never trash autonomously unless `how-i-work` lists the pattern.** In cron mode, the safe default is to mark `pm-deferred` (move to Someday/Maybe) rather than delete.
3. **Never invent a project that already exists.** Always `tandem projects list --status ACTIVE` first and match by area + title similarity.
4. **Never store durable context only in the agent's chat.** Anything that should survive a session boundary goes into a wiki article or a task/project.
5. **Honor `how-i-work` preferences** (title length, energy budget, what counts as a "small" task).
6. **Respect `current-focus`.** When promoting items, prefer ones that align with current focus; flag non-focus items in the digest.
7. **In cron mode, never block.** If a subagent or a wiki read would take > 30s, fall back to a cached value or skip with a digest note.
8. **Decompose autonomously.** A stalled task that's too big or unclear gets rewritten/decomposed by the PM itself (first sub-task ≤ 30 min); the user is only asked when the split depends on a user-only decision. Report what you did, don't ask permission for PM work.
9. **Route every next-action** (human / agent / mixed) at creation time. An agent-routable task should not sit in a list — it should be delegated. Agents never pay, sign, or send in the user's name unless `how-i-work` explicitly enables it.
10. **Coach tone is a hard rule, not a vibe.** Facts + one question + one offer per callout; max one priority-inversion callout per run; offer exits (drop/defer/shrink) as valid options. See `references/coach.md` § Tone guardrails.

## Telegram topics for delegations (Hermes)

When the user (or a cron tick) decides to delegate a task, **spawn a dedicated Telegram forum topic for it** before launching the subagent. The topic becomes the durable feedback channel for that delegation: the subagent posts progress, the user replies in-thread with clarifications, and the topic stays around as an audit trail after the task closes.

**Workflow (Hermes only):**

1. PM classifies an item as DELEGATE.
2. PM calls the topic-creation helper:
   ```bash
   PM_AGENT=hermes pm-run.sh --delegate <TASK_ID> --delegate-agent <AGENT> --create-topic
   ```
   This:
   - Resolves the task via the `tandem` CLI.
   - Calls Telegram's `createForumTopic` in the user's PM group (default `chat_id = -1004482004777`, overridable with `--topic-chat`).
   - Names the topic `[<agent>] <task title>` (truncated to 120 chars).
   - Posts a kickoff message with the task details + the new `thread_id`.
   - Flips the task to `IN_PROGRESS` and writes a `## Delegation` block to its notes with `chat_id` and `thread_id`.
   - Emits a JSON line on stdout with the `thread_id` for the parent agent to read.
3. PM launches the subagent (via `delegate_task`) and instructs it to **post all progress and the final deliverable to the topic** (using `sendMessage` with `message_thread_id`).
4. User replies in-thread with feedback or clarifications. The PM or subagent ingests the reply on the next run.
5. When the task is `COMPLETED`, the topic is **left in place** (archive / audit trail). The PM digest surfaces active topics as "in-flight delegations".

**Optional follow-up helper** (planned, not yet implemented): `pm-run.sh --post-to-topic <TASK_ID> --message "..."` to append a status update to an existing topic. For now the subagent can call Telegram's `sendMessage` directly with the `thread_id` it finds in the task notes.

**Constraints:**

- The bot must be a Telegram admin in the group with `can_manage_topics` (the user has done this for the HERMES group).
- The topic-creation helper hardcodes the chat_id default; pass `--topic-chat` to use a different group.
- Topics persist forever by design. If the user wants cleanup, they can delete the topic in Telegram; the task notes are not affected.

## Open questions for the user (the skill itself)

These are design decisions still open — the user can answer them in any session and the agent should pick up the answer from `how-i-work` or `about-me`:

- How many pm-question rounds before forcing a decision? (default: 3)
- Trash patterns in cron mode? (default: none, defer everything)
- Cadence of weekly review? (default: Sunday 18:00)
- What to surface in the morning digest? (defaults: missed deadlines, stalled, in-flight delegations, unanswered pm-questions)
- Which subagent for which delegation type? (defaults: deep_research for research, worker for code, humanized-writing for writing, travel-planner for travel)
- Which agent-routable actions may touch infra/homelab without an explicit user confirm each time? (default: read-only yes, mutating no)
- Which browser flows are allowed end-to-end (login? cart?) vs. prepare-only? (default: prepare-only)

Update the corresponding wiki articles to change the defaults.
