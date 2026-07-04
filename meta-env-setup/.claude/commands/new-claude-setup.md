---
description: Build the most effective Claude Code setup for a repo, end to end — a closed, measurement-driven loop (analyze → interview → spec → scaffold → author → validate → smoke-test → refine → prove).
argument-hint: "<path-to-repo or repo name>"
---

Build a Claude Code setup for: **$ARGUMENTS**

The meta-env runs **once per repo**, so optimize for *quality, not speed* — spend
agents and iterations freely. The goal is the most effective setup possible, then
*proven* effective, not merely scaffolded. Follow the `claude-setup-scaffolder`
skill; pull blocks from the [cookbook](../../cookbook/README.md).

## Pipeline

1. **Analyze** — delegate to the **`setup-analyzer`** agent (read-only). First, if
   session transcripts exist for the repo, it mines them
   (`python tools/mine_transcripts.py --repo <repo>`) — a command hand-rolled 15× is
   the strongest signal there is. It then reports across **nine determinants**: the
   stack + run commands **and the domain inner loop**; the *one rule that overrides
   others*; repetitive workflows; failure modes **incl. parity invariants**; existing
   setup **+ staleness**; **feedback-loop economics** (cost of one iteration);
   **direction of travel & product value**; **environment executability**; and a
   **Questions for the owner** section. It also reports the **mode** (code-bearing vs.
   **greenfield**) — on an empty repo it runs greenfield mode (interview-led,
   defer-and-note).

2. **Interview the owner** — take the analyzer's **Questions for the owner** and ask
   them with **AskUserQuestion** (batch, ≤ 4 per call). Only ask what the owner alone
   knows (where time is burned, what's coming next, team size, what must never break,
   tooling already rejected) — skip anything the analyzer could read from a file. In
   **greenfield mode** this is mandatory and wider (intended stack, the core workflow
   being built, what "done" looks like, expected hard parts). The answers become the
   spec's §0 and constrain the block list (e.g. don't propose heavyweight visual
   testing to a solo dev who declined it).

3. **Write the spec** — capture the analysis **and the interview answers** in a filled
   [`templates/setup-spec.md`](../../templates/setup-spec.md), saved as
   `claude-setups/<repo>/SETUP-SPEC.md`. This is the durable contract everything else
   is built and judged against. Each block carries a **target**: `active`,
   `tools-pool/<topic>` (built now, parked for a later phase), or `deferred (trigger:
   …)` (greenfield — noted, not built). Get a thumbs-up on the block list before building.

4. **Scaffold** — `tools/scaffold_claude_setup.py init claude-setups/<repo> --with-claude-md`,
   then `add` each decided block. Pick the closest **cookbook archetype** for each. For
   a block whose target is `tools-pool/<topic>`, scaffold it into the pool with
   `--pool <topic>` so it's parked, not active. `deferred` blocks are **not** scaffolded
   — they stay as spec candidates.

5. **Author** — for each block (active or pooled), delegate to the **`block-author`**
   agent: fill it with repo-specific content that encodes the real failure mode, write
   a trigger-rich description, and self-score. Pooled blocks meet the **same** quality
   bar. (Skills follow the `skill-creator-lite` skill.)

6. **Hooks — opt-in (always ask first).** Hooks change behavior (they can *block*
   actions), so they're the one block type you never add silently. For **each**
   candidate hook in the spec, *actively propose it and wait for a yes*:
   - **what** it guards/reminds, **which event** (PreToolUse / PostToolUse / …), and
     whether it's **advisory (exit 0)** or **blocking (exit 2)**;
   - a one-line **recommendation** (default to advisory) and the cost (it runs on
     every matching event).
   Scaffold + author (per the **`hook-design`** skill) only the approved ones; wire
   them in `settings.json`. If the user declines one, note it in the spec and move on.

7. **Validate** — `tools/validate_claude_setup.py claude-setups/<repo>`; fix every
   structural finding (including any hook wiring).

8. **Refine to target** — run **`/refine-setup claude-setups/<repo>`**: the
   `setup-critic` measures (`--score`, `--route`) and prescribes; the `block-author`
   rewrites; repeat until the targets hold:
   > composite **≥ 85** · **0 `[CUT?]`** · routing **100%** · every spec failure mode covered.

9. **Smoke-test every command** — before packaging, **execute each command once**
   against the real repo (read-only recipes as-is; mutating/credentialed/quota-burning
   ones via their dry-run path). A command that **fails on first run goes back to
   `block-author`** — TOM shipped `/verify-generate` (anonymous quota = 0 → useless)
   and `/hf-logs` (head-only) broken, and one execution each would have caught both.
   Record each result in the spec's §10 as **PASS / PASS-dry-run / UNTESTED+reason**;
   a command that genuinely can't run here (missing GPU/creds) is flagged `UNTESTED` in
   the setup README, never silently assumed working. This applies to **pooled** commands
   too — prove it works *before* parking, not just before promotion.

10. **Prove (gold standard, optional)** — when it's worth the compute, draft an eval
    suite and run ablation: `tools/validate_claude_setup.py claude-setups/<repo> --ablate --execute`.
    Cut anything earning a `CUT` verdict; that's the real proof of "minimal yet maximal."

11. **Package** — add a `README.md` and a **dry-run-by-default `install.sh`** to the
    folder. **Ship `/setup-retro` by default** (cookbook archetype) so the owner can
    turn a future painful session into a machine-consumable `setup-backlog.md` that
    `/upgrade-claude-setup` then works down — this is how the setup keeps up with the
    repo instead of rotting. In **greenfield mode**, also write the spec's §11
    **re-analysis trigger** into the README (this setup was built from intent; re-run
    `/new-claude-setup` when real code lands).

## Rules
- **Never write into the real repo** — everything lands under `claude-setups/<repo>/`.
- **Interview before spec** — never guess an owner-only answer that changes the block list.
- **Hooks are opt-in — always ask.** Propose each candidate hook (step 6) and add
  only what the user approves; default to **advisory over blocking**, and never ship a
  hook that could silently break a flow.
- **Complement, don't duplicate** an existing setup (the analyzer flags overlaps).
- **No command ships unexecuted** — step 9 is mandatory; flag `UNTESTED` explicitly.
- **Greenfield → defer-and-note.** On an empty repo, author only CLAUDE.md (+ maybe one
  intent-grounded skill); everything speculative is a spec candidate, not a pre-built
  pool block.
- The *generated* setup is loaded every session, so minimalism rules: prefer a
  small, sharp set; the `--score`/`--ablate` loop exists to keep you honest.
- Don't declare done at "it validates" — done is **targets met in step 8**, every
  command PASS/UNTESTED in step 9 (and ideally step 10).
