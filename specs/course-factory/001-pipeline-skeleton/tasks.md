---
description: "Task list for Course-Factory Pipeline & Instantiation (spec 001)"
---

# Tasks: Course-Factory Pipeline & Instantiation

**Input**: Design documents from `specs/course-factory/001-pipeline-skeleton/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ (all present)

**Tests**: INCLUDED. The plan names deterministic `pytest` modules and the spec's Success Criteria
are hard-zero measurable (SC-003/004/006/012 …); the whole point of the deterministic tool layer
(research R1) is that those guarantees are asserted by tests, not agent discipline. Test tasks are
written FIRST within each story and must FAIL before implementation.

**Organization**: By user story (US1 P1 → US2 P2 → US3 P3). The deliverable is the factory's own
build `.claude/` + a thin `course-factory/tools/` layer + `course-factory/tests/`. All paths are
repo-relative from `agent-lab/`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1 / US2 / US3 (setup, foundational, polish carry no story label)

## Path Conventions

- Factory engine: `course-factory/.claude/{commands,agents,skills}/`
- Deterministic tools: `course-factory/tools/*.py` (Python 3.11, **stdlib only**)
- Tests + fixtures: `course-factory/tests/`
- Generated courses (runtime, gitignored): `course-factory/courses/<name>/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Directory skeleton + test harness so every later task has a home.

- [X] T001 Create the factory engine skeleton: `course-factory/.claude/commands/`,
  `course-factory/.claude/agents/`, `course-factory/.claude/skills/`, `course-factory/tools/`,
  `course-factory/tests/fixtures/` — per plan.md Project Structure. Confirm it is **separate** from
  any `course-template/.claude/` (Structural Constraints). Note: `course-factory/insights/` already
  exists (empty, start-empty per Principle XII) so intake's FR-025 read path is concrete; 001 only
  reads it, 004 writes it.
- [X] T002 [P] Configure `pytest` discovery for `course-factory/tests/` (a minimal `conftest.py`;
  **no new dependencies** — stdlib + pytest only, per repo convention).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The shared state core + test fixtures every user story depends on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 Build the minimal frozen-template fixture in `course-factory/tests/fixtures/template-min/`
  (a `VERSION` semver, a `manifest`, a `default` profile, and 2–3 topic-neutral `.claude/` files) —
  the spec-000 stand-in that unblocks US1 without the real template (research R6,
  contracts/course-folder.md).
- [X] T004 [P] Create sample spec fixtures in `course-factory/tests/fixtures/specs/`:
  `well-formed.md`, `missing-running-example.md`, `malformed.md` (quickstart Prerequisites).
- [X] T005 Implement the state core in `course-factory/tools/progress.py`: parse + serialize the
  single fenced ` ```json ` block in `BUILD_PROGRESS.md` and validate its shape against
  contracts/build-progress-schema.md (**no** transition logic yet — that is US2). This is the shared
  read/write foundation US1 (init) and US2/US3 (transitions) both call.

**Checkpoint**: State can be read/written deterministically; fixtures exist. User stories can begin.

---

## Phase 3: User Story 1 — Intake into an instantiated, resumable course build (Priority: P1) 🎯 MVP

**Goal**: Turn a rough `COURSE_SPEC.md` into `courses/<name>/` with a complete `COURSE_BRIEF.md`
overlay (profile + modules), a stamped template version, an initialized `BUILD_PROGRESS.md`, and the
`SOURCES.md`/`FEEDBACK.md`/`DIFFS.md` stubs — without mutating the source template and without
fabricating a missing required field.

**Independent Test**: Run intake + instantiation on `well-formed.md` → a correct course folder;
on `missing-running-example.md` → a blocking question, no fabrication; on `malformed.md` → halt, no
partial folder; against an unversioned template → halt. Source template byte-for-byte unchanged.

### Tests for User Story 1 ⚠️ (write first, must FAIL)

- [X] T006 [P] [US1] `course-factory/tests/test_instantiate.py`: brief-completeness backstop (a
  brief missing a required field → `instantiate.py` **halts**, SC-001/002); overlay applied for the
  selected profile + enabled modules present + `template_version` stamped + three stubs created
  (SC-002); source `template-min/` **byte-for-byte unchanged** via checksum diff (SC-003).
- [X] T007 [P] [US1] Add to `test_instantiate.py`: absent-or-unversioned template → **halt**, write
  **no** partial folder (FR-001, SC-009); course-name collision → suffixed, never overwritten (spec
  Assumptions).

### Implementation for User Story 1

- [X] T008 [US1] Implement `course-factory/tools/instantiate.py`: (1) validate brief completeness and
  halt on any missing required field (running example, profile, modules, topic/scope, audience,
  source pointers) — the mechanical anti-fabrication backstop (FR-003, SC-001/002); (2) resolve
  course name/slug + collision suffix; (3) **copy-never-mutate** `course-template/` → `courses/<name>/`
  overlaying the selected profile + enabled modules; (4) stamp `template_version`; (5) init
  `BUILD_PROGRESS.md` at syllabus-start via `progress.py`; (6) create `SOURCES.md`, `FEEDBACK.md`,
  `DIFFS.md` stubs (FR-006/007/008).
- [X] T009 [US1] Add the absent/unversioned-template guard to `instantiate.py`: halt with a clear
  reason before any write (FR-001, SC-009).
- [X] T010 [US1] Author `course-factory/.claude/commands/course-intake.md`: read `COURSE_SPEC.md` and
  the `insights/` digest (empty/missing is valid — FR-025), run the upfront clarify interview, author
  `COURSE_BRIEF.md` (topic/scope, audience + prior knowledge, running example, source pointers),
  select exactly one archetype profile (default when the spec names none — FR-005/025) and the
  enabled/disabled module set (FR-002/004/005).
- [X] T011 [P] [US1] Author `course-factory/.claude/agents/intake-interviewer.md`: the upfront
  clarify discipline + anti-fabrication rule — surface any missing required field as a **blocking
  question**, never invent a default (FR-002/003, SC-001).
- [X] T012 [US1] Author `course-factory/.claude/commands/course-instantiate.md`: a thin command that
  hands the authored brief + selected template to `instantiate.py` and reports the created folder
  (FR-006).
- [X] T013 [US1] Validate US1 end-to-end per `quickstart.md` § US1 (well-formed → folder;
  missing-running-example → blocked; malformed → halt; unversioned template → halt).

**Checkpoint**: A rough spec becomes a correct, version-stamped, overlay-applied course folder — the
foundational MVP, independently demonstrable with no later phase required.

---

## Phase 4: User Story 2 — Walk the build through the phased pipeline to delivery (Priority: P2)

**Goal**: Advance an instantiated course through syllabus → skeletons → lessons → deliver, each ending
at its matched gate, with phase internals stubbed, finishing with the full per-course artifact set +
a `COURSE_REPORT.md`.

**Independent Test**: From an instantiated fixture course, drive `/course-build` with stub handlers;
phases run strictly in order, each gate is reached + recorded before advancing, and the run ends with
every required artifact plus a `COURSE_REPORT.md` scorecard.

**Depends on**: US1 (an instantiated folder) + Foundational (state core).

### Tests for User Story 2 ⚠️ (write first, must FAIL)

- [X] T014 [P] [US2] `course-factory/tests/test_progress.py` (transitions): the transition function
  **rejects** an advance with no recorded gate pass and any phase skip (SC-006); records `cleared_at`;
  each phase carries its **matched** `gate_type` (SC-007); movement is forward-only, never re-opening a
  passed phase (SC-010).
- [X] T015 [P] [US2] `course-factory/tests/test_phase_walk.py`: feed scripted stub gate results
  (`pass`, `loop→loop→pass`, cap-hit `needs-user`, `failed`) into the transition function; assert the
  ordered walk syllabus→skeletons→lessons→deliver and the **full** delivery artifact set at `done`
  (SC-007/008) — no agent in the loop (research R1).
- [X] T016 [P] [US2] `course-factory/tests/test_diffs.py`: a change to an already-gated artifact is
  appended to `DIFFS.md` (append-only), and `current_phase` never moves backward (FR-023/027, SC-010).

### Implementation for User Story 2

- [X] T017 [US2] Implement the **transition function** in `course-factory/tools/progress.py`:
  `(state, gate_result) → next legal state`; reject advance-without-gate-pass + phase-skip; stamp
  `gate_status=cleared` + `cleared_at`; encode the phase→gate_type map (FR-009/010/011, SC-006/007).
- [X] T018 [US2] Implement round-cap accounting in `progress.py`: increment `active_loop.round`, and
  at 3 convert a `loop` result to `needs-user` for the accept-or-comment decision (exactly one extra
  pass, then accepted regardless — FR-012).
- [X] T019 [P] [US2] Implement `course-factory/tools/diffs.py`: the append-only `DIFFS.md` writer per
  contracts/diffs-ledger.md (FR-027).
- [X] T020 [P] [US2] Implement `course-factory/tools/deliver_check.py`: the required-artifact-presence
  check per contracts/course-folder.md; delivery clears on `COURSE_REPORT.md` **presence**, any
  verdict (FR-020, SC-008).
- [X] T021 [US2] Implement the stub handlers in `course-factory/.claude/skills/phase-stubs/SKILL.md`:
  syllabus/skeleton/lesson/deliver stubs that write a placeholder artifact + return a scripted gate
  result, honoring the input envelope + gate-result contract (contracts/phase-seam.md, research R4).
- [X] T022 [US2] Author the orchestrator `course-factory/.claude/commands/course-build.md`
  (start-or-continue `<name>`): read state → invoke the current phase's handler (stub) → call the
  `progress.py` transition function → persist before the next unit → advance or **park**; enforce the
  gate mapping including the **blocking post-skeleton user scan** (FR-024, SC-011) and the delivery
  gate = report generated, any verdict (FR-011/021). On a post-skeleton scan **change request** (vs
  approval): re-enter the skeleton handler for a **fresh 3-round cap** folding in the author's
  requests, then re-present for **another** blocking scan — same accept-or-comment bound if the fresh
  cap is also exhausted (FR-024). Ask the author **no** open clarifying questions mid-batch — only the
  two ask-moments and the scheduled gates interrupt (FR-014). Append gate-event author feedback to
  `FEEDBACK.md` (FR-026); apply any change to a gated artifact as a forward diff via `diffs.py`
  (FR-023).
- [X] T023 [P] [US2] Author `course-factory/.claude/commands/course-status.md`: a read-only render of
  `BUILD_PROGRESS.md` (no state change).
- [X] T024 [US2] Validate US2 end-to-end per `quickstart.md` § US2 (ordered phases, matched
  reviewers, full delivery set incl. `COURSE_REPORT.md`, blocking post-skeleton scan honored).

**Checkpoint**: An instantiated course walks to delivery through recorded, matched gates — the
orchestration spine works with stubbed phase internals.

---

## Phase 5: User Story 3 — Pause and resume across sessions (Priority: P3)

**Goal**: A fresh session resumes a build exactly where it left off — correct phase, exact unfinished
lesson set — from the course folder alone, with a minimal lock preventing concurrent advances and an
integrity halt on bad state.

**Independent Test**: Take a course mid-lesson-phase (1–3 passed, 4–6 not started) in a new session →
it resumes at the lesson phase, works only 4–6, repeats nothing; a second concurrent session is
refused; a corrupt state file halts.

**Depends on**: US2 (the walk) + Foundational (state core).

### Tests for User Story 3 ⚠️ (write first, must FAIL)

- [X] T025 [P] [US3] Add to `test_progress.py` (resume): resume at the recorded phase + unfinished
  lessons, repeating **0** completed units (SC-004); resume point derived from the folder **alone**
  (SC-005); several courses in staging resolve to exactly the one named (FR-019).
- [X] T026 [P] [US3] Add to `test_progress.py` (lock): a live-holder concurrent advance is **blocked
  and surfaced** (SC-012); a **stale** lock is reclaimable with the reclaim recorded (FR-028).
- [X] T027 [P] [US3] Add to `test_progress.py` (integrity): missing / corrupt / internally
  inconsistent state → **halt + report** (SC-009); `template_version` drift on resume → halt (SC-009).

### Implementation for User Story 3

- [X] T028 [US3] Implement resume in `progress.py`: read state, drift-check `template_version`,
  continue at `current_phase` + the unfinished `lessons[]`, and perform **no** unit the file records as
  done (FR-017/018, SC-004/005).
- [X] T029 [US3] Implement the lock marker in `progress.py`: `/course-build` **mints a per-invocation
  `holder` token** (short random value — no stable Claude session id exists) and passes it in;
  `progress.py` acquires on entry; refuses a live-holder conflict and surfaces it; refreshes on each
  persisted unit; clears on park/clean exit; reclaims a stale lock and records the reclaim (FR-028,
  SC-012). Liveness/stale windows are configurable constants with sensible defaults; the token need
  only be unique per active invocation (contracts/build-progress-schema.md § lock.holder,
  data-model rule 8).
- [X] T030 [US3] Implement integrity validation in `progress.py`: detect missing/corrupt/inconsistent
  state + version drift and **halt + report** rather than guess (FR-022, SC-009).
- [X] T031 [US3] Wire multi-course isolation into `course-build.md`: `/course-build <name>` acts on
  exactly one named course's `BUILD_PROGRESS.md`, independent of other staged courses (FR-019).
- [X] T032 [US3] Validate US3 end-to-end per `quickstart.md` § US3 (resume without repeat, lock
  refusal + stale reclaim, integrity halt, version-drift halt).

**Checkpoint**: Builds pause and resume across sessions from disk alone, with concurrency + integrity
guarantees — the durability property that makes the spine usable over long multi-session builds.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T033 [P] Write `course-factory/tools/README.md`: what each tool guarantees and which command
  calls it (mirrors `meta-env-setup/tools/README.md` shape).
- [X] T034 [P] Add a `.gitignore` entry for `course-factory/courses/` (generated courses are runtime
  staging, not tracked — DESIGN.md).
- [X] T035 [P] Update `specs/course-factory/README.md` status for 001 from "Clarified" → "Planned →
  Tasked" (the index is the cold-session entry point).
- [X] T036 Run the full `pytest` suite over `course-factory/tests/` — all green — and walk
  `quickstart.md`'s four SC families end-to-end (anti-fabrication+integrity; overlay+copy;
  gates+delivery; resume+lock+forward-diff).

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (P1)** → **Foundational (P2)** → **US1 (P3)** → **US2 (P4)** → **US3 (P5)** → **Polish (P6)**.
- Unlike a typical independent-story feature, these stories are **layered** (the spec's own priority
  order): US2's walk needs US1's instantiated folder; US3's resume needs US2's walk. Each remains
  independently **testable** given its stated precondition (US2 starts "from an instantiated course
  folder"; US3 "from a mid-lesson-phase folder"), but they are implemented in order.

### Within each user story

- Test tasks first (they must FAIL), then implementation, then the end-to-end quickstart validation.
- In `progress.py`: state core (T005) before the transition function (T017) before resume/lock/
  integrity (T028–T030) — the file grows across phases.

### Parallel opportunities

- **Setup**: T002 ∥ (after T001).
- **Foundational**: T004 ∥ T005 (different files); T003 before T006/T008 (fixture needed).
- **US1**: T006 ∥ T007 (tests); T011 ∥ T008 (agent vs tool, different files).
- **US2**: T014 ∥ T015 ∥ T016 (tests); T019 ∥ T020 (diffs vs deliver_check); T023 ∥ T022's tail.
- **US3**: T025 ∥ T026 ∥ T027 (tests).
- **Polish**: T033 ∥ T034 ∥ T035.

---

## Parallel Example: User Story 2

```bash
# Tests first (all fail), in parallel — different files:
Task: "test_progress.py transition tests (SC-006/007/010)"
Task: "test_phase_walk.py scripted stub walk (SC-007/008)"
Task: "test_diffs.py forward-diff ledger (FR-023/027, SC-010)"

# Then the two independent tools in parallel:
Task: "Implement course-factory/tools/diffs.py"
Task: "Implement course-factory/tools/deliver_check.py"
```

---

## Implementation Strategy

### MVP first (User Story 1 only)

1. Phase 1 Setup → Phase 2 Foundational → Phase 3 US1.
2. **STOP and VALIDATE**: run `test_instantiate.py` + quickstart § US1. A rough spec → a correct,
   version-stamped, overlay-applied, resumable-shaped course folder, source template untouched. This
   is a demonstrable deliverable on its own (spec US1 "Why this priority").

### Incremental delivery

1. Setup + Foundational → state core + fixtures ready.
2. US1 → instantiation MVP (demo).
3. US2 → the phased walk to delivery with stubbed internals (demo).
4. US3 → pause/resume + concurrency + integrity (demo).
5. Each story adds value without breaking the previous.

### The seam to 002/003/004

The phase-stubs (T021) are the contract 002 (syllabus), 003 (skeleton/lesson), and 004 (deliver/
report) replace — against the **same** `contracts/phase-seam.md` envelope + gate result, without
touching the orchestrator or `progress.py`. Delivering 001 with stubs is what lets those three specs
be built in separate sessions (README decomposition premise).

---

## Notes

- `[P]` = different files, no dependency on an incomplete task.
- Every SC has a home: SC-001/002 → T006/T008; SC-003 → T006; SC-004/005 → T025/T028;
  SC-006/007 → T014/T017; SC-008 → T015/T020; SC-009 → T007/T027/T030; SC-010 → T016/T017;
  SC-011 → T022; SC-012 → T026/T029.
- Verify tests fail before implementing; commit after each task or logical group.
- Stdlib only, pytest only — no new dependencies (repo convention).

---

## Phase 7: Convergence

Appended by `/speckit-converge` (2026-07-23) after assessing the built code against spec/plan/tasks.
Each task traces to the gap that produced it.

- [X] T037 Seed `lessons[]` at the skeleton phase so a live walk reaches delivery with a real lesson
  set per US2/AC3 + FR-015 (missing). Today nothing populates it: `progress.py` only upserts via
  `set_lesson_status`, `phase-stubs/SKILL.md` writes `skeletons/<lesson-id>.md` "per planned lesson"
  with no defined source for that list, and `course-build.md`'s lessons loop iterates an empty
  `lessons[]` — so `deliver_check.py` reports `lessons[] (no lessons recorded)` and SC-008 fails.
  `test_phase_walk.py` masks this by hand-calling `set_lesson_status`. Define where the planned lesson
  ids come from (the syllabus artifact) in `contracts/phase-seam.md`'s terms, have the skeleton stub
  seed each at `not-started` via `progress.py`, document it in `phase-stubs/SKILL.md` +
  `course-build.md`, and add a `test_phase_walk.py` case that drives the walk **without** hand-seeding.
- [X] T038 Append the round-cap accept-or-comment feedback to `FEEDBACK.md` in
  `course-factory/.claude/commands/course-build.md` per FR-026 / Constitution XII (partial). The
  syllabus revision loop and the post-skeleton change request already append; the round-cap "comment"
  branch (skeletons step 2, and the lessons phase that refers back to it) does not — yet it is the
  first case FR-026 names. Append the author's comment before calling `extend-round-cap`.
- [X] T039 Add a `syllabus_subphase` writer + validation to `course-factory/tools/progress.py` per
  FR-015 / FR-022 / contracts/build-progress-schema.md rules 1–2 (missing). 002 owns the field but
  rule 1 forbids hand-editing the JSON block and no `set_syllabus_subphase()` (module or CLI) exists,
  unlike `set_lesson_status` for 003's field; `validate_state()` also never checks its enum or the
  "null unless `current_phase == syllabus`" rule, so an inconsistent value passes the integrity gate.
  Add the setter, the CLI subcommand, the enum + null-unless-syllabus validation, and tests.
- [X] T040 Make the lock refresh reachable per FR-028 / data-model rule 8 / T029 (partial).
  `refresh_lock()` exists and is unit-tested but has no CLI subcommand, and no mutating subcommand
  (`transition`, `set-lesson-status`, …) refreshes `last_progress_at` — so a long live build can go
  stale while actually progressing. Add a `lock-refresh <course_dir> --holder <token>` subcommand (or
  refresh inside the persisted-unit subcommands), and fix `course-build.md`: step 1's `lock-acquire`
  must capture the token and step 3's refresh must pass `--holder`, otherwise following the command
  literally mints a new token each refresh.

---

## Phase 8: Convergence

Appended by `/speckit-converge` (2026-07-23), second pass — after Phase 7's T037–T040 were
implemented. Each task traces to the gap that produced it.

- [X] T041 Add a multi-course isolation test per FR-019 / US3 AC4 (missing). T025 promised "several
  courses in staging resolve to exactly the one named" but no test exercises it — only single-course
  scenarios exist in `test_progress.py`. Add a case: instantiate/init two courses under one
  `courses_dir`, acquire a lock and transition one, and assert the other's `BUILD_PROGRESS.md`
  (state, lock, phase) is byte-for-byte/field-for-field untouched.
- [X] T042 Close the crash window between a lesson's round-cap settle and its terminal-status write
  per FR-016/017 + SC-004 (partial). `course-build.md`'s lessons step calls `clear-active-loop` (or
  `accept-round-cap`) and `set-lesson-status` as **two separate** `progress.py` invocations. A crash
  between them leaves `active_loop` cleared but the lesson still `not-started`/`in-progress` — on
  resume nothing shows the refine cycle completed, so it is redone from round 1, violating "0
  completed units repeated" (SC-004's hard zero). Add a single atomic operation in `progress.py`
  (function + CLI subcommand) that settles the active loop and records the lesson's terminal status
  in one read-mutate-write; update `course-build.md`'s lessons step to call it instead of two calls;
  add a `test_progress.py`/`test_phase_walk.py` case asserting a simulated crash between the two old
  calls cannot occur (i.e. the combined op is the only path).
- [X] T043 Make lessons[] seeding self-healing on resume per FR-017 / Principle XI (partial). Seeding
  is a second `progress.py seed-lessons` call after the syllabus `transition ... pass` in
  `course-build.md`'s syllabus step. A crash between the two leaves `current_phase == "skeletons"`
  with an empty `lessons[]`; `seed-lessons` is idempotent and `SYLLABUS.md` still exists, so this is
  recoverable, but the skeletons step has no defensive check and would stall instead of self-healing.
  Add a guard at the top of `course-build.md`'s skeletons step: if `lessons[]` is empty on entry,
  re-run `seed-lessons` against the already-frozen `SYLLABUS.md` before drafting; add a
  `test_phase_walk.py` case simulating this exact resume point.

---

## Phase 9: Convergence

Appended by `/speckit-converge` (2026-07-23), third pass — after Phase 8's T041–T043 were
implemented. Each task traces to the gap that produced it.

- [X] T044 Propagate T042's atomic lesson-settle into `phase-stubs/SKILL.md` per FR-016/017 + SC-004
  (partial). T042 replaced the lessons-phase two-call settle (`clear-active-loop`/`accept-round-cap`
  then a **separate** `set-lesson-status`) with the single atomic `settle-lesson`, and updated
  `course-build.md`'s lessons step + its Boundaries accordingly — but `.claude/skills/phase-stubs/
  SKILL.md`'s `lessons` bullet (the "The one nuance /course-build must get right per phase" list,
  ~line 74) still narrates the superseded two-call sequence: "run its own round-cap cycle … (`loop`
  → `clear-active-loop` on an early pass, or `accept`/`extend-round-cap` at the cap), then record
  the lesson with `progress.py set-lesson-status <dir> <id> passed`". That is the exact crash window
  T042 closed (a cleared loop stranded against a not-yet-terminal lesson → the cycle redone from
  round 1 on resume, violating SC-004's hard zero), and SKILL.md is read by the driving session, so
  the two docs now prescribe conflicting settles. Rewrite that `lessons` bullet to settle each
  lesson with `progress.py settle-lesson <dir> <id> passed` (or `accepted-at-cap`) — loop-clear and
  terminal-status in one write — matching `course-build.md`. Leave the `skeletons` bullet's
  `clear-active-loop`/`accept-round-cap`/`extend-round-cap` wording unchanged: skeletons carry no
  per-unit terminal status, so their settle is genuinely single-call already. No code or test change
  — `settle_lesson` and its coverage already exist (T042); this closes the doc-propagation gap only.
