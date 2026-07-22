# Contract — Course-evaluator (course-level grading engine)

**Owner:** spec 004 (FR-006/007/008/009/010). **Home:** `course-factory/course-template/.claude/agents/course-evaluator.md`
— a **frozen template asset**, copied into every course (000 distills the shell; 004 owns the grading
behavior). Invoked by `/course-report` at delivery and available post-delivery for `/improve-course`.

## Inputs

- The **finished course**: lessons (`.md`/`.ipynb`) + `SYLLABUS.md` + `COURSE_BRIEF.md` (which names
  any requested topic add-ons + the running example).
- The **rubric** — read from the course's frozen `.claude` residue (`rubric.md`), with 004's grading
  semantics (`rubric-grading-semantics.md`).
- `SOURCES.md` — the `[Sn]` resolution target (002).

## Behavior

1. **Assemble the per-course rubric** = generic core + the add-ons `COURSE_BRIEF.md` requested. An
   unknown requested add-on is **surfaced**, not silently dropped (FR-002).
2. **Score each dimension** (agent judgment — correctness, grounding, flow, clarity, coverage, practicality,
   and any add-on). Apply the **pass predicate** via `rubric_gate.py` (`rubric-grading-semantics.md`)
   — never an average.
3. **Grounding** — run the exhaustive `[Sn]` traceability sweep (`citation-traceability.md`, over the
   shared `sn_resolve.py`); honor `mentor-added` / `thinly-grounded` (FR-008).
4. **Independent course-level verdict (FR-009)** — additionally grade **whole-arc** dimensions
   (coverage across the syllabus, flow/continuity across the arc, the running-example thread) and MAY
   return **`needs-work` even when every lesson already passed** its per-lesson gate. The course
   verdict is **not** a roll-up of per-lesson passes (SC-011).
5. **Emit the `Scorecard`** (see `data-model.md`): `rubric_version`, per-dimension scores, `wins`,
   `cleanups`, `traceability` findings, `verdict`.

## Forward-diff on already-passed gaps (FR-010, 001 FR-023)

When grading surfaces a gap in an **already-passed** artifact (a passed lesson, a frozen syllabus),
the evaluator records it as a **forward diff / `/improve-course` backlog item** (001's `DIFFS.md`
ledger). It **MUST NOT** re-open, re-flow, or re-grade a passed phase (SC-006). Delivery is
forward-only.

## Outputs

- The `Scorecard`, consumed by `/course-report` → `COURSE_REPORT.md` (`course-report.md` contract).
- `TraceabilityFinding`s and course-level gaps → 001's `DIFFS.md` / the `/improve-course` backlog.

## What this contract does NOT do

- It does **not** populate `SOURCES.md` or `FEEDBACK.md` (002 / build-time write side).
- It does **not** apply the rubric **per lesson** — that is 003's `lesson-evaluator` (same rubric,
  same predicate, different granularity). 004 does course-level grading only (FR-003).
- It does **not** gate/withhold delivery on a `needs-work` verdict — see `course-report.md`.

## SC mapping

SC-002 (core always, add-on only when requested), SC-003 (scorecard shape), SC-004 (traceability),
SC-006 (0 phase re-opens), SC-011 (independent verdict).
