---
description: "Task list for Grading & Delivery — Rubric, Course-Evaluator, Report, Harvest & Comparison (spec 004)"
---

# Tasks: Grading & Delivery — Rubric, Course-Evaluator, Report, Harvest & Comparison

**Input**: Design documents from `specs/course-factory/004-grading-delivery/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ (all present)

**Tests**: INCLUDED. Four Success Criteria are stated in hard-zero / 100% terms (SC-001/004/007/008/009/010);
the whole point of the thin tool layer (research R1) is that those guarantees are asserted by `pytest`,
not agent discipline — so test tasks are written FIRST within each story and must FAIL before
implementation. Irreducible-judgment SCs (SC-003 scorecard shape; SC-011 the independent verdict;
SC-005 the report's contents; SC-002 add-on application; SC-006 no phase re-open) are validated as
`quickstart.md` scenario walkthroughs, not pytest (R1 honesty boundary).

**Organization**: By user story in priority order — **US1 (P1) rubric core** 🎯 MVP → **US2 (P2)
course-evaluator + report** → **US3 (P3) harvest** → **US4 (P4) comparison**. The deliverable spans
**two `.claude/` homes** (the frozen `course-template/` for the rubric asset + evaluator + report; the
factory's own `course-factory/.claude/` for harvest + comparison) plus **four stdlib tools** appended
to `course-factory/tools/` and two factory-level knowledge folders (`insights/`, `comparison/`). All
paths are repo-relative from `agent-lab/`.

**Cross-spec dependency & build slots**: Per the README build order
`000 → 001 → 002 → 004-rubric-core → 003 → 004-delivery`:

- **US1 is the `004-rubric-core` slot — built BEFORE 003.** It fills 000's rubric *shape* with grading
  semantics and ships the shared **`rubric_gate.py`** pass predicate; 003's `lesson-evaluator` then
  consumes that predicate (003's `contracts/rubric-gate.md` already names 004 the owner of the
  dimensions/thresholds/scale). *Coordination:* 003's already-planned tasks apply the threshold as
  agent judgment today; importing `rubric_gate.py` is an implementation convergence for the 003
  session to pick up — **not** a scope change, and this task list does not edit 003's files.
- **US2–US4 are the `004-delivery` slot — built AFTER 003.** US2's `course_trace.py` **imports** the
  shared `sn_resolve.py` that 003 builds ("one resolver, not three") — no rival resolver.
- 000/002/003 are **not built at plan time**, so the four tools + fixtures are standalone stdlib and
  testable now against the **shared fixtures** (003's `rubric/`, `sources/`, `lessons/`); the real
  rubric asset, `SOURCES.md`, and `sn_resolve.py` replace their stand-ins when those slots land, with
  the predicates and contracts unchanged.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1 / US2 / US3 / US4 (setup, foundational, polish carry no story label)

## Path Conventions

- Frozen template (copied into each course; 000 distills shells, 004 fills grading behavior):
  `course-factory/course-template/` + `course-factory/course-template/.claude/{agents,commands}/`
- Factory engine (spec 001's home; 004 appends): `course-factory/.claude/{commands,agents}/`
- Deterministic tools: `course-factory/tools/*.py` (Python 3.11, **stdlib only**)
- Tests + fixtures: `course-factory/tests/`
- Cross-course knowledge: `course-factory/insights/`, `course-factory/comparison/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the two `.claude/` homes and the test harness so every later task has a place.

- [ ] T001 Confirm `course-factory/tools/` and `course-factory/tests/` exist (siblings of 001's/002's/003's)
  and that `course-factory/.claude/{commands,agents}/` (001's engine) is kept **separate** from
  `course-factory/course-template/.claude/` (Structural Constraints — the two `.claude` folders never
  conflate). Create the `course-template/.claude/{agents,commands}/` path if running ahead of 000.
- [ ] T002 [P] Confirm `pytest` discovery covers `course-factory/tests/` for the 004 modules (reuse
  001's `conftest.py`; **no new dependencies** — stdlib + pytest only, repo convention).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Make the shared fixtures available to every story. No user-story work begins until this
is done.

**⚠️ CRITICAL**: US1 and US2 both grade against the rubric + sources fixtures.

- [ ] T003 [P] Reuse 003's/002's shared fixtures under `course-factory/tests/fixtures/` — `rubric/`
  (minimal per-dimension-threshold rubric), `sources/` (a `SOURCES.md` with a live entry + an
  `unresolvable`-flagged entry), `lessons/` (fully-cited, `unresolvable-[Sn]`, `mentor-added`,
  `silently-ungrounded`, and an `.ipynb` whose keys live in markdown cells). **Do not duplicate** — if
  they exist from 003, use them; only add what is missing.

**Checkpoint**: Shared fixtures ready — story implementation can begin.

---

## Phase 3: User Story 1 - Define the one-rubric-two-layers (Priority: P1) 🎯 MVP

**Goal**: The single rubric's **grading semantics** (scale, per-dimension thresholds, weights,
hard-gate rule) filling 000's two-layer shape, plus the **shared pass predicate** and the
**single-rubric invariant** — the independently-shippable increment that unblocks 003.

**Independent Test**: Inspect the rubric — generic core + a mechanism for spec-requested add-ons,
exactly one rubric in the repo (no rival), a pass/fail gate a lesson evaluator can apply. `pytest`
proves the predicate rejects aggregate masking and the lint rejects a rival.

### Tests for User Story 1 ⚠️ (write first, must FAIL before implementation)

- [ ] T004 [P] [US1] `course-factory/tests/test_rubric_gate.py`: all dimensions ≥ threshold →
  `passed=True` with per-dim scores retained; **one** below-threshold dim → `passed=False` even when
  others max out (**no aggregate masking**, SC-010); a requested add-on is gated like a core dim; an
  **unknown** requested add-on is **surfaced**, not silently dropped (SC-002).
- [ ] T005 [P] [US1] `course-factory/tests/test_single_rubric_lint.py`: exactly one rubric asset →
  passes; a planted second quality-definition file → **fails**; a `comparison/` proposal file does
  **not** count as a rival (SC-001/008/009).

### Implementation for User Story 1

- [ ] T006 [US1] Author `course-factory/course-template/rubric.md` — fill 000's two-layer **shape**
  (five core dimensions + add-on slots) with 004's grading **semantics**: concrete `scale`,
  per-dimension `threshold`, `weight` (reporting only, **not** a gate input), the **hard-gate rule**,
  and the rubric **version = the template `VERSION`** (one identity). Per
  `contracts/rubric-grading-semantics.md`. Until 000 ships, this parameterizes the `rubric/` fixture.
- [ ] T007 [US1] Implement `course-factory/tools/rubric_gate.py` — the **pass predicate**: given
  `{dimension: score}` + the rubric, return `PassResult(passed, per_dimension)` where `passed` iff
  **every** dimension (core + requested add-ons) ≥ its threshold; retain per-dim scores; surface an
  unknown requested add-on. **Shared**: 003's lesson gate + 004's course-evaluator call this one
  predicate. Makes T004 pass. Per `contracts/rubric-grading-semantics.md`.
- [ ] T008 [US1] Implement `course-factory/tools/single_rubric_lint.py` — enumerate every quality
  definition in the factory → assert **exactly one** rubric (0 rivals); a `comparison/` proposal is
  not a rubric. Makes T005 pass.

**Checkpoint**: US1 shippable — the rubric + shared predicate exist; **003 can now consume them** as
its lesson gate. This is the MVP; US2–US4 build after 003.

---

## Phase 4: User Story 2 - Grade a course & emit COURSE_REPORT.md (Priority: P2)

**Goal**: The course-evaluator applies the rubric to a finished course, runs the **exhaustive `[Sn]`
traceability** sweep (tracing, not truth) honoring mentor-added tags, **independently grades whole-arc
dimensions**, and emits a Scorecard; `/course-report` writes it to `COURSE_REPORT.md`.

**Independent Test**: Given a finished course + the rubric, run the evaluator → a scorecard with
per-dim scores, wins, cleanups, verdict; an unresolvable `[Sn]` is flagged while a mentor-added claim
is not; `COURSE_REPORT.md` reads as a quality report distinct from `FEEDBACK.md`.

### Tests & fixtures for User Story 2 ⚠️ (write first, must FAIL before implementation)

- [ ] T009 [P] [US2] Add `course-factory/tests/fixtures/course/` — a finished-course fixture with
  **every lesson passing** but **incomplete arc coverage** (a syllabus topic never taught): the
  SC-011 independent-verdict scenario.
- [ ] T010 [P] [US2] `course-factory/tests/test_course_trace.py`: over the **shared** `sn_resolve`, the
  course-wide sweep flags 100% of unresolvable `[Sn]` (no-such-entry **and** an entry 002 flagged
  `unresolvable` — the dead-source edge case); a `mentor-added` claim is **not** failed for lacking
  `[Sn]`; `thinly-grounded` flags are preserved; exhaustive, not sampled (SC-004).

### Implementation for User Story 2

- [ ] T011 [US2] Implement `course-factory/tools/course_trace.py` — a **thin course-scoped** layer over
  the shared `sn_resolve.py` (import it, do **not** re-author): extract every `[Sn]` across all lessons
  + `SYLLABUS.md` → resolve each → `TraceabilityFinding[]`. Analogous to 003's per-lesson
  `citation_trace.py`. Makes T010 pass. Per `contracts/citation-traceability.md`. (Until 003 lands
  `sn_resolve.py`, stub the import against the shared `lessons/`+`sources/` fixtures.)
- [ ] T012 [US2] Author `course-factory/course-template/.claude/agents/course-evaluator.md` — assemble
  the per-course rubric (core + requested add-ons; surface an unknown add-on), score each dimension,
  apply the pass predicate via `rubric_gate.py` (T007), run `course_trace.py` (T011), honor
  mentor-added / preserve thin-grounding, **independently grade whole-arc dimensions** (coverage /
  flow / running-example) and MAY return `needs-work` even when all lessons passed, emit the
  `Scorecard`, and record any already-passed-artifact gap as a **forward diff** (001's `DIFFS.md`) —
  **never** re-open a passed phase. Per `contracts/course-evaluator.md`.
- [ ] T013 [US2] Author `course-factory/course-template/.claude/commands/course-report.md` — generate
  `courses/<name>/COURSE_REPORT.md` from the Scorecard: rubric scores + verdict + **rubric version**;
  reads as a quality report to the **user**, distinct from `FEEDBACK.md`; delivered as-is at **any**
  verdict (a `needs-work` report is never withheld — its gaps feed `/improve-course`). 000 distills the
  command shell; 004 owns the contents. Per `contracts/course-report.md`.

**Checkpoint**: US2 — a finished course grades to a delivered `COURSE_REPORT.md`; gates delivery by
its generation, not its verdict.

---

## Phase 5: User Story 3 - Harvest FEEDBACK.md into insights/ (Priority: P3)

**Goal**: Two **user-invoked** paths (per-insight capture + `setup-retro`-style bulk harvest) that
append-only into the cross-course `insights/` digest — the compounding mechanism. No automatic trigger.

**Independent Test**: Given a course with a populated `FEEDBACK.md`, the user-invoked harvest distills
its critiques into `insights/` (append, not clobber); an empty `FEEDBACK.md` is a no-op; nothing
harvests until invoked.

### Tests & fixtures for User Story 3 ⚠️ (write first, must FAIL before implementation)

- [ ] T014 [P] [US3] Add `course-factory/tests/fixtures/feedback/` — `populated` (several critiques),
  `empty` (the no-op case), and a two-course pair (the no-clobber case).
- [ ] T015 [P] [US3] `course-factory/tests/test_harvest.py`: an empty `FEEDBACK.md` → **no-op**, not an
  error; harvesting course B does **not** overwrite course A's insights (append-only); re-harvesting is
  dedupe-safe (SC-007).

### Implementation for User Story 3

- [ ] T016 [US3] Implement `course-factory/tools/harvest.py` — the append-only `insights/` mechanics:
  append a distilled entry keyed by `source_course` + `date`, **no-op** on empty, **never clobber**,
  dedupe-safe. The *distillation* is the command's judgment; the *append* is the tool's. Makes T015
  pass. Per `contracts/insights-harvest.md`.
- [ ] T017 [P] [US3] Create `course-factory/insights/README.md` — fix the digest form (topic-organized
  `.md`, append-only, directory-shaped, each entry dated + sourced, **empty-is-valid**, **no seeded
  corpus**). `insights/` **starts empty**.
- [ ] T018 [US3] Author `course-factory/.claude/commands/harvest-feedback.md` — the
  `setup-retro`-style **bulk harvest**: distill a course's `FEEDBACK.md` (every critique represented,
  not verbatim) and append via `harvest.py`. Per `contracts/insights-harvest.md`.
- [ ] T019 [P] [US3] Author `course-factory/.claude/commands/insight-capture.md` — the user-triggered
  **per-insight capture**: log one insight to `insights/<theme>.md` on demand. **No hook / phase-call /
  scheduler wires either command** — "user-invoked only" is a construction guarantee (SC-007, R6).

**Checkpoint**: US3 — the harvest compounds `insights/`; readers (001/002/003) load it; 0 automatic
triggers.

---

## Phase 6: User Story 4 - Propose rubric revisions via comparison/ (Priority: P4)

**Goal**: Analyze a well-made external course → a **proposed revision to the one rubric** (never a
rival) + a per-course report feeding the `/improve-course` backlog; adoption is a deliberate,
human-reviewed re-stamp via 000's rubric-only path.

**Independent Test**: Given an external course, `comparison/` emits proposed revisions targeting the
**one** rubric + a per-course report; no rival rubric is created; the live rubric is unchanged until a
revision is deliberately adopted.

### Tests & fixtures for User Story 4 ⚠️ (write first, must FAIL before implementation)

- [ ] T020 [P] [US4] Add `course-factory/tests/fixtures/external-course/` — a well-made external-course
  stand-in for the comparison scenario.
- [ ] T021 [P] [US4] Extend `course-factory/tests/test_single_rubric_lint.py` — a `comparison/`
  **proposal file** present under `comparison/` does **not** trip the single-rubric invariant (the
  live rubric stays the only rubric; the proposal is not a rival), SC-008.

### Implementation for User Story 4

- [ ] T022 [US4] Author `course-factory/.claude/agents/comparison-analyst.md` — external-course
  analysis **reusing 002's research discipline** (weigh reliability over popularity → cite → converge
  or budget-cap), not a third method; produce a `ProposedRevision` targeting the one rubric with cited
  evidence. Per `contracts/comparison.md`.
- [ ] T023 [US4] Author `course-factory/.claude/commands/compare-course.md` — run the analysis → write
  a `ProposedRevision` + a per-course `ComparisonReport` into `course-factory/comparison/`; **never**
  mutate the live rubric; grading keeps using the current adopted rubric version until adoption.
- [ ] T024 [P] [US4] Create `course-factory/comparison/README.md` — fix the output shape + the
  **minimal adoption protocol**: maintainer reviews a proposal against real course evidence → approve
  re-stamps the template via **000's rubric-only revision path** (MINOR/PATCH `VERSION` bump) with
  provenance to the proposal (the stamp bump **is** the adoption record). Per `contracts/comparison.md`.

**Checkpoint**: US4 — comparison proposes revisions to the single rubric; 0 rivals; live rubric
untouched until deliberate adoption.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T025 [P] **Update** `course-factory/tools/README.md` (001's/002's/003's existing file — do **not**
  create a second): append the four 004 tools (`rubric_gate.py`, `single_rubric_lint.py`,
  `course_trace.py`, `harvest.py`), what each guarantees, the **shared-primitive reuse** notes (one
  `sn_resolve` across 002/003/004; `rubric_gate` is the one predicate shared with 003's lesson gate),
  and the R1 honesty boundary (the tools guarantee the predicate / resolution / append / single-rubric
  enumeration; the agent supplies the scores / verdict / distillation).
- [ ] T026 [P] Update `specs/course-factory/README.md` — 004 status "Clarified" → "Planned → Tasked";
  add to the seam log that `rubric_gate.py` is the **shared pass predicate** (003's lesson gate + 004's
  evaluator) and `course_trace.py` is a thin course-scoped layer over the shared `sn_resolve` (the
  index is the cold-session entry point).
- [ ] T027 Run the full `pytest` suite over `course-factory/tests/` (004 modules green) and walk
  `quickstart.md` Part A (mechanical SCs SC-001/004/007/008/009/010) + Part B (scenario SCs
  SC-002/003/005/006/011) end-to-end.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)** → **Foundational (Phase 2)** → **User Stories (Phases 3–6)** → **Polish
  (Phase 7)**.
- **Build-slot reality** (not team parallelism): **US1 is built at the `004-rubric-core` slot, before
  003**; **US2–US4 at the `004-delivery` slot, after 003**. US1 must land first regardless of staffing
  because 003 consumes its rubric + predicate.

### User-story dependencies

- **US1 (P1)** — no dependency on other 004 stories. **Produces** `rubric_gate.py` (consumed by 003)
  and the rubric asset (consumed by US2 + 003).
- **US2 (P2)** — depends on **US1** (`rubric_gate.py`, the rubric asset) **and** 003's `sn_resolve.py`
  (built by the US2 build slot). Independent of US3/US4.
- **US3 (P3)** — independent of US1/US2 (only `harvest.py` + `FEEDBACK.md` fixtures). Post-MVP.
- **US4 (P4)** — depends on **US1**'s `single_rubric_lint.py` (proposal-not-a-rival) and reuses 002's
  research method. Post-MVP.

### Within each story

- Tests are written FIRST and must FAIL before implementation.
- Tools before the agents/commands that call them (`rubric_gate`/`course_trace`/`harvest` before the
  evaluator/report/harvest commands).
- Story complete + its checkpoint validated before the next priority.

### Parallel opportunities

- **Setup**: T002 [P].
- **Per story**: the test tasks and fixture tasks marked [P] run together (different files); the
  README/knowledge-folder tasks (T017, T024) run [P] alongside their story's command authoring.
- **Polish**: T025 ∥ T026 (different files); T027 last (needs all modules green).
- The four tools live in different files — once their tests exist, `rubric_gate`, `single_rubric_lint`,
  `course_trace`, and `harvest` can be implemented in parallel **within their build slot**.

---

## Parallel Example: User Story 1 (the MVP)

```bash
# Write both US1 test modules first (different files, both must FAIL):
Task: "test_rubric_gate.py — no aggregate masking; unknown add-on surfaced (SC-002/010)"
Task: "test_single_rubric_lint.py — planted rival fails; proposal is not a rival (SC-001/008/009)"

# Then the rubric asset + the two tools (different files):
Task: "Author course-template/rubric.md — grading semantics over 000's shape"
Task: "Implement tools/rubric_gate.py — the shared pass predicate (makes test_rubric_gate pass)"
Task: "Implement tools/single_rubric_lint.py — the single-rubric invariant (makes test_single_rubric_lint pass)"
```

---

## Implementation Strategy

### MVP first (User Story 1 only — the `004-rubric-core` slot)

1. Phase 1 Setup → Phase 2 Foundational (shared fixtures).
2. Phase 3 US1 — the rubric asset + `rubric_gate.py` + `single_rubric_lint.py`.
3. **STOP and VALIDATE**: `pytest test_rubric_gate.py test_single_rubric_lint.py` green; the rubric is
   the sole quality definition with a pass/fail gate. **003 is now unblocked.**

### Incremental delivery (the `004-delivery` slot, after 003)

1. US2 → the course-evaluator + `COURSE_REPORT.md` (gates delivery by generation).
2. US3 → the harvest (compounds `insights/`).
3. US4 → `comparison/` (proposes rubric revisions).
4. Each story adds value without touching US1's rubric contract or 003's lesson gate.

---

## Notes

- [P] = different files, no dependency on an incomplete task.
- The **four deterministic tools** map 1:1 to the four hard-zero SC clusters (SC-010 → `rubric_gate`;
  SC-001/008/009 → `single_rubric_lint`; SC-004 → `course_trace` over shared `sn_resolve`; SC-007 →
  `harvest`). Everything else is agent judgment behind a `quickstart.md` scenario.
- **Do not re-author shared primitives**: import 003's `sn_resolve.py`; offer 003 the shared
  `rubric_gate.py` (do not edit 003's files here). **Do not create a second `tools/README.md`** — append.
- **Two `.claude/` homes stay distinct**: the rubric + evaluator + report are frozen-template assets;
  the harvest + comparison are the factory's own. Never conflate them (Structural Constraints).
- Commit after each task or logical group; stop at any checkpoint to validate the story independently.
