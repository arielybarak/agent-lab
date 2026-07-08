# course-factory specs — index & roadmap

The factory is decomposed into **four subject-specs**, ordered by pipeline flow. Each is an
independently specifiable / plannable / implementable unit (`spec.md` → `plan.md` → `tasks.md`), so
the work can be split across sessions: a fresh session reads this index, picks one spec, and works
it without re-deriving the decomposition.

Governing doc: [`course-factory/DESIGN.md`](../../course-factory/DESIGN.md) (source of truth) and
the project constitution at [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md).

> **Two "resumabilities" — don't conflate them.**
> - `BUILD_PROGRESS.md` resumes a **course build** (runtime, one per generated course).
> - This index + `specs/**` resumes **our development of the factory** (build-time, across sessions).

## The four specs

| # | Spec | Owns | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- |
| **001** | **Pipeline & Instantiation** | intake clarify interview, `COURSE_BRIEF.md` overlay + module selection, frozen-template copy/overlay/version contract, the phase state machine, gates, resume, delivery contract | course-template asset | **Clarified** (2 Qs resolved) — ready for `/speckit-plan` |
| **002** | **Syllabus** | research & sourcing → `SOURCES.md`, compose-as-mentor, the `.md`/`.ipynb` lesson-format decision, the user-approval gate's content | 001 | **Clarified** (2 Qs resolved) — ready for `/speckit-plan` |
| **003** | **Lessons** | skeleton & lesson authoring, the parallel author–critic worker pool, the fake-student learnability check | 001, 004 (rubric) | **Clarified** (3 Qs resolved) — ready for `/speckit-plan` |
| **004** | **Grading & Delivery** | the rubric & course-evaluator internals, `COURSE_REPORT.md` scorecard, `FEEDBACK.md` → `insights/` harvest, `comparison/` | 001 | **Clarified** (3 Qs resolved) — ready for `/speckit-plan` |

Status legend: **Not started** → **Drafted** (spec.md written) → **Clarified** → **Planned**
(plan.md) → **Tasked** (tasks.md) → **In progress** → **Done**.

## What each spec covers

### 001 — Pipeline & Instantiation → [`001-pipeline-skeleton/spec.md`](001-pipeline-skeleton/spec.md)

The front-end + the spine. Turns a rough `COURSE_SPEC.md` into a set-up, resumable course build and
walks it through the fixed phase sequence to delivery. Treats each phase's *internal work* as a
black box behind its gate. **Open questions:** backward-transition policy (FR-023), post-skeleton
user-scan blocking behavior (FR-024) — resolve with `/speckit-clarify` before planning.

### 002 — Syllabus

The depth behind the **syllabus gate**: shallow research (web + `gh` + Udemy/Coursera/edX
name-search) with a convergence + budget stopping rule, saved to `SOURCES.md` under `[Sn]` keys;
compose-as-mentor (sources inform, never dictate); decide course volume and the `.md`/`.ipynb`
format, writing the format back into `COURSE_BRIEF.md`. Ends at the user-approval gate; approved
syllabus is frozen.

### 003 — Lessons

The depth behind the **skeleton and lesson gates**: the shared author → critique → refine primitive
(3-round cap); the parallel author–critic worker pool (fresh-context authors + author-blind
evaluators, two pairs in flight); the once-per-course fake-student learnability check on the first
lessons. Consumes 004's rubric as the lesson gate.

### 004 — Grading & Delivery

The **rubric and everything it feeds**: the one-rubric-two-layers definition (generic core + topic
add-ons) and course-evaluator, the graded `COURSE_REPORT.md`, the `FEEDBACK.md` → `insights/`
harvest so the factory compounds, and `comparison/` (analyze GitHub courses → propose rubric
revisions). It owns the *only* definition of quality.

## Foundational assets (prerequisites, not specs)

- **`course-template/` distillation** (DESIGN roadmap task #1) — extract the topic-neutral core
  (syllabus, lesson arc, rubric, `/improve-course`, `/new-lesson`) from `System_Design_SelfLearn`
  into the frozen, tiered template; demote SD-specific pieces to optional modules. **001's copy
  contract depends on this existing.**
- **`COURSE_SPEC.template.md`** — the author-facing spec template (initial draft exists in
  `../templates/`).

## Seams to watch (cross-spec)

1. **The rubric is shared** — it is the *gate* in 003 but the *engine* in 004. Define it in 004;
   003 consumes it. 004's rubric core likely needs to land (or a thin shared contract) before 003.
2. **`COURSE_BRIEF.md`** — created by 001, augmented by 002 (the format decision), read by 002/003/004.
3. **`BUILD_PROGRESS.md` / phase state** — owned by 001; 002 and 003 update per-lesson/phase status
   as they run behind their gates.
4. **`course-template/`** — the foundational asset above; a hard prerequisite for 001.

## Resolved decisions (seam log)

Clarify outcomes per spec, recorded here so a cold session can honor settled decisions from **this
index alone** — without opening each spec's `Clarifications` section. **Update this whenever
`/speckit-clarify` resolves a marker** (mirror the spec's `Clarifications` entry, and note which
sibling specs it constrains).

### 001 — Pipeline & Instantiation · Session 2026-07-07

- **Backward transitions = forward-diff only** (FR-023). Gated phases are immutable once passed; a
  change to an earlier phase is applied as an explicit forward diff at the *current* phase — never by
  re-opening it. → *Constrains 002/003/004*: on finding a gap in an earlier artifact, surface a diff;
  do not reopen the phase.
- **Post-skeleton user scan = blocking gate** (FR-024). After agent review of the skeleton batch
  passes, the pipeline pauses for explicit user approval before the lesson phase starts. →
  *Constrains 003*: the skeleton phase presents for approval and waits; it does **not** auto-advance.

### 002 — Syllabus · Session 2026-07-07

- **Research cap unit = search/tool-call budget** (FR-005). Research stops at convergence or a max
  query/tool-call count — never unbounded. (Budget value calibratable; the unit is a query count.)
- **Thin-grounding policy = compose + flag** (FR-011). On near-zero reliable sources, compose from
  mentor judgment, mark the course/sections thinly-grounded, and tag affected topics mentor-added —
  never block or fabricate. → *Constrains 003*: lessons may rely on flagged, mentor-added grounding,
  but MUST preserve the thin-grounding flags and mentor-added tags rather than presenting them as
  sourced.

### 003 — Lessons · Session 2026-07-07

- **Pool ordering = gate-then-fan-out** (FR-018). The lesson worker pool drafts lessons 1 & 2 first,
  runs the once-per-course fake-student calibration, and **only then** fans out the remaining lessons
  (two pairs in flight) with the calibration folded in — no lesson beyond the first two begins before
  the calibration completes. → *Self-contained to 003*; sets the pool's ordering contract.
- **Fake-student trigger = first two to reach a terminal state** (FR-013). The check fires on the
  first two lessons that are rubric-passed **or** cap-surfaced-and-user-accepted (in syllabus order);
  with fewer than two lessons it runs once on what exists, and it never blocks on a lesson that never
  passes. → *Consumes 001's cap-surface/accept contract* (its FR-012) — "terminal state" includes a
  user-accepted-at-cap lesson.
- **Skeleton authoring = single batch-level loop** (FR-004). One author drafts all skeletons at once
  and one evaluator critiques the batch; the two-pairs-in-flight worker pool is **lesson-only**. →
  *Self-contained to 003*; distinguishes the batch skeleton loop from the per-lesson pool.

### 004 — Grading & Delivery · Session 2026-07-08

- **Rubric pass = per-dimension threshold** (FR-004). Every generic-core dimension and every requested
  topic add-on must clear its own minimum bar; a lesson or course passes only if **no** dimension is
  below threshold (no aggregate masking), while per-dimension scores are retained for the scorecard.
  → *Constrains 003*: this is the exact pass contract 003's per-lesson gate consumes — a lesson passes
  only when every rubric dimension clears its bar.
- **Course verdict = independent course-level grading** (FR-009). The course-evaluator additionally
  grades whole-arc dimensions (coverage across the syllabus, flow/continuity, the running-example
  thread) and MAY return a "needs work" verdict **even when every lesson already passed**; such gaps
  feed the `/improve-course` backlog as a forward diff (001 FR-023), never a phase re-open. →
  *Self-contained to 004*; distinguishes the course-level verdict from a per-lesson-pass roll-up.
- **Harvest = user-invoked only** (FR-015/016). No automatic/scheduled `FEEDBACK.md` → `insights/`
  harvest; both the per-insight capture and the `setup-retro`-style bulk harvest run only when the
  user invokes them, keeping 004 decoupled from 001's phase transitions. → *Loosens the 001 seam*: the
  harvest is **not** wired into delivery or phase advancement.

## Recommended build order

`course-template/` asset → **001** → **002** → **004 (rubric core)** → **003** → **004 (delivery,
feedback harvest, comparison)**. Rationale: the spine and instantiation first; then the first gate's
depth (syllabus); the rubric must exist before lessons can be graded; delivery/feedback last.
