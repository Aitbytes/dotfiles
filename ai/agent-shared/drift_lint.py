#!/usr/bin/env python3
"""drift_lint.py — byte-equality guard for canonical blocks (research-stack refactor).

Checks that the CANONICAL BLOCK hosted in each master is pasted byte-identical
into its consumer skills:
  budgets.md           -> 6 executor skills
  user-preferences.md  -> 3 executor skills

Run after ANY edit to a canonical block. Exit 1 on drift.
"""
import hashlib
import sys
from pathlib import Path

HOME = Path.home()
MASTERS = {
    HOME / "dotfiles/ai/agent-shared/budgets.md": (
        "## CANONICAL BLOCK",
        "## Execution Audit block",
        ["retail-research", "social-marketplace-research", "research-assistant",
         "youtube-research", "reddit-research", "playwright-browser"],
        "## Execution Budgets (canonical block",
        "## Escalation & Reporting Contract (canonical, BINDING)",
    ),
    HOME / "dotfiles/ai/agent-shared/user-preferences.md": (
        "## 7. CANONICAL DISTILLED BLOCK",
        "## 8. Maintenance protocol",
        ["retail-research", "social-marketplace-research", "research-assistant"],
        "## User Preferences (distilled",
        "## Execution Budgets (canonical block",
    ),
}

def block_between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]

def skill_block(text: str, start: str, next_anchor: str) -> str:
    i = text.index(start)
    # the pasted block ends right before the next top-level section that follows it
    j = text.index(next_anchor, i) if next_anchor in text[i:] else len(text.rstrip()) 
    chunk = text[i:j].rstrip()
    # strip the '---' separator(s) that sit between the pasted block and the next section
    while chunk.endswith('---'):
        chunk = chunk[:-3].rstrip()
    return chunk + "\n"

def main() -> int:
    fail = 0
    for master_path, (m_start, m_end, skills, s_start, s_next) in MASTERS.items():
        master = master_path.read_text()
        mb = block_between(master, m_start, m_end)
        # extract fenced content for budgets (inside ```markdown fences); prefs block is raw
        if "```markdown" in mb:
            mb = mb[mb.index("```markdown") + len("```markdown\n"):mb.rindex("```")].rstrip() + "\n"
        digest = hashlib.sha256(mb.encode()).hexdigest()[:12]
        print(f"\n== {master_path.name} canonical {digest} ==")
        for s in skills:
            sp = HOME / f".agents/skills/{s}/SKILL.md"
            text = sp.read_text()
            if s_start not in text:
                print(f"  MISSING  {s} (no '{s_start}')")
                fail += 1
                continue
            got = skill_block(text, s_start, s_next)
            ok = got == mb
            fail += 0 if ok else 1
            print(f"  {'OK      ' if ok else 'DRIFT   '} {s}")
    print(f"\ndrift-lint: {'PASS' if fail == 0 else f'FAIL ({fail} problems)'}")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main())
