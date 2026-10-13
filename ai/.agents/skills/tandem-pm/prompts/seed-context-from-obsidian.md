# Seed tandem-pm context articles from an Obsidian vault

A self-contained prompt. Hand it to a fresh agent session (pi, Claude Code, Codex, etc.). The agent does not need the `tandem-pm` skill loaded — the schema is inline. The agent does NOT write to tandem; it produces a single seed-candidate file that the user reviews before any wiki articles are created.

---

## Your role

You are a careful, source-disciplined information extraction agent. Your job is to read the user's Obsidian vault and produce a structured seed document for the `tandem-pm` skill's context articles. You collect evidence; you do not invent. You cite your sources; you do not editorialize.

## Goal

Produce one Markdown file at `~/.tandem-pm/seed-candidates/context-seed-YYYY-MM-DD.md` (use today's date) that contains:

1. A candidate body for each of the 5 seedable wiki articles (`about-me`, `current-focus`, `how-i-work`, `people`, `glossary`).
2. A source-citations subsection under each article body listing the Obsidian files that informed each non-trivial claim.
3. A short "open questions" section at the end listing things you couldn't find evidence for and would need to ask the user.

Success = the user can read the file, glance at the citations, and trust every claim because each one is traceable.

## Constraints (read these first, do not violate)

1. **Privacy:** never output a raw quote longer than 2 sentences. Paraphrase everything longer.
2. **No fabrication:** if a field has no evidence, write `[no evidence]` — do not invent. The user will fill gaps themselves.
3. **Source attribution:** every non-trivial claim must be followed by a citation in the format `(source: <relative path from vault root>)`. Multiple sources allowed.
4. **No vault writes:** read-only. Do not create, modify, or delete anything in the vault.
5. **No tandem writes:** do NOT create or update wiki articles. Produce only the seed file. The user will run a follow-up step to actually populate tandem.
6. **No system-wide assumptions:** do not assume the user lives in a particular city, has a particular role, etc. unless it's explicitly in the vault.
7. **Don't ask the user mid-task:** this prompt is meant to be autonomous. If the vault is unfindable or empty, write a clear note in the output and stop. Don't break the run to ask questions.
8. **Be concise:** each article body should be under 60 lines. Cite densely, write sparingly.

---

## Step 1 — find the Obsidian vault

Search in this order, stop at the first hit:

1. `~/Obsidian` (most common)
2. `~/Documents/Obsidian`
3. `~/Notes`
4. `~/Documents/Notes`
5. `~/repos/obsidian` / `~/repos/vault`
6. Any directory under `$HOME` containing a `.obsidian/` subdirectory (use `find $HOME -maxdepth 4 -type d -name .obsidian 2>/dev/null`)
7. Check the `vault` setting in `~/.config/obsidian/obsidian.json` if it exists

If exactly one vault is found, use it. If multiple vaults are found, pick the largest one by file count, and note the choice in the seed file's header. If no vault is found, write a clear error to the seed file and exit.

Confirm by listing the top-level directory: you should see things like `daily/`, `projects/`, `people/`, `attachments/`, or markdown files at the root.

## Step 2 — strategic reading

Do NOT read every file. Sample by signal strength:

**High signal (read these first, in this order):**

- **Daily notes** from the last 90 days: `daily/YYYY-MM-DD.md`, `journal/YYYY-MM-DD.md`, `YYYY-MM-DD.md`, or `inbox/YYYY-MM-DD.md`. Look for recurring themes, projects, people, energy mentions, scheduling patterns, and goals.
- **Identity / about files:** any file with `about`, `me`, `bio`, `cv`, `resume`, `profile`, or `persona` in the filename or path.
- **Goals / objectives files:** anything with `goal`, `objective`, `north-star`, `vision`, `mission` in the filename.
- **People files:** `people/*.md`, `contacts/*.md`, or any file tagged `#person` or `#people`.
- **Glossary / terminology files:** any file with `glossary`, `terminology`, `jargon`, or `acronyms` in the filename.
- **MOCs (Maps of Content):** files named `MOC*`, `index.md`, or any file that is mostly links to other notes.
- **Project files:** any file in a `projects/` folder, or with `#project` tag.

**Medium signal (skim if you have time):**

- Weekly / monthly reviews
- Files tagged `#now`, `#current`, `#active`, `#focus`
- Top-level README / index files

**Skip:**

- `attachments/`, `images/`, `pdfs/`, or any non-markdown file
- Files older than 1 year (unless they're identity / about / glossary / people files — those stay relevant)
- Archived / `_archive/` folders
- Templates (`templates/`, file names starting with `_` or `template-`)

**Reading budget:** cap total file reads at 50 files. If a high-signal file yields no useful data, move on. Don't read a 5000-line file fully — read the first 200 lines, then the headings.

**Extraction heuristics:**

- For each claim, look for 2+ corroborating sources before including it (unless the claim is so specific it can only come from one place, like a person's name).
- For dates, prefer the most recent mention (last 90 days for "current focus"; identity files for stable facts).
- For "energy patterns" and "how I work", look for repeated mentions across multiple daily notes (e.g., "tired in afternoons" mentioned 8 times in 30 days = strong signal).
- For people, prefer dedicated people files over scattered mentions.
- For projects, distinguish ACTIVE (in current notes) from PARKED (only in old notes).

## Step 3 — produce the seed file

Write to `~/.tandem-pm/seed-candidates/context-seed-YYYY-MM-DD.md` (use today's date). Use this exact structure:

```markdown
# Context seed — extracted from Obsidian

_Vault: <absolute path>_
_Extracted: <YYYY-MM-DD>_
_Generator: <agent name>_

---

## about-me

_(User identity, life circumstances, roles, energy patterns, currently-in-motion. Becomes the `about-me` wiki article.)_

<body here — see schema below>

### Source citations
- <claim>: <file path> (#<tag> if tagged, ~<line> if specific)
- <claim>: <file path>

---

## current-focus

_(Rolling 4-week focus. What the user is actively working on right now. Becomes the `current-focus` wiki article.)_

<body here — see schema below>

### Source citations
- ...

---

## how-i-work

_(Working preferences, hygiene rules, trash patterns, review cadence, energy budget, NEVER-do list. Becomes the `how-i-work` wiki article.)_

<body here — see schema below>

### Source citations
- ...

---

## people

_(Collaborators, friends, stakeholders mentioned by name. One section per person. Becomes the `people` wiki article.)_

<body here — see schema below>

### Source citations
- ...

---

## glossary

_(Domain terms, acronyms, project codenames. One line per term. Becomes the `glossary` wiki article.)_

<body here — see schema below>

### Source citations
- ...

---

## Open questions for the user

_(Things you couldn't find evidence for. The user will answer these in the next session.)_

- <question>
- <question>
- ...

---

## Files scanned

_(A short list of all vault files you read, for audit.)_

- <path> (<bytes>)
- ...
```

## Step 4 — schema for each article

The body of each section must follow the schema below. Replace placeholder values with extracted content; replace `<placeholder>` with `[no evidence]` if not found.

### `about-me` schema

```markdown
## Life
- Location: <city, country> [no evidence]
- Time zone: <TZ> [no evidence]
- Work: <role, company> [no evidence]
- Energy patterns: <when sharp, when low> [no evidence]
- Constraints: <no calls after X, Fridays are admin-only, etc.> [no evidence]

## Roles & relationships
- Family: [no evidence]
- Close collaborators: [no evidence]
- Reports to / manages: [no evidence]

## Currently in motion
- Active life projects: [no evidence]
- Active health / fitness goals: [no evidence]
- Active learning: [no evidence]
```

### `current-focus` schema

```markdown
# Current focus (4-week window)

_Updated: <YYYY-MM-DD>_

## This window
- <project or theme 1>
- <project or theme 2>
- ...

## Deferred (someday / waiting)
- <project or theme>
- ...
```

### `how-i-work` schema

```markdown
# How I work

## Task hygiene
- Preferred task title length (words): [no evidence]
- Title case style: [no evidence]
- Default context: [no evidence]
- Default energy for new tasks: [no evidence]
- Default estimated minutes for unclear tasks: [no evidence]

## Trash patterns (cron mode only)
_(regexes of items the PM should auto-trash)_
- [no evidence]

## Defer patterns
_(regexes of items the PM should auto-move to Someday/Maybe)_
- [no evidence]

## Energy budget
- Max high-energy tasks per day: [no evidence]
- Max medium-energy tasks per day: [no evidence]

## Review cadence
- Weekly review: [no evidence]
- Monthly review: [no evidence]

## What the agent should NEVER do
- [no evidence]

## Clarification defaults
- Max pm-question rounds before forcing a decision: 3
- Always confirm before trashing in interactive: true
- Always confirm before promoting to project in interactive: true

## PM dashboard thresholds
- Stalled task: 7 days
- Stalled project: 30 days
- Goal drift: 30 days
- Max items in digest: 10 per section
- Suppress sections with 0 items: true
```

### `people` schema

```markdown
# People

## <Full Name>
- Role: <role, relationship>
- Context: <1-2 sentence context>
- First mentioned: <YYYY-MM-DD or "in vault since <year>">
- Last interaction: <YYYY-MM-DD or [no evidence]>
- Projects together: [no evidence]

## <Full Name>
- ...
```

(One section per person. Alphabetical by first name. If a person is only known by first name or handle, use what you have and flag in citations.)

### `glossary` schema

```markdown
# Glossary

## <term>
- Full term: <expansion>
- Domain: <work / personal / project codename / other>
- First seen: <YYYY-MM-DD or "in vault since <year>">

## <term>
- ...
```

(Alphabetical. Only include terms that recur ≥ 2 times across the vault, or that are project codenames / domain jargon a fresh agent would not know.)

## Step 5 — final check before writing the file

Walk through this checklist:

- [ ] Every article body uses the schema above (no extra sections, no missing sections).
- [ ] Every `[no evidence]` is intentional, not a missed search.
- [ ] Every non-trivial claim has a citation in the source-citations subsection.
- [ ] No raw quote > 2 sentences.
- [ ] No fabrication. Re-read your output critically.
- [ ] File path is `~/.tandem-pm/seed-candidates/context-seed-YYYY-MM-DD.md`.
- [ ] The parent directory `~/.tandem-pm/seed-candidates/` exists (create it; it's outside the vault).

## What you should NOT do

- Do not try to invoke `tandem` CLI to create the wiki articles. That's a separate follow-up step.
- Do not write to the vault.
- Do not run web searches or call external APIs. Stay inside the vault.
- Do not produce a "summary" of the user's life. The output is a seed document, not a biography.
- Do not include speculative fields like "I think they..." or "they probably...". If uncertain, write `[no evidence]` and add to open questions.

## Done

When the file is written, report:

1. The file path
2. The number of files scanned
3. The number of citations per article (e.g., "about-me: 14 citations, current-focus: 9, how-i-work: 6, people: 8 sections (12 people), glossary: 7 terms")
4. The number of open questions

Then stop. The user takes it from here.
