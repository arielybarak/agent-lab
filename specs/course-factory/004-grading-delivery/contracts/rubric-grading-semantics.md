# Contract — Rubric grading semantics (the layer 004 fills into 000's shape)

**Owner:** spec 004 (Principle VIII — the one rubric). **Producer side** of 003's
`rubric-gate.md` (which is 003's *consumption* contract). **Consumers:** 003's `lesson-evaluator`
(per-lesson gate), 004's `course-evaluator` (course-wide engine). **Enforced by:** `rubric_gate.py`
(the pass predicate) + `single_rubric_lint.py` (the single-rubric invariant).

This file defines the **grading semantics** 004 layers onto the two-layer **shape** spec 000 owns
(000 FR-013/015). 000 gives the dimensions their names + the version identity; **004 gives them their
numbers and the gate rule.**

## What 000 owns vs. what 004 owns

| Owned by 000 (the shape) | Owned by 004 (the semantics) |
| :--- | :--- |
| The two-layer structure (core + add-on slots) | The concrete `scale` (e.g. `1..5`) |
| The five core-dimension **names** (FR-013) | Each dimension's `threshold` |
| The semver `VERSION` = the rubric's identity | The `weight` (reporting only, **not** a gate input) |
| The provenance record (FR-019) | The **hard-gate rule** (pass iff every dim ≥ threshold) |

## The pass predicate (`rubric_gate.py`)

```text
rubric_gate(scores: {dimension: score}, rubric) -> PassResult
  passed = all(scores[d] >= rubric.threshold[d] for d in rubric.dimensions)   # core + requested add-ons
  per_dimension = { d: {score, threshold, cleared: scores[d] >= threshold} }
  return PassResult(passed, per_dimension)
```

**Invariants:**

1. **No aggregate masking (SC-010).** There is no average / weighted sum that lets a below-threshold
   dimension pass. A strong dimension MUST NOT mask a failing one. `weight` is used only to rank
   wins/cleanups in the scorecard, never in `passed`.
2. **Every requested add-on is a gated dimension.** The per-course rubric = core + the add-ons
   `COURSE_BRIEF.md` requested. An add-on the rubric has no definition for is **surfaced** (a distinct
   error), not silently dropped (FR-002).
3. **Scores retained.** `per_dimension` is carried into the scorecard even when `passed` is true
   (FR-004).
4. **One predicate, two consumers (SC-009).** 003's lesson gate and 004's course-evaluator call this
   **same** function — there is not a second copy of "every dim ≥ threshold." (003's `rubric-gate.md`
   already names 004 the owner of the dimensions/thresholds/scale.)

## Reproducibility

The `scale`, per-dimension `threshold`s, and `weight`s are **recorded alongside the rubric version**
(FR-004/005) so a course's pass/fail is reproducible against the exact thresholds that graded it. A
course records which rubric `VERSION` graded it (see `course-report.md`).

## Single-rubric invariant (`single_rubric_lint.py`)

Enumerate every "quality definition" in the factory (the rubric asset; any file claiming to define
pass/fail dimensions). **Exactly one** must exist — 0 rivals (SC-001). A `comparison/` proposal is a
*proposal file*, not a rubric, and does not count as a rival (SC-008).

## Fixture stand-in (until 000 ships)

Validated against `tests/fixtures/rubric/` — the **same** minimal rubric fixture 003 defines (a
handful of core dimensions each with a threshold + one requested add-on). When 000 lands its
rubric-shape asset and 004 fills the semantics, the fixture is replaced by the real `rubric.md`; the
predicate is unchanged.
