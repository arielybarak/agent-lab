---
description: Close the loop on a setup — measure (score/route/ablate), critique, rewrite the weak blocks, and re-measure until effectiveness targets are hit.
argument-hint: "<path to a setup folder, e.g. claude-setups/<repo>>"
---

Iteratively optimize the Claude Code setup at: **$ARGUMENTS**

This is the meta-env's *thermostat*: it doesn't just report quality, it drives it
up. The meta-env runs once per repo, so spend freely here — keep iterating until
the numbers plateau at the targets. Don't stop at "it validates."

## Effectiveness targets (the exit condition)
- **Structural:** `validate` passes with 0 errors.
- **Score:** composite **≥ 85**, and **0 `[CUT?]`** findings, and every `[SHARPEN]`
  resolved or consciously accepted.
- **Routing:** **100%** of `--route` assertions pass (if a suite exists; if not,
  consider asking `block-author` to draft `evals/<repo>/routing-tests.json`).
- **Coverage:** every failure mode / repetitive workflow in the setup spec maps to a block.
- **Minimalism (optional, gold standard):** if asked to spend the compute, no block
  is flagged `CUT` by `--ablate --execute`.

## The loop
1. **Measure.** Run the critic's battery and read the evidence:
   ```bash
   python tools/validate_claude_setup.py $ARGUMENTS
   python tools/validate_claude_setup.py $ARGUMENTS --score
   python tools/validate_claude_setup.py $ARGUMENTS --route   # if a suite exists
   ```
2. **Critique.** Delegate to the **`setup-critic`** agent (or apply its rubric):
   get the prioritized fix list — CUT / SHARPEN / GAP / TIGHTEN, with evidence.
3. **Rewrite.** For each item, delegate to the **`block-author`** agent:
   - **SHARPEN** → rewrite the description/body; re-score that block.
   - **CUT / MERGE** → remove or fold the block (show the diff first).
   - **GAP** → scaffold and author the missing block (`scaffold_claude_setup.py add …`).
     **If the gap is best filled by a hook, propose it and ask first** (hooks are
     opt-in; default to advisory) — see the `hook-design` skill.
   - **TIGHTEN** → narrow agent `tools:`, make a hook advisory.
4. **Re-measure.** Re-run step 1. If any target is unmet, go to step 2.
5. **Prove (optional).** When the static targets hold and it's worth the compute,
   run `--ablate --execute` and cut anything that earns a `CUT` verdict.

## Rules
- Show diffs before applying destructive changes (cutting/merging blocks).
- Iterate on **descriptions first** — they're the highest-leverage text and drive
  both the score and real routing.
- Record what changed and the before/after composite score, so the gain is visible.
- Stop when targets are met — don't manufacture churn.
