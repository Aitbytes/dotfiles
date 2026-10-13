# PM dashboard — drift, missed deadlines, stalled work

The dashboard sub-workflow surfaces the signals that distinguish "I have a lot of tasks" from "I'm drifting". Read this when the user invokes `/skill:tandem-pm dashboard`, when running the cron morning digest, or when a `review` is requested.

## The four signal families

### 1. Missed deadlines

**Signal:** Tasks with `dueDate` in the past and `status != COMPLETED` (and not DROPPED).

**Why it matters:** Either the user is over-committed, or the dates were wishful. Both are worth surfacing.

**Detection:**

```bash
# tandem CLI doesn't have a direct "past due" filter; fetch + filter
tandem tasks list --status NOT_STARTED --json
# then filter in the agent: dueDate < now AND status != COMPLETED
```

Or for tasks that are `IN_PROGRESS` past their due date — same rule.

**Surfacing format (digest):**

```markdown
## Missed deadlines (3)

- **M1: Skill skeleton + 4 reference docs ready** — due 2026-06-13 (1 day overdue)
- **Call dentist** — due 2026-06-10 (4 days overdue)
- **File Q2 expenses** — due 2026-06-05 (9 days overdue)
```

**Action recommendation:** For each, suggest one of:
- Reschedule (push `dueDate`)
- Delegate (if the work is well-defined and unstarted)
- Drop (if no longer relevant)
- Break down (if too big)

### 2. Stalled tasks

**Signal:** Tasks `NOT_STARTED` with no activity for > N days. Default N = 7, configurable in `how-i-work` § Stalled threshold.

**Why it matters:** A NOT_STARTED task is a promise the user made to themselves. Stale promises are cognitive load.

**Detection:**

```bash
tandem tasks list --status NOT_STARTED --json
# filter: createdAt OR lastUpdatedAt < (now - N days)
```

The `tandem` CLI doesn't expose `lastUpdatedAt` in the default list. The agent may need to use the API directly or infer from history.

**Surfacing format (digest):**

```markdown
## Stalled (>7d untouched, 5)

- **Write blog post on GTD agents** — untouched 12 days
- **Migrate old notes to new wiki** — untouched 9 days
- ...
```

**Action recommendation:** For each, suggest one of:
- Do it now (if < 30 min)
- Schedule it (give it a `scheduled` date)
- Break it down (if it was too vague to start)
- Delete (if no longer relevant)
- Delegate (if it became well-defined)

### 3. Stalled projects

**Signal:** ACTIVE projects with no task activity (no task created, completed, or updated) in > N days. Default N = 30, configurable in `how-i-work` § Project stall threshold.

**Why it matters:** Projects in the GTD sense are commitments. A project with no movement is a hidden abandoned promise.

**Detection:**

```bash
tandem projects list --status ACTIVE --json
# for each, fetch tasks, check recent activity
```

**Surfacing format (digest):**

```markdown
## Stalled projects (>30d, 2)

- **Compétences Agents IA** — no task activity in 47 days
  - Last action: completed "deep_research on agent skills" on 2026-04-28
  - Next-action tasks: 3 (all untouched)
- **Appartement équipement** — no task activity in 62 days
```

**Action recommendation:** For each:
- Does this still matter? If no → mark `SOMEDAY_MAYBE` or `DROPPED`
- Is the next-action still clear? If no → ask in PM Q
- Should this be broken down further?

### 4. Goal drift

**Signal:** HORIZON_3 or HORIZON_2 goals with no contributing task activity in > N days. Default N = 30.

**Why it matters:** Goals only matter if they have momentum. A goal with no contributing tasks in a month is a forgotten goal.

**Detection:**

```bash
tandem goals list --json
# filter by horizon, then check contributing projects/tasks
```

**Surfacing format (digest):**

```markdown
## Goal drift (>30d no contributing activity, 1)

- **Get French citizenship** — HORIZON_3, last contributing task 5 days ago
  - (Still on track — flagging because target window is approaching)

(no goals fully stalled today)
```

**Action recommendation:** For each drifted goal:
- Surface 1-2 next actions that would contribute
- If the goal is no longer relevant, mark it (no API to "abandon" a goal; surface in digest for user action)

### 5. Priority inversion (coach signal)

**Signal:** lower-energy tasks completed in the last 7 days while one or more HIGH-energy / `current-focus` tasks are stalled ≥ 7 days or overdue.

**Why it matters:** this is the difference between "busy" and "effective". It is also the signal where a naive PM turns into a nag — interpret strictly through `references/coach.md` § move 1 (Surface): facts, one question, one offer, **max one callout per digest**, framed around the goal not the person.

**Detection:** pre-computed in every brief snapshot under `## Coach signals` (`Completed last 7d` energy mix vs `HIGH stalled ≥7d`). No extra calls needed.

**Action recommendation:** pair the callout with exactly one of: decompose (PM does it), delegate (agent does it), shrink (5-min version), re-prioritize (update `current-focus`). Never surface inversion without one of these offers.

### 6. Routing debt (coach signal)

**Signal:** stalled tasks that fall in the agent-doable category (research, writing, code, infra/homelab ops, browser automation — see `references/coach.md` § Route) but were never delegated.

**Why it matters:** a to-do an agent could execute is PM inventory doing nothing. Delegating it IS the coaching move.

**Surfacing:** in the digest Suggestions — "Delegate X to Y (ready to spawn)" — or, in cron mode within delegation budget, just spawn it.

## Putting it together: the digest

The cron morning digest format:

```markdown
# PM Digest — YYYY-MM-DD

_Good morning. <one-line framing based on the day's signals.>_

## Top of mind (current-focus)
- <1-3 lines from current-focus wiki>

## Coach corner (max 3 lines — see references/coach.md)
- 1 priority-inversion callout (facts + one question + one offer)
- 1 stall question on the highest-impact stalled item
- 1 win (focus item completed / delegation returned)

## Missed deadlines (N)
- ...

## Stalled tasks (N)
- ...

## Stalled projects (N)
- ...

## Goal drift (N)
- ...

## Delegations in flight (N)
- ...

## Unanswered PM questions (N)
- ...

## Suggestions (3-5, one-liners each)
- Reschedule **Call dentist** to this week or drop it
- Promote **"naturalisation docs research"** — ready to delegate to research subagent
- Break down **Migrate old notes to new wiki** into 3 sub-tasks

_Run by `tandem-pm` cron at HH:MM. Next run: HH:MM._
```

## Detection implementation (cron mode)

Cron mode should produce the digest efficiently. Suggested approach:

```bash
# 1. Single bulk fetch
tandem tasks list --json > /tmp/tasks.json
tandem projects list --status ACTIVE --json > /tmp/projects.json
tandem goals list --json > /tmp/goals.json

# 2. Per-project task fetch (for stalled-project detection)
tandem --json projects get <id> | jq '.tasks' >> /tmp/all-tasks.json
# (loop over active project ids)

# 3. Hand to the agent with a digest-generation prompt
echo "Generate today's PM digest from these files..." | \
  pi --mode rpc --no-session \
     --session-dir ~/.pi/agent/sessions/tandem-pm/digest-$(date -I) \
     > ~/.tandem-pm/digest-$(date -I).md
```

The agent reads the files, applies the four signal families, produces the digest, and (optionally) sends a desktop notification.

## What to surface vs. what to hide

**Surface always:**
- Missed deadlines (N > 0)
- Goal drift (N > 0)
- A goal that's > 7 days from its implicit deadline (goals don't have hard dates; estimate from contributing task cadence)

**Surface in interactive mode, suppress in cron (too noisy):**
- Stalled tasks older than 30 days (probably the user knows and chose to defer)
- Stalled projects older than 90 days (might be intentionally parked)

**Never surface:**
- Completed tasks (the user did the work; celebrating is fine but not in the digest)
- Tasks in `WAITING` status (those are tracked, not stalled)
- DROPPED tasks
- SOMEDAY_MAYBE projects (those are deliberately parked)

## Threshold configuration

The thresholds above default to 7d / 30d / 30d. The user can override in `how-i-work`:

```markdown
## PM dashboard thresholds
- Stalled task: 7 days
- Stalled project: 30 days
- Goal drift: 30 days
- Max items in digest: 10 per section
- Suppress sections with 0 items: true
```

The agent reads these on every digest run. Defaults are used if missing.

## Anti-patterns

- Showing 50 stalled tasks at once (overwhelm; the user closes the digest). Cap at 10 per section; mention the rest in a "and N more, run `/tandem-pm dashboard full` to see all".
- Always recommending "do it now" (the user has finite energy; respect current-focus)
- Triggering panic by listing every missed deadline in order of age (lead with the most impactful)
- Producing the digest without suggestions (the user wants guidance, not a status report)
- Running the dashboard at the wrong time (08:00 local; not 04:00 when the user is asleep)
- More than one priority-inversion callout per digest (that's lecturing — `references/coach.md` tone guardrails)
- Surfacing inversion without an offer (complaint, not coaching)
- Recommending "break it down" as homework for the user when the PM could decompose it itself
