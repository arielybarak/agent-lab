---
name: "speckit-harden"
description: "Run the full plan -> review-and-fix -> tasks -> analyze cycle for one feature spec in one go: /speckit-plan, then a gaps-then-optimizations review-and-fix pass on the plan artifacts, then /speckit-tasks, then /speckit-analyze."
argument-hint: "<spec-name> — e.g. \"001\" or \"001-pipeline-skeleton\" (matched against specs/*/NNN-*/)"
compatibility: "Requires spec-kit project structure with .specify/ directory; the target spec must already be Clarified (no unresolved [NEEDS CLARIFICATION] markers)"
metadata:
  author: "custom, authored for agent-lab"
user-invocable: true
disable-model-invocation: true
---

## User Input

```text
$ARGUMENTS
```

`$ARGUMENTS` MUST name exactly one spec. Do not proceed on an empty, missing, or ambiguous argument
— resolve it in Step 0 below, and stop to ask if it doesn't resolve to exactly one spec.

## Why this exists

Chains four steps normally run by hand, one at a time, against a single feature spec:

1. `/speckit-plan`
2. A review-and-fix pass on what step 1 produced — gaps/holes first, then optimizations — asking
   the user only where a fix is genuinely ambiguous.
3. `/speckit-tasks`
4. `/speckit-analyze`

Designed to be run **concurrently, in separate sessions, against different specs** — see
"Parallel-safety" in Step 0. One invocation handles exactly one spec; for N specs, run N sessions.

## Step 0 — Resolve the target spec (parallel-safety)

1. Run `.claude/skills/speckit-harden/resolve.sh "$ARGUMENTS"` from repo root. It searches
   `specs/*/*/spec.md` for a folder matching `$ARGUMENTS` (exact folder name, or an unambiguous
   numeric/name prefix, e.g. `001` matching `specs/course-factory/001-pipeline-skeleton/`) and prints
   one JSON line: `RESOLVED_FEATURE_DIR`, `CLARIFIED`, `MATCH_COUNT`, `CANDIDATES`. Deterministic —
   this is plumbing, not something to hand-roll with `grep`/`find` each run.
2. If `MATCH_COUNT` is not `1`, **stop** — list `CANDIDATES` and ask the user to disambiguate rather
   than guessing.
3. If `MATCH_COUNT` is `1` but `CLARIFIED` is `false`, don't treat that as final — the script only
   checks for a `## Clarifications` heading in `spec.md`; some specs record "Clarified" only in the
   project's spec index (`specs/<project>/README.md`). Check the README before concluding. If it's
   genuinely not clarified, stop and say so — this skill assumes a clarified spec, it does not run
   `/speckit-clarify` itself.
4. Call the resolved path `RESOLVED_FEATURE_DIR` (e.g. `specs/course-factory/001-pipeline-skeleton`)
   for the rest of this run.
5. **Parallel-safety rule — apply for the rest of this run:** every underlying
   `.specify/scripts/bash/*.sh` call this skill triggers — directly, or while carrying out
   `/speckit-plan`'s, `/speckit-tasks`'s, or `/speckit-analyze`'s own steps below — MUST be prefixed
   inline with `SPECIFY_FEATURE_DIRECTORY=<RESOLVED_FEATURE_DIR>` on that exact command line. Do not
   rely on `.specify/feature.json` alone. `SPECIFY_FEATURE_DIRECTORY` outranks `feature.json` in
   `common.sh`'s resolution order (checked first), so every call this session makes stays correct
   regardless of what any other concurrent session has written to the shared `feature.json` in the
   meantime. This one rule is what makes it safe to run this skill in parallel across sessions.

## Step 1 — Plan

Invoke `speckit-plan` via the Skill tool **now, at this step** — a fresh load, not a reuse of
anything read earlier in this run. This matters: a fresh invocation re-surfaces `/speckit-plan`'s own
Pre-Execution Checks (its extension-hook check) as the next thing to do, right when it's relevant,
instead of you relying on a synthesis from Step 0 and silently skipping a re-check. Then carry out
its Outline, applying the Step 0 pinning rule to its `setup-plan.sh --json` call — that pinning is
your responsibility regardless of how the instructions arrived; invoking via the Skill tool doesn't
change which exact Bash command line you issue. Produces/updates `plan.md` and whichever of
`research.md`, `data-model.md`, `contracts/`, `quickstart.md` its template calls for.

## Step 2 — Review and fix the plan (gaps, then optimizations)

Re-read every artifact Step 1 touched, against `RESOLVED_FEATURE_DIR/spec.md`, the active project's
constitution (`.specify/memory/constitution.md`), and its governing design doc (e.g.
`course-factory/DESIGN.md`) — the same discipline as a manual deep-design review, scoped to the plan
layer instead of the spec layer.

**2a. Gaps & holes — fix directly, no need to ask:**
Missing pieces the plan should cover for the spec's FRs/SCs but doesn't; contradictions between
plan.md and spec.md/constitution; unresolved `NEEDS CLARIFICATION` markers the plan should have
settled; a Constitution Check gate violation left unjustified.

**2b. Optimizations — implement directly, no need to ask. Do it in this order:**

  **First — the substance (critical-thinking pass on the plan's core).** Before any tidying, reason
  about whether this is the *right* plan: actively hunt for genuine improvement/optimization
  opportunities in the **design itself** — a stronger technical approach, a better-chosen structure
  or phase sequencing, more robust handling of a specific FR/SC, a decision the research digest or
  constitution suggests should go a different way, a cheaper path to the same deliverable. This is
  the high-value pass; spend the thinking here, not on cosmetics.

  **Then — the refinements (only after the substance pass).** Simplifications, redundancy removal,
  better decomposition — tidying that improves how the plan reads/organizes **without** changing
  what it delivers.

**Ambiguity gate:** if a change has more than one reasonable resolution, or would alter the **spec's
scope** or the **deliverable's behavior** (as opposed to improving the plan's approach to the *same*
deliverable), **stop and ask** — using the plain-language-first style from the global communication
instructions (state the question in one or two plain sentences before any technical framing; a
recommended option + short table is fine, dense jargon up front is not). Don't guess on anything that
meets this bar. A substantive core improvement that is clearly correct and keeps the same
deliverable/scope is applied directly; one that reshapes scope or has a real fork goes to the gate.

Save edits as you go (same incremental-save discipline as `/speckit-clarify`).

## Step 3 — Tasks

Invoke `speckit-tasks` via the Skill tool **now, at this step** — same reasoning as Step 1: a fresh
load re-surfaces its own Pre-Execution Checks at the right moment instead of coasting on a synthesis
from earlier steps. Carry out its Outline, applying the Step 0 pinning rule to its
`setup-tasks.sh --json` call. Produces/updates `tasks.md`.

## Step 4 — Analyze

Invoke `speckit-analyze` via the Skill tool **now, at this step** — same reasoning again. Carry out
its Outline, applying the Step 0 pinning rule to its
`check-prerequisites.sh --json --require-tasks --include-tasks` call. This step stays **read-only**,
matching its own documented behavior — report findings here, do not silently fix them (unlike Step
2, which fixes directly). If it surfaces anything, list it in the Completion Report as follow-up
work, not as something already handled.

## Completion Report

- Spec: `RESOLVED_FEATURE_DIR`
- Plan artifacts written/updated (list)
- Step 2: gaps fixed (list), optimizations applied (list), anything you had to stop and ask about
  (and the resolution)
- Tasks: task count / notable structure decisions
- Analyze: findings, if any, and whether they warrant a follow-up pass
- Suggested next command: `/speckit-implement` (or `/speckit-taskstoissues`)
