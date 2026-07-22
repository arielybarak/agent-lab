---
description: "Task list for Lessons Phase — Skeletons, Parallel Author–Critic Authoring & Learnability (spec 003)"
---

# Tasks: Lessons Phase — Skeletons, Parallel Author–Critic Authoring & Learnability

**Input**: Design documents from `specs/course-factory/003-lessons/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ (all present)

**Tests**: INCLUDED. The plan names deterministic `pytest` modules and the spec's Success Criteria are
hard-zero measurable (SC-002/003/004/010); the point of the thin tool layer (research R1) is that those
guarantees are asserted by tests, not agent discipline. Test tasks are written FIRST within each story
and must FAIL before implementation. Irreducible-judgment SCs (SC-005 no-auto-advance is a handler
contract property; SC-009 skeleton topic-match/clarity; the *truth* of a claim; whether a confusion
point is real) are validated as `quickstart.md` scenario walkthroughs, not pytest (R2).

**Organization**: By user story (US1 P1 skeletons → US2 P2 lesson pool → US3 P3 fake-student). The
deliverable **adds to** the factory's own build `.claude/` (spec 001's) — one shared `author-critic-loop`
primitive skill, two phase-handler skills (`skeleton-phase`, `lesson-phase`), a shared `mentor-author`
agent plus `skeleton-evaluator` / `lesson-evaluator` / `fake-student` agents — plus four stdlib tools in
`course-factory/tools/` and their tests. It replaces 001's **skeletons** and **lessons** phase-stubs
against `contracts/phase-seam.md` **without touching the orchestrator**. All paths are repo-relative from
`agent-lab/`.

**Cross-spec dependency**: 003 is built **after** 001 and **after 004's rubric core** (README build
order 000 → 001 → 002 → 004-rubric → 003). It writes `lessons[]` via 001's
`course-factory/tools/progress.py`, appends forward diffs via 001's `diffs.py`, and consumes 004's
rubric via `contracts/rubric-gate.md`. 001/004 are not yet built, so the four 003 tools + fixtures are
standalone stdlib and testable now; the rubric is a **fixture** until 004 lands (R5), and live
end-to-end integration (orchestrator invoking the real handlers) is exercised once 001 is implemented
(mirrors 002 validating at the seam + fixtures).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1 / US2 / US3 (setup, foundational, polish carry no story label)

## Path Conventions

- Factory engine (spec 001's, 003 adds to it): `course-factory/.claude/{skills,agents}/`
- Deterministic tools: `course-factory/tools/*.py` (Python 3.11, **stdlib only**)
- Tests + fixtures: `course-factory/tests/`
- Generated courses (runtime, gitignored): `course-factory/courses/<name>/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the factory engine's homes and the test harness so every later task has a place.

- [ ] T001 Confirm the factory `.claude/skills/` and `.claude/agents/` dirs exist (001's Setup) and are
  kept **separate** from any `course-template/.claude/` (Structural Constraints — the two `.claude`
  folders never conflate); create them if running ahead of 001. Confirm `course-factory/tools/` and
  `course-factory/tests/` exist (siblings of 001's / 002's).
- [ ] T002 [P] Confirm `pytest` discovery covers `course-factory/tests/` for the 003 modules (reuse
  001's `conftest.py`; **no new dependencies** — stdlib + pytest only, repo convention). A `.ipynb`
  fixture is plain JSON read with the stdlib `json` module — **no `nbformat` dependency** (R7).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The fixtures and the **single shared** author→critique→refine primitive both phases drive
(FR-001) — nothing story-specific can be built until these exist.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T003 [P] Create lesson-grounding fixtures in `course-factory/tests/fixtures/`:
  `lessons/{fully-cited.md,unresolvable-sn.md,mentor-added.md,silently-ungrounded.md,cited.ipynb}`
  (the `.ipynb` carries its `[Sn]` keys in **markdown** cells, with a decoy `[Sn]`-looking token in a
  code cell that MUST be ignored — R7), `sources/` (a `SOURCES.md` resolution target — reuse 002's
  `sources/well-formed` where it fits; contracts/rubric-gate.md), and `rubric/` (a **minimal**
  per-dimension-threshold rubric standing in for not-yet-built 004 — one requested topic add-on
  included; contracts/rubric-gate.md, R5).
- [ ] T004 [P] Create pool + brief fixtures in `course-factory/tests/fixtures/`:
  `skeletons/{topic-matched,topic-mismatched}/` (data-model "Skeleton"), `brief/` (a `COURSE_BRIEF.md`
  with audience + assumed prior knowledge, running example, selected profile, and `lesson_format`), and
  `pool-scenarios/{serial-1,parallel-2,pre-calibration-barrier,fewer-than-two}` — each a `lessons[]`
  slice + `pool_width` + `calibration_done` flag (data-model "worker-pool state").
- [ ] T005 Author `course-factory/.claude/skills/author-critic-loop/SKILL.md` — the **single shared**
  primitive (FR-001) both phases invoke (per contracts/author-critic-primitive.md): author
  produces/refines → author-blind evaluator emits **cited deltas** → author refines *the deltas*
  (targeted, not a restart — FR-003) → repeat until pass or 001's cap (FR-002). Parameterized by the
  evaluator **checklist** (topic-match+clarity vs. rubric+traceability) and driven by either phase; it
  **never** owns the round counter (001's `active_loop`) and, on the cap, emits the best-effort artifact
  + delta for 001 to surface (FR-002). Records the FR-020 durable-finding → `FEEDBACK.md` append rule.
- [ ] T006 [P] Author `course-factory/.claude/agents/mentor-author.md` — the shared fresh-context
  **domain-mentor** persona (FR-004 note / FR-016: sources inform, never dictate), usable in **batch
  mode** (all skeletons at once, US1) or **per-lesson mode** (one lesson, US2) from a fixed input set;
  respects the selected profile's scaffolding depth (FR-019) without touching the primitive.

**Checkpoint**: Fixtures exist for every tool + scenario, and the one shared primitive + author persona
are ready for both phases to drive. Stories can begin.

---

## Phase 3: User Story 1 — Author the skeleton batch and present it for the blocking scan (Priority: P1) 🎯 MVP

**Goal**: Draft **all** per-lesson skeletons at once as a domain mentor (single batch-level loop,
FR-004), run the shared primitive until every skeleton matches its lesson topic and reads clearly
(FR-005), and **present the batch review-ready and wait** — return `needs-user`, never auto-advance to
lessons (FR-006, honoring 001 FR-024).

**Independent Test**: Given an approved syllabus fixture, run the skeleton phase → all skeletons drafted
in one batch (not one interruption per lesson), the evaluator flags a topic mismatch and the author
corrects it within the cap, and the handler returns **`needs-user`** without advancing (quickstart B1,
SC-005/009).

**Depends on**: Foundational (the shared primitive T005 + mentor-author T006 + skeleton fixture T004).

### Implementation for User Story 1

- [ ] T007 [P] [US1] Author `course-factory/.claude/agents/skeleton-evaluator.md` — the author-blind
  evaluator whose checklist is (a) **topic-match** to each lesson and (b) **clarity / simple language**
  (FR-005); emits cited deltas in the primitive's format (contracts/author-critic-primitive.md).
- [ ] T008 [US1] Author `course-factory/.claude/skills/skeleton-phase/SKILL.md` per
  contracts/skeleton-handler.md: read the seam envelope (frozen `SYLLABUS.md` **+ its `DIFFS.md`**,
  brief, profile, insights); draft **all** skeletons in one batch as `mentor-author` (batch mode,
  FR-004 — the two-in-flight pool is lesson-only); run the **single batch-level** shared primitive with
  `skeleton-evaluator` (FR-005) capped by 001's counter; on a **syllabus gap** append a **forward diff**
  via 001's `diffs.py` and draft against it (never re-open/edit the frozen syllabus — FR-017, SC-008);
  append durable evaluator findings to `FEEDBACK.md` (FR-020); on convergence **or** cap, **present
  review-ready and return `needs-user`** — there is **no `pass` path** (SC-005). On a change-request
  re-invocation, read scan comments from `FEEDBACK.md`, re-run under a **fresh** cap, re-return
  `needs-user` (contracts/skeleton-handler.md).
- [ ] T009 [US1] Validate US1 end-to-end per `quickstart.md` § B1: all skeletons drafted in one batch;
  `topic-mismatched` fixture → evaluator flags mismatch, author corrects within cap; a cap-hit variant
  surfaces best-batch + unresolved deltas (FR-002); handler returns **`needs-user`**, never `pass`
  (SC-005) — 0 auto-advances; each delivered skeleton is topic-matched + clear or explicitly at-cap
  (SC-009, judgment).

**Checkpoint**: An approved syllabus → a review-ready skeleton batch presented for the blocking user
scan, exercising the shared primitive end-to-end before a single full lesson exists (spec US1 rationale).

---

## Phase 4: User Story 2 — Draft lessons via a parallel author–critic worker pool graded by the rubric (Priority: P2)

**Goal**: For each lesson, spin up a **fresh-context author** and a **separate author-blind evaluator**;
mediate their loop keeping **at most `pool_width`** pairs in flight (MVP 1, target 2, FR-009); grade each
lesson against 004's rubric (per-dimension threshold, FR-010) with **every** `[Sn]` traceability-checked
(FR-011); write per-lesson status to `lessons[]` before a lesson is done (FR-012).

**Independent Test**: Given approved skeletons + `SOURCES.md` + the rubric fixture, run the pool → each
author starts fresh-context with the FR-007 inputs, the evaluator never gets author reasoning (SC-002),
at most `pool_width` pairs run (SC-003), a lesson passes only if the rubric passes **and** every `[Sn]`
resolves — an unresolvable citation blocks the pass (SC-004) — and each terminal lesson's status is
written to `lessons[]` (SC-007) (quickstart B2/B5/B6).

**Depends on**: US1 (approved skeletons are the pool's input) + Foundational.

### Tests for User Story 2 ⚠️ (write first, must FAIL)

- [ ] T010 [P] [US2] `course-factory/tests/test_pool_scheduler.py` over `pool-scenarios/*`: the
  scheduler never returns more than `pool_width` lessons to hold `in-progress` at once (`serial-1`,
  `parallel-2` — SC-003); over `pre-calibration-barrier`, no lesson at `syllabus_index ≥ 3` is eligible
  while `calibration_done == false`, all become eligible once true (SC-010); over `fewer-than-two`, the
  only lesson schedules with no barrier deadlock (SC-010 edge). `syllabus_index` is the **1-based list
  position** in `lessons[]`, not a new field (data-model).
- [ ] T011 [P] [US2] `course-factory/tests/test_citation_trace.py` over `lessons/*` + `sources/`:
  `fully-cited.md` passes; `unresolvable-sn.md` **fails** on the unresolvable key (exhaustive, not
  sampled — SC-004); `mentor-added.md` passes (a mentor-added claim is not failed for lacking `[Sn]`;
  thin-grounding tags preserved — SC-004); `silently-ungrounded.md` **fails** (neither cited nor
  mentor-added); `cited.ipynb` traces by the **same** method as `.md` — `[Sn]` in markdown cells
  resolve, the code-cell decoy token is ignored (R7). Assert the failure **reason**, not just exit code.
- [ ] T012 [P] [US2] `course-factory/tests/test_author_envelope.py`: the **evaluator** envelope carries
  the artifact + grading inputs but **no** author-reasoning field (SC-002); the **author** envelope is
  exactly the FR-007 set, and `CALIBRATION.md` is present **iff** the lesson's `syllabus_index > 2` and
  calibration has run (FR-007/021).

### Implementation for User Story 2

- [ ] T013 [P] [US2] Implement `course-factory/tools/sn_resolve.py` — the **canonical** `[Sn]`→
  `SOURCES.md` resolution primitive (honors 002's mentor-added / thin-grounding tags; tracing, not
  truth), the single resolver 002/003/004 import (R2). If 002's `syllabus_lint.py` already exists, lift
  its resolution primitive here and re-point it (a refactor, not a fork). **Keep the citation namespace
  a parameter, not a literal**: `pedagogy/`'s `[Pn]` keys are out of scope here (003 spec Out-of-Scope;
  002 `sources-schema.md` reserves the namespace against collision), but admitting a second key space at
  wiring time must be an argument, not a rewrite (A15).
- [ ] T014 [US2] Implement `course-factory/tools/citation_trace.py` — a thin layer over `sn_resolve`:
  **format-aware extraction** (scan `.md` prose and, for `.ipynb`, only `markdown`-cell `source` via the
  stdlib `json` parser — R7) + the **exhaustive** per-lesson sweep (every claim cited-or-mentor-added;
  **every** `[Sn]` resolved — SC-004). Depends on T013.
- [ ] T015 [P] [US2] Implement `course-factory/tools/pool_scheduler.py` — a **pure function** over
  `(lessons[], pool_width, calibration_done)` → the set eligible to be in flight: enforce the in-flight
  cap (SC-003) and the gate-then-fan-out barrier (no `syllabus_index ≥ 3` before `calibration_done`,
  SC-010); `pool_width = 1` is the serial degenerate case (data-model, R3). Document the honesty
  boundary (decides eligibility; the session does the spawning).
- [ ] T016 [P] [US2] Implement `course-factory/tools/author_envelope.py` — builds the **author** input
  set (FR-007, incl. `CALIBRATION.md` iff `syllabus_index > 2` and calibration ran) and the
  **author-blind evaluator** input set (artifact + grading inputs, **no** author-reasoning channel —
  SC-002, R4). Document the boundary (guarantees the evaluator's *input* is blind; does not scrub the
  artifact itself).
- [ ] T017 [P] [US2] Author `course-factory/.claude/agents/lesson-evaluator.md` — the author-blind
  evaluator whose checklist is the **rubric** (per-dimension threshold, contracts/rubric-gate.md,
  FR-010) **+** the exhaustive `[Sn]` traceability check via `citation_trace.py` (FR-011); MAY flag a
  claim matching an existing-but-unpassed `SOURCES.md` entry as a likely **input-selection** miss
  (distinct from a genuinely ungrounded claim — spec edge case). The evaluator **supplies the
  per-dimension scores; it MUST NOT restate the pass rule** — the all-clear verdict comes from calling
  004's shared `course-factory/tools/rubric_gate.py` (see T018). Writing "every dimension ≥ threshold"
  into this agent's prose would create the second copy of the predicate that 004 SC-009 forbids.
- [ ] T018 [US2] Author `course-factory/.claude/skills/lesson-phase/SKILL.md` per
  contracts/lesson-handler.md: dispatch **only** `pool_scheduler`-eligible lessons (SC-003/010); per
  lesson build envelopes via `author_envelope.py`, spawn fresh `mentor-author` (per-lesson mode) + a
  separate `lesson-evaluator` (SC-002), run the shared primitive, gate on rubric + full traceability
  (a lesson **passes** only if the rubric passes **and** every `[Sn]` resolves — SC-004). The rubric
  half of that gate is decided by **calling 004's `course-factory/tools/rubric_gate.py`** with the
  evaluator's per-dimension scores — **do not re-derive the predicate** here or in the evaluator agent
  (004 SC-009/SC-010: one predicate, two consumers, no aggregate masking). 004's rubric core is built
  **before** 003 in the README build order, so the tool exists; until then it resolves against
  `tests/fixtures/rubric/`, which 004 reuses unchanged. Write each
  lesson's status to `lessons[]` via 001's `progress.py` **before** it is done (FR-012, SC-007); surface
  cap-hit lessons as `needs-user` (accept-or-comment) and return `pass` only when **all** lessons are
  terminal; on a syllabus/skeleton gap append a **forward diff** via `diffs.py` (FR-017, SC-008); honor
  the `.ipynb`/thin-grounding/empty-insights degradations (contracts/lesson-handler.md). **Leaves a hook
  for the US3 calibration trigger** (grown in T021). Depends on T014/T015/T016/T017 + the primitive T005.
- [ ] T019 [US2] Validate US2 end-to-end per `quickstart.md` § B2 (fresh-context author, author-blind
  evaluator SC-002, ≤ `pool_width` in flight SC-003, rubric+traceability gate SC-004, `lessons[]` write
  SC-007), § B5 (a syllabus gap surfaces a **forward diff**, never a phase re-open — SC-008), and § B6
  (resume: a `passed` lesson is skipped from `lessons[]`).

**Checkpoint**: Approved skeletons → graded, `[Sn]`-grounded lessons via the worker pool, each recorded
in `lessons[]` — the phase's headline output (spec US2 rationale). MVP `pool_width = 1` is a fully serial
walk; target 2 is the same scheduler at a config flip (FR-009).

---

## Phase 5: User Story 3 — Calibrate explanation depth with a once-per-course fake-student check (Priority: P3)

**Goal**: When the **first two lessons reach a terminal state** (rubric-passed **or**
cap-surfaced-and-user-accepted), run a **single** lightweight fake-student check (FR-013), fix its
confusion points in those two lessons and **fold them into the drafting guidance for every remaining
lesson** (FR-014), persist to `CALIBRATION.md` (FR-021), and run it **at most once** (FR-015) — enforcing
gate-then-fan-out (no lesson beyond the first two begins before calibration, FR-018/SC-010).

**Independent Test**: With the first two lessons terminal, run the check → a fresh subagent gets **only**
audience + assumed prior knowledge + those two lessons, reports confusion points, the points are fixed
and each edited lesson **re-graded** (SC-006), the guidance is folded into `CALIBRATION.md`, lessons at
index ≥ 3 begin only after (SC-010), and re-invoking with `CALIBRATION.md` present does **not** re-run it
(SC-006) (quickstart B3/B4).

**Depends on**: US2 (the pool producing the first two terminal lessons) + Foundational.

### Implementation for User Story 3

- [ ] T020 [P] [US3] Author `course-factory/.claude/agents/fake-student.md` per contracts/calibration.md:
  a **fresh** subagent whose input is **only** the brief's audience + assumed prior knowledge and the
  first two terminal lessons; it reads them and **attempts the exercise**, reporting concrete confusion
  points (undefined terms, too-fast steps). **No-exercise fallback**: read-and-report-confusion only
  (still folds in — FR-014).
- [ ] T021 [US3] **Grow** `course-factory/.claude/skills/lesson-phase/SKILL.md` with the calibration
  portion (contracts/calibration.md): when the first two lessons are terminal, run `fake-student` **iff
  `CALIBRATION.md` is absent** (once-per-course guard, R8); fix confusion points in the two lessons and
  **re-grade each edited lesson** against the rubric before completing — a failing re-grade re-enters the
  primitive under a **fresh** cap (FR-014, SC-006); fold the guidance into **`CALIBRATION.md`** (FR-021),
  whose presence flips `pool_scheduler`'s `calibration_done` (SC-010); **idle** (not skip) while a
  cap-surfaced first/second lesson awaits accept-or-comment (FR-018). Fewer-than-two-lessons → run once
  on what exists, no deadlock (FR-013). Same file as T018 → **sequential**, not `[P]`.
- [ ] T022 [US3] Validate US3 end-to-end per `quickstart.md` § B3 (only audience+priors+two lessons;
  confusion points fixed + **re-graded** SC-006; folded into `CALIBRATION.md`; index ≥ 3 begins only
  after SC-010; **exactly once** — re-invoke with `CALIBRATION.md` present is a no-op SC-006) and § B4
  (no-exercise read-only fallback; one-lesson course runs once, no deadlock).

**Checkpoint**: The first two lessons calibrate the whole course's explanation format once; every
remaining lesson is authored with the calibration folded in — the learnability surface of the phase.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T023 [P] **Update** `course-factory/tools/README.md` (001's/002's existing file — do **not** create
  a second): append the 003 tools (`sn_resolve.py`, `citation_trace.py`, `pool_scheduler.py`,
  `author_envelope.py`), what each guarantees, the **canonical-resolver reuse** note (one `sn_resolve`
  across 002/003/004 — R2), and the two honesty boundaries (scheduler decides eligibility, not spawning;
  envelope blinds the evaluator's input, not the artifact — R3/R4).
- [ ] T024 [P] Update `specs/course-factory/README.md` status for 003 from "Clarified" → "Planned →
  Tasked" (the index is the cold-session entry point).
- [ ] T025 Run the full `pytest` suite over `course-factory/tests/` (003 modules green) and walk
  `quickstart.md` Part A (mechanical SCs SC-002/003/004/010) + Part B (scenario SCs B1–B6) end-to-end.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (P1)** → **Foundational (P2)** → **US1 (P3)** → **US2 (P4)** → **US3 (P5)** → **Polish (P6)**.
- The stories are **layered** (the spec's own priority order): US2's pool consumes US1's approved
  skeletons; US3's calibration consumes US2's first two terminal lessons. Each remains independently
  **testable** given its stated precondition (US1 "given an approved syllabus"; US2 "given approved
  skeletons + rubric"; US3 "given two terminal lessons"), but they are implemented in order.

### Within each user story

- Test tasks first (they must FAIL), then implementation, then the end-to-end quickstart validation.
- The **`lesson-phase/SKILL.md` handler grows across stories** — pool + gate portion (T018, US2) →
  calibration portion (T021, US3); these edit the same file and are therefore **sequential**, not `[P]`
  (mirrors 002's `syllabus-phase` growing across phases).

### Parallel opportunities

- **Setup**: T002 (after T001).
- **Foundational**: T003 ∥ T004 (different fixture dirs); T006 ∥ T005-then (agent vs. skill, different
  files) — both before any story.
- **US1**: T007 (evaluator agent) before T008 (skeleton skill needs it).
- **US2**: T010 ∥ T011 ∥ T012 (tests, different files); T013 before T014 (citation_trace imports
  sn_resolve); T015 ∥ T016 ∥ T017 (scheduler vs. envelope vs. evaluator agent, different files) — all
  before T018 (the handler wires them).
- **US3**: T020 (fake-student agent) before T021 (the skill's calibration portion invokes it).
- **Polish**: T023 ∥ T024.

---

## Parallel Example: User Story 2

```bash
# Tests first (all fail), in parallel — different files:
Task: "test_pool_scheduler.py — ≤ pool_width in flight + gate-then-fan-out (SC-003/010)"
Task: "test_citation_trace.py — exhaustive [Sn] resolve, .md/.ipynb parity (SC-004)"
Task: "test_author_envelope.py — evaluator envelope is author-blind (SC-002)"

# Then the independent tools/agent in parallel — different files (sn_resolve before citation_trace):
Task: "Implement course-factory/tools/pool_scheduler.py"
Task: "Implement course-factory/tools/author_envelope.py"
Task: "Author course-factory/.claude/agents/lesson-evaluator.md"
```

---

## Implementation Strategy

### MVP first (User Story 1 only)

1. Phase 1 Setup → Phase 2 Foundational → Phase 3 US1.
2. **STOP and VALIDATE**: run quickstart § B1 — an approved syllabus → a review-ready skeleton batch
   that returns `needs-user` (0 auto-advances, SC-005), exercising the shared primitive end-to-end. A
   demonstrable, independently-valuable deliverable before a single full lesson (spec US1 rationale).

### Incremental delivery

1. Setup + Foundational → fixtures + the shared primitive + author persona ready.
2. US1 → the review-ready skeleton batch (demo — SC-005/009).
3. US2 → the worker pool of graded, `[Sn]`-grounded lessons (demo — SC-002/003/004/007).
4. US3 → the once-per-course fake-student calibration + gate-then-fan-out (demo — SC-006/010).
5. Each story adds value without breaking the previous.

### The seam to 001 and 004 (and upstream from 002)

003 **replaces 001's `skeletons` and `lessons` phase-stubs** against the **same**
`contracts/phase-seam.md` envelope + gate-result vocabulary, touching neither the orchestrator nor
`progress.py`/`diffs.py`. It **consumes 004's rubric** as a pass/fail gate via
`contracts/rubric-gate.md` (a fixture until 004's rubric core lands, R5) and reads 002's frozen
`SYLLABUS.md` + `DIFFS.md` and populated `SOURCES.md`. Building 003 against the seam is what lets it drop
into 001 without a spine change (README decomposition premise).

### Deferred (flagged, not built here)

- **`pool_width = 2` live concurrency** — the scheduler is tested at width 2, but the target-2
  concurrency model (incl. per-lesson round tracking, which a single `active_loop` cannot hold — R9) is
  validated on **real runs** (DESIGN "Open decisions"; FR-009). MVP ships serial (`pool_width = 1`),
  where 001's single `active_loop` is authoritative verbatim.

---

## Notes

- `[P]` = different files, no dependency on an incomplete task.
- Every SC has a home: **SC-001** (cap) → T005 + 001's counter; **SC-002** → T012/T016; **SC-003** →
  T010/T015; **SC-004** → T011/T013/T014; **SC-005** → T008/T009 (handler contract + scenario);
  **SC-006** → T021/T022 + T012 (fold-in via envelope); **SC-007** → T018/T019 (via `progress.py`);
  **SC-008** → T008/T018 + T009/T019 (forward diff via `diffs.py`, scenario); **SC-009** → T009
  (judgment scenario); **SC-010** → T010/T015 (scheduler) + T021/T022 (runtime barrier).
- The **round-cap counter is 001's** (`active_loop`), not 003's — the shared primitive (T005) owns the
  round *body*, not the count (contracts/author-critic-primitive.md).
- **`syllabus_index` is derived from `lessons[]` list position**, so 003 needs **no** change to 001's
  `{ id, status }` schema (data-model).
- Verify tests fail before implementing; commit after each task or logical group.
- Stdlib only, pytest only — no new dependencies (repo convention).
