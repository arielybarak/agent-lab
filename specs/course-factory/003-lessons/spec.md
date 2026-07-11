# Feature Specification: Lessons Phase — Skeletons, Parallel Author–Critic Authoring & Learnability

**Feature Branch**: `003-lessons`

**Created**: 2026-07-07

**Status**: Draft

**Input**: User description: "Build the Lessons phase of the course factory — the depth behind the skeleton and lesson gates that spec 001 orchestrates. This owns: (1) the shared author → agent-critique → refine primitive, capped at 3 rounds, that powers BOTH the skeleton phase and the lesson phase; (2) skeleton authoring — draft all per-lesson skeletons at once as a domain mentor, run the agent author↔critique↔refine loop until every skeleton matches its lesson topic and is clear/simple, then PRESENT the batch for user approval and WAIT (per 001 FR-024, a blocking gate — do NOT auto-advance to lessons); (3) lesson authoring executed as a parallel author–critic worker pool — each lesson gets a fresh-context author subagent (inputs: COURSE_BRIEF.md + syllabus + its skeleton + relevant SOURCES.md [Sn] entries + the insights digest) and a SEPARATE author-blind evaluator subagent (never sees the author's reasoning), with the orchestrating session mediating each pair's loop and keeping TWO pairs in flight at a time (fan-out/fan-in), grading each lesson against 004's rubric as the gate, with mandatory [Sn] citations the evaluator spot-checks for traceability (verifies tracing, not truth); (4) the once-per-course, lightweight fake-student learnability check — when the first two lessons pass the rubric, a fresh subagent gets only the brief's audience + assumed prior knowledge plus those two lessons, reads them and attempts the exercise, and its confusion points are fixed there AND folded into the drafting guidance for every remaining lesson (one run, it calibrates the explanation format). Consumes 004's rubric as the lesson gate; consumes 001's phase/state contract (updates BUILD_PROGRESS.md per lesson). Explicitly OUT of scope: pipeline orchestration / gates / state machine / resume (spec 001); research + SOURCES.md population + syllabus composition (spec 002); the rubric contents + course-evaluator internals + COURSE_REPORT.md (spec 004). Honor the settled seam decisions: 001 FR-023 forward-diff-only (a gap found in an earlier gated artifact surfaces as a forward diff, never reopens the phase) and 001 FR-024 blocking post-skeleton user scan."

## Overview

This is **spec #3 of four subject-specs**. It fills the **depth behind the skeleton gate and the
lesson gate** that spec 001 orchestrates: how per-lesson skeletons and full lessons are actually
authored, critiqued, and hardened. Its deliverables are a **review-ready skeleton batch** (handed to
001's blocking user-scan gate) and a set of **rubric-passing lessons**, each grounded by traceable
`[Sn]` citations.

It runs *inside* 001's skeleton and lesson phases. 001 owns the state machine, the gate loop control,
the freeze/forward-diff rules, and whose reviewer blocks each phase. 003 owns the *work behind those
gates*: the shared author → critique → refine primitive, the mentor-led skeleton batch, the parallel
author–critic worker pool that drafts lessons, and the once-per-course fake-student learnability
calibration.

Two seams it consumes rather than owns:

- **004's rubric** is the **lesson gate**. 003 grades each lesson against it as a pass/fail gate; the
  rubric's contents and the course-evaluator internals are 004's.
- **001's phase/state contract** governs advancement, blocking gates, and resume. 003 does the
  phase-internal work and writes per-lesson status into `BUILD_PROGRESS.md`; it does not own the
  state schema, the gate mechanics, or the pause.

### Out of Scope (owned by other specs)

- **Pipeline orchestration / gates / state machine / resume** — spec **001**. 003 produces the
  skeleton batch and the lessons and reports per-lesson status; 001 owns the phase sequence, the
  blocking user-scan pause (FR-024), the forward-diff rule (FR-023), the round-cap surface-to-user
  decision (its FR-012), and all resume logic.
- **Research + `SOURCES.md` population + syllabus composition** — spec **002**. 003 *reads*
  `SOURCES.md` and cites into it; it does not search, weigh, or populate it, and it does not compose
  the syllabus. It consumes the frozen, approved syllabus as an input.
- **The rubric's contents, the course-evaluator internals, and `COURSE_REPORT.md`** — spec **004**.
  003 consumes the rubric as a pass/fail gate over a lesson; it does not define what the rubric
  measures or emit the final scorecard.
- **The `COURSE_BRIEF.md` overlay authoring and the lesson-format decision** — specs **001** (brief)
  and **002** (`.md`/`.ipynb`). 003 reads both and authors lessons in the decided format.
- **Harvesting `FEEDBACK.md` into `insights/`** — spec **004**. 003 *reads* the insights digest as an
  author input; it does not produce or harvest it.
- **Inline mid-lesson comprehension checks (MCQs)** — a deferred, opt-in `course-template/` module
  (would slot alongside katas/diagrams/Socratic), not this spec's initial scope.
- **A per-phase quality checklist for the skeleton/lesson gates, and status-stamping the skeleton
  batch / lessons as artifacts** — deferred, spec-kit-style additions to this spec's gates.
- **Consuming `pedagogy/`'s `[Pn]`-keyed technique catalog** — built and populated (2026-07-10) but
  not yet wired into any spec. When it is wired in, this spec's citation contract (FR-011, currently
  `[Sn]`-or-mentor-added) will need a `[Pn]` slot alongside `[Sn]` (see
  `course-factory/pedagogy/README.md` § Consumption points). Not required for this spec's initial
  scope.

  All tracked in `course-factory/DESIGN.md` § Deferred extensions.

## Clarifications

### Session 2026-07-07

- Q: How should the two-pairs-in-flight lesson pool and the once-per-course fake-student calibration
  be ordered (FR-018)? → A: **Gate then fan-out** — the pool drafts lessons 1 & 2 first, runs the
  fake-student check, and only then fans out the remaining lessons (two in flight) with the
  calibration already folded in. A single serialization point sits after the first two lessons; no
  remaining lesson begins before the calibration completes.
- Q: When does the fake-student check fire if two lessons never cleanly pass the rubric within the
  cap (or the course has fewer than two lessons)? → A: **On the first two lessons to reach a terminal
  state** — rubric-passed *or* cap-surfaced-and-user-accepted, in syllabus order; if fewer than two
  lessons exist, it runs once on what exists. It never blocks on a lesson that never passes.
- Q: Does the skeleton phase use the same per-item two-in-flight author–critic pool as lessons, or a
  single batch-level loop? → A: **Single batch-level loop** — one author drafts all skeletons at once
  and one evaluator critiques the batch; the two-pairs-in-flight worker pool is lesson-only.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Author the skeleton batch and present it for the blocking user scan (Priority: P1)

Given an instantiated course with an approved, frozen syllabus, the factory drafts **all** per-lesson
skeletons at once as a domain mentor, runs the shared author → critique → refine loop until every
skeleton matches its lesson's topic and reads clearly, and then **presents the whole batch for user
approval and waits** — it does not advance to the lesson phase on its own.

**Why this priority**: The skeleton batch is the first artifact this phase owns and the smallest
independently valuable slice — it exercises the shared author→critique→refine primitive end to end
and produces the approved per-lesson plans every later lesson depends on. It is demonstrable before a
single full lesson is written.

**Independent Test**: Given an approved syllabus, run the skeleton phase; confirm all skeletons are
drafted in one batch, the agent loop refines each until it matches its lesson topic and is clear (or
stops at the round cap and surfaces the unresolved delta), and the batch is presented for user
approval **without auto-advancing** to the lesson phase.

**Acceptance Scenarios**:

1. **Given** an approved, frozen syllabus, **When** the skeleton phase runs, **Then** it drafts
   **all** lesson skeletons in a single batch (not one interruption per lesson) and as a domain
   mentor (not by parroting sources).
2. **Given** a drafted skeleton batch, **When** the agent loop runs, **Then** an evaluator checks
   every skeleton for (a) match to its lesson's topic and (b) clarity / simple language, and the
   author refines against the evaluator's cited deltas.
3. **Given** the loop reaches the 3-round cap without every skeleton passing, **When** it stops,
   **Then** it emits the current best batch plus the unresolved deltas rather than looping further.
4. **Given** the agent loop has converged (or hit the cap), **When** the phase finishes its work,
   **Then** it **presents the batch for user approval and waits** — it does not treat the phase as
   complete or advance to the lesson phase without a recorded approval (honoring 001 FR-024).

---

### User Story 2 - Draft lessons via a parallel author–critic worker pool graded by the rubric (Priority: P2)

For each lesson, the factory spins up a **fresh-context author** and a **separate author-blind
evaluator**, and the orchestrating session mediates their author → critique → refine loop, keeping
**at most `pool_width` pairs in flight** at a time (MVP: 1; target: 2). Each lesson is graded against
004's rubric as the gate, every claim carries an `[Sn]` citation, and the evaluator checks that every
citation resolves to a real source. Per-lesson status is written to `BUILD_PROGRESS.md` as lessons
finish.

**Why this priority**: This is the phase's core output — the actual lessons. It builds on the
approved skeletons from US1 and turns each into graded, grounded content. Testable on its own given
an approved skeleton set and the rubric.

**Independent Test**: Given approved skeletons, a `SOURCES.md`, and the rubric, run the lesson pool;
confirm each lesson's author starts from a fresh context with the specified inputs, the evaluator
never receives the author's reasoning, at most `pool_width` pairs run concurrently, each lesson is
graded against the rubric, an unresolvable `[Sn]` citation fails the traceability check, and each
lesson's terminal status is recorded in `BUILD_PROGRESS.md`.

**Acceptance Scenarios**:

1. **Given** an approved skeleton for a lesson, **When** its author subagent starts, **Then** it runs
   in a **fresh context** whose inputs are the `COURSE_BRIEF.md`, the syllabus, that lesson's
   skeleton, the relevant `SOURCES.md` `[Sn]` entries, and the insights digest.
2. **Given** an authored lesson, **When** the evaluator subagent grades it, **Then** the evaluator is
   **author-blind** — it receives the lesson and the grading inputs but never the author's private
   reasoning.
3. **Given** several lessons to draft, **When** the pool runs, **Then** at most **`pool_width`**
   author–critic pairs are in flight at once (fan-out / fan-in), and the orchestrating session mediates each pair's
   author → critique → refine loop.
4. **Given** a lesson under evaluation, **When** the evaluator gates it, **Then** it grades the lesson
   against **004's rubric** and passes only if the rubric passes (subject to the same 3-round cap).
5. **Given** a lesson with factual claims, **When** the evaluator checks grounding, **Then** every
   claim carries an `[Sn]` key and the evaluator checks **traceability for every citation** — that
   each key resolves to a real `SOURCES.md` entry (it verifies tracing, not truth); an unresolvable
   citation fails the check.
6. **Given** a lesson reaches a terminal state (rubric-passed, or cap-hit and surfaced), **When** the
   pool records it, **Then** the lesson's per-lesson status is written to `BUILD_PROGRESS.md` before
   the pool considers that lesson done.

---

### User Story 3 - Calibrate explanation depth with a once-per-course fake-student check (Priority: P3)

When the **first two lessons** pass the rubric, the factory runs a single lightweight fake-student
check: a fresh subagent gets **only** the brief's audience + assumed prior knowledge and those two
lessons, reads them, and attempts the exercise. Its confusion points are fixed in those two lessons
**and folded into the drafting guidance for every remaining lesson**. It runs **once** per course.

**Why this priority**: This calibrates the whole course's explanation format from real reader
confusion, but only after there is passing content to test. It depends on US2 producing at least the
first two passing lessons and is separable: given two passing lessons, the check and its fold-in are
testable on their own.

**Independent Test**: With the first two lessons passing the rubric, run the fake-student check;
confirm the subagent receives **only** the audience + assumed prior knowledge and those two lessons
(no author reasoning, no other course context), that it reports concrete confusion points, that those
points are fixed in the two lessons, that they are folded into the drafting guidance used for the
remaining lessons, and that the check runs **exactly once** for the course.

**Acceptance Scenarios**:

1. **Given** the first two lessons have passed the rubric, **When** the fake-student check runs,
   **Then** a fresh subagent receives **only** the brief's audience + assumed prior knowledge and
   those two lessons, and attempts the exercise.
2. **Given** the fake-student reports confusion points (undefined terms, too-fast steps), **When**
   the phase responds, **Then** those points are fixed in the two lessons **and** folded into the
   drafting guidance for every remaining lesson.
3. **Given** a course build, **When** the phase completes, **Then** the fake-student check has run
   **exactly once** — it calibrates the explanation format, it is not re-run per lesson.

---

### Edge Cases

- **A skeleton never matches its topic within the cap** — the loop stops at 3 rounds and surfaces the
  best skeleton plus the unresolved delta for 001's round-cap decision; it does not loop forever.
- **A lesson never passes the rubric within the cap** — the pool stops at 3 rounds and emits the best
  lesson plus its scorecard for 001 to present to the user (accept-or-comment); the pool does not
  block on that lesson forever.
- **An author cites an `[Sn]` key absent from `SOURCES.md`** — the evaluator's traceability check
  fails; the lesson does not pass the gate until the citation resolves or the claim is removed. It is
  never passed on an unresolvable citation.
- **`SOURCES.md` is too thin to ground a lesson** — 003 follows 002's resolved thin-grounding policy
  (compose from mentor judgment, flag the thin grounding, tag affected claims mentor-added); it does
  not fabricate grounding and MUST preserve those flags/tags rather than present them as sourced. If
  the thin grounding exposes a syllabus gap, it is surfaced (see forward-diff below), not silently
  filled.
- **Authoring reveals a gap in an earlier gated artifact** (the frozen syllabus, or an approved
  skeleton once the lesson phase has started) — 003 surfaces it as an **explicit forward diff** to be
  applied at the current phase and does **not** re-open the earlier phase (honoring 001 FR-023).
- **Fewer than two lessons in the whole course** — the fake-student check runs once on the lesson(s)
  that exist rather than being skipped; it still runs at most once.
- **A lesson's format is `.ipynb`** (code-heavy course, decided in 002) — authoring and the
  traceability check operate on that format as written in `COURSE_BRIEF.md`; the pool does not
  re-decide the format.
- **The insights digest is empty** (early in the factory's life) — authors proceed without it; an
  empty digest is a valid input, not a blocker.
- **A lesson has no exercise** (possible under some profiles/modules) — the fake-student subagent
  falls back to **read-and-report-confusion only**: it reads the lesson and reports confusion points
  without attempting an exercise; the calibration still fixes and folds in those points (FR-014)
  despite the missing exercise step.
- **The orchestrating session selects the wrong or incomplete `[Sn]` entries for an author** (FR-007)
  — the author cannot cite a source it was never given, so an under-cited claim in this case is a
  **selection failure**, not an authoring one. The evaluator MAY flag a claim that plausibly matches
  an *existing but unpassed* `SOURCES.md` entry as a likely selection miss (distinct from a genuinely
  ungrounded claim), so the orchestrator's input-selection step can be corrected rather than only
  failing the lesson.

## Requirements *(mandatory)*

### Functional Requirements

**Shared author → critique → refine primitive**

- **FR-001**: The skeleton phase and the lesson phase MUST both use a **single shared** author →
  critique → refine primitive: an author produces or refines an artifact, an evaluator critiques it
  with specific deltas, and the author refines against those deltas, iterating until the evaluator
  passes or the round cap is reached.
- **FR-002**: The primitive MUST be capped at **3 refine rounds**. On reaching the cap without a
  pass, it MUST stop and emit the current best artifact plus its unresolved deltas / scorecard — it
  MUST NOT loop indefinitely. Presenting that surfaced artifact to the user for an accept-or-comment
  decision is owned by 001 (its FR-012); 003 produces the best-effort artifact and the delta report.
- **FR-003**: A refine round MUST address the evaluator's **cited deltas** (targeted revision), not
  restart the artifact from scratch, so the loop converges within the cap.

**Skeleton authoring**

- **FR-004**: The skeleton phase MUST draft **all** lesson skeletons in a **single batch** (big
  chunk), never interrupting the user per lesson, and MUST author them **as a domain mentor** —
  applying current-industry judgment, not parroting sources. Skeleton authoring MUST use a **single
  batch-level** author → critique → refine loop (one author over the whole set, one evaluator over
  the batch); the two-pairs-in-flight worker pool (FR-009) is **lesson-only** and MUST NOT be used
  for skeletons. **This mentor stance is factory-wide, not skeleton-specific** — FR-016 extends the
  same "sources inform, do not dictate" rule to lesson authoring.
- **FR-005**: The skeleton evaluator MUST check every skeleton for (a) **match to its lesson's
  topic** and (b) **clarity / good quality / simple language**, and the author MUST refine against
  the cited deltas via the shared primitive (FR-001, capped per FR-002).
- **FR-006**: After the agent loop converges (or hits the cap), the phase MUST **present the skeleton
  batch as a review-ready artifact for user approval and MUST NOT auto-advance** to the lesson phase.
  The blocking pause and the recording of approval are owned by 001 (FR-024); 003 MUST leave the
  skeleton phase in a review-ready, not-yet-advanced state.

**Lesson authoring — parallel author–critic worker pool**

- **FR-007**: Each lesson MUST be authored by a **fresh-context author subagent** whose inputs are
  the `COURSE_BRIEF.md`, the frozen syllabus **plus its `DIFFS.md` entries** (001 FR-027 — the frozen
  artifact and its applied diffs together are the canonical read, never the frozen artifact alone),
  that lesson's approved skeleton (plus any diffs applied against it), the **relevant** `SOURCES.md`
  `[Sn]` entries, the insights digest, and — for any lesson beyond the first two, once the fake-student
  calibration has run — `CALIBRATION.md` (FR-021) — and no other course context.
- **FR-008**: Each lesson MUST be graded by a **separate, author-blind evaluator subagent** that
  receives the authored lesson and the grading inputs but **never** the author's private reasoning.
- **FR-009**: The orchestrating session MUST mediate each author–evaluator pair's author → critique →
  refine loop and MUST keep **at most `pool_width` pairs in flight at a time** (a fan-out / fan-in
  worker pool), where `pool_width` is a **configurable parameter**. **MVP ships with `pool_width` =
  1** (fully serial — no fan-out/fan-in mediation, no concurrent `BUILD_PROGRESS.md` writes to order);
  the **design target is 2** once real runs validate the concurrency model. Every other FR/SC in this
  spec is unaffected by the value of `pool_width` — a single-pair pool is a valid, degenerate case of
  "at most `pool_width` in flight."
- **FR-010**: Each lesson MUST be gated by **004's rubric**: the evaluator grades the lesson against
  the rubric and the lesson passes only if the rubric passes, subject to the 3-round cap (FR-002).
  003 consumes the rubric as a pass/fail gate and MUST NOT redefine its contents.
- **FR-011**: Every factual claim in a lesson MUST either carry an `[Sn]` citation key resolving to
  `SOURCES.md` **or** be explicitly marked as **mentor-added judgment** (mirroring 002's grounding
  rule and its resolved compose-and-flag thin-grounding policy) — there MUST be no silently
  ungrounded claim. The evaluator MUST check **traceability for every citation in the lesson** — that
  each `[Sn]` key resolves to a real source entry (it verifies tracing, **not** truth) — and MUST fail
  a lesson whose citation does not resolve or whose claim is neither cited nor marked mentor-added.
  Resolution is a cheap, mechanical lookup against `SOURCES.md` — unlike verifying truth, it does not
  require sampling, so the check covers every citation, not a subset (see SC-004). Thin-grounding
  flags and mentor-added tags inherited from 002 MUST be preserved, never re-presented as sourced.
  This is the lesson-level application of the factory's **canonical citation/grounding contract** (004
  FR-007/FR-008); 003 applies it per lesson rather than re-deriving an independent rule.
- **FR-012**: As each lesson reaches a terminal state (rubric-passed, or cap-hit and surfaced), the
  phase MUST write that lesson's **per-lesson status** to `BUILD_PROGRESS.md` before treating the
  lesson as done. The state file's schema and resume semantics are owned by 001; 003 only updates the
  per-lesson status within the lesson phase.

**Fake-student learnability check**

- **FR-013**: When the **first two lessons reach a terminal state** — rubric-passed, or
  cap-surfaced-and-user-accepted — the phase MUST run a **single**, lightweight fake-student check: a
  fresh subagent that receives **only** the brief's audience + assumed prior knowledge and those two
  lessons, reads them, and attempts the exercise. If the course has fewer than two lessons, the check
  runs once on the lesson(s) that exist; it MUST NOT block waiting for a lesson that never passes.
- **FR-014**: The fake-student's confusion points (e.g., undefined terms, too-fast steps) MUST be
  **fixed in those two lessons** AND **folded into the drafting guidance for every remaining lesson**.
  Because this **edits an already-passed lesson**, each edited lesson MUST be **re-graded against the
  rubric** (FR-010) before the fake-student check is considered complete — a fix MUST NOT silently
  regress a previously-passed dimension. If a re-grade fails, the edited lesson re-enters the
  author→critique→refine loop (FR-001) under a fresh round cap (mirroring FR-024's change-request
  pattern in 001).
- **FR-015**: The fake-student check MUST run **at most once per course** — it calibrates the
  explanation format for the whole course; it MUST NOT be re-run per lesson.

**Mentor stance, grounding & cross-phase seams**

- **FR-016**: Lessons MUST be authored **as a domain mentor** — sources inform but do not dictate —
  the same stance FR-004 already requires for skeletons (see FR-004's note); the evaluator's grounding
  checks are about **traceability**, not about parroting sources.
- **FR-017**: When authoring reveals a gap in an already-gated earlier artifact (the frozen syllabus,
  or an approved skeleton once the lesson phase has begun), the phase MUST surface it as an
  **explicit forward diff** applied at the current phase and MUST NOT re-open or re-flow the earlier
  gated phase (honoring 001 FR-023). It MUST NOT change a frozen artifact silently.
- **FR-018**: The pool MUST author the **first two lessons first**, run the fake-student calibration
  (FR-013–FR-015), and **only then fan out the remaining lessons** — every remaining lesson MUST be
  authored with the calibration already folded into its drafting guidance (**gate-then-fan-out**).
  The pool MUST NOT begin any lesson beyond the first two before the calibration completes. **While a
  cap-surfaced first-or-second lesson awaits the author's accept-or-comment decision** (001 FR-012),
  **the pool idles** — it does not proceed to calibration or fan-out on a partial/unaccepted terminal
  state. This is a wait, not a skip, and matches 001's ask-moment carve-out (001 FR-014), which
  treats this accept-or-comment decision as a gate, not a content ask-moment.

**Profile consumption (000's archetype profiles)**

- **FR-019**: Skeleton and lesson authoring MUST respect the course's selected archetype profile
  (001's overlay decision, per 000 FR-022) — its scaffolding depth and the placement of any
  **advisory** checkpoint notes (000 FR-022: never a hard gate) — without altering the shared
  author→critique→refine primitive (FR-001) or the rubric gate (FR-010), which apply uniformly
  regardless of profile.

**Feedback capture (write side of Principle XII)**

- **FR-020**: When the evaluator's critique (skeleton or lesson) surfaces a durable finding worth
  carrying forward — not merely a delta the author already resolved within the round cap — the phase
  MUST append it to the course's `FEEDBACK.md`. This is 003's write-side contribution to Principle
  XII's compounding loop, alongside 001's gate-event writes (001 FR-026); harvesting `FEEDBACK.md`
  into `insights/` remains 004's and is user-invoked only.

**Calibration persistence**

- **FR-021**: The fake-student calibration's output (confusion points + resulting drafting guidance)
  MUST be persisted to the course's **`CALIBRATION.md`**, created once the check completes
  (FR-013–FR-015). Every author subagent for a lesson beyond the first two MUST read `CALIBRATION.md`
  as an input (FR-007) — a session dying post-calibration resumes from this file rather than losing
  the guidance (honoring 001's disk-only resume rule, 001 FR-018).

### Key Entities

- **Skeleton** — a per-lesson plan; the skeleton phase's batch artifact, checked for topic-match and
  clarity, then presented for the user scan.
- **Lesson** — a full lesson in the decided format (`.md`/`.ipynb`); the lesson phase's headline
  output, graded against the rubric and grounded by `[Sn]` citations.
- **Author subagent** — a fresh-context worker that drafts/refines one skeleton or lesson from a fixed
  input set; carries no cross-lesson context.
- **Evaluator subagent** — an author-blind worker that critiques an artifact against its checks
  (topic-match + clarity for skeletons; the rubric + full citation-traceability check for lessons —
  every citation, not a sample); never sees the author's reasoning.
- **Author–critic pair** — one author + one evaluator running the shared author → critique → refine
  loop for a single artifact.
- **Worker pool** — the fan-out / fan-in orchestration that keeps at most `pool_width` author–critic
  pairs in flight over the lesson set (FR-009); a configurable parameter, MVP = 1, target = 2.
- **Author → critique → refine primitive** — the shared, 3-round-capped loop used by both phases.
- **Round cap** — the hard limit of 3 refine rounds; on reaching it, the best-effort artifact + delta
  is surfaced (for 001's decision).
- **Rubric** — the lesson gate; defined and owned by 004, consumed here as pass/fail.
- **`[Sn]` citation** — a claim's pointer into `SOURCES.md`; required on every sourced lesson claim
  (mentor-added claims are explicitly marked instead) and checked for traceability, every citation,
  not a sample (FR-011).
- **Traceability check** — the evaluator's verification that **every** citation in a lesson resolves
  to a real source (tracing, not truth) — a full check, not a spot-check, because resolution is a
  cheap mechanical lookup.
- **Fake-student subagent** — the once-per-course learnability probe reading the first two lessons as
  the target audience.
- **Confusion points / calibration** — the fake-student's findings, fixed in the first two lessons and
  folded into the drafting guidance for the rest.
- **Drafting guidance** — the shared explanation-format guidance given to lesson authors; updated once
  by the fake-student calibration.
- **Insights digest** — the cross-course learnings (from `insights/`) read as an author input; may be
  empty.
- **`BUILD_PROGRESS.md` per-lesson status** — the phase's write into 001's state file as each lesson
  finishes.
- **Forward diff** — the mechanism by which a gap found in an earlier gated artifact is surfaced at
  the current phase without re-opening it (001 FR-023), recorded in 001's `DIFFS.md` ledger (001
  FR-027). Authors read the frozen artifact **plus** its `DIFFS.md` entries as one canonical input.
- **Selected profile** — the course's chosen archetype profile (001's overlay decision, 000's
  mechanism); shapes this phase's scaffolding depth and advisory-checkpoint placement (FR-019).
- **`FEEDBACK.md`** — the per-course critique file; this phase **appends** durable evaluator findings
  to it (FR-020) alongside 001's gate-event writes. Harvesting into `insights/` is 004's, user-invoked
  only.
- **`CALIBRATION.md`** — the fake-student calibration's persisted output (confusion points + drafting
  guidance), created once the check completes (FR-021); read by every author of a lesson beyond the
  first two.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The author → critique → refine loop runs **at most 3 rounds** per artifact in **100%**
  of runs — **0** unbounded loops; on the cap it surfaces a best-effort artifact + delta **100%** of
  the time.
- **SC-002**: **100%** of lessons are authored by a fresh-context author and graded by a separate
  author-blind evaluator — the evaluator receives the author's private reasoning **0** times.
- **SC-003**: The worker pool holds **at most `pool_width`** author–critic pairs in flight at any
  moment (MVP: `pool_width` = 1; target: 2) — **0** runs exceed the configured `pool_width`.
- **SC-004**: **100%** of factual claims in passed lessons are either `[Sn]`-cited or explicitly
  marked mentor-added judgment (**0** silently ungrounded claims), and **0** lessons pass the gate
  with an unresolvable citation (every traceability failure blocks the pass).
- **SC-005**: The skeleton phase presents the batch for user approval and **auto-advances 0 times**
  to the lesson phase without a recorded user approval (consistent with 001 FR-024).
- **SC-006**: The fake-student check runs **exactly once** per course (never 0 when ≥1 lesson reaches
  a terminal state, never more than 1), and its confusion points are folded into the drafting
  guidance for **100%** of the remaining lessons. Both calibration-edited lessons are **re-graded**
  against the rubric before the check is considered complete — **0** unregraded edits to an
  already-passed lesson.
- **SC-007**: **100%** of lessons reaching a terminal state have their per-lesson status written to
  `BUILD_PROGRESS.md` before the pool treats them as done — **0** lessons finalized without a status
  write.
- **SC-008**: Every gap found in an earlier gated artifact is surfaced as a forward diff **100%** of
  the time; the phase re-opens a passed, gated phase **0** times (consistent with 001 FR-023).
- **SC-009**: Each skeleton in an approved batch matches its lesson's topic and reads clearly (passed
  the skeleton evaluator or was explicitly user-accepted at the cap) in **100%** of delivered batches
  — **0** silently unmatched skeletons.
- **SC-010**: In **100%** of multi-lesson courses, **0** lessons beyond the first two are begun before
  the fake-student calibration has completed (gate-then-fan-out ordering is never violated).

## Assumptions

- **The approved, frozen syllabus and the instantiated course exist** — 001 has produced the course
  folder, `COURSE_BRIEF.md`, and `BUILD_PROGRESS.md`, and 002 has produced the approved syllabus and
  populated `SOURCES.md`. 003 reads these; it does not create them.
- **004's rubric exists before the lesson phase runs** — per the seam log and recommended build order
  (004's rubric core lands before 003). 003 consumes it as a pass/fail gate; if the rubric is absent,
  the lesson gate cannot run (a 001/004 prerequisite, not a 003 responsibility).
- **The lesson-file-format decision (`.md`/`.ipynb`)** was made in 002 and recorded in
  `COURSE_BRIEF.md`; 003 authors in that format and does not re-decide it.
- **"Relevant `[Sn]` entries"** for an author are the `SOURCES.md` entries tied to that lesson's
  skeleton topics; the orchestrating session selects and passes them, so a fresh author need not scan
  all of `SOURCES.md`.
- **The evaluator re-grades the current artifact each round** and may see its own prior critiques (to
  confirm cited deltas were addressed), but it never receives the author's private reasoning — the
  "author-blind" property is about the author's chain of thought, not about the artifact's history.
- **The insights digest may be empty** early in the factory's life; authors treat an empty digest as
  a valid input.
- **002's resolved thin-grounding policy (its FR-011: compose + flag) governs how much grounding a
  lesson may assume** when `SOURCES.md` is thin: lessons may rely on flagged, mentor-added grounding
  but MUST preserve the thin-grounding flags and mentor-added tags rather than presenting them as
  sourced. 003 follows that policy rather than defining its own.
- **The round cap (3), the fresh-context author / author-blind evaluator split, and the once-per-course
  fake-student scope** are taken as fixed from the design and the constitution; they are calibratable
  later but treated as hard constraints here. (`pool_width` is the one exception, deliberately made
  configurable — FR-009 — starting at MVP = 1.) **Of these, the fake-student scope is the first knob
  to revisit** if early real runs show low calibration yield — the settled gate-then-fan-out ordering
  (FR-018) governs it *given* it runs, not whether it ships in the first increment.
- **`.ipynb` citation mechanics are plan-level detail.** When a lesson's format is `.ipynb` (002's
  decision), `[Sn]` keys live in markdown cells (not code-cell comments or outputs) so the
  traceability check can read them via the same text-scan method as `.md` lessons; the exact
  cell-parsing approach is left to this spec's `/speckit-plan`.
- **"First two lessons" means the first two to reach a terminal state** (rubric-passed or
  cap-surfaced-and-user-accepted), in syllabus order; the fake-student check keys off accepted
  content, not merely drafted content, and cannot deadlock on a lesson that never passes (see
  Clarifications).
- **The pool is gate-then-fan-out** — the first two lessons (up to two pairs in flight) are drafted,
  the fake-student calibration runs, and only then are the remaining lessons fanned out two-at-a-time
  with the calibration folded in. Skeleton authoring is a separate single batch-level loop (FR-004).
