# dotfiles
my config since 04/2023

Machine configuration only: terminal, window manager, editors, themes, shell.

## `ai/` is a symlink, on purpose

`ai` points to a **separate private repository** —
[Aitbytes/agent-stack](https://github.com/Aitbytes/agent-stack) — which holds the
agent layer: skills, agents, prompts, tools, `bootstrap.sh`, `doctor.sh`, CI.
It used to live here as a plain directory. It was extracted because it had
outgrown this repo's job: it needed to be private (the skills name the homelab
and the Vault paths), it needed its CI to actually run (workflows only run from
the repository root), and it needed a single source of truth instead of a frozen
`git subtree split` living in a second repo.

The symlink exists so that **every hardcoded `~/dotfiles/ai/...` path keeps
working** — the skills reference each other through it, `doctor.sh` validates it,
and `~/.agents` still resolves through it.

```
~/dotfiles/ai  ->  ../repos/agent-stack
```

A fresh clone therefore gives a dangling `ai` symlink. To rebuild the layer:

```bash
git clone git@github.com:Aitbytes/agent-stack.git ~/repos/agent-stack
bash ~/repos/agent-stack/bootstrap.sh          # symlinks de découverte + venvs + doctor
```

## Note on history

`ai/` was removed from the index, **not from this repository's history**: the
full agent layer is still reachable in the commits before 2026-11-09. Rewriting
that history is a separate, deliberate operation.
