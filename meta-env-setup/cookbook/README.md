# cookbook — proven block archetypes

A library of **block patterns that keep recurring** across good Claude Code setups,
distilled from the kit's four reference setups (TinyML, SystemVerilog, C++ perf,
design-patterns curriculum). Don't reinvent a block from a blank `TODO` — start
from the closest archetype here, then specialize it to the repo.

This catalog is **self-contained** (sketches are inline). Where a real instance
exists in `claude-setups/`, it's named so you can read a filled example. Copy-paste
templates for the trickiest archetypes live in [`templates/`](templates/).

> **How to use:** the `setup-architect`/analyzer picks archetypes during "decide
> blocks"; the `block-author` instantiates one and specializes it; the
> `setup-critic` checks each still earns its place. Match the *pattern*, then make
> the *content* ruthlessly repo-specific — a generic instance scores badly and won't help.

---

## Skills — on-demand expertise

| Archetype | Use when | Real instance | The trap it removes |
|---|---|---|---|
| **Canonical-contract** | a domain artifact has a fixed shape you must not silently change | `audio-dsp-pipeline` (16 kHz/3 s/96-mel input contract) | someone "tidies" a parameter the model was trained on |
| **Methodology playbook** | a hard problem is solved by an expert procedure people do ad hoc | `timing-closure-playbook`, `benchmarking-methodology`, `ml-experiment-tracking` | reinventing (and botching) the procedure each time |
| **Resource/budget constraints** | hard ceilings are easy to forget | `tinyml-deployment` (Flash/PSRAM/**tensor arena**) | "it fits in Flash" while the arena overflows |
| **Execution model** | how the project actually runs is non-obvious | `colab-drive-workflow` (logic in `src/`, notebooks orchestrate) | logic written where it can't be tested/reused |
| **House format** | output consistency matters (docs/curriculum) | `pattern-lesson-format` | every lesson/report drifts in structure |

**Skill skeleton** (specialize every line):
```markdown
---
name: <kebab>
description: >-
  <distinctive domain nouns> for this project — <the specifics>. USE WHEN <real
  trigger phrasings>.
---
## When to Activate This Skill
- <trigger> · <trigger>
## <Core conventions / the procedure>
- <imperative, repo-specific steps; cite real files/commands>
## Gotchas
- <the exact thing people get wrong HERE — point to CLAUDE.md, don't restate it>
```

---

## Commands — repeatable, promptable workflows

| Archetype | Use when | Real instance |
|---|---|---|
| **Append-to-ledger** | decisions/changes need a durable, structured record | `decision-log` (appends an ADR entry) |
| **Scaffold-an-artifact** | you keep creating the same artifact shape | `new-experiment`, `new-rtl-module`, `new-lesson` |
| **Explain / translate** | a dense artifact is hard to read | `explain-rtl`, `explain-asm` |
| **Report / check** | a standard analysis is rerun often | `timing-report`, `sva-check`, `eval-report`, `perf-compare` |
| **Guided transform** | a repetitive code move has rules | `notebook-to-src` |

**Command skeleton:**
```markdown
---
description: <what it does + when to reach for it>
argument-hint: "<args>"
---
<The prompt that runs, in imperative voice.> Operate on **$ARGUMENTS**.
Pull live context with !`<cmd>` and @path/to/file where it sharpens the result.
```

---

## Agents — scoped, least-privilege roles

| Archetype | Use when | Real instance | `tools:` |
|---|---|---|---|
| **Read-only reviewer** | recurring domain review with house rules | `rtl-reviewer`, `cpp-reviewer`, `data-pipeline-reviewer` | `Read, Grep, Glob` |
| **Planner / architect** | a high-stakes design choice precedes building | `ml-experiment-planner`, `architecture-decider` | `Read, Grep, Glob` (+ `Bash` read-only) |
| **Auditor (quantitative gate)** | a property must be checked against limits | `model-size-auditor` (fits on device?) | `Read, Grep, Glob, Bash` |
| **Socratic mentor** | a learning repo — teach without spoiling | `socratic-mentor` | `Read, Grep, Glob` |

Ready-to-copy: [`templates/reviewer-agent.md`](templates/reviewer-agent.md). Rule:
**a reviewer never gets `Write`/`Edit`.** Give every agent an explicit "you do NOT" line.

---

## Hooks — deterministic automation (the enforcement superpower)

| Archetype | Event / matcher | Behavior | Real instance |
|---|---|---|---|
| **Frozen-region guard** | `PreToolUse` · `Edit\|Write\|MultiEdit` | **block** (exit 2) edits to a protected path/branch | `branch_guard` (project-A frozen) |
| **Quality/fairness nag** | `PreToolUse` · `Bash` | advise (exit 0 + stdout) before a risky action | `bench_fairness_guard` (cold cache, repeats) |
| **Wrong-place guard** | `PreToolUse` · `Edit\|Write` | advise when code lands in the wrong file | `notebook_logic_guard` |
| **Consistency reminder** | `PostToolUse` · `Edit` | nudge after editing a certain file type | `lesson_diagram_reminder` |
| **Secret guard** | `PreToolUse` + `settings.json` `deny` | block reads/writes of secret files | (compose: `deny: Read(./.env)` + guard) |

Ready-to-copy: [`templates/guard-hook.py`](templates/guard-hook.py). **Advisory by
default; blocking is opt-in.** A hook must never break a workflow on its own bug
(parse errors → exit 0). Wire it in `settings.json` and confirm the matcher fires
with a sample event JSON on stdin. For *how* to choose the event, exit code, and
safety model — and whether a hook is even the right block — see the
[`hook-design`](../.claude/skills/hook-design/SKILL.md) skill.

---

## CLAUDE.md — the always-loaded brief
Not an archetype but the backbone. Order that works: **the one overriding rule**
first → what the repo is → layout → exact build/test/lint commands (a newcomer must
run the tests from this file alone) → conventions → gotchas. Keep it tight; it loads
every session. Everything else *points* to it.

## Anti-archetypes (don't ship these)
- **The generic skill** ("best practices for Python") — no repo-specific failure mode → fails `--score` specificity.
- **The command that's really a rule** — if it's always true, it belongs in CLAUDE.md.
- **The kitchen-sink agent** with all tools and a vague scope.
- **The silent blocking hook** that can wedge a workflow when it misfires.
