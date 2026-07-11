# Feature Specification: Syllabus Phase — Research & Mentor-Led Composition

**Feature Branch**: `002-syllabus`

**Created**: 2026-07-07

**Status**: Draft

**Input**: User description: "Build the syllabus phase of the course factory — the depth behind the syllabus gate that spec 001 orchestrates. Given an instantiated course (a COURSE_BRIEF.md overlay plus selected modules), run a shallow, budget-capped research step that searches the web, GitHub (via the gh CLI), and course platforms (Udemy/Coursera/edX via shallow name-search) for existing courses and publicly-visible syllabi, critically weighs each source for reliability over popularity (high stars are a green flag, not proof), and records what is kept in SOURCES.md under stable [Sn] citation keys as the anti-fabrication grounding for the whole course; stop when sources converge (new ones stop adding topics) with a hard budget/cost cap as backstop. Then compose the syllabus as a domain mentor — sources inform but never dictate, filling gaps and correcting stale or industry-irrelevant sources — deciding the course volume and the lesson file format (.md by default, .ipynb when code-heavy) and writing that format decision back into COURSE_BRIEF.md. If sources diverge widely on the topic's angle, ask the user directional questions (the second of the two designated ask-moments). Present the syllabus for user review and loop until the user is pleased; once approved it is frozen (later changes surface as an explicit diff). Scope this to producing an approved, frozen syllabus plus a populated SOURCES.md — NOT the pipeline orchestration/state machine (spec 001), NOT lesson skeletons or lesson authoring (spec 003), and NOT the grading rubric or course-evaluator (spec 004)."

## Overview

This is **spec #2 of four subject-specs**. It fills the **depth behind the syllabus gate** that
spec 001 orchestrates: the expensive research that grounds the course, and the mentor-led
composition of the syllabus itself. Its two deliverables are a **populated `SOURCES.md`** (the
anti-fabrication grounding for *every* later lesson, not just the syllabus) and a **review-ready,
ultimately-approved syllabus**.

It runs *inside* 001's syllabus phase: 001 owns the state machine, the approval-gate loop control,
and the freeze-on-approval rule; 002 owns the *content* — what the research finds, how the syllabus
is composed, the course volume and lesson-format decision, and the trigger + content of the
post-research divergence question.

### Out of Scope (owned by other specs)

- **Pipeline orchestration / state machine, the approval-gate loop control, and the
  freeze-on-approval mechanics** — spec **001**. 002 produces the reviewable syllabus artifact and
  revises it on feedback; 001 controls the loop and enforces the freeze.
- **The intake interview and initial `COURSE_BRIEF.md` authoring** — spec **001**. 002 *reads* the
  brief and *augments* it with the lesson-format decision only.
- **Lesson skeletons and lesson authoring** — spec **003**. 002 stops at an approved syllabus; it
  does not draft per-lesson plans or content.
- **The grading rubric and course-evaluator** — spec **004**. The syllabus is user-approved, not
  rubric-graded.
- **Heavy platform tooling** — no scrapers, pullers, logins, or paid APIs for course platforms;
  research stays light (web search + `gh` CLI + shallow public name-search).
- **Per-artifact / multi-format lesson rendering (HTML, slides)** — a deferred extension to the
  `.md`/`.ipynb` format decision above; depends on a future `course-template/` renderer module.
- **A per-phase quality checklist as a gate artifact** for the syllabus gate, mirroring spec-kit's
  `checklists/requirements.md` — a deferred, non-mandatory addition.

  Both tracked in `course-factory/DESIGN.md` § Deferred extensions, not this spec's initial scope.

## Clarifications

### Session 2026-07-07

- Q: What unit expresses the hard backstop cap that stops research when sources haven't converged? →
  A: **A search/tool-call budget** — a maximum number of research queries across web + `gh` +
  platform searches; deterministic and testable. The value is calibratable; the unit is a query count.
- Q: When research yields too few reliable sources to ground the syllabus safely, what should the
  phase do? → A: **Compose from mentor judgment and flag the thin grounding** — mark the course/
  sections as thinly-grounded and tag every affected topic as mentor-added (never fabricate sourced
  claims). It does not block or demand a minimum source count.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ground the topic in a weighed, cited SOURCES.md (Priority: P1)

Given an instantiated course, the factory researches the topic across the web, GitHub, and course
platforms, critically weighs each candidate source for reliability (not popularity alone), and
records what it keeps in `SOURCES.md` under stable `[Sn]` citation keys. It stops when sources
converge, with a hard budget cap as a backstop.

**Why this priority**: `SOURCES.md` is the anti-fabrication foundation for the whole course — every
later lesson cites into it. It is the highest-value, independently-testable slice: valuable even
before a single syllabus line is written.

**Independent Test**: Run research on a brief for a well-covered topic; confirm `SOURCES.md` is
produced with stable `[Sn]` keys, each entry carries a reliability judgment (not just a star count),
research stops at convergence or the cap rather than running unbounded, and no login/scraper was
used for the platforms.

**Acceptance Scenarios**:

1. **Given** an instantiated course, **When** research runs, **Then** it searches the web, GitHub,
   and course platforms (shallow public name-search) for existing courses and syllabi.
2. **Given** candidate sources, **When** the factory evaluates them, **Then** each is weighed for
   reliability with popularity treated as a signal (not proof), and only kept sources are recorded.
3. **Given** kept sources, **When** they are recorded, **Then** each gets a stable `[Sn]` key in
   `SOURCES.md` (links for heavy sources; inline citations for posts/comments/tips).
4. **Given** research is underway, **When** new sources stop adding topics **or** the budget cap is
   reached, **Then** research stops instead of continuing unbounded.

---

### User Story 2 - Compose a mentor-led syllabus from the sources (Priority: P2)

The factory composes the syllabus as a **domain mentor**: sources inform but never dictate. It fills
gaps, corrects stale or industry-irrelevant sources with current judgment, decides the course volume
(approximate phases / lesson count), and decides the lesson file format (`.md` by default, `.ipynb`
when the course is code-heavy) — writing that format decision back into `COURSE_BRIEF.md`.

**Why this priority**: This turns grounding into an actual course shape. It depends on US1's
`SOURCES.md` and is independently testable given a set of sources.

**Independent Test**: Given a `SOURCES.md` (including a deliberately stale and an off-topic source),
compose a syllabus; confirm the syllabus reflects current-industry judgment (stale/irrelevant
material not blindly carried), each topic either cites `[Sn]` or is marked as mentor-added, a course
volume is set, and the `.md`/`.ipynb` decision is recorded in `COURSE_BRIEF.md`.

**Acceptance Scenarios**:

1. **Given** a `SOURCES.md`, **When** the syllabus is composed, **Then** sources inform the content
   but do not dictate it — gaps are filled and stale/irrelevant material is corrected.
2. **Given** a composed syllabus, **When** its topics are inspected, **Then** each topic either
   traces to a `[Sn]` source or is explicitly marked as mentor-added judgment (no silently
   ungrounded topics).
3. **Given** the course's nature, **When** the syllabus takes shape, **Then** a course volume and a
   lesson file format are decided, and the format decision is written into `COURSE_BRIEF.md`.

---

### User Story 3 - Surface divergence and present a review-ready syllabus (Priority: P3)

If sources diverge widely on the course's angle, the factory asks the user directional questions
(the second designated ask-moment) before finalizing. It then presents a review-ready syllabus and
revises it on the user's feedback, so 001's approval gate has a clean artifact to act on.

**Why this priority**: This is the user-facing surface of the phase — the divergence question and
the review-ready artifact. It depends on US2 and is separable: given a draft syllabus and a set of
conflicting sources, the divergence-ask and revision behavior are testable on their own.

**Independent Test**: Compose from sources that conflict on the course's core arc; confirm the
factory asks a directional question rather than silently picking; then, given user feedback on the
draft, confirm the syllabus is revised and re-presented. With non-conflicting sources, confirm no
divergence question is asked.

**Acceptance Scenarios**:

1. **Given** sources that diverge widely on the topic's angle, **When** composition finishes,
   **Then** the factory asks the user directional questions before finalizing the syllabus.
2. **Given** sources that agree, **When** composition finishes, **Then** no divergence question is
   asked (the ask-moment fires only on real divergence).
3. **Given** user feedback on the presented syllabus, **When** the factory responds, **Then** it
   revises the syllabus and re-presents it for 001's approval gate.

---

### Edge Cases

- **Sparse or no reliable sources** for an obscure topic — the factory does not fabricate coverage;
  it composes from mentor judgment with the thin grounding made explicit (see FR-011).
- **All sources are stale or industry-irrelevant** — the factory corrects rather than carrying them
  forward, and marks the corrected/added topics as mentor judgment.
- **Course platforms require login or block public syllabus viewing** — the factory falls back to
  web + GitHub grounding and records the platform limitation, rather than scraping or paying.
- **Search/tool-call budget reached before convergence** — research stops at the budget and the
  syllabus notes that grounding was capped, not converged.
- **A citation `[Sn]` becomes unresolvable** (dead link, removed post) — if discovered during this
  phase's own research/composition, the entry is flagged in `SOURCES.md` immediately; 002 does not
  run ongoing liveness re-checks after that (avoids repeated fetch cost, per the light-tooling
  assumption). A link that dies later is caught downstream by 004's traceability check (004
  FR-007) at grading time — entries outlive links, and a dead link is never silently invisible.
- **The topic cannot support the brief's requested depth (or vastly exceeds it)** — the phase
  corrects the volume decision (FR-008) toward what the topic can actually sustain, using mentor
  judgment (FR-006), and flags the deviation from the brief's stated depth rather than silently
  padding or truncating content.
- **User keeps requesting syllabus changes without converging** — handled by 001's approval-loop
  control; 002 keeps revising the content each cycle.

## Requirements *(mandatory)*

### Functional Requirements

**Research & sourcing**

- **FR-001**: The syllabus phase MUST research the topic across the web, GitHub (via the `gh` CLI),
  and course platforms (Udemy/Coursera/edX) using a **shallow name-search of publicly-visible
  syllabi** — no logins, scrapers, or pullers. **Course-platform search runs last** in the research
  sequence (after web + GitHub) and is **explicitly degradable**: if platform syllabi are inaccessible
  without login, the phase completes on web + GitHub grounding alone (see Edge Cases), never blocking
  on platform access — platform search is the most fragile, lowest-yield leg and is sequenced
  accordingly.
- **FR-002**: The phase MUST critically weigh each candidate source for **reliability**, treating
  popularity/stars as a green-flag signal, not proof of correctness; only kept sources are recorded.
- **FR-003**: Kept sources MUST be recorded in `SOURCES.md` under **stable `[Sn]` keys** — links for
  heavy sources, inline citations for posts / comments / tips — with each entry carrying its
  reliability judgment.
- **FR-004**: `SOURCES.md` MUST be the anti-fabrication grounding for the **whole course**; its
  `[Sn]` keys MUST be stable so later lessons (spec 003) can cite into them.
- **FR-005**: Research MUST stop when sources **converge** (new sources stop adding topics) **or** a
  hard **search/tool-call budget** is reached — a maximum number of research queries across web,
  `gh`, and platform searches — whichever comes first, never running unbounded. The budget value is
  calibratable after real runs; the *unit* is a query / tool-call count.

**Mentor-led composition**

- **FR-006**: The syllabus MUST be composed **as a domain mentor** — sources inform but MUST NOT
  dictate; the phase MUST fill gaps and correct stale or industry-irrelevant sources with
  current-industry judgment.
- **FR-007**: Every syllabus topic MUST either trace to a `[Sn]` source **or** be explicitly marked
  as mentor-added judgment; there MUST be no silently ungrounded topics. This is the syllabus-level
  application of the factory's **canonical citation/grounding contract** (004 FR-007/FR-008); 002
  applies it at topic granularity rather than re-deriving an independent rule.
- **FR-008**: The phase MUST decide the course **volume** (approximate phase / lesson count),
  grounded in the brief's stated depth and size.
- **FR-009**: The phase MUST decide the **lesson file format** — `.md` by default, `.ipynb` when the
  course is code-heavy — and MUST write that decision back into `COURSE_BRIEF.md`.
- **FR-010**: The phase MUST read the audience, scope, and required running example from
  `COURSE_BRIEF.md` and keep the syllabus consistent with them.
- **FR-011**: When research yields too little reliable grounding to compose safely, the phase MUST
  **compose from mentor judgment and flag the thin grounding**: it MUST mark the course (or the
  affected sections) as thinly-grounded and tag every affected topic as mentor-added (FR-007), and
  MUST NOT fabricate sourced claims. It MUST NOT block or demand a minimum source count.

**Divergence & review (content side; gate mechanics owned by 001)**

- **FR-012**: When sources **diverge widely** on the course's angle, the phase MUST ask the user
  directional questions (the second designated ask-moment) before finalizing; when sources do not
  diverge, it MUST NOT ask.
- **FR-013**: The phase MUST present a **review-ready syllabus** (course shape + scope) for the
  user-approval gate that spec 001 orchestrates.
- **FR-014**: On user feedback, the phase MUST **revise** the syllabus and re-present it. The
  approval-loop control and the freeze-on-approval rule are owned by spec 001 (its FR-011 / FR-013);
  002 MUST NOT re-implement or contradict them, and MUST keep the syllabus in a form that supports
  001's diff-based change presentation after freezing.

**Profile consumption (000's archetype profiles)**

- **FR-015**: The syllabus MUST be composed **consistent with the course's selected archetype
  profile** (001's overlay decision, per 000 FR-022/023) — honoring that profile's macro organizing
  spine, entry point (theory-first vs problem-first), and checkpoint placement/frequency (advisory
  only, per 000 FR-022) — while still reusing the mandatory core's invariants (000 FR-024); the phase
  MUST NOT redefine or bypass those invariants when applying a profile.

**Cross-phase reads (constitution Principle XII, 001's diff ledger)**

- **FR-016**: Composition MUST read the `insights/` digest (004's harvested output) as an input,
  alongside `SOURCES.md`; an **empty or missing digest is a valid input**, not a blocker (mirrors
  003's precedent). This is the syllabus-side implementation of Principle XII's read rule.
- **FR-017**: Where composition works against an already-gated earlier artifact that carries applied
  forward diffs (001 FR-027), the phase MUST read the **frozen artifact plus its `DIFFS.md` entries**
  together as the canonical input, never the frozen artifact alone.

**Sub-phase resumability**

- **FR-018**: The syllabus phase MUST record its **sub-phase status** — one of `research-in-progress`,
  `research-done`, `composed`, or `presented` — in `BUILD_PROGRESS.md` (001 FR-015) as it completes
  each sub-step, so a session dying mid-phase resumes at the correct sub-step (e.g., skipping
  already-completed research) rather than restarting the whole phase.

**Post-divergence re-research**

- **FR-019**: After the user answers a divergence question (FR-012), the phase MAY resume research to
  fill gaps the answer reveals, chargeable against the **same** search/tool-call budget (FR-005) — it
  MUST NOT open a fresh budget. If the remaining budget is insufficient, the phase composes from the
  directional answer plus existing sources per the thin-grounding policy (FR-011) rather than
  exceeding the cap.

### Key Entities

- **COURSE_BRIEF.md** — the overlay (from 001) that the phase *reads* (audience, scope, running
  example, depth) and *augments* with the lesson-format decision.
- **SOURCES.md** — the anti-fabrication grounding store: `[Sn]`-keyed entries, each with a
  link-or-inline citation and a reliability judgment. The phase's primary durable output.
- **Source** — a single kept research find: its type (course, repo, syllabus, post), its citation,
  its reliability weighting, and the topics it covers (used for convergence).
- **Convergence signal** — the condition that new sources stop adding topics; one of the two
  research-stop triggers.
- **Search/tool-call budget** — the hard backstop (a max query / tool-call count) that stops
  research even without convergence.
- **Syllabus** — the composed course shape and scope (phases, lessons, arc); the phase's headline
  artifact, ultimately user-approved. Its on-disk identity is **`SYLLABUS.md`**, at the course
  folder's root; a required delivery artifact (001 FR-020).
- **Lesson-format decision** — `.md` vs `.ipynb`, decided here and written back to `COURSE_BRIEF.md`.
- **Divergence** — wide disagreement across sources on the course's angle; the trigger for the
  second ask-moment.
- **Selected profile** — the course's chosen archetype profile (001's overlay decision, 000's
  mechanism); shapes this phase's macro spine, entry point, and checkpoint placement (FR-015).
- **Insights digest** — the cross-course knowledge store (004's harvest output); read as a composition
  input (FR-016). May be empty.
- **Syllabus sub-phase status** — the phase's checkpoint state (`research-in-progress` /
  `research-done` / `composed` / `presented`) recorded in `BUILD_PROGRESS.md` (FR-018) so a mid-phase
  interruption resumes at the right sub-step.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **100%** of `SOURCES.md` entries have a stable `[Sn]` key and a recorded reliability
  judgment (not merely a popularity/star figure).
- **SC-002**: Research halts at convergence or the cap in **100%** of runs — **0** unbounded runs.
- **SC-003**: **100%** of syllabus topics are traceable to a `[Sn]` source or explicitly marked as
  mentor-added judgment — **0** silently ungrounded topics.
- **SC-004**: The lesson-format decision (`.md`/`.ipynb`) is recorded in `COURSE_BRIEF.md` in
  **100%** of completed syllabi.
- **SC-005**: The divergence ask-moment fires **only** when sources diverge — **0** divergence
  questions on agreeing-source runs — and **every run records an explicit divergence assessment**
  (converged / diverged, naming the sources compared) in the syllabus's composition notes, making the
  fire/no-fire decision auditable after the fact even though the underlying divergence judgment is
  agent-rendered (see Assumptions).
- **SC-006**: When platform syllabi are inaccessible, the phase completes on web + GitHub grounding
  and records the limitation **100%** of the time — **0** uses of scrapers, logins, or paid pullers.
- **SC-007**: A composed syllabus stays consistent with the brief's audience, scope, and running
  example in **100%** of runs (no drift from the brief).
- **SC-008**: When grounding is thin, the course/section is flagged as thinly-grounded and every
  affected topic is tagged mentor-added — **0** silently thin-grounded courses.

## Assumptions

- **The instantiated course exists** (spec 001 has produced the folder, `COURSE_BRIEF.md`, and the
  `SOURCES.md` stub); 002 populates `SOURCES.md` and augments the brief.
- **Research tooling stays light** — web search + `gh` CLI + shallow public name-search; dedicated
  fetch tools are added only if real runs prove repeated cost (per the design's "prove out shallow
  research" step).
- **Platform syllabi are often publicly viewable without registering** — to be verified on first
  run; if not, the phase falls back gracefully (edge case + SC-006).
- **The divergence threshold is an agent judgment** — the ask-moment fires when the top-weighted
  sources disagree on the course's core arc/angle, not on minor topic-ordering differences.
- **Convergence is judged by topic coverage** — sources stop "adding topics" when new finds repeat
  already-captured topics; the exact heuristic is an implementation detail.
- **The approval loop and freeze belong to 001** — 002 supplies and revises the syllabus content;
  it does not own when the loop ends or how the freeze is enforced.
- **`[Sn]` keys are append-stable** — once assigned, a key is not reused for a different source, so
  later lesson citations remain valid.
- **Research reuses the `mentor-research` skill** (`skills/mentor-research/`, extracted from the
  `pedagogy/` build expressly for this spec's own future research runs) as the shared discipline —
  research → weigh reliability → cite under stable keys → converge-or-budget — rather than inventing
  a second method; FR-001–FR-005 are this discipline applied to per-course syllabus research.
