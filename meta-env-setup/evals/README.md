# evals/ — does a setup actually help, and is it minimal?

`tools/validate_claude_setup.py` proves a setup is **well-formed**. It does *not*
prove the setup is **effective** (helps the agent) or **minimal** (no dead-weight
blocks burning routing budget). This folder holds the data that answers those
questions, plus the methodology behind it.

## Why eval data lives here (not in `claude-setups/`)
`claude-setups/` is **gitignored** (it's generated, per-target output). The task
suites and routing tests below are reusable, version-worthy meta-tool assets, so
they live in a tracked folder instead. One suite per target: `evals/<repo>/`.

## The three layers (cheap → expensive, static → behavioral)

| Layer | Command | What it measures | Proves |
|---|---|---|---|
| **1. Inspection** | `--score` | context budget, redundancy, trigger quality, specificity, least-privilege | flags *suspects* (instant, stdlib) |
| **1b. Staleness** | `--stale --repo` | is each block still *true* — do the code identifiers it cites still exist in the repo (active **and** pooled blocks) | flags blocks that drifted after a refactor/migration |
| **2. Routing** | `--route` | does each description fire on the right prompts, and stay quiet on the wrong ones | the labels actually steer |
| **3. Ablation** | `--ablate --execute` | run real tasks full vs. leave-one-out vs. none → KEEP/CUT per block | exactly what earns its place |

**The honest hierarchy:** Layers 1–2 are *cheap proxies* — they flag likely waste
in seconds without running an agent, but they can only **guess**. Only Layer 3
**proves** a block can be cut (remove it; if no task degrades, it was dead weight).
Ablation is nondeterministic and costs compute, so it is opt-in.

## What the `--score` composite is made of

The Layer-1 score is a **weighted blend of five sub-scores**, each normalized to
0–1, then `round(100 × Σ weightᵢ·subscoreᵢ)`.

| Sub-score | Weight | Measures | How it's computed (high level) |
|---|---|---|---|
| **trigger** | 0.35 | does each description say *what* **and** *when* | share of descriptions carrying both a distinctive domain noun and a trigger cue (`USE WHEN`, "when…") |
| **specificity** | 0.25 | grounded in *this* repo, not generic | share of blocks whose description vocabulary overlaps `CLAUDE.md` (low overlap ⇒ generic filler) |
| **redundancy** | 0.25 | no duplicate or echoed blocks | `1 −` penalties for near-duplicate descriptions (word-set Jaccard) and bodies copying `CLAUDE.md`'s figures |
| **budget** | 0.10 | always-loaded cost stays sane | `1.0` under a token ceiling (`≈ chars/4`), decaying above it |
| **leastpriv** | 0.05 | agents don't over-reach | share of agents that declare a narrowed `tools:` list |

**How it's computed, in one line:** every sub-score is a cheap, **deterministic
heuristic** over the *always-loaded* text (`CLAUDE.md` + every block description) —
token overlap, trigger-cue detection, a `chars/4` token estimate. No model call, so
the same input always yields the same score. Weights live in `WEIGHTS` in
`tools/validate_claude_setup.py` and are tunable.

> **Not scored (advisory only):** *coverage* — a `[HINT]` line listing recurring
> `CLAUDE.md` terms no block surfaces. It returned a flat ~0.66 for every setup (no
> discriminating power), so it's shown but kept out of the number.

## Run it
```bash
# Layer 1 — static effectiveness score (advisory; never gates CI)
python tools/validate_claude_setup.py claude-setups/DL-Project --score

# Layer 2 — routing tests (deterministic, stdlib classifier)
python tools/validate_claude_setup.py claude-setups/DL-Project --route

# Layer 3 — ablation: preview the run matrix for free …
python tools/validate_claude_setup.py claude-setups/DL-Project --ablate
# … then actually run it (launches `claude -p` many times)
python tools/validate_claude_setup.py claude-setups/DL-Project --ablate --execute --repeats 3
```

## File formats
- **`<repo>/routing-tests.json`** — `{ "<skill-name>": { "should_fire": [...], "should_not_fire": [...] } }`.
  A `should_fire` prompt must route to that skill; a `should_not_fire` prompt must not.
- **`<repo>/tasks.json`** — `{ "tasks": [ { "id", "prompt", "assertions": [...] } ] }`.
  Assertion types: `output_contains`, `output_contains_any`, `output_excludes`,
  `file_exists`, `file_contains`. A run passes a task iff **all** its assertions hold.
  Keep each task tied to one block so leave-one-out shows a clear drop.

See `DL-Project/` for a worked example (the proof-of-concept suite).

## Add a suite for another setup
1. `mkdir evals/<repo>`
2. Copy `DL-Project/routing-tests.json` + `tasks.json` and rewrite them for that
   repo's skills and failure modes (the things people get wrong there).
3. `python tools/validate_claude_setup.py claude-setups/<repo> --route` and `--ablate`.

## Tests
The deterministic scorers + the ablation verdict logic (with a mocked agent) are
covered by `tools/test_audit.py`:
```bash
python tools/test_audit.py
```
