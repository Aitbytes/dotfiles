# Cron mode — the always-on PM

This is the architecture for running the PM skill on a schedule. The goal: a low-overhead, fully autonomous loop that processes what it can, surfaces what it can't, and never blocks the user.

## The cadence

Three runs per day. Each is a single `pi --mode rpc` invocation with a short wake-up prompt. Sessions are persisted under `~/.pi/agent/sessions/tandem-pm/` so the user can `/resume` any run interactively.

| Run | Time (local) | Purpose | Output |
|---|---|---|---|
| Morning | 08:00 | Dashboard, missed deadlines, top-of-mind | Digest file + notification |
| Midday | 13:00 | Promote answered PM Qs, spawn any ready delegations | Inbox/tasks updated; digest append |
| Evening | 19:00 | Spawn research delegations, prep tomorrow | Delegation runs launched |

Why three and not one daily?

- Morning digest lands when the user starts the day.
- Midday catches any PM Q answers the user gave in the morning.
- Evening pre-stages research that will be ready by tomorrow's morning digest.

The user can adjust the cadence by editing the systemd timer (or cron table). Defaults are conservative; can be tuned to once-daily if 3x feels noisy.

## The entry point: `~/.tandem-pm/scripts/pm-run.sh`

This is the single entry point for all PM runs (interactive, cron, batch). It does the pre-fetch, composes the prompt, and dispatches to `pi`. **Do not invoke `pi` directly for PM work — always go through `pm-run.sh` so the agent has pre-fetched state.**

```bash
# Morning digest (08:00)
~/.tandem-pm/scripts/pm-run.sh dashboard --run-mode cron --name morning

# Midday promotion (13:00)
~/.tandem-pm/scripts/pm-run.sh process-inbox --run-mode cron --name midday

# Evening research spawn (19:00)
~/.tandem-pm/scripts/pm-run.sh process-inbox --run-mode cron --name evening
```

`pm-run.sh` does:
1. `tandem auth status` check
2. `~/.tandem-pm/scripts/fetch-context.py --workflow <name> --run-mode cron` to build the snapshot (with 5-min cache)
3. Composes prompt: skill pointer + pre-fetched context + workflow-specific instructions
4. Dispatches:
   - Interactive: `pi -p @prompt-file` (output to chat)
   - Cron: `pi --mode rpc ... @prompt-file` (output to digest file)

The session log lands at `~/.pi/agent/sessions/tandem-pm/<workflow>-<date>-<hash>.jsonl` so you can `/resume` any run interactively.

## Differences from interactive mode

| Aspect | Interactive | Cron |
|---|---|---|
| User prompt | `ctx.ui.input`, `ctx.ui.select` | None — read PM Queue, write to digest |
| Clarification | Inline multi-round | Create PM Q tasks |
| Trash | Ask before deleting | Move to Someday/Maybe (unless `how-i-work` has a trash pattern) |
| Delegation | `subagent()` with `async: true` | `subagent()` with `async: true` + delegation file output |
| Output | Chat | `~/.tandem-pm/digest-YYYY-MM-DD.md` + optional notification |
| Wiki updates | As needed, with care | Append-only; never rewrite `about-me` or `how-i-work` without a clear trigger |
| Errors | Surface in chat | Log to `.err` file; surface in next morning digest |
| Cost ceiling | (user is present) | Hard cap: 3 concurrent delegations, 5 delegations per run, 30 min per delegation |

## File layout on the cron host

```
~/.tandem-pm/
├── scripts/
│   ├── fetch-context.py        # pre-fetches PM state as Markdown
│   ├── pm-run.sh               # entry point: fetch + pi
│   ├── ensure-state.sh         # creates wiki articles + PM Queue if missing (TODO: M3)
│   └── notify.sh               # desktop notification
├── digest-YYYY-MM-DD.md         # per-day digests
├── delegations/                 # subagent output files
│   └── <delegation-id>.md
├── state-cache.json             # 5-min cache of fetch-context output
└── discarded/                   # archive of context demoted during audits

~/.pi/agent/sessions/tandem-pm/   # session logs (one per cron run, /resume-able)
├── morning-2026-06-14-<hash>.jsonl
├── midday-2026-06-14-<hash>.jsonl
└── ...
```

The `state-cache.json` is invalidated by running `~/.tandem-pm/scripts/fetch-context.py --invalidate-cache` after a write. TTL is 60s (interactive) / 300s (cron).

## What cron does NOT do

- **Never asks questions.** All clarification goes through PM Queue. The user must check the queue at least once a day.
- **Never deletes inbox items.** Defers them (SOMEDAY_MAYBE) or moves them to the trash-pattern-matched bucket.
- **Never silently edits `about-me` or `how-i-work`.** Only `agent-state`, `current-focus` (in review mode), `people`, and `glossary` are auto-rewritten.
- **Never starts an unbounded delegation chain.** If a subagent needs another subagent, it returns and the cron parent decides.
- **Never runs without a digest file.** If the digest file is empty after a run, the run is treated as failed.

## The cron run sequence (with pre-fetch)

Each cron entry runs the same script with a different `--name` and a different `--workflow`:

```bash
# 08:00 morning — produce the digest
~/.tandem-pm/scripts/pm-run.sh dashboard --run-mode cron --name morning

# 13:00 midday — promote PM Q answers, spawn ready delegations
~/.tandem-pm/scripts/pm-run.sh process-inbox --run-mode cron --name midday

# 19:00 evening — pre-stage tomorrow's research
~/.tandem-pm/scripts/pm-run.sh process-inbox --run-mode cron --name evening
```

The `pm-run.sh` script:
1. Checks `tandem auth status` (aborts if failed)
2. Runs `fetch-context.py --workflow X --run-mode cron` (5-min cache)
3. Composes prompt: skill pointer + snapshot + workflow instructions
4. Dispatches to `pi --mode rpc @prompt-file` (output to `~/.tandem-pm/digest-YYYY-MM-DD.md`)
5. The agent reads only the skill files (4 reads total — see SKILL.md "Pre-fetched context" section for the measured breakdown)

The cron run does NOT pass `run-mode=cron` in the message — the script passes `--run-mode cron` to `fetch-context.py` (which adjusts the snapshot: 5-min cache, no `agent-state` article in output). The skill auto-detects mode from the absence of interactive features in the prompt.

## Systemd timer (preferred over cron)

`~/.config/systemd/user/tandem-pm-morning.timer`:

```ini
[Unit]
Description=Tandem PM morning digest

[Timer]
OnCalendar=Mon-Sun 08:00:00
Persistent=true
Unit=tandem-pm-morning.service

[Install]
WantedBy=timers.target
```

`~/.config/systemd/user/tandem-pm-morning.service`:

```ini
[Unit]
Description=Tandem PM morning digest
After=network-online.target

[Service]
Type=oneshot
ExecStart=%h/.tandem-pm/morning-digest.sh
```

Enable:

```bash
systemctl --user daemon-reload
systemctl --user enable --now tandem-pm-morning.timer
# repeat for midday and evening
```

Why systemd over cron:

- Survives laptop sleep (with `Persistent=true`)
- Logs to journald
- Per-user timers (no root needed)
- Easy to inspect: `systemctl --user list-timers`

## Failure handling

Each script must:

1. Exit non-zero on failure.
2. Log the error to the `.err` file.
3. Send a desktop notification if the failure is critical (auth, no wiki state).

A weekly watchdog cron checks that digests have been produced for each of the last 7 days; if any are missing, it surfaces a "PM cron is broken" notification.

## Cost / resource budget

Defaults (configurable in `how-i-work`):

- Max tokens per cron run: 500k input / 100k output
- Max concurrent delegations: 3
- Max delegations per run: 5
- Per-delegation timeout: 30 min
- Max wiki reads per run (cache miss): 12
- Max task list fetches per run: 20

The agent checks these at the start of a run; if a previous run blew the budget, it skips and notifies.

## Manual override: running cron-mode interactively

To preview what a cron run would do, without committing:

```bash
~/.tandem-pm/morning-digest.sh --dry-run
```

The script passes `--dry-run` to pi, which (via a flag the skill checks) suppresses all writes and just prints the diff of what would have changed.

## Anti-patterns

- Running cron in a tty (use `--no-session` + `--mode rpc`)
- Blocking the cron entry on a slow subagent (delegations are `async: true`; cron returns as soon as the subagent is spawned)
- Editing `how-i-work` or `about-me` from cron (always user-mediated)
- Producing digests with 50+ items (cap at 10 per section)
- Sending a desktop notification for every cron run (only on failure or first success of the day)
- Forgetting the digest file (cron is "successful" only if a non-empty file is written)
