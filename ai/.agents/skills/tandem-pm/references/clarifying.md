# Clarification protocol

How the PM skill handles vague inbox items, ambiguous tasks, and stalled work that needs user judgment. Read this section whenever the core engine classifies an item as CLARIFY.

## The decision: when to clarify

Always clarify when ANY of the following is true:

- The item has no concrete verb ("thing about X", "naturalisation", "look into Y")
- The item has a verb but no clear object ("improve", "research")
- The item has both, but no scope ("research X" — what about X? for whom? by when?)
- The item references a person, project, or concept not yet in `people`, `glossary`, or `current-focus`
- Two or more plausible classifications apply (could be a project OR a task; could be a goal OR a someday/maybe)
- Energy, time, or deadline information is needed to make the action concrete

Do not clarify (just promote) when:

- The item is unambiguous and < 2 minutes (TRIVIAL)
- The item names a concrete next action with a clear object ("email X about Y", "buy Z")
- A matching project already exists with `current-focus` alignment — promote to that project as a next-action

## The question budget

The PM Queue question budget per inbox item is set in `how-i-work` § Clarification defaults. Default: **3 rounds**. After 3 rounds, the agent must:

- Make a best-guess classification
- Surface the guess + reasoning in the digest (cron) or chat (interactive)
- Let the user correct in the next session

A "round" is one cycle of ask → answer → re-evaluate. A single round can include multiple sub-questions in one `ctx.ui.input` if they're tightly related.

## How to ask

**Interactive mode:**

- Use `ctx.ui.input` for free-form answers; use `ctx.ui.select` for classification confirmations; use `ctx.ui.confirm` for yes/no.
- One question at a time, but group tightly related sub-questions into one input. Example for naturalisation:

  > "Round 1 of up to 3. A few quick ones to scope this:
  > - Current residency status (type of permit, how long)?
  > - Target timeline (when do you want to apply)?
  > - Current French level (B1, B2, etc.)?
  > - Target country (FR citizenship, or another)?
  > Answer any way — even one or two helps."

- Each round: show the prior answers so the user doesn't have to remember.

**Cron mode:**

- Never ask. Create a PM Queue task per round.
- Each task body lists the open question(s) in plain text. User answers by editing the task notes.
- Next cron run picks up answered questions and continues the loop.
- **Detection heuristic for "this round is answered":** the PM Q task's notes contain a section matching `^## Round N` that has both an `Asked:` line AND an `Answer:` line (i.e., the user wrote an answer). The cron agent should scan all PM Q tasks, find the highest answered round, and either:
  - Add the next round (if still vague and budget remains), OR
  - Re-classify and either promote or close.

**Multi-round in a single print/RPC invocation (testing or batch):**

- Accept a `--simulated-answers "round1: ..., round2: ..."` flag in the prompt.
- The agent treats these as if the user had answered each round, runs all rounds in one pass, then applies the core engine.
- This is for testing only — real cron mode never sees this flag.

## The clarification state machine

```
                        ┌────────────────────────────┐
                        │                            │
                        ▼                            │
                  ┌──────────┐                       │
                  │ UNPROC.  │  (tandem inbox)       │
                  └────┬─────┘                       │
                       │ core engine classifies      │
                       ▼                             │
              ┌────────────────┐                      │
              │  NEEDS-CLARIFY │ ◀──────────────────┤
              │   (PM Q task)  │                    │
              └────┬───────────┘                    │
                   │ user answers (interactive      │
                   │  or cron-detected)             │
                   ▼                                │
       ┌────────────────────────┐                   │
       │  re-evaluate           │                   │
       │  - still vague?        │                   │
       │  - budget left?        │                   │
       └─┬──────────┬───────────┘                   │
         │          │                               │
    yes  │          │ no                            │
         ▼          ▼                               │
   next PM Q    ┌──────────────┐                    │
                │ READY        │                    │
                │ (actionable) │                    │
                └──────┬───────┘                    │
                       │ core engine creates        │
                       │ task/project/goal          │
                       ▼                            │
                ┌──────────────┐                    │
                │  PROMOTED    │ ───────────────────┘
                │ (PM Q done)  │   link to original
                └──────────────┘   item in notes
```

## Question design rules

A good clarifying question is:

1. **Specific** — names the dimension ("FR language level", not "tell me more about yourself")
2. **Bounded** — the answer fits in a sentence or two
3. **Orthogonal** — doesn't overlap with other questions in the same round
4. **Decision-enabling** — the answer should change the agent's next move

Bad: "Tell me everything about naturalisation."
Good: "Round 1. Three quick ones: (1) Current permit type and how long? (2) Target apply date? (3) Current French level?"

## Linking PM Q tasks back to inbox items

The PM Queue task notes must always contain:

```markdown
## Original item
- Inbox id: <inbox-id>
- Captured: <date>
- Content: <verbatim>

## Open question
<the specific question>
```

This lets `tandem inbox process <id>` (run later when resolved) find the context, and lets the user `/resume` the inbox item's history.

## Resolution: how PM Q closes

When the agent promotes the original item (creates the real task/project/goal), it:

1. Marks the PM Queue task `COMPLETED`
2. Updates its notes with a `## Resolution` section:

   ```markdown
   ## Resolution (YYYY-MM-DD HH:MM)
   - Created project: <name> (<id>) — or — Created task: <name> (<id>) — or — Linked to existing project: <name> (<id>)
   - Round used: N of M
   - User effort: <short description>
   ```

3. Optionally captures any new persistent context (person, term, preference) into the relevant wiki article.

## When clarification is FORBIDDEN

Some items must not go to PM Q, even if vague. They get promoted with a best-guess:

- "Test inbox item from API" — clear test, drop after flagging in `agent-state`
- One-word jargon the user uses casually (just add to `glossary` and drop)
- Items captured by the agent itself (e.g., "agent: detected stalled task X" — agent decides unilaterally)

## PM Q task: complete creation template (copy-paste ready)

When the core engine classifies an item as CLARIFY, the agent must create a PM Queue task with this exact structure. The PM Queue project id is fetched on every run via `tandem projects list --status ACTIVE` (filter by title "PM Queue").

```bash
# 1. Find the PM Queue project id
PMQ_ID=$(tandem --json projects list --status ACTIVE | python3 -c "
import sys, json
for p in json.load(sys.stdin):
    if p.get('title') == 'PM Queue':
        print(p['id']); break
")

# 2. Create the task with the structured notes (use heredoc to preserve markdown)
tandem tasks create "PM Q: <TOPIC> — <SPECIFIC QUESTION>" \
  --project-id "$PMQ_ID" \
  --notes "$(cat <<'NOTES'
## Original item
- Inbox id: <INBOX_ID>
- Captured: <CAPTURED_AT>
- Content: <VERBATIM>
- Notes: <INBOX_NOTES_IF_ANY>

## Open question

<the specific question, phrased for the user>

Example for "naturalisation":
## Open question
Round 1 of 3. A few quick ones:
- Current residency status (permit type, how long)?
- Target timeline (when do you want to apply)?
- Current French level (B1, B2, etc.)?

## Round 1 (<TIMESTAMP>)
- Asked: <what was asked>
- Answer: <user fills this in by editing the task notes>

## Round 2 (<TIMESTAMP>)
- Asked:
- Answer:
NOTES
)"
```

The agent's job on subsequent runs is to:
1. Find PM Q tasks in the PM Queue project
2. For each, check the notes for an `Answer:` line under the latest `## Round N` header
3. If answered: re-evaluate (still CLARIFY → add Round N+1, or PROMOTED → create the real task and mark COMPLETED)
4. If not answered: skip (the user hasn't responded yet)

## PM Q task: concrete example (naturalisation, round 1 created)

```bash
PMQ_ID="cmqdznx9l00fs51cwxe0ch0y1"  # from the user's instance

tandem tasks create "PM Q: naturalisation — residency + timeline + language?" \
  --project-id "$PMQ_ID" \
  --notes "$(cat <<'NOTES'
## Original item
- Inbox id: cmqe1ed3h00i151cw5ytrveux
- Captured: 2026-06-14T<actual>Z
- Content: naturalisation
- Notes: M3 test case for the clarifying protocol. Simulate multi-round clarification: residency, timeline, language, target country.

## Open question

Round 1 of 3. A few quick ones to scope this:
- Current residency status (type of permit, how long)?
- Target timeline (when do you want to apply)?
- Current French level (B1, B2, etc.)?

## Round 1 (2026-06-14 <actual_time>)
- Asked: residency, timeline, language
- Answer:
NOTES
)"
```

The agent's run on a future cron tick would see the task in the PM Queue, find that the user has filled in the `Answer:` line, and continue.

## Worked example: naturalisation, full trace

| Round | Trigger | Question | Answer | Re-classify |
|---|---|---|---|---|
| 0 | Inbox capture "naturalisation" | — | — | CLARIFY (no verb) |
| 1 | `/skill:tandem-pm process-inbox` (interactive) | 4 sub-questions: residency, timeline, language, target country | "FR resident, 3 years, B1 FR, applying in 6 months" | CLARIFY (need: docs, marital, sponsored?) |
| 2 | Same session, next `ctx.ui.input` | "What docs have you gathered? Married? Sponsored or self-initiated?" | "Nothing yet. Married, spouse also applying. Self-initiated." | READY (have: scope, timeline, status, marital, mode) |
| 3 | Core engine: detect existing project "Naturalisation française" (id `cmqb3yy7k006g51cwh7ykgry0`) → link, don't create | — | — | PROMOTED (next-action: "List required documents for FR naturalisation 2026") |
| 4 | Classify next-action: research → DELEGATE → spawn deep_research subagent | — | — | DELEGATED |

User effort: 2 short answers, ~ 3 minutes. Agent effort: ~ 12 tool calls, ~ 90 seconds.

## Edge cases

- **User says "I don't know"** to a sub-question: agent skips that dimension, may re-prioritize others, may re-classify as SOMEDAY/MAYBE.
- **User says "later"**: PM Q task stays in queue, but agent bumps its `scheduled` date if the user named one.
- **User contradicts a prior answer**: PM Q notes get a "Contradiction" section; agent asks for resolution.
- **Multiple inbox items share the same PM Q** (e.g., "naturalisation" and "ceremony prep"): agent detects this, links them, asks one PM Q that covers both.
- **PM Queue grows past N items** (default 10): agent pauses accepting new PM Qs, surfaces a digest item "PM Queue is full — please review".

## Anti-patterns

- Asking 5 sub-questions in one round (cognitive load; user abandons)
- Asking the same dimension twice across rounds (annoying)
- Asking a question whose answer is already in `about-me` (read the wiki first)
- Re-classifying a PM Q as TRIVIAL just to close it (defeats the point)
- Skipping clarification because the item is "probably obvious" (the whole point of PM is to remove guessing)
