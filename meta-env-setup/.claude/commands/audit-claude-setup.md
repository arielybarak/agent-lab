---
description: Validate and quality-review an existing Claude Code setup — structure + frontmatter + does each block pull its weight.
argument-hint: "<path to a setup folder or .claude/>"
---

Audit the Claude Code setup at: **$ARGUMENTS**

1. **Structural check** (gate) — run:
   ```bash
   python tools/validate_claude_setup.py $ARGUMENTS
   ```
   Report every error/warning and fix the easy ones (missing or placeholder
   descriptions, `name` ≠ folder).
2. **Effectiveness score** (automates the "does each block pull its weight" review):
   ```bash
   python tools/validate_claude_setup.py $ARGUMENTS --score
   python tools/validate_claude_setup.py $ARGUMENTS --route   # if a routing-tests.json exists
   ```
   Read off the composite score, the budget, and every `[CUT?]` / `[SHARPEN]` /
   `[HINT]` finding. These are advisory suspects, not verdicts — use your judgment.
3. **Human review** (what the score still can't see):
   - Does each **skill** encode the non-obvious thing people get wrong, or is it
     generic filler the score happened to miss?
   - Does each **command** replace real repeated work?
   - Does each **agent** have a crisp scope and least-privilege `tools`?
   - Any **duplication** with a setup already present in the target repo?
   - Are **hooks** advisory-by-default and unable to silently break flow?
4. **Verdict** — what to cut, what to sharpen, what's missing. Prefer fewer, better
   blocks. Show the diff before applying changes. To *prove* a block is removable
   rather than guess, point the user at ablation: `--ablate --execute` (see `evals/`).
