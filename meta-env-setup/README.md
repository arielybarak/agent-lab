# meta-env-setup — a kit for building & evaluating Claude Code setups

A self-contained toolkit for giving any repository a high-quality **Claude Code
(`.claude/`) setup** — and then *measuring* whether that setup is actually
effective and minimal, instead of guessing.

> **Run everything from inside this folder** (`cd meta-env-setup`). Every path in
> the docs below is relative to here, so the kit is portable: copy or share the
> whole `meta-env-setup/` folder and it works as a unit.

## What you actually get

**The deliverable** is a complete, installable **`.claude/` setup** for a target
repo — its `CLAUDE.md` plus the skills / slash-commands / subagents / hooks that
repo actually needs — landed under `claude-setups/<repo>/` with a dry-run
`install.sh`. It's **config-as-files** Claude Code reads, not a runtime or a library.

**The differentiator** is everything *around* that deliverable: the kit doesn't just
*generate* a setup, it **measures** whether each block earns its place — because every
always-loaded block costs the agent's routing budget, so "more" is not "better."

**How a setup is evaluated — three layers, cheap → expensive, static → behavioral:**

| Layer | Command | Answers | Cost |
|---|---|---|---|
| **1 · Inspection** | `--score` | Is each block well-targeted? (0–100) | instant, no model call |
| **1b · Staleness** | `--stale --repo <path>` | Does each block still describe code that *exists* (incl. pooled blocks)? | instant, no model call |
| **2 · Routing** | `--route` | Do descriptions fire on the right prompts (and stay quiet on the wrong ones)? | instant, no model call |
| **3 · Ablation** | `--ablate --execute` | Does *removing* a block actually hurt real tasks? | runs an agent many times |

Layers 1–2 are **cheap proxies** that flag suspects in seconds; only Layer 3 **proves**
a block can be cut. The **`--score`** number is a deterministic blend of five
heuristics over the always-loaded text — **trigger** (says *what* + *when*, 0.35),
**specificity** (grounded in this repo's `CLAUDE.md`, 0.25), **redundancy** (no echoed
or duplicate blocks, 0.25), **budget** (always-loaded cost stays sane, 0.10), and
**leastpriv** (agents narrow their `tools:`, 0.05). No model call, so it's reproducible
and CI-able. Full breakdown + data formats: **[`evals/README.md`](evals/README.md)**.

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

## The workflow — a closed, measurement-driven loop

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

You can drive it end-to-end (`/new-claude-setup <repo>`) or run the steps by hand:

**1 — Scaffold a new setup**
```bash
python tools/scaffold_claude_setup.py init claude-setups/<repo> --with-claude-md
python tools/scaffold_claude_setup.py add skill <name> --dir claude-setups/<repo> --desc "…"
```
Then fill in each file (the `claude-setup-scaffolder` skill walks you through it).

**2 — Validate (structural gate, fails CI on errors)**
```bash
python tools/validate_claude_setup.py claude-setups/<repo>
python tools/validate_claude_setup.py claude-setups/*/ .          # everything at once
```

**3 — Evaluate effectiveness (is it helpful *and* minimal?)** — a 3-layer
methodology, cheap static guesses → behavioral proof. Only the validate gate above
fails CI; these are advisory / their own test suites.
```bash
python tools/validate_claude_setup.py claude-setups/<repo> --score                     # Layer 1: 0-100 audit
python tools/validate_claude_setup.py claude-setups/<repo> --stale --repo ../<repo>     # Layer 1b: any block gone stale?
python tools/validate_claude_setup.py claude-setups/<repo> --route                     # Layer 2: do descriptions route right?
python tools/validate_claude_setup.py claude-setups/<repo> --ablate                    # Layer 3: dry-run preview
python tools/validate_claude_setup.py claude-setups/<repo> --ablate --execute          # …actually run it
```
What the score is made of, the eval data formats, and the honest limits of each
layer are in **[`evals/README.md`](evals/README.md)**.

**4 — Refine to target (close the loop)** — measurement only matters if you act on
it. `/refine-setup` runs `setup-critic` → `block-author` repeatedly until:
> composite **≥ 85** · **0 `[CUT?]`** · routing **100%** · every spec failure mode covered.
```bash
# in the kit's own Claude Code session (cd meta-env-setup):
/refine-setup claude-setups/<repo>
```

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

Every skill in `.claude/skills/` (and every command/agent description) loads into the
always-on routing budget. For a block built for a topic you're **not** working on right
now, park it in one `.claude/tools-pool/` folder, organized by block type then topic:

```
.claude/tools-pool/
├── skills/<topic>/<skill-name>/SKILL.md
├── commands/<topic>/<command-name>.md
└── agents/<topic>/<agent-name>.md
```

```bash
# park (frees budget)         → and promote when its phase starts (reactivate)
mv .claude/skills/<name>            .claude/tools-pool/skills/<topic>/
mv .claude/tools-pool/skills/<topic>/<name> .claude/skills/
```

Claude Code only reads the **active** folders (`skills/`, `commands/`, `agents/`), so
anything under `tools-pool/` is invisible — **zero budget cost** until you move it back.
The kit's tools (`--score`, `import`, structural `validate`) only glob the active folders,
so a pool never affects scoring or imports. The scaffolder can park a block directly:

```bash
python tools/scaffold_claude_setup.py add skill <name> --dir <setup> --pool <topic>
```

One `tools-pool/` per setup, split by topic (`tools-pool/skills/geometry/`,
`tools-pool/commands/frontend/`); promote what the current phase needs. `--stale --repo`
scans pooled blocks too, so a pre-built parked block can't rot unnoticed before promotion.
