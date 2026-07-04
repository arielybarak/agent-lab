---
description: Upgrade an existing Claude Code setup using a setup-backlog — import the live .claude/ into claude-setups/<repo>/, reconcile blocks (ADD/FIX/REWRITE/KEEP/CUT), scaffold and author missing ones, validate and score, then refine until targets hold.
argument-hint: "<repo-path> [backlog-doc-path]"
---

Upgrade the Claude Code setup for: **$ARGUMENTS**

Brownfield counterpart to `/new-claude-setup`. The repo already has a `.claude/`;
the backlog (`setup-backlog.md` / `tooling-review.md`) says what to change. Goal:
work the backlog down to zero using the same author/validate/refine machinery —
never touching the real repo until `install.sh --apply`.

## Pipeline

1. **Import** — copy the repo's live `.claude/` (+ `CLAUDE.md`) into a working copy:
   ```bash
   python tools/scaffold_claude_setup.py import <repo-path> --dir claude-setups/<repo>
   ```
   Also grabs the root `CLAUDE.md` and surfaces any discovered backlog doc alongside.

2. **Locate the backlog** — check (in order):
   - `<repo>/.claude/setup-backlog.md` (the kit's own template)
   - `<repo>/.claude/tooling-review.md` (common in-the-wild name)
   - `$ARGUMENTS` second word (explicit path)
   - Ask the user if none found; or offer to author one from `templates/setup-backlog.md`.

3. **Reconcile** — delegate to **`setup-analyzer`** in *brownfield mode*: read the
   imported setup + the backlog together; run the staleness check on every existing
   block (`python tools/validate_claude_setup.py claude-setups/<repo> --stale --repo
   <repo-path>`) and fold its `stale-suspect` findings into the table; then produce a
   confirmed reconciliation table. The backlog usually *is* the owner's voice, so only
   interview (AskUserQuestion) for holes it leaves open — ask at this table stage.

   | Item | Block | Tag | Priority |
   |---|---|---|---|
   | Add `/stl-bench` | new command | ADD | 1 |
   | Fix `/hf-logs` tail | commands/hf-logs.md | FIX | 2 |
   | Rewrite `tactile-stl-geometry` | skills/tactile-stl-geometry | REWRITE | 3 |
   | Keep `hooks/sync-guard.py` | hooks/sync-guard.py | KEEP | — |

   Show the table, get a thumbs-up before editing anything.

4. **Work the backlog** (priority order) using existing machinery:
   - **ADD** → `scaffold add` the block, then delegate to **`block-author`** to fill it.
   - **FIX / REWRITE** → delegate to **`block-author`**: rewrite the specific file(s);
     self-score; show the diff before applying. For REWRITE (stale), state explicitly
     what the block used to say vs. what it must say now. For a command, **execute its
     backlog "Done when" check** — don't eyeball it; a FIX that never ran isn't fixed.
   - **KEEP** → leave untouched; log it in the summary.
   - **CUT / MERGE** → show the diff; confirm before removing.
   - **Hooks** → always opt-in: propose what it guards + event + advisory vs blocking;
     wait for a yes before scaffolding. Default advisory.

5. **Drive quality** — once the backlog items are done, hand off to **`/refine-setup
   claude-setups/<repo>`** and iterate until targets hold:
   > composite **≥ 85** · **0 `[CUT?]`** · routing **100%** · every backlog item addressed.

6. **Package** — refresh or write `claude-setups/<repo>/README.md` (what changed, how
   to install) and a dry-run-by-default `install.sh`. Real repo stays clean until:
   ```bash
   bash claude-setups/<repo>/install.sh --apply
   ```

## Rules
- **Never write into the real repo** — all edits land in `claude-setups/<repo>/`.
- **Hooks are opt-in — always ask.** Never add a hook without explicit approval.
- **Don't touch KEEP items** — the backlog named them for a reason.
- **Reconcile first, edit second** — get the table confirmed before touching any file.
- Done = targets in step 5 met AND every §2 backlog item has its done-check ticked.
</content>
