# State management — wiki convention

The PM skill is **stateless** between runs. All persistent state lives in the tandem instance. This document defines the schema, the init flow, the read/write policy, and the cache layer.

## Overview: where each thing lives

| Layer | Lives in | Schema | Who writes |
|---|---|---|---|
| Structured work | tandem API | goals, projects, tasks, areas, contexts | agent (via tandem-gtd CLI) |
| Unstructured context | tandem **wiki** | markdown articles | user (initial) + agent (updates) |
| Agent working memory | wiki `agent-state` + project "PM Queue" | rewritten each run | agent only |
| Session log | `~/.pi/agent/sessions/tandem-pm/*.jsonl` | pi JSONL | pi (auto) |
| Digest cache | `~/.tandem-pm/digest-YYYY-MM-DD.md` | Markdown | cron mode only |

## The six wiki articles

### `about-me`

**Purpose:** Life circumstances, constraints, energy patterns, roles. The "user model".

**Owner:** User seeds it. Agent appends when it learns new persistent facts (e.g., "user mentioned they're getting married" → `about-me` gets a "Spouse: Marie" line).

**Init template:**

```markdown
# About me

## Life
- Location:
- Work:
- Energy patterns (when are you sharp / when are you low):
- Time zones:
- Constraints (e.g., "no calls after 19:00", "Fridays are admin-only"):

## Roles & relationships
- Family:
- Close collaborators:
- Reports to / manages:

## Currently in motion
- Active life projects (e.g., "naturalisation in progress", "moving in Q3"):
- Active health / fitness goals:
- Active learning:
```

### `current-focus`

**Purpose:** Rolling 4-week focus. What the agent should prefer when promoting items; what the dashboard should highlight.

**Owner:** Agent rewrites weekly (during `review` workflow). User can override by editing directly.

**Init template:**

```markdown
# Current focus (4-week window)

_Updated: never_

## This window
(none yet)

## Deferred
(none yet)
```

**Update rule:** Agent rewrites this on:
- Every `review weekly` run
- When an item promoted to a project materially shifts the focus
- When a project completes and frees bandwidth

### `how-i-work`

**Purpose:** User preferences. The "operating manual" for the agent.

**Owner:** User-editable. Agent suggests additions; never edits without asking.

**Init template:**

```markdown
# How I work

## Task hygiene
- Preferred task title length (words): 8
- Title case style: lowercase (e.g., "draft blog post on X")
- Default context: @Computer
- Default energy for new tasks: medium
- Default estimated minutes for unclear tasks: 30

## Trash patterns (cron mode only)
- Items matching these regexes get auto-trashed in cron:
  (none yet — add patterns like `^spam from .*` to enable)

## Defer patterns
- Items matching these are auto-moved to Someday/Maybe:
  (none yet)

## Energy budget
- Max high-energy tasks per day:
- Max medium-energy tasks per day:

## Review cadence
- Weekly review: Sunday 18:00
- Monthly review: first Sunday of month

## What the agent should NEVER do
- (e.g., "do not contact my mother")
- (e.g., "do not suggest meditation")

## Clarification defaults
- Max pm-question rounds before forcing a decision: 3
- Always confirm before trashing in interactive: true
- Always confirm before promoting to project in interactive: true
```

### `people`

**Purpose:** People the user works with or mentions. Richer than `tandem waiting --person` because it persists past the wait.

**Owner:** Agent appends whenever a name comes up in a clarifying conversation. User can edit.

**Format:** One section per person:

```markdown
# People

## Marie Dupont
- Role: spouse
- Context: also applying for FR citizenship; works in finance
- First mentioned: 2026-06-14 (naturalisation PM Q)
- Last interaction: 2026-06-14

## Jane (last name?)
- Role: colleague at <company>
- Context: working on <project>; mentioned Q2 retro
- First mentioned: 2026-05-20
- Last interaction: 2026-05-20
```

### `glossary`

**Purpose:** Domain terms the user uses. Prevents the agent from asking "what's an OAT?" when the user writes it casually.

**Owner:** Agent appends when a term appears > 2 times and its meaning is non-obvious from context.

**Format:**

```markdown
# Glossary

## OAT
- Full term: Origination Account Takeover
- Domain: fraud
- First seen: 2026-04-12

## GMF
- Full term: Generate My Future (project codename)
- Domain: internal
- First seen: 2026-05-01
```

### `agent-state`

**Purpose:** The only article the agent fully owns. Rewritten (not appended) on each run.

**Format:**

```markdown
# Agent state

_Last run: YYYY-MM-DD HH:MM (mode: interactive|cron|batch)_

## In flight
- N active delegations (list with: task-id, subagent session path, started at)
- M PM questions waiting on user (list with: task-id, original item, asked at)

## Last digest delivered
- YYYY-MM-DD — <one-line summary>

## Run log (last 20 entries)
- [YYYY-MM-DD HH:MM] <item-id>: <classification> → <action>
- ...
```

**Append-vs-rewrite rule:** § In flight and § Last digest are **rewritten** every run. § Run log is **appended then trimmed** to last 20 entries.

## PM Queue project

A tandem project (not a wiki article) with:

- **Title:** "PM Queue"
- **Type:** `SINGLE_ACTIONS`
- **Description:** "Agent's clarifying-question queue. Each task = one open question. Title starts with `PM Q:`. User answers by editing task notes or via /skill:tandem-pm clarify-pending."
- **Status:** `ACTIVE`

**Task shape in PM Queue:**

```yaml
title: "PM Q: <topic> — <specific question>"
notes: |
  ## Original item
  <inbox item content, with id and capture date>

  ## Open question
  <the specific question, phrased for the user>

  ## Round 1 (YYYY-MM-DD HH:MM)
  Asked: <what was asked>
  Answer: <user's answer, if any>

  ## Round 2 (YYYY-MM-DD HH:MM)
  ...
```

**Lifecycle in PM Queue:**

1. Created by the agent when it classifies an inbox item as CLARIFY.
2. Lives there until the user answers enough rounds OR the question budget is exhausted.
3. When actionable: agent creates the real project/task, marks the PM Queue task COMPLETED with a `resolution:` note in its own notes.
4. When budget exhausted without resolution: agent marks the PM Queue task COMPLETED with `resolution: deferred-to-user` and a one-line summary in the digest.

## Tiered hydration (read model)

Hydration is **tiered** — the goal is that a run pays only for the context a specific decision needs.

| Tier | What | Size | When |
|---|---|---|---|
| **brief** (default) | 6 wiki articles trimmed (see skip table below) + open tasks & completions ≤ 14d + inbox + goals + computed coach signals | ~ 17 KB | every run |
| **detail** (`--detail <slug>`) | one wiki article in full | ~ 1–4 KB | when a decision needs an omitted section |
| **full** (`--full`) | legacy unfiltered dump | ~ 25 KB | interactive debugging only |

### Brief-mode skip table (defaults, overridable)

| Article | Trimmed in brief | Why |
|---|---|---|
| `about-me` | § Professional context, § Currently in motion | PM is personal-scoped (pro context on trigger); rolling state belongs to `current-focus` |
| `how-i-work` | § Subagent mapping, § PM scope, § Contact info, § Open preferences | stable policy, rarely needed verbatim; delegation.md carries fallback defaults |
| `agent-state` | all § Session summary except the last; § Run log trimmed to last 5 entries | continuity needs the latest, not the history |
| `glossary` | definitions body → term + full-term one-liners | disambiguation, not encyclopaedia |
| `people` | context body → name + role one-liners | presence check, not biography |
| `current-focus` | nothing (shown in full) | it IS the steering wheel |

Every omission is announced in the snapshot with the drill-down command, so the agent (and the user reading over its shoulder) always knows what's hidden.

### User overrides

Add or remove skips in `how-i-work` under a `## Hydration brief skips` section, one line per skip:

```markdown
## Hydration brief skips
- about-me: Some Section Title
```

These are merged over the script defaults (prefix match, case-insensitive). To *un-skip* a default, ask the user to remove/rename — the script has no negative syntax (on purpose: the default table stays the single source of truth).

### Manual hydration (no pm-run.sh)

If the pre-fetched snapshot is unavailable (bare `/skill:tandem-pm` invocation), hydrate surgically instead of bulk-fetching:

```bash
# Required
fetch-context.py --detail current-focus   # steering
fetch-context.py --detail how-i-work       # operating rules
# Then targeted reads, only as decisions require:
tandem wiki get about-me
tandem tasks list --json                   # signals live here (dueDate, updatedAt, energyLevel)
```

**Cache layer:** `fetch-context.py` caches to `~/.tandem-pm/state-cache.json`, TTL 60s (interactive) / 300s (cron), keyed by workflow + tier + detail. `--no-cache` bypasses, `--invalidate-cache` clears.

## Edit policy

| Article | Agent can edit? | When |
|---|---|---|
| `about-me` | append only | When a clarifying conversation reveals a new persistent fact |
| `current-focus` | full rewrite | Weekly review, or when focus shifts |
| `how-i-work` | never silently | Suggest in chat; user commits |
| `people` | append | New name appears in PM Q or delegation context |
| `glossary` | append | A term recurs and meaning is non-obvious |
| `agent-state` | full rewrite | Every run |

## First-run init flow

If any of the six articles is missing, the agent (in interactive mode) should:

1. Tell the user: "The PM skill expects 6 wiki articles. I'll create them now — I'll seed `about-me`, `current-focus`, and `how-i-work` with templates and ask you a few questions to fill them in. The other three start empty."
2. Create all 6 with their init templates.
3. Walk the user through `about-me` and `how-i-work` interactively (use `ctx.ui.input`).
4. Confirm the PM Queue project exists (create if not).

In cron mode: create the articles with templates only, no interactive population. User runs `/skill:tandem-pm setup` interactively when ready.

## Where the naturalisation example updates these

- `agent-state` — rewritten each run with the new run's log entry
- `about-me` — gains "Spouse: Marie, also applying for FR citizenship"
- `current-focus` — gains "Naturalisation — gather docs, file prefecture appt"
- `people` — gains "Marie Dupont" section
- PM Queue — gains (then loses) the 2 PM Q tasks
- The naturalisation project (existing) — gains notes linking back to the inbox item
