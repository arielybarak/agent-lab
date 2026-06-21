# meta-env-setup — a kit for building & evaluating Claude Code setups

A self-contained toolkit for giving any repository a high-quality **Claude Code
(`.claude/`) setup** — and then *measuring* whether that setup is actually
effective and minimal, instead of guessing.

> **Run everything from inside this folder** (`cd meta-env-setup`). Every path in
> the docs below is relative to here, so the kit is portable: copy or share the
> whole `meta-env-setup/` folder and it works as a unit.

## What's inside

| Folder | What it is |
|---|---|
| **`tools/`** | The machinery (stdlib-only Python, no deps): `scaffold_claude_setup.py` (create a `.claude/` skeleton), `validate_claude_setup.py` (structural gate **+** effectiveness scoring/routing/ablation), `_ablation.py`, `test_audit.py`. |
| **`.claude/skills/`** | The kit's method skills (auto-activate when you work inside the kit): **`claude-setup-scaffolder`** (the whole pipeline), **`skill-creator-lite`** (author one skill well, sharpened against `--score`), and **`hook-design`** (when a hook earns its place + the event/exit-code/safety model). |
| **`evals/`** | The effectiveness methodology + per-repo eval data (task suites, routing tests). |
| **`cookbook/`** | A library of **proven block archetypes** (skills/commands/agents/hooks) distilled from the real setups, with copy-paste templates. Start here instead of a blank `TODO`. |
| **`templates/`** | The **setup-spec** PRD the analysis step fills before scaffolding. |
| **`claude-setups/<repo>/`** | Ready-made `.claude/` setups authored for other repos, each with a dry-run `install.sh`. *(gitignored — generated output)* |
| **`.claude/`** | The kit's *own* setup — a multi-agent pipeline. Commands: `/new-claude-setup`, `/refine-setup`, `/audit-claude-setup`. Agents: `setup-analyzer` (inspect), `block-author` (fill), `setup-critic` (judge + prescribe). Plus the method **`skills/`** (above). Auto-loads when you work from inside this folder. |

## The workflow — a closed, measurement-driven loop

The meta-env runs **once per repo**, so it optimizes for *quality, not speed*: it
doesn't just scaffold and validate, it **measures effectiveness and iterates until
the numbers hit target**. The whole pipeline is one command — `/new-claude-setup` —
which orchestrates the agents:

```
analyze ─▶ spec ─▶ scaffold ─▶ author ─▶ validate ─▶ refine ⟲ ─▶ prove ─▶ package
(analyzer)(spec) (scaffold) (block-   (validate) (critic⇄    (ablate
                              author)             author loop) --execute)
```

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
python tools/validate_claude_setup.py claude-setups/<repo> --score    # Layer 1: 0-100 audit
python tools/validate_claude_setup.py claude-setups/<repo> --route    # Layer 2: do descriptions route right?
python tools/validate_claude_setup.py claude-setups/<repo> --ablate   # Layer 3: dry-run preview
python tools/validate_claude_setup.py claude-setups/<repo> --ablate --execute   # …actually run it
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
python tools/test_audit.py          # deterministic scorers + ablation verdict logic (mocked agent)
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
