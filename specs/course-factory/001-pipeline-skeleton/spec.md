# Feature Specification: Course-Factory Pipeline & Instantiation

**Feature Branch**: `001-pipeline-skeleton`

**Created**: 2026-07-07

**Status**: Draft

**Input**: User description: "Build the course-factory pipeline skeleton: given a user-written COURSE_SPEC.md, run an intake step that produces a COURSE_BRIEF.md overlay and a selected set of optional modules, copy the frozen course-template into a new course folder with that overlay applied, then execute a phased review loop — syllabus (user-approved), lesson skeletons (agent-reviewed then user-scanned), and full lessons (automated rubric-graded) — tracking the current phase and per-lesson status in BUILD_PROGRESS.md so the process can pause and resume across sessions, and finishing with a delivered course plus a graded COURSE_REPORT.md."

## Overview

This is **spec #1 of four subject-specs** for the course factory. It owns two joined subjects:

1. **Instantiation (the front-end)** — turning a rough author-written `COURSE_SPEC.md` into a
   set-up course: the intake clarify interview, the `COURSE_BRIEF.md` overlay, the optional-module
   selection, and the copy of the frozen template into a new course folder.
2. **Orchestration (the spine)** — the fixed phase sequence, the gates between phases, and the
   on-disk state (`BUILD_PROGRESS.md`) that makes a build pausable and resumable across sessions.

It treats each *phase's internal work* (research, content authoring, grading) as a black box that
emits an artifact and a gate result. The three later subject-specs fill that depth:

- **Spec 002 — Syllabus**: research & sourcing → `SOURCES.md`, compose-as-mentor, the `.md`/`.ipynb`
  lesson-format decision (written back into the brief), the user-approval gate's content.
- **Spec 003 — Lessons**: skeleton & lesson authoring, the parallel author–critic worker pool, the
  fake-student learnability check.
- **Spec 004 — Grading & delivery**: the rubric contents & course-evaluator internals, the graded
  `COURSE_REPORT.md` scorecard, `FEEDBACK.md` → `insights/` harvest, and `comparison/`.

### Out of Scope (owned by the specs above)

- **Syllabus-phase depth** — how research searches the web / GitHub / course platforms and populates
  `SOURCES.md`, and how the syllabus is composed. Here, `SOURCES.md` is created and referenced, not
  populated; the syllabus phase is a black box behind its gate. → **002**
- **Lesson-phase depth** — skeleton/lesson authoring, the fan-out/fan-in worker pool of
  fresh-context authors and author-blind evaluators, the fake-student check. → **003**
- **Grading depth** — the rubric's contents and the course-evaluator internals; the lesson gate and
  the final report are treated as pass/fail + scorecard black boxes here. → **004**
- **The pedagogical content of `course-template/`** — distilling the frozen template's lessons,
  rubric, and modules from `System_Design_SelfLearn` is a **foundational asset** (roadmap task #1).
  This spec defines only the *copy / overlay / version* contract over that template, not its content.
- **The physical move of a delivered course out of the staging repo** — done by the author manually.
- **Content quality itself** — this spec governs *movement between phases, instantiation, and
  state*, not whether a lesson is well written.

## Clarifications

### Session 2026-07-07

- Q: When the author wants a change that belongs to an already-gated earlier phase (beyond the
  frozen-syllabus diff rule), how should the state machine handle it? → A: **Forward-diff only** —
  earlier gated phases are immutable; the change is applied as an explicit forward diff at the
  current phase, and the machine never re-opens or re-flows a passed phase.
- Q: After lesson skeletons pass agent review, is the author's scan a blocking gate or an advisory
  review? → A: **Blocking** — the pipeline pauses after agent review passes and waits for the
  author's explicit approval (or change request) before starting the lesson phase; a single
  batch-level pause.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Intake a spec into an instantiated, resumable course build (Priority: P1)

An author points the factory at a rough `COURSE_SPEC.md`. The factory runs an **upfront clarify
interview** (the first of the two designated ask-moments), resolves knowable ambiguities without
inventing missing content, authors a `COURSE_BRIEF.md` overlay, and picks the optional modules. It
then copies the **frozen** `course-template/` into a new course folder, applies the overlay, stamps
the template version, and initializes `BUILD_PROGRESS.md` at the start of the syllabus phase — never
editing the template.

**Why this priority**: This is the foundational MVP. Everything downstream needs a correctly set-up,
version-stamped, overlay-applied course folder. Built alone it delivers real value — the hard
intake + overlay + versioning contract — and is independently demonstrable from a rough spec, with
no later phase required.

**Independent Test**: Provide a rough `COURSE_SPEC.md` (with a knowable gap and a missing required
field); run intake + instantiation; confirm the interview surfaces the gap and blocks on the missing
required field instead of inventing it; confirm a new course folder exists with a `COURSE_BRIEF.md`
capturing the required elements, an explicit module selection, a stamped template version, and a
`BUILD_PROGRESS.md` positioned at syllabus start; confirm the source `course-template/` is unchanged.

**Acceptance Scenarios**:

1. **Given** a rough `COURSE_SPEC.md`, **When** intake runs, **Then** it conducts an upfront clarify
   interview that resolves knowable ambiguities before any downstream phase begins.
2. **Given** a spec missing a required field (e.g., the running example), **When** intake runs,
   **Then** it surfaces this as a blocking question and does **not** fabricate a value.
3. **Given** a clarified spec, **When** intake completes, **Then** it produces a `COURSE_BRIEF.md`
   overlay capturing topic & scope, audience + assumed prior knowledge, the required running example,
   and pointers to the spec's source material, plus an explicit enabled/disabled module selection.
4. **Given** intake output, **When** the copy step runs, **Then** the frozen template is copied into
   a new course folder, the overlay is applied, the enabled modules are present, and the template
   version is stamped into the course.
5. **Given** the copy step has run, **When** the source `course-template/` is inspected, **Then** it
   is byte-for-byte unchanged (overlay, not mutation).
6. **Given** a fresh course folder, **When** instantiation finishes, **Then** `BUILD_PROGRESS.md`
   exists and records the pipeline positioned at the start of the syllabus phase.

---

### User Story 2 - Walk the instantiated build through the phased pipeline to delivery (Priority: P2)

Given an instantiated course, the factory advances it through the fixed sequence of phases —
syllabus, lesson skeletons, full lessons, delivery — each ending at a review gate matched to the
competent reviewer. When every gate clears, the author receives a delivered course folder and a
graded `COURSE_REPORT.md`.

**Why this priority**: This is the orchestration spine that makes it a *pipeline*. It builds on the
instantiated folder from US1 and turns it into a delivered course. Testable on its own by driving an
already-instantiated course through the phase gates.

**Independent Test**: Start from an instantiated course folder; drive it through the phases with each
phase's work stubbed to "produced + gate cleared"; confirm phases run strictly in order, each gate
is reached and recorded before advancing, and the run ends with the required per-course artifacts
plus a `COURSE_REPORT.md` scorecard.

**Acceptance Scenarios**:

1. **Given** an instantiated course, **When** the pipeline runs, **Then** it advances through the
   phases strictly in order (syllabus → skeletons → lessons → deliver), never skipping a phase.
2. **Given** any phase's work has completed, **When** the pipeline evaluates that phase's gate,
   **Then** it advances only if the gate clears and otherwise loops the phase.
3. **Given** the pipeline reaches delivery, **When** it finishes, **Then** the course folder contains
   `COURSE_BRIEF.md`, `SOURCES.md`, `BUILD_PROGRESS.md`, `FEEDBACK.md`, `COURSE_REPORT.md`, and the
   `.claude/` residue.
4. **Given** delivery completes, **When** the author inspects `COURSE_REPORT.md`, **Then** it holds a
   graded scorecard (rubric scores + verdict) for the course.

---

### User Story 3 - Pause and resume a build across sessions (Priority: P3)

A build spans many sessions. The author (or a fresh session) can stop at any point and later resume
exactly where the build left off — the correct phase, and within a phase, the exact set of lessons
already done — without redoing completed work or losing progress.

**Why this priority**: Course builds are long and multi-session; resumability is the durability
property that keeps the spine usable across interruptions. Separable: given a mid-build course
folder, resuming is testable on its own.

**Independent Test**: Take a course folder whose `BUILD_PROGRESS.md` shows it mid-way through the
lesson phase with some lessons passed and some not; start a new session pointed at it; confirm the
pipeline resumes at the lesson phase, skips the passed lessons, and works only the remaining ones.

**Acceptance Scenarios**:

1. **Given** a course whose `BUILD_PROGRESS.md` records the current phase and per-lesson status,
   **When** a new session starts, **Then** the pipeline reads that file and resumes at the recorded
   phase without repeating completed phases.
2. **Given** the lesson phase with lessons 1–3 marked passed and 4–6 not started, **When** the build
   resumes, **Then** only lessons 4–6 are worked and 1–3 are left untouched.
3. **Given** a unit of progress completes (a phase clears, or a lesson changes status), **When** the
   pipeline records it, **Then** `BUILD_PROGRESS.md` is updated before the next unit begins, so an
   interruption immediately after loses no progress.
4. **Given** several courses exist in staging, **When** a session resumes a build, **Then** it acts
   on the one named course and its own `BUILD_PROGRESS.md`, independent of the others.

---

### Edge Cases

- **Missing or malformed `COURSE_SPEC.md`** — the pipeline halts at intake with a clear reason and
  writes no partial course folder.
- **Missing required spec fields** (e.g., no running example) — intake surfaces this as a blocking
  question rather than inventing content, consistent with anti-fabrication.
- **Corrupt, missing, or internally-inconsistent `BUILD_PROGRESS.md` on resume** — the pipeline
  refuses to guess; it reports the inconsistency and asks the author how to proceed rather than
  silently redoing or skipping work.
- **A gate never clears** (author never approves syllabus; lessons never pass the rubric within the
  round cap) — after the capped rounds, the pipeline surfaces the current best artifact plus its
  status to the author for an accept-or-comment decision instead of looping forever.
- **A later phase reveals a gap in an already-gated earlier artifact** (e.g., syllabus) — the
  change is shown to the author as an explicit forward diff and applied at the current phase; the
  earlier phase is never silently re-opened (FR-023).
- **The frozen `course-template/` is missing or unversioned at instantiation** — the pipeline halts
  rather than copying an unversioned or absent template.
- **Resuming a course whose stamped template version differs from the current template** — the
  pipeline flags the version drift rather than mixing versions silently.
- **Two sessions attempt to advance the same course at once** — only one may hold the build; the
  state file is the single source of truth for whose turn it is.

## Requirements *(mandatory)*

### Functional Requirements

**Foundational dependency**

- **FR-001**: The pipeline MUST depend on a **frozen, versioned, tiered** `course-template/` (a small
  mandatory core plus opt-in optional modules) existing at build time. Instantiation COPIES it and
  MUST NOT author or mutate its pedagogical content. If the template is absent or unversioned,
  instantiation MUST halt.

**Intake & brief authoring**

- **FR-002**: Intake MUST read the author's `COURSE_SPEC.md` and conduct an **upfront clarify
  interview** (ask-moment #1) that resolves knowable ambiguities **before** any downstream phase
  begins.
- **FR-003**: Intake MUST NOT invent missing required content; a missing required field (e.g., the
  running example) MUST surface as a **blocking question**, not a fabricated default.
- **FR-004**: Intake MUST produce a `COURSE_BRIEF.md` overlay capturing at minimum: topic & scope
  (in/out), audience + assumed prior knowledge, the required running example, and pointers to the
  spec's source material.
- **FR-005**: Intake MUST produce an **explicit** optional-module selection (enabled/disabled) over
  the template's available modules.

**Overlay instantiation**

- **FR-006**: The instantiation step MUST copy the frozen `course-template/` into a new course
  folder, apply the overlay, include the enabled optional modules, and stamp the copied template's
  version into the course.
- **FR-007**: The pipeline MUST NOT modify the source `course-template/` at any point (overlay, not
  mutation).
- **FR-008**: Instantiation MUST create an empty `BUILD_PROGRESS.md` positioned at the start of the
  syllabus phase, and MUST create the `SOURCES.md` and `FEEDBACK.md` stubs so the folder contract
  holds even before later phases populate them.

**Pipeline shape & gates**

- **FR-009**: The pipeline MUST advance through a fixed, ordered phase sequence: intake → template
  instantiation (copy + overlay) → syllabus → lesson skeletons → full lessons → delivery.
- **FR-010**: The pipeline MUST NOT advance from a phase until that phase's gate has cleared, and
  MUST record which gate cleared and when.
- **FR-011**: Each phase's gate MUST be matched to the competent reviewer: **syllabus →
  user-approval**; **lesson skeletons → agent review passes, then user scan**; **full lessons →
  automated rubric grade passes** (no mandatory deep user review).
- **FR-012**: The automated inner loop for the skeleton and lesson phases (author → critique →
  refine) MUST be capped at 3 rounds; on reaching the cap without clearing, the pipeline MUST
  surface the current best artifact plus its status to the author for an accept-or-comment decision.
- **FR-013**: Once the syllabus gate clears, the syllabus MUST be treated as frozen: any later
  change to it MUST be presented to the author as an explicit diff and MUST NOT be applied silently.
- **FR-014**: The pipeline MUST ask the author only at the two designated moments — upfront intake
  (FR-002), and post-research only when sources diverge — and MUST NOT interrupt the author per-item
  during batch generation.

**State, resumability & delivery**

- **FR-015**: `BUILD_PROGRESS.md` MUST record the current phase and, within the lesson phases, the
  per-lesson status of every lesson.
- **FR-016**: The pipeline MUST persist state to `BUILD_PROGRESS.md` after each unit of progress (a
  phase clearing, or a lesson changing status) before beginning the next unit.
- **FR-017**: On start, the pipeline MUST read `BUILD_PROGRESS.md` and resume at the recorded phase
  and lesson set, performing no work that the file records as already complete.
- **FR-018**: Resuming MUST require no state beyond what lives in the course folder — a fresh session
  with no memory of prior sessions MUST be able to continue solely from on-disk artifacts.
- **FR-019**: Multiple courses MUST be able to coexist in staging, each with its own independently
  resumable `BUILD_PROGRESS.md`; a resume operation MUST act on exactly one named course.
- **FR-020**: On delivery, the course folder MUST contain the required per-course artifacts:
  `COURSE_BRIEF.md`, `SOURCES.md`, `BUILD_PROGRESS.md`, `FEEDBACK.md`, `COURSE_REPORT.md`, and the
  `.claude/` residue.
- **FR-021**: Delivery MUST produce a `COURSE_REPORT.md` holding the final graded scorecard (rubric
  scores + verdict) certifying the course to the author.
- **FR-022**: When a `BUILD_PROGRESS.md` is missing, corrupt, or internally inconsistent, the
  pipeline MUST refuse to guess and MUST surface the problem to the author rather than silently
  redoing or skipping work.

**Backward movement**

- **FR-023**: Gated phases are **immutable once passed**. When the author requests a change that
  belongs to an already-gated earlier phase, the pipeline MUST apply it as an **explicit forward
  diff at the current phase** and MUST NOT re-open or re-flow the completed phase. This generalizes
  the frozen-syllabus diff rule (FR-013) to every gated phase, keeping the pipeline a strict
  forward-only sequence.

- **FR-024**: The post-skeleton user scan (FR-011) is a **blocking gate**. After agent review of the
  skeleton batch passes, the pipeline MUST pause and wait for the author's explicit approval (or
  change request) before starting the lesson phase. It is a single batch-level pause, consistent
  with the no-per-item-interruption rule (FR-014).

### Key Entities

- **COURSE_SPEC.md** — the author-written input describing the desired course (topic, scope,
  audience, depth, required running example, optional modules, source material). Its quality caps
  the course's quality.
- **Clarified spec** — the intake-resolved version of the spec after the upfront interview, with
  knowable ambiguities settled and missing required fields obtained (never fabricated).
- **course-template** — the frozen, versioned, tiered skeleton (mandatory core + optional modules)
  that instantiation copies; a foundational asset, not authored by this feature.
- **COURSE_BRIEF.md** — the factory-generated overlay derived from the clarified spec; the thin
  per-course delta the frozen template reads.
- **Module selection** — the explicit set of optional modules enabled/disabled for this course.
- **Course folder** — the staging instance of a course (one per course), holding all per-course
  artifacts and the `.claude/` residue.
- **BUILD_PROGRESS.md** — the pipeline's on-disk state: current phase + per-lesson status; the sole
  source of truth for resuming.
- **Phase** — one step in the fixed sequence, each with a designated reviewer and a gate condition.
- **Gate** — a phase's pass condition (user-approval / agent-pass-then-user-scan / rubric-pass) that
  must clear before advancement.
- **Template version stamp** — the record of which frozen template version a course was copied from,
  enabling later manual re-sync.
- **SOURCES.md** — the anti-fabrication grounding store (created and referenced here; populated by
  spec 002).
- **COURSE_REPORT.md** — the final graded scorecard delivered to the author.
- **FEEDBACK.md** — the per-course critique file (created empty; harvested into the factory's
  insights by spec 004).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Intake fabricates a missing required field **0** times — every missing required field
  surfaces as a blocking question **100%** of the time.
- **SC-002**: **100%** of instantiated courses have a `COURSE_BRIEF.md` capturing all required
  elements (topic & scope, audience + prior knowledge, running example, source-material pointers)
  and an explicit module selection.
- **SC-003**: The source `course-template/` is modified **0** times across any number of builds
  (verifiable by comparison against a known-good copy).
- **SC-004**: A build interrupted at any phase and resumed in a fresh session continues from the
  exact recorded phase and lesson set, with **0** completed units of work repeated.
- **SC-005**: A fresh session can determine the correct resume point using **only** the course
  folder's on-disk artifacts, with no reliance on prior-session memory.
- **SC-006**: Across all runs, the pipeline advances past a gate **0** times without a recorded gate
  pass for that phase (no silent skips).
- **SC-007**: For each phase, the reviewer that blocks advancement is the matched one (user for
  syllabus; agent-then-user for skeletons; rubric for lessons) in **100%** of runs.
- **SC-008**: **100%** of delivered course folders contain all required per-course artifacts
  (`COURSE_BRIEF.md`, `SOURCES.md`, `BUILD_PROGRESS.md`, `FEEDBACK.md`, `COURSE_REPORT.md`,
  `.claude/`) and a `COURSE_REPORT.md` with a graded scorecard and verdict.
- **SC-009**: When state is missing or inconsistent — or the frozen template is absent/unversioned —
  the pipeline halts and reports **100%** of the time rather than proceeding on a guess.
- **SC-010**: The pipeline re-opens a passed, gated phase **0** times; every change to an earlier
  phase is applied as a forward diff at the current phase (verifiable from the phase-transition log).
- **SC-011**: After the skeleton batch passes agent review, the pipeline advances to the lesson
  phase **only** after a recorded explicit author approval — **0** auto-advances without it.

## Assumptions

- **Post-intake phase work is black-boxed here.** The internal work of the syllabus, lesson, and
  grading phases is owned by specs 002–004; this spec governs instantiation, movement between
  phases, and state.
- **The frozen `course-template/` exists as a foundational asset.** Its distillation from
  `System_Design_SelfLearn` (roadmap task #1) precedes this feature; this spec defines only the
  copy / overlay / version contract over it.
- **Course folders live in a staging area** (one subfolder per course) and are moved out of the repo
  by the author manually after delivery; "delivery" here means the pipeline reaching its terminal
  state with all artifacts present, not the physical move.
- **Course folder naming** is derived from the spec (e.g., a slug of the course title); collisions
  are resolved by the pipeline (e.g., suffixing) rather than overwriting an existing course.
- **The lesson-file-format decision (`.md` vs `.ipynb`)** is made during the syllabus phase (spec
  002) and written back into `COURSE_BRIEF.md`; intake here does not fix it.
- **Per-lesson status** is drawn from a small fixed set sufficient to drive resume (at minimum:
  not-started, in-progress, passed/accepted); the exact vocabulary is an implementation detail as
  long as it distinguishes "done" from "still to do."
- **The round cap (3), the two ask-moments, and the reviewer-per-phase mapping** are taken as fixed
  from the design and treated as hard constraints here; they are calibratable later but not part of
  this feature's variability.
- **One build advances a given course at a time**; the state file is authoritative for whose turn it
  is, avoiding concurrent-advance conflicts.
