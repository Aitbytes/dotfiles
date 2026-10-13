---
name: tandem-gtd
description: Interact with a Tandem GTD instance via its REST API. Create and manage tasks, projects, areas, goals, contexts, inbox items, waiting-for items, weekly reviews, horizon reviews, wiki articles, teams, routines, time tracking, and more. Use when the user wants to capture thoughts, organize projects, check their task list, start a review, or manage any GTD workflow in Tandem.
---

# Tandem GTD

Tandem is a Getting Things Done (GTD) productivity system built with Next.js. Use the `tandem` CLI for all interactions — it handles auth, formatting, and provides discoverable help at every level.

## Setup

The API key is stored in HashiCorp Vault. Login once:

```bash
tandem auth login
```

This runs `vault login` and retrieves the key. Verify connectivity:

```bash
tandem auth status
```

### Alternative auth methods

Set the `TANDEM_KEY` environment variable, or use `tandem config set-api-key <key>` to store it in `~/.config/tandem-gtd/config.json`. The default instance URL is `https://gtd.aitbytes.fyi` — override with `tandem config set-base-url <url>`.

## Discovery

The CLI is self-documenting. Explore at every level:

```bash
tandem --help                  # All commands
tandem tasks --help            # Task subcommands
tandem tasks create --help     # Create task flags + examples
tandem help tasks create       # Same as above
tandem help inbox capture      # Discovery path
```

Every subcommand includes an `Examples:` section showing real-world usage.

## GTD Workflow (5 Steps)

1. **Capture** → `tandem inbox capture "thought"`
2. **Clarify** → `tandem inbox process <id>`
3. **Organize** → `tandem tasks create "title" --project-id <id> --context-id <id> --energy high`
4. **Reflect** → `tandem reviews start --notes "Weekly review"`
5. **Engage** → `tandem tasks available` or `tandem ai context`

## Most Common Commands

```bash
# Inbox
tandem inbox capture "Fix leaking faucet" --notes "Under the kitchen sink"
tandem inbox list --status UNPROCESSED
tandem inbox process <id>

# Tasks
tandem tasks list
tandem tasks list --status NOT_STARTED --due today
tandem tasks available                          # What to work on right now
tandem tasks tickler                            # Deferred tasks
tandem tasks create "Call dentist" --energy low --mins 15 --context-id <id>
tandem tasks update <id> --status COMPLETED --version 1
tandem tasks complete <id>                     # With cascade
tandem tasks bulk-update --ids id1,id2 --status COMPLETED

# Projects
tandem projects list --status ACTIVE
tandem projects create "Redesign website" --type SEQUENTIAL --outcome "New site live"
tandem projects outline                         # Full tree view

# Contexts
tandem contexts list

# Reviews
tandem reviews start --notes "Weekly review - Week 24"
tandem reviews current

# Dashboard & Search
tandem dashboard
tandem search "marketing plan"
```

## Output Formats

All commands support `--json` for raw JSON output (useful for piping to `jq`). Default is human-readable tables with colored status indicators.

## Full CLI Reference

For a complete listing of every subcommand with examples, run `tandem --help` and drill down from there. The CLI covers all Tandem API domains:

| Domain | Command | Quick Example |
|--------|---------|---------------|
| Tasks | `tandem tasks ...` | `tandem tasks list --due today` |
| Projects | `tandem projects ...` | `tandem projects create "Name" --type SEQUENTIAL` |
| Inbox | `tandem inbox ...` | `tandem inbox capture "Thought"` |
| Contexts | `tandem contexts ...` | `tandem contexts create "@Garden"` |
| Areas | `tandem areas ...` | `tandem areas create "Health"` |
| Goals | `tandem goals ...` | `tandem goals create "Goal" --horizon HORIZON_3` |
| Reviews | `tandem reviews ...` | `tandem reviews start` |
| Waiting-for | `tandem waiting ...` | `tandem waiting create "Report" --person "Jane"` |
| Teams | `tandem teams ...` | `tandem teams create "Engineering"` |
| Threads | `tandem threads ...` | `tandem threads create --title "API?" --purpose QUESTION --project-id <id>` |
| Decisions | `tandem decisions ...` | `tandem decisions create --question "Which?" --type poll` |
| Routines | `tandem routines ...` | `tandem routines create --title "Morning" --cron daily` |
| Wiki | `tandem wiki ...` | `tandem wiki create "Guide" guide-slug --content "# Text"` |
| Time | `tandem time ...` | `tandem time start <task-id>` |
| AI | `tandem ai ...` | `tandem ai context --energy medium --time 30` |
| History | `tandem history ...` | `tandem history feed --days 7` |
| Search | `tandem search ...` | `tandem search "keyword" --scope tasks` |
| Notifications | `tandem notifications ...` | `tandem notifications list --unread` |
| Import/Export | `tandem export/import` | `tandem export --format json` |
| Config | `tandem config ...` | `tandem config show` |

## Reference Files (Raw API)

For debugging or raw curl access, the reference files document the underlying REST API directly:

| File | Content |
|------|---------|
| [`reference/tasks.md`](reference/tasks.md) | Task fields, dependencies, history, snapshots, NLP, bulk ops |
| [`reference/projects.md`](reference/projects.md) | Project fields, sub-projects, baselines, templates |
| [`reference/inbox-contexts.md`](reference/inbox-contexts.md) | Inbox + contexts endpoints |
| [`reference/areas-goals.md`](reference/areas-goals.md) | Areas of focus + goals with horizon levels |
| [`reference/reviews.md`](reference/reviews.md) | Weekly reviews + horizon reviews |
| [`reference/collaboration.md`](reference/collaboration.md) | Teams, threads, decisions |
| [`reference/time-tracking.md`](reference/time-tracking.md) | Timer, time audit, calendar |
| [`reference/routines.md`](reference/routines.md) | Routines with windows and items |
| [`reference/wiki.md`](reference/wiki.md) | Wiki articles, backlinks, history |
| [`reference/ai.md`](reference/ai.md) | AI context, capture, scaffold, chat |
| [`reference/meta.md`](reference/meta.md) | Dashboard, insights, history, search, notifications, import/export, settings, waiting-for |
