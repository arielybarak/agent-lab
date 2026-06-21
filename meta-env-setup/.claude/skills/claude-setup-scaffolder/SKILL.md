---
name: claude-setup-scaffolder
description: >-
  End-to-end method for designing a Claude Code (.claude/) setup for ANY repo —
  analyze the repo, decide which building blocks it needs (CLAUDE.md, skills, slash
  commands, subagents, hooks, settings), scaffold them with
  tools/scaffold_claude_setup.py, and validate with tools/validate_claude_setup.py.
  USE WHEN bootstrapping or improving an AI setup for a project, or when asked to
  "set up Claude Code for <repo>".
---

# Claude Setup Scaffolder

## When to Activate This Skill
- "Set up Claude Code for <repo>" / "give <repo> an AI setup"
- Designing or improving a `.claude/` configuration
- Deciding which of CLAUDE.md / skills / commands / agents / hooks a repo needs

## The building blocks (and when each earns its place)
| Block | Lives in | Add it when |
|---|---|---|
| **CLAUDE.md** | repo root | always — the project brief + the one rule that overrides others |
| **skill** (`.claude/skills/<n>/SKILL.md`) | on-demand expertise | a domain has non-obvious conventions worth loading only when relevant |
| **slash command** (`.claude/commands/<n>.md`) | a repeated, promptable workflow | "I keep asking for the same multi-step thing" |
| **subagent** (`.claude/agents/<n>.md`) | a scoped, tool-restricted role | read-only review, planning, auditing — work to isolate + least-privilege |
| **hook** (`settings.json` + script) | deterministic automation | enforce/remind a rule the model shouldn't have to remember (branch guard) |
| **settings.json** | permissions + hooks | cut prompts (allow safe cmds), protect secrets (deny .env), wire hooks |

Rule of thumb: **CLAUDE.md first, then a couple of high-value skills, then commands
for repeated workflows, then agents for review/planning, then hooks last.** Don't
ship a block that doesn't pull its weight — every skill description costs the
model's routing budget.

## Workflow
1. **Analyze the repo** — language, build/test commands, the *one rule that
   overrides others* (recall-first? frozen branch? no logic in notebooks?), the
   repetitive tasks, and where people get it wrong. The `setup-analyzer` agent does
   this read-only.
2. **Decide the blocks** from the table above. Favor a small, sharp set.
3. **Scaffold** the skeleton with the hub tool:
   ```bash
   python tools/scaffold_claude_setup.py init claude-setups/<repo> --with-claude-md
   python tools/scaffold_claude_setup.py add skill   <name> --dir claude-setups/<repo> --desc "..."
   python tools/scaffold_claude_setup.py add command <name> --dir claude-setups/<repo>
   python tools/scaffold_claude_setup.py add agent   <name> --dir claude-setups/<repo> --desc "..."
   python tools/scaffold_claude_setup.py add hook    <name> --dir claude-setups/<repo>   # then wire it in settings.json
   ```
4. **Fill in** each file. For skills, follow the `skill-creator-lite` skill (frontmatter
   `name` + a trigger-rich `description`; "When to Activate"; conventions; gotchas).
5. **Validate**:
   ```bash
   python tools/validate_claude_setup.py claude-setups/<repo>
   ```
6. **Add a README + install.sh** to the per-repo folder (what it is; how to install
   into the target repo — dry-run by default).
7. **Evaluate effectiveness** — validity ≠ usefulness. Operationalize the quality
   bar below instead of eyeballing it:
   ```bash
   python tools/validate_claude_setup.py claude-setups/<repo> --score   # budget, redundancy, trigger quality
   python tools/validate_claude_setup.py claude-setups/<repo> --route   # do descriptions fire correctly?
   python tools/validate_claude_setup.py claude-setups/<repo> --ablate  # which blocks earn their place? (preview)
   ```
   `--score`/`--route` are cheap static proxies (flag suspects); `--ablate --execute`
   is the behavioral proof of "minimal yet maximal". Methodology + eval data: `evals/`.

## House conventions for these setups (this hub)
- Per-repo setups live in `claude-setups/<repo>/`, **never** written into the real
  repo directly. A dry-run-by-default `install.sh` copies them over on request.
- Don't duplicate an existing setup — **complement** it (see `claude-setups/project-VLSI`:
  an engineering layer beside the repo's existing report layer, new names only).
- Descriptions must state **what + when** (trigger phrases). Claude routes on them.
- Hooks are **advisory by default**; hard-blocking is opt-in. Never ship a hook
  that can silently break a workflow.

## Quality bar (what "good" looks like)
- A newcomer could run the repo's tests from CLAUDE.md alone.
- Each skill encodes the thing people get wrong here, not generic best practice.
- Each command replaces a paragraph you'd otherwise retype.
- Each agent has a crisp scope and least-privilege `tools`.
- `validate_claude_setup.py` passes with 0 errors.
