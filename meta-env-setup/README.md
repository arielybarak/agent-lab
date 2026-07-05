# meta-env-setup — a kit for building and evaluating Claude Code setups

Bootstraps a **Claude Code `.claude/` setup** for any repo — `CLAUDE.md`, skills, commands,
agents, hooks — then **measures** whether it's actually effective and minimal, instead of
assuming it is.

`stdlib only` · `zero third-party deps` · `24 tests passing`

> **Run everything from inside this folder** (`cd meta-env-setup`). Every path below is
> relative to here — copy or share the whole folder and it works as a unit.

## Contents
- [meta-env-setup — a kit for building and evaluating Claude Code setups](#meta-env-setup--a-kit-for-building-and-evaluating-claude-code-setups)
  - [Contents](#contents)
  - [The problem](#the-problem)
  - [Features](#features)
  - [Quickstart](#quickstart)
  - [How it works](#how-it-works)
  - [Evidence](#evidence)
  - [What's inside](#whats-inside)
  - [Install a setup into its target repo](#install-a-setup-into-its-target-repo)
  - [Tests](#tests)
  - [Conventions](#conventions)
  - [Tool pool — park blocks to save budget](#tool-pool--park-blocks-to-save-budget)

## The problem

In most `.claude/` setups, developers attempt to guess from the outside which tools an
AI will actually need.

> When you do a job, nobody should dictate your toolkit without understanding your actual
> workflow. The same logic applies to AI: a human speculating on what an agent needs is no
> better positioned than a stranger prescribing your toolbox. This kit reverses that
> dynamic. An agent—`setup-analyzer`—inspects the codebase and mines historical session
> transcripts to determine what is genuinely needed, grounding the setup in empirical
> usage rather than external guesswork.

**Rule of thumb: Let AI analyze which tools are needed for AI.**

Even with the right tools, three **major pain points remain:
- **Building it manually takes time you don't have.** → One command scaffolds the entire
  setup: see [Quickstart](#quickstart).
- **Evaluating quality is often subjective.** → [Score it, route-test it, ablate it](#features) —
  replace intuitive vibes with verifiable numbers.
- **Environments evolve; setups rot.** → Use `--stale` alongside `/upgrade-claude-setup`
  and `/setup-retro` (see [Features](#features)) to continuously refine what exists
  instead of starting over from scratch.

## Features

- 🏗️ **Scaffold a complete `.claude/` setup** — `CLAUDE.md`, skills, commands, agents, hooks —
  for any repo, from one command.
- 📊 **Score effectiveness, not just structure** — a 0–100 composite across trigger quality,
  specificity, redundancy, budget, and least-privilege. No model call, fully reproducible.
- 🕵️ **Catch staleness before it misleads** — `--stale --repo <path>` flags any block citing
  code that's been renamed, moved, or deleted (including pooled blocks).
- 🎯 **Route-test descriptions** — confirm each skill fires on the prompts it should, and
  stays quiet on the ones it shouldn't.
- 🧪 **Prove it with ablation** — `--ablate --execute` removes a block, reruns real tasks, and
  shows what actually broke (or didn't).
- 🔍 **Mine your own session history** — `tools/mine_transcripts.py` scans a repo's past
  Claude Code transcripts for repeated commands, throwaway scripts, and deploy-wait loops —
  pain the code alone never shows.
- 🧭 **An agent decides, not a human guessing** — a 9-determinant analyzer inspects the repo
  (and mines its own past session transcripts) to find the domain's inner loop, silent-drift/
  parity invariants, and iteration-cost economics, then asks the repo owner only what it
  genuinely can't infer itself.
- 🌱 **Greenfield mode** — on an empty repo, it interviews first and defers speculative blocks
  instead of guessing.
- 🔁 **Brownfield upgrade path** — import an existing setup + a backlog, reconcile block-by-
  block (ADD/FIX/REWRITE/KEEP/CUT).
- 📝 **`/setup-retro`** — ships into every generated setup, so the next painful session turns
  into a backlog automatically instead of evaporating.
- 🗂️ **Tool pool** — park a fully-built block for a later phase at zero routing-budget cost
  until you need it.
- 🔒 **Dry-run installs** — nothing lands in the target repo until you explicitly
  `install.sh --apply`.

## Quickstart

```bash
cd meta-env-setup
python tools/scaffold_claude_setup.py init claude-setups/<repo> --with-claude-md
python tools/scaffold_claude_setup.py add skill <name> --dir claude-setups/<repo> --desc "<what + when>"
# fill in the file (the claude-setup-scaffolder skill walks you through it), then:
python tools/validate_claude_setup.py claude-setups/<repo> --score
```

Or drive the whole pipeline — analyze, interview, scaffold, author, refine, prove — with one
command from inside a Claude Code session:
```
/new-claude-setup <repo>
```

## How it works

**Two entry points** depending on whether the repo already has a `.claude/`:
- **Greenfield** (no existing setup): `/new-claude-setup <repo>` — analyze (mining transcripts +
  nine determinants) → **interview the owner** → spec → scaffold → author → refine → **smoke-test
  every command**. On a truly empty repo (README/about only) the analyzer switches to **greenfield
  mode**: the interview leads, and speculative blocks are *deferred + noted* rather than pre-built.
- **Brownfield** (existing `.claude/` + a backlog): `/upgrade-claude-setup <repo>` — import →
  reconcile blocks (ADD/FIX/REWRITE/KEEP/CUT, incl. a `--stale` pass over existing blocks) →
  author → refine.
  - Backlog template: `templates/setup-backlog.md` (save as `<repo>/.claude/setup-backlog.md`) —
    or run **`/setup-retro`** inside the target repo (shipped into every generated setup) to author
    one from the session that surfaced the pain.
  - Import step: `python tools/scaffold_claude_setup.py import <repo> --dir claude-setups/<repo>`.

The meta-env runs **once per repo**, so it optimizes for *quality, not speed*: it
doesn't just scaffold and validate, it **measures effectiveness and iterates until
the numbers hit target**. The whole pipeline is one command — `/new-claude-setup` —
which orchestrates the agents:

```
analyze ─▶ interview ─▶ spec ─▶ scaffold ─▶ author ─▶ validate ─▶ refine ⟲ ─▶ smoke-test ─▶ prove ─▶ package
```
- **analyze** — `setup-analyzer`, mining transcripts first if any exist
- **interview** — AskUserQuestion on the analyzer's owner-only questions
- **refine** — `setup-critic` ⇄ `block-author`, looped to target
- **smoke-test** — every command executed once (dry-run for credentialed ones)
- **prove** — optional ablation (`--ablate --execute`)
- **package** — README + `install.sh`, ships `/setup-retro` by default

> **Note on minimalism:** "fewer, sharper blocks" applies to the **generated
> setups** (loaded every session in the target repo) — *not* to this meta-env, which
> is rich on purpose. The `--score`/`--ablate` loop enforces minimalism on the
> output; the kit itself spends freely to get there.

You can drive it end-to-end (`/new-claude-setup <repo>`) or run the steps by hand — see
[Quickstart](#quickstart) above for scaffolding a block, then:

**Validate (structural gate, fails CI on errors)**
```bash
python tools/validate_claude_setup.py claude-setups/<repo>
python tools/validate_claude_setup.py claude-setups/*/ .          # everything at once
```

**Evaluate effectiveness (is it helpful *and* minimal?)** — a 3-layer methodology, cheap
static guesses → behavioral proof. Only the validate gate above fails CI; these are advisory /
their own test suites.
```bash
python tools/validate_claude_setup.py claude-setups/<repo> --score                     # Layer 1: 0-100 audit
python tools/validate_claude_setup.py claude-setups/<repo> --stale --repo ../<repo>     # Layer 1b: any block gone stale?
python tools/validate_claude_setup.py claude-setups/<repo> --route                     # Layer 2: do descriptions route right?
python tools/validate_claude_setup.py claude-setups/<repo> --ablate                    # Layer 3: dry-run preview
python tools/validate_claude_setup.py claude-setups/<repo> --ablate --execute          # …actually run it
```
The `--score` composite blends five weighted heuristics over the always-loaded text —
**trigger** (0.35), **specificity** (0.25), **redundancy** (0.25), **budget** (0.10), and
**leastpriv** (0.05). What the score is made of, the eval data formats, and the honest limits
of each layer are in **[`evals/README.md`](evals/README.md)**.

**Refine to target (close the loop)** — measurement only matters if you act on it.
`/refine-setup` runs `setup-critic` → `block-author` repeatedly until:
> composite **≥ 85** · **0 `[CUT?]`** · routing **100%** · every spec failure mode covered.
```bash
# in the kit's own Claude Code session (cd meta-env-setup):
/refine-setup claude-setups/<repo>
```

## Evidence

Reproducible on a fresh clone — the kit's own `.claude/` is checked in (unlike generated
`claude-setups/<repo>/`, which is gitignored):

```bash
python tools/validate_claude_setup.py . --score          # → 90/100
python tools/validate_claude_setup.py . claude-setups/*/  # → 0 errors across the kit + 5 real setups
python tools/test_audit.py                                 # → 24/24 tests pass
```

The analyzer itself has closed 9 blind spots that a real production setup's post-hoc
critique surfaced — see [`plans/2026-07-03-analysis-phase-improvements.md`](plans/2026-07-03-analysis-phase-improvements.md)
for the full writeup.

## What's inside

| Folder | What it is |
|---|---|
| **`tools/`** | The machinery (stdlib-only Python, no deps): `scaffold_claude_setup.py` (create a `.claude/` skeleton, `--pool` to park a block), `mine_transcripts.py` (mine a repo's session transcripts for repeated commands/throwaway scripts/deploy-wait loops), `validate_claude_setup.py` (structural gate **+** effectiveness scoring/staleness/routing/ablation), `_ablation.py`, `test_audit.py`. |
| **`.claude/skills/`** | The kit's method skills (auto-activate when you work inside the kit): **`claude-setup-scaffolder`** (the whole pipeline), **`skill-creator-lite`** (author one skill well, sharpened against `--score`), and **`hook-design`** (when a hook earns its place + the event/exit-code/safety model). |
| **`evals/`** | The effectiveness methodology + per-repo eval data (task suites, routing tests). |
| **`cookbook/`** | A library of **proven block archetypes** (skills/commands/agents/hooks) distilled from the real setups, with copy-paste templates — incl. **`setup-retro`**, shipped into every generated setup so a painful session turns into a `setup-backlog.md` instead of evaporating. Start here instead of a blank `TODO`. |
| **`templates/`** | The **setup-spec** PRD the analysis step fills before scaffolding. |
| **`claude-setups/<repo>/`** | Ready-made `.claude/` setups authored for other repos, each with a dry-run `install.sh`. *(gitignored — generated output)* |
| **`.claude/`** | The kit's *own* setup — a multi-agent pipeline. Commands: `/new-claude-setup` (greenfield), `/upgrade-claude-setup` (brownfield), `/refine-setup`, `/audit-claude-setup`. Agents: `setup-analyzer` (inspect / reconcile), `block-author` (fill), `setup-critic` (judge + prescribe). Plus the method **`skills/`** (above). Auto-loads when you work from inside this folder. |

## Install a setup into its target repo
```bash
bash claude-setups/<repo>/install.sh            # dry-run (prints what it would copy)
bash claude-setups/<repo>/install.sh --apply    # actually copy into the real repo
```

## Tests
```bash
python tools/test_audit.py          # deterministic scorers, staleness, transcript miner, ablation verdict (mocked agent)
```

## Conventions
- Setups **complement** a repo's existing setup, never duplicate it.
- Descriptions state **what + when** (Claude routes on them).
- Hooks are **advisory by default**; hard-blocking is opt-in.
- Prefer **fewer, sharper** blocks **in the generated setup** — every description
  costs routing budget there. (The meta-env itself is rich; the `--score`/`--ablate`
  loop is what enforces minimalism on the output.)
- **Act on the measurements.** A setup isn't done when it validates — it's done when
  `/refine-setup` hits its targets.

## Tool pool — park blocks to save budget

A block built for a phase you're not in yet still costs routing budget sitting in
`.claude/skills/` (or `commands/`/`agents/`). Park it instead:

```
.claude/tools-pool/
├── skills/<topic>/<skill-name>/SKILL.md
├── commands/<topic>/<command-name>.md
└── agents/<topic>/<agent-name>.md
```

```bash
mv .claude/skills/<name>            .claude/tools-pool/skills/<topic>/   # park (frees budget)
mv .claude/tools-pool/skills/<topic>/<name> .claude/skills/              # promote when its phase starts
```

Claude Code only reads the active folders, so anything under `tools-pool/` is invisible until
you move it back. The scaffolder can park directly (`add skill <name> --dir <setup> --pool
<topic>`), and `--stale --repo` scans pooled blocks too, so a parked block can't rot unnoticed
before promotion.
