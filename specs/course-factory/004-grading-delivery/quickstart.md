# Quickstart — validate Grading & Delivery (spec 004)

How to prove each user story works end-to-end **without a live pipeline**, using the shared fixtures
(003's `tests/fixtures/{rubric,sources,lessons}/`, reused) plus the 004-specific fixtures
(`course/`, `feedback/`, `external-course/`). Two parts: **Part A** — the deterministic tools
(mechanical SCs, unit-asserted); **Part B** — the agent-judgment surfaces (scenario SCs, walked).

Prerequisites: Python 3.11 (stdlib only), `pytest`. Run from `course-factory/`.

---

## Part A — Mechanical SCs (`pytest`)

```bash
cd course-factory
python -m pytest tests/test_rubric_gate.py tests/test_single_rubric_lint.py \
                 tests/test_course_trace.py tests/test_harvest.py -q
```

| Test | Asserts | SC |
| :--- | :--- | :--- |
| `test_rubric_gate.py::test_all_clear_passes` | every dimension ≥ its threshold → `passed=True`; per-dim scores retained | SC-010 |
| `test_rubric_gate.py::test_one_below_fails_despite_strong_others` | a single below-threshold dim → `passed=False` even when others max out (**no aggregate masking**) | SC-010 |
| `test_rubric_gate.py::test_requested_addon_is_gated` | a requested add-on dim is gated like a core dim; an **unknown** requested add-on is **surfaced**, not dropped | SC-002 |
| `test_single_rubric_lint.py::test_exactly_one_rubric_passes` | one rubric asset → lint passes | SC-001 |
| `test_single_rubric_lint.py::test_planted_rival_fails` | a second quality-definition file → lint **fails**; a `comparison/` proposal file does **not** count as a rival | SC-001/008 |
| `test_course_trace.py::test_every_citation_resolved` | over the **shared** `sn_resolve`, an unresolvable `[Sn]` anywhere in the course is flagged (exhaustive, not sampled) | SC-004 |
| `test_course_trace.py::test_mentor_added_not_failed` | a `mentor-added` claim is **not** flagged for lacking `[Sn]`; `thinly-grounded` flags preserved | SC-004 |
| `test_harvest.py::test_empty_feedback_is_noop` | an empty `FEEDBACK.md` harvests as a **no-op**, not an error | SC-007 |
| `test_harvest.py::test_two_courses_no_clobber` | harvesting course B does not overwrite course A's insights (append-only) | SC-007 |

**Same-predicate check (SC-009).** `test_rubric_gate.py` is imported/exercised by both 003's
lesson-gate tests and 004's course tests — the pass predicate is one function, not two. (When 003's
lesson-evaluator adopts `rubric_gate.py`, this becomes a shared import; until then, both target the
identical fixture rubric so the definitions cannot diverge.)

---

## Part B — Scenario SCs (agent-judgment surfaces, walked)

These exercise the `.claude/` surfaces against fixtures. They are **walks**, not unit assertions —
the judgment (dimension scores, verdict, distillation, comparison) is the agent's; the fixture pins
the *expected shape of the outcome*.

### B1 — Course-evaluator emits a scorecard (SC-003) · US2

Run `course-evaluator` over `tests/fixtures/course/` (a finished course). **Expect:** a `Scorecard`
with per-dimension scores, `wins`, `cleanups`, `traceability` (empty here), and a `verdict`.

### B2 — Independent course-level verdict (SC-011) · US2

The `course/` fixture has **every lesson passing** but **incomplete arc coverage** (a syllabus topic
never taught). **Expect:** `verdict = needs-work` *even though no lesson failed* — the course-level
grade is independent, not a roll-up. Confirm the gap is recorded as a **forward diff / `/improve-course`
item** (001's `DIFFS.md`), **not** a phase re-open (SC-006).

### B3 — `COURSE_REPORT.md` generated + distinct from `FEEDBACK.md` (SC-005) · US2

Run `/course-report` on the scorecard. **Expect:** `COURSE_REPORT.md` with rubric scores + verdict +
**rubric version**; it reads as a **quality report to the user**, distinct from `FEEDBACK.md`. A
`needs-work` verdict is **delivered as-is**, never withheld.

### B4 — Harvest compounds `insights/` (SC-007) · US3

Run `/harvest-feedback` on `tests/fixtures/feedback/populated`. **Expect:** every critique
**represented** (distilled) in `insights/<theme>.md`, dated + sourced to the course; re-running is
dedupe-safe. Run `/insight-capture` — one insight added on demand. Confirm **nothing** harvested
until invoked (no automatic trigger).

### B5 — `comparison/` proposes a revision, never a rival (SC-008) · US4

Run `/compare-course` on `tests/fixtures/external-course/`. **Expect:** a `ProposedRevision` targeting
the **one** rubric (diffed against the current version) + a per-course `/improve-course` report;
`single_rubric_lint.py` still passes (**0 rivals**); the live rubric is **unchanged** until a revision
is deliberately adopted (re-stamp via 000's rubric-only path).

---

## What "done" looks like

- **Part A green** — the four 0-exception SC clusters (SC-001/004/007/008/009/010) are mechanically
  guaranteed.
- **Part B walked** — the scorecard, the independent verdict, the report, the harvest, and the
  comparison behave as their contracts specify.
- **No live pipeline required** — every check runs against fixtures; the real 000 rubric asset,
  002's `SOURCES.md`, and 003's `sn_resolve.py` replace their fixtures/imports when those specs' build
  slots land, with the predicates and contracts unchanged.
