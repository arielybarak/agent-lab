# Quickstart — validating the Syllabus Phase

How to prove the feature works **end-to-end without a live research run or a built 000/001**, by
exercising the deterministic tool layer against fixtures (mechanical SCs) and walking the judgment paths
as scenarios (irreducible-judgment SCs, R2). Mirrors 001's fixture-first validation (R6).

## Prerequisites

- Python **3.11** (stdlib only — no install step).
- Fixtures under `course-factory/tests/fixtures/` (this spec ships them):
  - `brief-min/` — a minimal `COURSE_BRIEF.md` with a default-profile stand-in, in two variants
    (`lesson_format` unset / set).
  - `sources/` — `SOURCES.md` samples: `well-formed`, `missing-key`, `reliability-absent`,
    `duplicate-work`.
  - `syllabi/` — `SYLLABUS.md` samples: `fully-traced`, `ungrounded-topic`, `dangling-citation`
    (cites an `[Sn]` absent from `SOURCES.md`), `thin-grounding`, `missing-divergence-assessment`.
  - `query-log/` — research query-log samples: `under-budget`, `at-budget`, `over-budget`.

## Part A — mechanical SCs (pytest over the tool layer)

```bash
cd course-factory
python -m pytest tests/test_sources_lint.py tests/test_syllabus_lint.py tests/test_research_budget.py
```

| Test | Fixture(s) | Asserts | SC |
| :--- | :--- | :--- | :--- |
| `test_sources_lint.py` | `sources/*` | `well-formed` passes; `missing-key` and `reliability-absent` **fail**; `duplicate-work` warns (one work, two links → one key). | SC-001 |
| `test_syllabus_lint.py` | `syllabi/*`, `brief-min/*`, `sources/well-formed` | `fully-traced` passes; `ungrounded-topic` **fails** (SC-003); `dangling-citation` **fails** — a `[Sn]` absent from `SOURCES.md` is not a landing trace (SC-003); `thin-grounding` fails unless every flagged topic is `mentor-added` (SC-008); `missing-divergence-assessment` **fails** (SC-005); a brief with `lesson_format` unset **fails** (SC-004). | SC-003/004/005/008 |
| `test_research_budget.py` | `query-log/*` | `under-budget` → `exhausted()==False`; `at-budget`/`over-budget` → `True` (stop). A **re-research** call after a divergence answer continues the same count and **cannot exceed** the original cap (FR-019). | SC-002 |

**Expected outcome:** all pass; each negative fixture fails for the stated reason (assert the message,
not just the exit code, so a lint that passes for the *wrong* reason is caught).

## Part B — judgment SCs (scenario walkthroughs)

These exercise the `.claude/` surface (`syllabus-phase` handler + `syllabus-composer` + re-homed
`mentor-research`). No pytest — a reviewer follows the script against the handler and confirms the
observable behavior. Each maps to a User Story Independent Test in the spec.

### B1 — US1: ground the topic (research → SOURCES.md)
1. Invoke the handler with the `brief-min` envelope for a **well-covered** topic.
2. Confirm research searches **web → GitHub → platform (last)**; platform is skipped-with-a-recorded-
   limitation if it needs a login (FR-001, SC-006) — **no** scraper/login/paid pull.
3. Confirm it **stops at convergence or the budget**, never unbounded (SC-002), and that `SOURCES.md`
   entries each carry an `[Sn]` key + a reliability judgment (not a bare star count) — run
   `sources_lint.py` on the result (SC-001).

### B2 — US2: compose as a mentor
1. Feed a `SOURCES.md` containing a **deliberately stale** and an **off-topic** source.
2. Confirm the syllabus **corrects** them (stale/irrelevant material not blindly carried — FR-006),
   every topic is `[Sn]`-traced **or** `mentor-added` (SC-003), a **volume** is set (FR-008), and
   `lesson_format` is written to `COURSE_BRIEF.md` (SC-004) — run `syllabus_lint.py` (SC-003/004/008).
3. Confirm the composed syllabus stays **consistent with the brief** — its audience, scope, and the
   required **running example** thread the course, with no drift from `brief-min` (FR-010, SC-007).
   This is a judgment check (not linted): confirm the running example named in the brief actually
   appears as the backbone the phases build on.

### B3 — US3: divergence ask + review-ready artifact
1. **Diverging** sources (conflict on the core arc): confirm the handler **asks the directional
   question inline** (ask-moment #2, R3) rather than silently picking, and writes a `diverged`
   assessment naming the sources (SC-005).
2. **Agreeing** sources: confirm **no** question is asked and a `converged` assessment is still written
   (SC-005 — every run records the assessment).
3. Give feedback on the presented syllabus: confirm the handler **revises and re-presents** (returns
   `needs-user` again), never re-implementing 001's approval loop or freeze (FR-014).

### B4 — thin-grounding path (edge case + SC-008)
Feed near-zero reliable sources: confirm the handler **composes from mentor judgment**, flags the
course/sections `thinly-grounded`, tags every affected topic `mentor-added`, and **does not** block or
fabricate (FR-011) — `syllabus_lint.py` passes only because the thin scope is fully mentor-tagged.

### B5 — resume mid-phase (FR-018)
Set `resume_state.syllabus_subphase = research-done` and re-invoke: confirm the handler **skips
research** and resumes at composition — no repeated queries against the budget.

## What is intentionally NOT here

- No live network research, no built `course-template` — deferred to DESIGN roadmap task #5 (prove out
  shallow research on real runs); the budget value and convergence heuristic are calibrated then
  (spec Assumptions), not asserted now.
- No orchestrator / state-machine tests — those are 001's (`test_phase_walk.py`); 002 plugs into the
  seam and is validated at the seam boundary, not by re-testing the spine.
- No rubric — the syllabus is user-approved, not rubric-graded (004 owns the rubric).
