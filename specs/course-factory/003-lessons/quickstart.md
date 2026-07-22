# Quickstart — validating the Lessons Phase

How to prove 003 works. Split the way 001/002 split: the **mechanical, 0-exception SCs** are asserted
by `pytest` over the tool layer (Part A); the **irreducibly-judgment SCs** are scenario walkthroughs
(Part B). No live run of the whole factory is needed — 000/001/004 are not yet built, so validation is
against **contracts + fixtures**, exactly as 002 validated against not-yet-built 001.

## Prerequisites

- Python **3.11**, stdlib only. `pytest` for Part A.
- Fixtures under `course-factory/tests/fixtures/`:
  - `skeletons/` — a topic-matched batch and a topic-mismatched batch.
  - `lessons/` — `fully-cited.md`, `unresolvable-sn.md`, `mentor-added.md`, `silently-ungrounded.md`,
    and `cited.ipynb` (a notebook whose `[Sn]` keys live in **markdown** cells).
  - `sources/` — a `SOURCES.md` fixture (the `[Sn]` resolution target; reuse 002's where it fits).
  - `rubric/` — a **minimal** per-dimension-threshold rubric standing in for not-yet-built 004
    (`contracts/rubric-gate.md`).
  - `brief/` — a `COURSE_BRIEF.md` with audience + assumed prior knowledge, running example, profile,
    and `lesson_format`.
  - `pool-scenarios/` — lessons-list + `pool_width` + `calibration_done` fixtures: `serial-1`,
    `parallel-2`, `pre-calibration-barrier`, `fewer-than-two`.
- No network, no subagent spawns in Part A — the tools are pure functions over fixtures.

## Part A — mechanical SCs (pytest over the tool layer)

Run: `cd course-factory && python -m pytest tests/`

| Test | Asserts | SC |
| :--- | :--- | :--- |
| `test_pool_scheduler.py::test_never_exceeds_pool_width` | over `serial-1` and `parallel-2`, the scheduler never returns more than `pool_width` lessons to hold `in-progress` at once | SC-003 |
| `test_pool_scheduler.py::test_gate_then_fan_out` | over `pre-calibration-barrier`, no lesson with `syllabus_index ≥ 3` is eligible while `calibration_done == false`; all become eligible once true | SC-010 |
| `test_pool_scheduler.py::test_fewer_than_two` | over `fewer-than-two`, the first (only) lesson is scheduled and no barrier deadlock occurs | SC-010 edge |
| `test_citation_trace.py::test_resolves_every_citation` | `fully-cited.md` passes; `unresolvable-sn.md` fails on the unresolvable key (exhaustive, not sampled) | SC-004 |
| `test_citation_trace.py::test_mentor_added_not_failed` | `mentor-added.md` passes (a mentor-added claim is not failed for lacking `[Sn]`); thin-grounding tags preserved | SC-004 |
| `test_citation_trace.py::test_silently_ungrounded_fails` | `silently-ungrounded.md` fails (a claim neither cited nor mentor-added) | SC-004 |
| `test_citation_trace.py::test_ipynb_markdown_cells` | `cited.ipynb` traces by the same method as `.md` — `[Sn]` keys in markdown cells resolve; code cells/outputs ignored | SC-004 (`.ipynb` parity, research R7) |
| `test_author_envelope.py::test_evaluator_is_author_blind` | the evaluator envelope contains the artifact + grading inputs but **no** author-reasoning field | SC-002 |
| `test_author_envelope.py::test_author_envelope_is_fr007_set` | the author envelope is exactly the FR-007 set; `CALIBRATION.md` is included **iff** the lesson index > 2 and calibration ran | SC-002 (author side), FR-007/021 |

These are the four 0-exception SCs made mechanical (research R1). The remaining SCs are either 001's
mechanics reused (SC-007 status-write via `progress.py`; SC-005 the handler's `needs-user`-only success
path; SC-008 the `diffs.py` append) or judgment (Part B).

## Part B — judgment SCs (scenario walkthroughs)

Walk each with the fixtures; these exercise the `.claude/` judgment surface that `pytest` cannot assert.

### B1 — US1: mentor-authored skeleton batch, agent loop, present-and-wait
Drive `skeleton-phase` over `brief/` + a syllabus fixture: confirm **all** skeletons are drafted in one
batch (not one interruption per lesson), the `skeleton-evaluator` checks topic-match + clarity and the
author refines the **cited deltas**, and the handler returns **`needs-user`** (never `pass`) — no
auto-advance (SC-005, SC-009). Run the topic-mismatched batch to see the evaluator flag the mismatch and
the author correct it within the cap; run a cap-hit variant to see best-batch + unresolved deltas
surfaced (FR-002).

### B2 — US2: the parallel author–critic pool graded by the rubric
Drive `lesson-phase` over approved skeletons + `sources/` + `rubric/`: confirm each lesson's author
starts **fresh-context** with the FR-007 inputs, the `lesson-evaluator` never receives author reasoning
(SC-002), at most `pool_width` pairs run (SC-003), each lesson is graded per-dimension-threshold
(`rubric-gate.md`) and passes only if the rubric passes **and** every `[Sn]` resolves (SC-004), and each
terminal lesson's status is written to `lessons[]` before it is done (SC-007). Run
`unresolvable-sn.md` to see the traceability failure block the pass.

### B3 — US3: once-per-course fake-student calibration + gate-then-fan-out
With the first two lessons terminal, run the fake-student check: confirm the subagent gets **only**
audience + assumed prior knowledge + the two lessons, reports confusion points, the points are fixed in
the two lessons **and** each edited lesson is **re-graded** (SC-006), the guidance is folded into
`CALIBRATION.md`, and only **then** do lessons at index ≥ 3 begin (SC-010). Confirm the check runs
**exactly once** — re-invoking with `CALIBRATION.md` present does not re-run it (SC-006, research R8).

### B4 — no-exercise and fewer-than-two fallbacks (edge cases)
Run the fake-student over a lesson with no exercise (read-and-report-only fallback, still folds in) and
over a one-lesson course (runs once on what exists, no deadlock).

### B5 — forward diff on an earlier-artifact gap (SC-008)
Drive a lesson whose authoring reveals a syllabus gap: confirm a **forward diff** is appended via 001's
`diffs.py` and the lesson is authored against it — the frozen syllabus is **never** edited and the
syllabus phase is **never** re-opened (FR-017, honors 001 FR-023).

### B6 — resume mid-phase (FR-012/021)
Kill the run after one lesson is `passed` and after `CALIBRATION.md` is written; restart and confirm the
handler skips the terminal lesson (from `lessons[]`), skips the calibration (from `CALIBRATION.md`
presence), and resumes the pool — no lost state, no double calibration.

## What is intentionally NOT here

- **The rubric's contents / dimensions / thresholds** — 004's (`rubric-gate.md` consumes only the pass
  predicate + the grounding check). Part B uses a fixture rubric.
- **Whether a claim is *true*** — the traceability check verifies *tracing*, not truth (research R2);
  truth is the mentor/evaluator's judgment.
- **The state-machine mechanics, the cap counter, the freeze, the park** — 001's; 003 validates only
  that it returns the right gate result and writes its owned `lessons[]` field.
- **`pool_width = 2` live concurrency correctness** — the scheduler is tested at width 2, but the
  target-2 concurrency model is validated on **real runs** (DESIGN "Open decisions"); MVP ships serial.
