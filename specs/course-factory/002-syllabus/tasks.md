---
description: "Task list for Syllabus Phase — Research & Mentor-Led Composition (spec 002)"
---

# Tasks: Syllabus Phase — Research & Mentor-Led Composition

**Input**: Design documents from `specs/course-factory/002-syllabus/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ (all present)

**Tests**: INCLUDED. The plan names deterministic `pytest` modules and the spec's Success Criteria are
hard-zero measurable (SC-001/002/003/005/008); the whole point of the thin tool layer (research R1) is
that those guarantees are asserted by tests, not agent discipline. Test tasks are written FIRST within
each story and must FAIL before implementation. Irreducible-judgment SCs (SC-006 platform-degrade,
SC-007 brief-consistency) are validated as `quickstart.md` scenario walkthroughs, not pytest (R2).

**Organization**: By user story (US1 P1 → US2 P2 → US3 P3). The deliverable **adds to** the factory's
own build `.claude/` (spec 001's) — one `syllabus-phase` handler skill (grown across the three stories),
the re-homed `mentor-research` skill, a `syllabus-composer` agent — plus three stdlib tools in
`course-factory/tools/` and their tests. It replaces 001's syllabus **phase-stub** against
`contracts/phase-seam.md` **without touching the orchestrator**. All paths are repo-relative from
`agent-lab/`.

**Cross-spec dependency**: 002 is built **after** 001 (README build order 000 → 001 → 002). The handler
writes `syllabus_subphase` via 001's `course-factory/tools/progress.py` and replaces 001's
`phase-stubs` syllabus path; the three 002 tools + fixtures are standalone stdlib and are testable now
regardless. Live end-to-end integration (orchestrator invoking the real handler) is exercised once 001
is implemented; until then the handler is authored against the seam contract and validated at the seam
boundary + fixtures (mirrors 001 validating against a template fixture without 000).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1 / US2 / US3 (setup, foundational, polish carry no story label)

## Path Conventions

- Factory engine (spec 001's, 002 adds to it): `course-factory/.claude/{skills,agents}/`
- Deterministic tools: `course-factory/tools/*.py` (Python 3.11, **stdlib only**)
- Tests + fixtures: `course-factory/tests/`
- Generated courses (runtime, gitignored): `course-factory/courses/<name>/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Re-home the shared research skill and confirm the test harness so every later task has a home.

- [ ] T001 Re-home the research discipline: **copy** `/.claude/skills/mentor-research/SKILL.md` (repo
  root) → `course-factory/.claude/skills/mentor-research/SKILL.md`, per the skill's own re-home note
  ("copy into `course-factory/.claude/skills/` once spec 001 scaffolds the factory environment", R5).
  Do **not** re-author it — one research discipline, two homes (repo-dev vs. course-build). Confirm the
  factory `.claude/skills/` and `.claude/agents/` dirs exist (001's Setup); create them if running ahead
  of 001, kept **separate** from any `course-template/.claude/` (Structural Constraints).
- [ ] T002 [P] Confirm `pytest` discovery covers `course-factory/tests/` for the 002 modules (reuse
  001's `conftest.py`; **no new dependencies** — stdlib + pytest only, repo convention).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The fixtures every story's tests and scenarios depend on (research R6).

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T003 [P] Create `SOURCES.md` + query-log fixtures in `course-factory/tests/fixtures/`:
  `sources/{well-formed,missing-key,reliability-absent,duplicate-work}.md`
  (contracts/sources-schema.md) and `query-log/{under-budget,at-budget,over-budget}`
  (the persistent research counter, data-model "Research budget").
- [ ] T004 [P] Create syllabus + brief fixtures in `course-factory/tests/fixtures/`:
  `syllabi/{fully-traced,ungrounded-topic,dangling-citation,thin-grounding,missing-divergence-assessment}.md`
  (contracts/syllabus-schema.md; `dangling-citation` cites an `[Sn]` absent from the paired
  `SOURCES.md`) and `brief-min/` — a minimal `COURSE_BRIEF.md` in two variants (`lesson_format`
  unset / set) with a **default-profile** stand-in (the spec-000 profile stand-in, FR-015, R6).

**Checkpoint**: Fixtures exist for both linters, the budget counter, and every scenario. Stories can begin.

---

## Phase 3: User Story 1 — Ground the topic in a weighed, cited SOURCES.md (Priority: P1) 🎯 MVP

**Goal**: Research the topic across web → GitHub → course-platforms (platform last, degradable), weigh
each source for reliability over popularity, record kept sources in `SOURCES.md` under stable `[Sn]`
keys with a reliability judgment, and **stop at convergence or the budget cap** — never unbounded.

**Independent Test**: Run research on a well-covered topic → `SOURCES.md` with stable `[Sn]` keys, each
entry carrying a reliability judgment (not a star count); research stops at convergence or the cap; no
login/scraper used for platforms (quickstart B1). `sources_lint.py` passes on the result.

### Tests for User Story 1 ⚠️ (write first, must FAIL)

- [ ] T005 [P] [US1] `course-factory/tests/test_research_budget.py`: over the `query-log/*` fixtures,
  `exhausted()` is False under budget and True at/over the cap (SC-002, 0 unbounded); a **re-research**
  call after a divergence answer continues the **same** count and **cannot** exceed the original cap —
  no reset path exists (FR-019, R4).
- [ ] T006 [P] [US1] `course-factory/tests/test_sources_lint.py`: `well-formed` passes;
  `missing-key` and `reliability-absent` **fail** (every entry needs a stable `[Sn]` + a non-empty
  reliability judgment — a bare star count fails, SC-001); `duplicate-work` **warns** (two links, one
  work → one key; mentor-research dedupe-by-work).

### Implementation for User Story 1

- [ ] T007 [P] [US1] Implement `course-factory/tools/research_budget.py`: a persistent query/tool-call
  counter in the course folder (e.g. `.syllabus-research-log`), exposing `increment()`, `remaining()`,
  `exhausted()` as pure functions of the log — and **no `reset()`** (the structural enforcement of
  FR-019's one-budget rule, R4). Document the honesty boundary (counts only logged queries) in the code.
- [ ] T008 [P] [US1] Implement `course-factory/tools/sources_lint.py` per contracts/sources-schema.md:
  reject any entry lacking a stable/unique `[Sn]` key or a non-empty reliability judgment; flag a reused
  key (append-stable, FR-004) and an obvious duplicate-work (SC-001).
- [ ] T009 [US1] Author the **research portion** of `course-factory/.claude/skills/syllabus-phase/SKILL.md`:
  read the seam input envelope (contracts/syllabus-handler.md); invoke re-homed `mentor-research`;
  search **web → GitHub → platform last**, degrading gracefully if platform syllabi need a login and
  **recording the limitation** (never scrape/login/pay — FR-001, SC-006); route every query through
  `research_budget.increment()`; stop on **convergence or `exhausted()`** (FR-005, SC-002); write kept
  sources to `SOURCES.md` (`[Sn]` + reliability, SC-001) and run `sources_lint.py`; persist
  `syllabus_subphase` `research-in-progress` → `research-done` via 001's `progress.py` (FR-018).
- [ ] T010 [US1] Validate US1 end-to-end per `quickstart.md` § B1 (web→GitHub→platform-last;
  platform-degrade recorded, no scraper/login/paid — SC-006; stop at convergence-or-cap — SC-002;
  keyed + reliability-judged entries — SC-001) and § B5 (resume at `research-done` skips research, FR-018).

**Checkpoint**: A topic becomes a weighed, `[Sn]`-keyed `SOURCES.md` that stops at convergence or the
budget — the anti-fabrication foundation, demonstrable before a single syllabus line exists (spec US1
"Why this priority").

---

## Phase 4: User Story 2 — Compose a mentor-led syllabus from the sources (Priority: P2)

**Goal**: Compose the syllabus **as a domain mentor** — sources inform but do not dictate; fill gaps,
correct stale/irrelevant material; every topic traces to `[Sn]` or is marked mentor-added; decide the
course **volume** and the `.md`/`.ipynb` **format**, writing the format back into `COURSE_BRIEF.md`.

**Independent Test**: Given a `SOURCES.md` with a deliberately stale + an off-topic source, compose a
syllabus that corrects them, every topic `[Sn]`-traced or mentor-added, a volume set, and the format
recorded in `COURSE_BRIEF.md` (quickstart B2). `syllabus_lint.py` passes.

**Depends on**: US1 (a populated `SOURCES.md`) + Foundational (fixtures).

### Tests for User Story 2 ⚠️ (write first, must FAIL)

- [ ] T011 [P] [US2] `course-factory/tests/test_syllabus_lint.py` (over `syllabi/*` + `brief-min/*` +
  `sources/well-formed`): `fully-traced` passes; `ungrounded-topic` **fails** (SC-003);
  `dangling-citation` **fails** — a `[Sn]` absent from `SOURCES.md` is not a landing trace, a
  cross-file resolution check (SC-003); `thin-grounding` fails unless **every** flagged topic is
  mentor-added (SC-008); `missing-divergence-assessment` **fails** (SC-005); a brief with
  `lesson_format` unset **fails** (SC-004). Assert the failure **reason**, not just the exit code.

### Implementation for User Story 2

- [ ] T012 [P] [US2] Implement `course-factory/tools/syllabus_lint.py` per contracts/syllabus-schema.md:
  every topic has a `[Sn]` **that resolves into the course's `SOURCES.md`** (cross-file) or a
  `mentor-added` tag (SC-003); thin-grounding scope ⇒ all its topics mentor-added (SC-008); a divergence
  assessment naming the compared sources is present (SC-005); `COURSE_BRIEF.md.lesson_format ∈ {.md,.ipynb}`
  (SC-004).
- [ ] T013 [P] [US2] Author `course-factory/.claude/agents/syllabus-composer.md`: the fresh-context
  **domain-mentor** persona — inputs (brief, `SOURCES.md`, `insights/` digest, selected profile);
  compose honoring the profile's macro spine / entry point / **advisory** checkpoints while reusing the
  mandatory-core invariants (never redefining them — FR-006/010/015); correct stale/industry-irrelevant
  sources; keep the brief's **running example** threaded (FR-010, SC-007).
- [ ] T014 [US2] Author the **compose portion** of `syllabus-phase/SKILL.md`: read `insights/` (empty
  valid, FR-016) + `prior_artifacts` as **frozen + DIFFS** (FR-017, vacuous at first compose — R7);
  invoke `syllabus-composer`; decide **volume** (FR-008) and **format**, writing `lesson_format` back
  to `COURSE_BRIEF.md` (FR-009, the only brief field 002 writes); write `SYLLABUS.md` with every topic
  `[Sn]`/mentor-added and the composition notes (grounding-stop note converged|budget-capped, thin-grounding
  flag if applicable — FR-011/SC-008); run `syllabus_lint.py`; persist `syllabus_subphase` `composed`.
- [ ] T015 [US2] Validate US2 end-to-end per `quickstart.md` § B2 (stale/off-topic corrected, topics
  traced-or-tagged, volume set, format recorded, running-example consistent — SC-003/004/007) and § B4
  (thin-grounding: compose + flag + tag, never block/fabricate — FR-011, SC-008).

**Checkpoint**: A `SOURCES.md` becomes a mentor-composed `SYLLABUS.md` — grounded-or-tagged topics, a
set volume, and a recorded format — demonstrable given any source set.

---

## Phase 5: User Story 3 — Surface divergence and present a review-ready syllabus (Priority: P3)

**Goal**: On wide source divergence, ask the user a directional question (ask-moment #2, **inline**);
otherwise ask nothing — and record an explicit divergence assessment either way; then present a
review-ready syllabus and revise it on feedback, so 001's approval gate has a clean artifact.

**Independent Test**: Conflicting sources → the handler asks a directional question rather than silently
picking, and writes a `diverged` assessment; agreeing sources → no question, a `converged` assessment
still written; given feedback on the draft → the syllabus is revised and re-presented (quickstart B3).

**Depends on**: US2 (a composed syllabus) + Foundational.

### Implementation for User Story 3

- [ ] T016 [US3] Author the **divergence portion** of `syllabus-phase/SKILL.md`: at
  `syllabus_subphase == composed`, judge divergence on the **top-weighted** sources; **inline-ask** the
  directional question **only** on real divergence (not on minor ordering — FR-012), never routing it
  through 001's `needs-user` park (an ask-moment, not a gate — R3); write the divergence assessment on
  **every** run naming the compared sources (SC-005) and record a **pending** question until answered;
  after the answer, **MAY** re-research against the **same** budget (FR-019) and re-compose, staying at
  `composed` (R4).
- [ ] T017 [US3] Author the **present + revise portion** of `syllabus-phase/SKILL.md`: run
  `sources_lint.py` + `syllabus_lint.py`, persist `syllabus_subphase` `presented`, and return
  **`needs-user`** for 001's user-approval gate — the **only** seam park 002 triggers. On a change-request
  re-invocation, read the user's revision comments from **`FEEDBACK.md`** in `course_dir` (001's
  gate-event write side, 001 FR-026 / data-model rule 9 — 002 only reads it), re-enter at `composed`,
  revise, re-present, return `needs-user` again. **Never** return `pass`/`loop`; never freeze, re-open,
  or edit a frozen syllabus — 001 owns the loop + freeze (FR-013/014); keep `SYLLABUS.md` diff-friendly
  for 001's forward-diff presentation.
- [ ] T018 [US3] Validate US3 end-to-end per `quickstart.md` § B3 (diverged → inline ask + `diverged`
  assessment; agreeing → no ask + `converged` assessment, SC-005; feedback → revise + re-present without
  re-implementing 001's loop/freeze, FR-014).

**Checkpoint**: Divergence is surfaced (or correctly not), the assessment is always recorded, and a
review-ready syllabus is presented + revised at the seam — the user-facing surface of the phase.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T019 [P] **Update** `course-factory/tools/README.md` (001's existing file — do **not** create a
  second): append the three 002 tools (`research_budget.py`, `sources_lint.py`, `syllabus_lint.py`),
  what each guarantees, and the budget counter's **honesty boundary** (it counts only logged queries — R4).
- [ ] T020 [P] Update `specs/course-factory/README.md` status for 002 from "Clarified" → "Planned →
  Tasked" (the index is the cold-session entry point).
- [ ] T021 Run the full `pytest` suite over `course-factory/tests/` (002 modules green) and walk
  `quickstart.md` Part A (mechanical SCs) + Part B (scenario SCs B1–B5) end-to-end.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (P1)** → **Foundational (P2)** → **US1 (P3)** → **US2 (P4)** → **US3 (P5)** → **Polish (P6)**.
- Like 001, these stories are **layered** (the spec's own priority order): US2's compose needs US1's
  `SOURCES.md`; US3's divergence/present needs US2's composed syllabus. Each remains independently
  **testable** given its stated precondition (US2 "given a `SOURCES.md`"; US3 "given a draft syllabus +
  conflicting sources"), but they are implemented in order.

### Within each user story

- Test tasks first (they must FAIL), then implementation, then the end-to-end quickstart validation.
- The **`syllabus-phase/SKILL.md` handler grows across stories** — research portion (T009) → compose
  portion (T014) → divergence portion (T016) → present+revise portion (T017); these edit the same file
  and are therefore **sequential**, not `[P]` (mirrors 001's `progress.py` growing across phases).

### Parallel opportunities

- **Setup**: T002 ∥ (after T001).
- **Foundational**: T003 ∥ T004 (different fixture dirs).
- **US1**: T005 ∥ T006 (tests); T007 ∥ T008 (budget vs sources_lint, different files) — both before T009.
- **US2**: T011 (test) before T012; T012 ∥ T013 (lint tool vs composer agent, different files) — both
  before T014.
- **Polish**: T019 ∥ T020.

---

## Parallel Example: User Story 1

```bash
# Tests first (both fail), in parallel — different files:
Task: "test_research_budget.py — stop-at-cap + FR-019 same-budget (SC-002)"
Task: "test_sources_lint.py — [Sn] key + reliability judgment (SC-001)"

# Then the two independent tools in parallel — different files:
Task: "Implement course-factory/tools/research_budget.py (no reset path)"
Task: "Implement course-factory/tools/sources_lint.py"
```

---

## Implementation Strategy

### MVP first (User Story 1 only)

1. Phase 1 Setup → Phase 2 Foundational → Phase 3 US1.
2. **STOP and VALIDATE**: run `test_research_budget.py` + `test_sources_lint.py` + quickstart § B1. A
   topic → a weighed, `[Sn]`-keyed `SOURCES.md` that halts at convergence-or-cap, no scraper/login. This
   is a demonstrable, independently-valuable deliverable before any syllabus line (spec US1 rationale).

### Incremental delivery

1. Setup + Foundational → fixtures + shared research skill ready.
2. US1 → the grounded `SOURCES.md` (demo).
3. US2 → the mentor-composed `SYLLABUS.md` + format decision (demo).
4. US3 → divergence ask + review-ready present/revise at the seam (demo).
5. Each story adds value without breaking the previous.

### The seam to 001 (and downstream to 003/004)

002 **replaces 001's syllabus phase-stub** against the **same** `contracts/phase-seam.md` envelope +
gate result, touching neither the orchestrator nor `progress.py`. 002's frozen `SYLLABUS.md` + its
`DIFFS.md` becomes the canonical paired read for 003 (003 FR-007); its populated `SOURCES.md` is the
`[Sn]` cite target for every 003 lesson and the 004 traceability check. Building 002 against the seam is
what lets it drop into 001 without a spine change (README decomposition premise).

---

## Notes

- `[P]` = different files, no dependency on an incomplete task.
- Every SC has a home: **SC-001** → T006/T008; **SC-002** → T005/T007; **SC-003** → T011/T012;
  **SC-004** → T011/T012/T014; **SC-005** → T011/T012/T016; **SC-006** → T009/T010 (scenario);
  **SC-007** → T013/T015 (scenario); **SC-008** → T011/T012/T014.
- Verify tests fail before implementing; commit after each task or logical group.
- Stdlib only, pytest only — no new dependencies (repo convention).
