---
description: Build the most effective Claude Code setup for a repo, end to end — a closed, measurement-driven loop (analyze → spec → scaffold → author → validate → refine → prove).
argument-hint: "<path-to-repo or repo name>"
---

Build a Claude Code setup for: **$ARGUMENTS**

The meta-env runs **once per repo**, so optimize for *quality, not speed* — spend
agents and iterations freely. The goal is the most effective setup possible, then
*proven* effective, not merely scaffolded. Follow the `claude-setup-scaffolder`
skill; pull blocks from the [cookbook](../../cookbook/README.md).

## Pipeline

1. **Analyze** — delegate to the **`setup-analyzer`** agent (read-only). It reports
   the repo's stack + run commands, the *one rule that overrides others*, the
   repetitive workflows, the failure modes, and any existing setup to complement.

2. **Write the spec** — capture the analysis in a filled
   [`templates/setup-spec.md`](../../templates/setup-spec.md), saved as
   `claude-setups/<repo>/SETUP-SPEC.md`. This is the durable contract everything
   else is built and judged against. Get a thumbs-up on the block list before building.

3. **Scaffold** — `tools/scaffold_claude_setup.py init claude-setups/<repo> --with-claude-md`,
   then `add` each decided block. Pick the closest **cookbook archetype** for each.

4. **Author** — for each block, delegate to the **`block-author`** agent: fill it with
   repo-specific content that encodes the real failure mode, write a trigger-rich
   description, and self-score. (Skills follow the `skill-creator-lite` skill.)

5. **Hooks — opt-in (always ask first).** Hooks change behavior (they can *block*
   actions), so they're the one block type you never add silently. For **each**
   candidate hook in the spec, *actively propose it and wait for a yes*:
   - **what** it guards/reminds, **which event** (PreToolUse / PostToolUse / …), and
     whether it's **advisory (exit 0)** or **blocking (exit 2)**;
   - a one-line **recommendation** (default to advisory) and the cost (it runs on
     every matching event).
   Scaffold + author (per the **`hook-design`** skill) only the approved ones; wire
   them in `settings.json`. If the user declines one, note it in the spec and move on.

6. **Validate** — `tools/validate_claude_setup.py claude-setups/<repo>`; fix every
   structural finding (including any hook wiring).

7. **Refine to target** — run **`/refine-setup claude-setups/<repo>`**: the
   `setup-critic` measures (`--score`, `--route`) and prescribes; the `block-author`
   rewrites; repeat until the targets hold:
   > composite **≥ 85** · **0 `[CUT?]`** · routing **100%** · every spec failure mode covered.

8. **Prove (gold standard, optional)** — when it's worth the compute, draft an eval
   suite and run ablation: `tools/validate_claude_setup.py claude-setups/<repo> --ablate --execute`.
   Cut anything earning a `CUT` verdict; that's the real proof of "minimal yet maximal."

9. **Package** — add a `README.md` and a **dry-run-by-default `install.sh`** to the folder.

## Rules
- **Never write into the real repo** — everything lands under `claude-setups/<repo>/`.
- **Hooks are opt-in — always ask.** Propose each candidate hook (step 5) and add
  only what the user approves; default to **advisory over blocking**, and never ship a
  hook that could silently break a flow.
- **Complement, don't duplicate** an existing setup (the analyzer flags overlaps).
- The *generated* setup is loaded every session, so there minimalism rules: prefer a
  small, sharp set; the `--score`/`--ablate` loop exists to keep you honest.
- Don't declare done at "it validates" — done is **targets met in step 7** (and
  ideally step 8).
