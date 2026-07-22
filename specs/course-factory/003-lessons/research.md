# Phase 0 Research — Lessons Phase

The spec is fully clarified (three 2026-07-07 clarifications: gate-then-fan-out ordering, first-two-to-
terminal-state trigger, single batch-level skeleton loop) and inherits every cross-spec seam already
settled by 001/002/004. So Phase 0 is **not** about resolving `NEEDS CLARIFICATION` — there are none —
it is about recording the **design decisions** that turn a clarified spec into a buildable plan: where
determinism earns its place, what stays agent judgment, and how 003 plugs into three not-yet-built
seams (001's engine, 004's rubric, 000's template). Each decision is stated as
Decision / Rationale / Alternatives, the format the plan template asks for.

## R1 — Where determinism earns its place (the tool/skill split)

**Decision.** Mechanize exactly the SCs stated in **100% / 0-exception** terms, and only those, in a
thin stdlib tool layer: the **pool scheduler** (SC-003 at-most-`pool_width`, SC-010 gate-then-fan-out),
the **citation-traceability resolver** (SC-004 exhaustive `[Sn]` resolution), and the
**author/evaluator envelope builder** (SC-002 author-blindness of the evaluator's input). Everything
else — authoring, critique, grading, reading-as-student — stays agent judgment.

**Rationale.** These four SCs are *count/coverage* properties an agent cannot self-certify reliably
run-over-run: "never more than `pool_width` in flight," "no lesson≥3 before calibration," "every
citation resolved," "the evaluator never saw the author's reasoning." A deterministic function over
on-disk state gives a `0`-exception guarantee and a test that asserts it directly. This is the same
reasoning 001 (R1) and 002 (R1) recorded; 003 adds no new abstraction pattern, it applies the settled
one to its own SCs.

**Alternatives considered.** *All-agent* (the orchestrating session self-polices in-flight count,
citation coverage, and author-blindness) — rejected: the SCs are exactly the properties an over-long
agent turn silently drops, and they would be untestable without an agent in the loop. *Heavier
framework* (a real work queue / async runtime for the pool) — rejected as over-engineering: the pool is
a handful of subagent spawns per course, `pool_width` tops out at 2, and MVP is fully serial; a pure
scheduling function over the lessons list is sufficient and keeps the stdlib-only constraint.

## R2 — The citation-traceability check is the factory's CANONICAL check — reuse it, don't author a third

**Decision.** Factor the `[Sn]`→`SOURCES.md` resolution into **one shared resolver module**
(`course-factory/tools/sn_resolve.py`) that all three consumers import: 002's `syllabus_lint.py`
(topic traceability), 003's `citation_trace.py` (per-lesson evaluator gate), and 004's course-evaluator.
The shared module owns the *primitive* — "does this `[Sn]` key resolve to a real `SOURCES.md` entry,
honoring 002's mentor-added / thin-grounding tags" — with identical semantics (mechanical,
tracing-not-truth). 003's `citation_trace.py` is a **thin layer** over it that adds only what is
003-specific: **format-aware extraction** (scan `.md` prose and `.ipynb` markdown cells, research R7)
and the **exhaustive per-lesson sweep** (every claim → cited-or-mentor-added; every key resolved). So
"reuse" is a concrete shared import, not merely matching semantics by hand.

Since 002 is not yet built, 003 **authors `sn_resolve.py`** as the canonical module and 002/004 import
it when they land; if 002's `syllabus_lint.py` already exists at 003 build time, the resolution
primitive is **lifted into `sn_resolve.py`** and `syllabus_lint.py` re-pointed at it (a refactor, not a
fork). Either way there is exactly one resolver.

**Rationale.** The spec is explicit that this is the factory's **canonical citation/grounding
contract** (FR-011 cites "004 FR-007/FR-008") and that 003 "applies it per lesson rather than
re-deriving an independent rule." 004 FR-007 says the same in the other direction ("mirrors 003
FR-011"). Three specs naming the *same* check is a strong signal it is one function with three callers,
not three implementations that will drift. A drifted grounding check is precisely the anti-fabrication
failure Principle II exists to prevent.

**Alternatives considered.** *A 003-private resolver* — rejected: guarantees eventual drift from
002/004 and violates the spec's "canonical, not re-derived" language. *Wait for 004 to own it* —
rejected: 004 is not built and 003 needs the check now; 003 ships the shared `sn_resolve.py` (referenced
by `contracts/rubric-gate.md`), which 004 then consumes rather than re-writes. The honest boundary: this
is *tracing*, not *truth* — the resolver confirms a key resolves to a real entry; it cannot and does not
judge whether the claim is correct (that is the mentor/evaluator's judgment and the rubric's).

## R3 — The worker pool: a scheduling function, MVP fully serial, gate-then-fan-out as a hard barrier

**Decision.** `pool_scheduler.py` is a **pure function** over `(lessons[], pool_width,
calibration_done)` → the set of lessons eligible to be *in flight* right now. It enforces two
invariants: never more than `pool_width` non-terminal lessons dispatched at once (SC-003), and **no
lesson at syllabus-index ≥ 3 is eligible until `calibration_done` is true** (SC-010, the
gate-then-fan-out barrier). The orchestrating session asks the scheduler what to dispatch, spawns those
author–critic pairs, and re-asks as each reaches a terminal state. **MVP `pool_width = 1`** collapses
this to a fully serial walk — no concurrency to reason about, no concurrent `lessons[]` writes to
order — while the same function at `pool_width = 2` is the target with zero code change (FR-009).

**Rationale.** Separating *scheduling* (deterministic, testable) from *spawning* (the session's live
act) lets SC-003/SC-010 be asserted by `pytest` over the function, independent of any real subagent
run. Shipping serial-first (per DESIGN "Open decisions" and FR-009) de-risks the concurrency model: the
correctness of every other FR does not depend on `pool_width`, so the target-2 flip is a config change
validated by the same tests, not a rewrite. The gate-then-fan-out barrier is modeled as an eligibility
predicate rather than a side effect so it *cannot* be bypassed by an agent forgetting to wait.

**Honesty boundary (stated, not hidden).** The scheduler decides *eligibility*; it does not itself
spawn or throttle subagents — the session does. The guarantee is: *if the session dispatches only what
the scheduler returns*, SC-003/SC-010 hold. The handler contract (`lesson-handler.md`) makes "dispatch
only scheduler-eligible lessons" the binding rule, and the quickstart's scenario walkthrough exercises
that the session honors it.

**Alternatives considered.** *Bake the ordering into prose guidance only* — rejected: "no lesson≥3
before calibration" is exactly the invariant a long orchestration turn drops; a predicate makes it
mechanical. *A stateful scheduler object holding in-flight state* — rejected for MVP: the authoritative
in-flight state already lives in `lessons[]` (001's `BUILD_PROGRESS.md`); a pure function over that
avoids a second, drift-prone state copy.

## R4 — Author-blindness is a property of the evaluator's INPUT envelope, mechanized by the builder

**Decision.** `author_envelope.py` builds two disjoint input sets: the **author** envelope (exactly the
FR-007 set — brief, frozen syllabus + its `DIFFS.md` entries, the lesson's approved skeleton + its
diffs, the relevant `[Sn]` entries, the insights digest, and `CALIBRATION.md` for lessons beyond the
first two) and the **evaluator** envelope (the authored artifact + the grading inputs — rubric,
`SOURCES.md` for resolution — but **no** author-reasoning channel). "Author-blind" (SC-002, FR-008) is
enforced structurally: the evaluator subagent is a *separate fresh-context spawn* whose input is the
evaluator envelope, so the author's private chain-of-thought is never in scope by construction.

**Rationale.** The spec's Assumptions pin this precisely: "the 'author-blind' property is about the
author's chain of thought, not about the artifact's history" — the evaluator may re-read the artifact
and its own prior critiques, it just never receives the author's reasoning. Modeling blindness as
"which envelope the evaluator is handed" makes SC-002 a testable property of the builder (does the
evaluator envelope contain an author-reasoning field? it must not), rather than a hope about how a
prompt was written.

**Honesty boundary.** The builder guarantees the evaluator's *input* excludes the author's separate
reasoning channel. It **cannot** police what an author chooses to embed *inside the artifact itself* —
but that is the lesson, which the evaluator is *supposed* to read. Blindness is about the private
reasoning channel, not about scrubbing the artifact. This limit is stated so the guarantee is not
oversold.

**Alternatives considered.** *One subagent grading its own draft* — rejected outright: violates FR-008
and the entire author-blind design. *Trust prompt wording to keep the evaluator blind* — rejected: not
testable and easy to regress; the envelope builder makes it a checked invariant.

## R5 — Consume 004's rubric via a thin stand-in contract now; it becomes the live seam when 004 lands

**Decision.** Publish `contracts/rubric-gate.md` — the **minimum** 003's lesson evaluator needs from
the rubric: (a) a **pass is a per-dimension threshold** (every dimension clears its own bar; a strong
dimension never masks a failing one — 004 FR-004), and (b) the **canonical citation/grounding check**
is part of grading (every `[Sn]` resolves; mentor-added claims are not failed for lacking a key — 004
FR-007/FR-008). Validate the lesson gate against a **minimal rubric fixture** shaped to that contract.
When 004 ships its rubric core, this contract is the seam it must satisfy; 003 does not redefine the
rubric's *contents* (FR-010).

**Rationale.** This is exactly the move 002 made against not-yet-built 001 (validate against contracts
+ fixtures, never re-derive the other spec's internals). The recommended build order puts "004 rubric
core" before 003 precisely because of this seam; publishing the thin contract now lets 003 be planned,
tasked, and tested without blocking on 004, and gives 004 a concrete consumption target.

**Alternatives considered.** *Invent a full rubric inside 003* — rejected: violates Principle VIII
(one rubric, owned by 004) and FR-010. *Block 003 until 004 is built* — rejected: the specs are
explicitly separable across sessions, and 003's authoring/pool/calibration design is independent of the
rubric's exact dimensions — only the *pass predicate* and the *grounding check* cross the seam, and
both are already settled (004 FR-004/007/008, mirrored in the README seam log).

## R6 — One shared author→critique→refine primitive, authored once as a skill both phases invoke

**Decision.** Implement the primitive **once** (`author-critic-loop` skill): author produces/refines →
author-blind evaluator emits **cited deltas** → author refines *the deltas* (targeted revision, not a
restart) → repeat until the evaluator passes or 001's counter hits the cap. The skeleton phase and the
lesson phase are **thin drivers** over this one skill; they differ only in (i) the *driver* — a single
batch loop over all skeletons (FR-004) vs. a worker pool over lessons (FR-009) — and (ii) the
evaluator's *checklist* — topic-match + clarity (FR-005) vs. rubric + full traceability (FR-010/011).

**Rationale.** FR-001 mandates a "single **shared**" primitive for both phases; authoring it twice
would guarantee the two copies drift (one gets a fix the other misses), reintroducing the very
inconsistency the shared-primitive rule prevents. Making the *evaluator checklist* and the *driver* the
only parameters keeps the loop body identical, satisfying FR-001 structurally. FR-003's "address cited
deltas, don't restart" lives in the one loop body, so both phases inherit convergence-within-cap for
free.

**Alternatives considered.** *Two independent loops (one per phase)* — rejected: violates FR-001's
"single shared" and invites drift. *A single mega-skill that also owns the batch/pool drivers* —
rejected: conflates the loop body (shared) with the phase orchestration (distinct), making the shared
core harder to test in isolation; the driver/loop split keeps each testable.

## R7 — `.ipynb` citation mechanics: scan markdown cells with the stdlib JSON parser

**Decision.** When a lesson's format is `.ipynb` (002's decision, recorded in `COURSE_BRIEF.md`),
`citation_trace.py` parses the notebook as JSON (stdlib `json`), extracts the `source` of every cell
whose `cell_type == "markdown"`, and runs the **same** `[Sn]` text-scan it uses on `.md` lessons —
ignoring `code` cells and outputs. Authors place `[Sn]` keys in markdown cells (never code-cell
comments or outputs), so `.md` and `.ipynb` lessons trace by one method.

**Rationale.** The spec's Assumptions explicitly punt this to "this spec's `/speckit-plan`": "`[Sn]`
keys live in markdown cells … so the traceability check can read them via the same text-scan method as
`.md` lessons; the exact cell-parsing approach is left to this spec's `/speckit-plan`." Resolving it
here keeps one resolver with a format-aware *extraction* step, not two resolvers — consistent with R2's
canonical-check decision. Stdlib `json` honors the zero-deps constraint (a notebook is JSON; no
`nbformat` dependency needed for a read-only markdown-cell scan).

**Alternatives considered.** *A separate `.ipynb` resolver* — rejected: duplicates the canonical check
(violates R2). *Scanning code cells / outputs too* — rejected: citations belong in prose; scanning code
would surface false `[Sn]`-looking tokens and blur the author's placement contract. *Add `nbformat`* —
rejected: an unnecessary dependency for a read-only markdown-cell extraction the stdlib already covers
(and the repo's stdlib-only convention).

## R8 — The fake-student trigger and once-per-course guarantee key off `CALIBRATION.md` presence

**Decision.** The fake-student check fires when the **first two lessons reach a terminal state**
(rubric-passed *or* cap-surfaced-and-user-accepted, in syllabus order) and is gated by the **presence
of `CALIBRATION.md`**: the check runs iff `CALIBRATION.md` does not yet exist; on completion it writes
`CALIBRATION.md`, which both (a) makes the run idempotent/once-per-course (SC-006, FR-015) and (b)
flips the scheduler's `calibration_done` barrier (R3) so fan-out may begin. Fewer-than-two-lesson and
no-exercise cases fall back per the spec's edge cases (run once on what exists; read-and-report-only)
without changing the guard.

**Rationale.** Tying "at most once" to a durable on-disk artifact rather than an in-memory flag honors
001's disk-only resume rule (FR-021 cites 001 FR-018): a session dying after calibration resumes and
sees `CALIBRATION.md` already present, so it neither re-runs the check nor loses the guidance. Reusing
the *same* artifact as the scheduler's fan-out barrier keeps one source of truth for "calibration done"
instead of two flags that could disagree.

**Alternatives considered.** *An in-memory "already ran" flag* — rejected: lost across a session
boundary, would re-run the check on resume (violates SC-006 and FR-021's resume intent). *A separate
`calibration_done` field in `BUILD_PROGRESS.md`* — rejected as a redundant second source of truth;
`CALIBRATION.md`'s presence is unambiguous and is already the artifact FR-021 requires.

## R9 — Per-lesson round tracking: MVP fits 001's single `active_loop`; target-2 is a flagged seam item

**Decision.** At **MVP `pool_width = 1`** the lesson phase has exactly **one** lesson in flight at a
time, so 001's single `active_loop = { phase, round }` counter (`build-progress-schema.md`) is
authoritative verbatim — the seam's `loop`→increment→re-invoke cycle drives that one lesson, and moving
to the next lesson resets the loop. The skeleton phase is likewise a **single** batch-level loop
(FR-004), so it too fits one `active_loop`. **The tension is lesson-only and target-2-only:** at
`pool_width = 2`, two lessons are in flight with **independent** round counts, which a single
`{ phase, round }` cannot represent. 003 records this as an **explicit open item of FR-009's deferred
concurrency model** — *"the design target is 2 once real runs validate the concurrency model"* — to be
resolved when target-2 lands, as **either** (a) a forward-diff extension of 001's schema (`active_loop`
gains a per-lesson round map) **or** (b) 003 tracking per-lesson rounds internally with `active_loop`
demoted to a phase-level marker. It is **not** resolved silently now, and it does **not** affect any
MVP FR/SC (every FR/SC is `pool_width`-invariant, FR-009).

**Rationale.** Surfacing this is the honest reading of the seam: `phase-seam.md`'s `loop` semantics and
`build-progress-schema.md`'s single `active_loop` are a *serial-loop* abstraction, exactly matching the
serial MVP. Pretending one counter tracks two concurrent loops would be a latent defect; naming it as
the concrete thing "validate the concurrency model" defers keeps MVP correct and gives target-2 a
known, scoped decision instead of a surprise.

**Alternatives considered.** *Extend `active_loop` to a round-map now* — rejected: it is a change to
001's owned schema for a capability (pool_width=2) that MVP does not ship and real runs have not yet
validated; premature, and it belongs to 001 via forward diff, not to 003 unilaterally. *Let 003 own
per-lesson rounds now and ignore `active_loop`* — rejected: contradicts the seam's stated round-cap
ownership (001 owns the counter) for the MVP where one counter is sufficient; the decision is only
forced at target-2.
