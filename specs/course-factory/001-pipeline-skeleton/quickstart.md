# Quickstart — validating the pipeline spine

How to prove the three user stories end-to-end using the in-repo **template fixture** (R6) and the
**stub phase handlers** (R4) — no dependency on spec 000 being built, no real syllabus/lesson work.
All commands run from the repo root unless noted. The deterministic layer is tested with `pytest`;
the pipeline surface is driven as `.claude/` commands.

## Prerequisites

- Python 3.11 (stdlib only).
- `course-factory/tests/fixtures/template-min/` — the minimal frozen `course-template` stand-in.
- `course-factory/tests/fixtures/specs/` — sample `COURSE_SPEC.md` files: `well-formed.md`,
  `missing-running-example.md`, `malformed.md`.
- Stub phase handlers registered behind the seam (`contracts/phase-seam.md`).

## US1 — Intake → instantiated, resumable course (SC-001/002/003/009)

```bash
# 1. Intake a well-formed spec → brief + profile + module selection
#    (driven as the /course-intake command against the fixture spec)
# 2. Instantiate: copy the fixture template into a staging course folder
python course-factory/tools/instantiate.py \
    --spec course-factory/tests/fixtures/specs/well-formed.md \
    --template course-factory/tests/fixtures/template-min \
    --brief <generated COURSE_BRIEF.md> \
    --courses-dir <staging dir>
```

**Expect:**
- A new `courses/<slug>/` with `COURSE_BRIEF.md` (topic/scope, audience, running example, an explicit
  `archetype_profile`, and a `modules` selection), `BUILD_PROGRESS.md` positioned at **syllabus
  start**, and `SOURCES.md` / `FEEDBACK.md` / `DIFFS.md` stubs (SC-002).
- The fixture `template-min/` is **byte-for-byte unchanged** (SC-003) — assert via checksum diff.
- Running intake on `missing-running-example.md` **blocks** with a question and fabricates nothing
  (SC-001); on `malformed.md` the pipeline **halts** with a clear reason and writes **no** partial
  folder (edge case).
- Pointing instantiation at an **unversioned** template **halts** rather than copying (FR-001, SC-009).

Automated: `pytest course-factory/tests/test_instantiate.py`.

## US2 — Walk the instantiated build to delivery with stubbed phases (SC-006/007/008)

```bash
# Drive the orchestrator; every phase handler is the stub → "produced + gate result"
# (driven as the /course-build command against the instantiated fixture course)
```

**Expect:**
- Phases run **strictly in order** syllabus → skeletons → lessons → deliver; the run never skips a
  phase (SC-006 — `progress.py` refuses an advance without a recorded gate pass).
- Each gate is the **matched reviewer**: user-approval / agent-then-user / rubric / report-generated
  (SC-007), verified from `BUILD_PROGRESS.md.phases[].gate_type`.
- The run parks at each **user** gate (syllabus approval, blocking post-skeleton scan) and resumes on
  re-invocation with the recorded approval.
- At `done`, `deliver_check.py` confirms the full required artifact set incl. a `COURSE_REPORT.md`
  with a scorecard + verdict — **any** verdict clears delivery (SC-008, FR-011/021).

Automated: `pytest course-factory/tests/test_phase_walk.py`.

## US3 — Pause and resume across sessions (SC-004/005/012)

```bash
# 1. Instantiate; advance into the lesson phase with lessons 1–3 passed, 4–6 not started
# 2. Simulate a fresh session (no memory): re-invoke the orchestrator on the same course
```

**Expect:**
- The pipeline reads `BUILD_PROGRESS.md`, resumes at the **lesson phase**, works **only** lessons
  4–6, and leaves 1–3 untouched (SC-004) — **0** completed units repeated.
- The resume point is determined from the **course folder alone** (SC-005) — no prior-session state.
- With several courses in staging, resume acts on exactly **one** named course (FR-019).
- **Concurrency:** a second session attempting to advance a course whose `lock` shows a live holder is
  **refused** and the conflict surfaced (SC-012); a **stale** lock is reclaimable, and the reclaim is
  recorded (FR-028).
- A **corrupt/inconsistent** `BUILD_PROGRESS.md`, or a `template_version` drift on resume, **halts**
  and reports rather than guessing (SC-009).

Automated: `pytest course-factory/tests/test_progress.py`.

## Forward-diff ledger (SC-010, FR-023/027)

Request a change to an already-gated syllabus after the syllabus gate cleared:

**Expect:** the change is applied as a forward diff at the current phase and appended to `DIFFS.md`
(`contracts/diffs-ledger.md`); `current_phase` never moves backward and the passed phase is **not**
re-opened (SC-010). Assert `DIFFS.md` is append-only.

Automated: `pytest course-factory/tests/test_diffs.py`.

## What "passing" means

All four `pytest` modules green **and** the four SC families above observed:
- anti-fabrication + integrity halt (SC-001/009),
- overlay + copy-never-mutate (SC-002/003),
- ordered gates + matched reviewers + full delivery set (SC-006/007/008),
- resume-without-repeat + lock (SC-004/005/012),
- forward-only + ledger (SC-010).
