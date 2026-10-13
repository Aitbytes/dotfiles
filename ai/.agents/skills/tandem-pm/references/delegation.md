# Delegation — when and how to spawn subagents

The PM skill is a delegator, not a worker. For well-defined items, it spawns subagents (via `pi-subagents` `subagent()` in interactive mode, or via `pi --mode rpc` in cron mode) and tracks their progress in tandem.

## Capability routing — what agents CAN actually do

Before deciding HUMAN vs AGENT vs MIXED (see `references/coach.md` § Route), check the real capability surface:

**Agent-doable (no user in the loop):**
- Web research, comparisons, monitoring, summarization (`researcher`)
- Writing drafts, docs, articles (`worker` + humanized-writing)
- Code, repo work, refactors, tests (`worker`)
- **Infra & homelab operations** — SSH, Dokploy deploys, Proxmox/blithe stack, Terraform/Ansible (`worker`; glossary § blithe). Read-only ops by default; mutating ops need a user confirm unless `how-i-work` says otherwise.
- **Browser automation** — product research, form filling, scraping, cart preparation via the `steel-browser` / `browser-use` / `playwright-browser` skills (`worker` + skill). Prepare-only by default: agents stop before payment, identity-authenticated submission, or sending in the user's name.
- API / GitHub / data-pipeline operations

**Human-only (route: human):**
- Physical actions, in-person appointments, signatures, presence (technicien, magasin)
- Payments and anything identity-authenticated
- Personal decisions and anything in `how-i-work` § What the agent should NEVER do
- **Meta-work: creating the skills and connectors that expand what agents can do** — until the user delegates that too; when a new skill/connector lands, re-route past tasks during `review`

**Mixed (agent prepares, human finishes):** split into two linked tasks — one delegated ("préparer sélection + panier"), one human ("valider et payer").

**Routing corollary:** a stalled task that an agent could do 80% of is not a user problem — it's an unspawned delegation. The coaching move is to spawn it.

## When to delegate

Delegate when ALL of the following are true:

- The task is well-defined (single clear outcome, not "explore")
- The task is in scope for an existing skill (research, code, writing, travel, etc.)
- The user has either explicitly asked to delegate, or `how-i-work` defaults to delegation for that type
- The expected runtime is > 5 minutes (otherwise, just do it inline)

Do NOT delegate when:

- The task is a personal judgment call (delegating defeats the PM purpose)
- The task requires context the subagent can't have (e.g., a private conversation)
- The task is part of an active multi-turn PM Q (clarify first)
- The task is one of: reading a file, running a single command, sending a message

## Delegation policy: which subagent for which type

The default mapping lives in `how-i-work` § Subagent mapping. The skill's built-in defaults (using `pi-subagents` builtin agents):

| Item type | Subagent | Skill/prompt | Model |
|---|---|---|---|
| Research ("find X", "compare Y vs Z", "what's the state of the art in X") | `researcher` (builtin) | none — agent has its own system prompt | default (deepseek-v4-pro) |
| Heavy research (multi-wave, time-consuming) | `researcher` with deep_research hint | `~/.pi/agent/prompts/deep_research.md` | default |
| Code task (real engineering job in a repo) | `worker` (builtin) | none | default |
| Writing task (article, doc) | `worker` with `humanized-writing` skill | `~/.agents/skills/humanized-writing/` | default |
| Travel planning | `worker` with `travel-planner` skill | `~/.agents/skills/travel-planner/` | default |
| Retail product search | `worker` with `retail-research` skill | `~/.agents/skills/retail-research/` | default |
| Browser task (forms, scraping, cart prep) | `worker` + `steel-browser` (fallback `browser-use` / `playwright-browser`) | `~/.agents/skills/steel-browser/` | default |
| Infra / homelab op (blithe, Dokploy, Proxmox) | `worker` | — (glossary § blithe for paths) | default |
| Wiki / blog post | `worker` with `wikipedia-article` or `medium-blog` skill | `~/.agents/skills/wikipedia-article/`, `~/.agents/skills/medium-blog/` | default |
| Review / audit (looking at code or content) | `reviewer` (builtin) | none | default |
| Decision / scope check (architecture, model routing) | `oracle` (builtin) | none | default |
| Recon / codebase context | `scout` or `context-builder` (builtin) | none | default |

**Why `researcher` and not `worker + research-assistant`:** the `researcher` agent is purpose-built for web research and ships with a documented output format (`research.md`). The `worker` agent is for code writes. For M4 we use `researcher` for all research delegations; we only fall back to `worker` with a skill when the task type has no builtin agent (writing, travel, retail, etc.).

The user can override the mapping per-task by adding a `delegate-to: <subagent>` line in the task notes.

## Spawning a subagent

### Interactive mode (TUI / chat)

```typescript
// Inside the agent's tool call
subagent({
  agent: "worker",
  async: true,
  context: "fresh",  // fresh so the subagent doesn't inherit PM context
  task: `
    Implement the approved feature.

    Task context:
    - Project: <project-name> (tandem project id: <id>)
    - Task: <task-name> (tandem task id: <id>)
    - User notes: <notes from task>
    - Relevant wiki context: <paste from about-me, current-focus, glossary as needed>

    Validation contract:
    - <what "done" means>

    Return a handoff with: changed files, what was implemented, what was left undone,
    commands run with exit codes, validation evidence, surprises/risks, decisions
    needing PM approval.
  `,
  output: "~/.tandem-pm/delegations/<delegation-id>.md",
  outputMode: "file-only"
})
```

### Cron mode

```bash
# Recommended: use pm-run.sh --delegate (M4)
~/.tandem-pm/scripts/pm-run.sh --delegate <task-id> \
  --delegate-agent researcher \
  --delegate-output ~/.tandem-pm/delegations/nat-2026-06-14.md

# Manual: one-shot pi -p (no RPC needed for fire-and-forget research)
pi --name "pm-delegation-<task-id>" \
  --system-prompt "$(cat ~/.pi/agent/npm/node_modules/pi-subagents/agents/researcher.md | sed -n '/^---$/,/^---$/!p' | sed -n '1,/^---$/d')" \
  -p "$(cat <<'PROMPT'
You are a research subagent working on a delegated PM task.
Read the task from tandem (id: <task-id>). Research the topic, write your
deliverable to <output-path>, and exit.
PROMPT
)" \
  --no-session \
  --session-dir ~/.pi/agent/sessions/tandem-pm/delegations/$(date +%Y%m%d-%H%M%S) \
  > ~/.tandem-pm/delegations/<task-id>-$(date +%Y%m%d-%H%M%S).out 2>&1
```

The cron agent should use the `subagent()` tool with `async: true` and a delegation `output` file. The delegation status is tracked in `agent-state` § In flight.

## Tracking the delegation in tandem

Before spawning, the agent must:

1. Mark the task `IN_PROGRESS` in tandem (use `tandem tasks update <id> --status IN_PROGRESS --version N`).
2. Set the task's `externalLink` to the subagent session path or the delegation output file path.
3. Append to task notes:

   ```markdown
   ## Delegation (YYYY-MM-DD HH:MM)
   - Subagent: <name>
   - Skill: <skill used>
   - Session: <path>
   - Output: <path>
   - PM round: <which PM round triggered this>
   ```

4. Append a `delegations` entry to `agent-state` § In flight:

   ```markdown
   - [YYYY-MM-DD HH:MM] task=<id> subagent=<name> skill=<skill> session=<path> started
   ```

## On delegation completion

The PM agent (parent) receives the subagent's handoff and:

1. Reads the delegation output file.
2. Summarizes the outcome into the task notes (a `## Outcome` section).
3. If the subagent succeeded: mark task `COMPLETED` with `percentComplete: 100` and a `resolution:` line.
4. If the subagent needs user input or is blocked: push a new PM Q to the queue (e.g., "Subagent for 'naturalisation docs' asks: is your spouse's dossier identical or simplified procedure?").
5. If the subagent failed: leave the task `IN_PROGRESS`, append the error, surface in the digest.
6. Remove from `agent-state` § In flight.

## Delegation budget

To prevent runaway costs:

- Max concurrent delegations: 3 (configurable in `how-i-work` § Delegation budget)
- Max delegations per cron run: 5
- Per-delegation timeout: 30 minutes (configurable)
- If budget exceeded: defer to next cron run, log a digest warning

## Worked example: naturalisation research

**Trigger:** PM Q resolved; first next-action = "List required documents for FR naturalisation procedure in 2026".

**Classification:** Research task, well-defined, in scope of `researcher` builtin agent.

**Spawn (cron / batch via pm-run.sh):**

```bash
~/.tandem-pm/scripts/pm-run.sh --delegate <task-id> \
  --delegate-agent researcher \
  --delegate-output ~/.tandem-pm/delegations/nat-2026-06-14.md
```

This single command:

1. Fetches the task from tandem
2. Pre-fetches relevant wiki context (about-me, current-focus, glossary)
3. Spawns a `pi -p` one-shot session with the `researcher` system prompt
4. The researcher agent does web research and writes the deliverable to the output path
5. Updates the task: `IN_PROGRESS` → (awaiting user review) and links the output
6. Logs the delegation in `agent-state` § In flight
7. Returns the delegation id to the caller

**Spawn (interactive, from the PM agent's own tool call):**

```typescript
subagent({
  agent: "researcher",
  async: true,
  context: "fresh",
  task: `
    Research the official documentation and popular discourse around the French
    naturalisation procedure in 2026. Produce a checklist of required documents
    and a curated set of tips and common pitfalls.

    User context (from tandem wiki):
    - Resident in France for 3 years
    - B1 French
    - Married, spouse also applying (self-initiated, not employer-sponsored)
    - Target apply date: ~ 6 months from now

    Source priorities (in order):
    1. Official French government sources (service-public.fr, prefecture pages)
    2. Reputable legal-aid or immigration-lawyer explainers
    3. Recent first-hand accounts (Reddit r/france, forums; YouTube testimonials)
    4. Skip: SEO-driven "apply for citizenship" content farms

    Deliverable:
    - A Markdown checklist of required documents, with each item annotated
      "official source verified" or "community-sourced, verify"
    - Top 5 tips and top 5 pitfalls, each with a source link
    - A list of 3 next actions the user can do this week

    Save to: ~/.tandem-pm/delegations/nat-2026-06-14.md
  `,
  output: "~/.tandem-pm/delegations/nat-2026-06-14.md",
  outputMode: "file-only"
})
```

**On return (interactive):**

- The subagent's handoff is delivered via the intercom bridge.
- The PM agent reads the output file, updates the task: status COMPLETED, notes get a `## Outcome` section.
- Capture the checklist into the naturalisation project as a wiki article (or task sub-tasks).
- The user sees a complete answer and 3 actionable next steps.

**On return (cron):**

- Next cron run sees the delegation output file exists.
- The PM agent summarizes the result into a new digest entry, marks the task COMPLETED, captures the checklist into the project.

## Anti-patterns

- Delegating vague tasks (delegate after clarifying, not before)
- Delegating to a subagent without giving it user context (the subagent will ask "who is this user?")
- Delegating without updating tandem first (task stays NOT_STARTED, looks stalled)
- Spawning many parallel delegations for the same user question (wasteful, confusing)
- Delegating to a subagent that will itself spawn more subagents (chain depth > 1 not allowed by default; explicit fanout children only)
- Delegating with `context: "fork"` (the subagent inherits the PM session context, which leaks the PM's working state into the worker)
