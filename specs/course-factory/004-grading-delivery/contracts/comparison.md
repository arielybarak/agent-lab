# Contract — `comparison/` (external-course analysis → rubric revisions)

**Owner:** spec 004 (FR-018/019). **Homes:** `course-factory/.claude/commands/compare-course.md` +
`course-factory/.claude/agents/comparison-analyst.md` + `course-factory/comparison/` (outputs).
**Coordinates with:** 000 (the rubric-only re-stamp path for adoption) + the `/improve-course` backlog.

## What it produces

For a well-made external course, `/compare-course` (driven by `comparison-analyst`) writes into
`course-factory/comparison/`:

1. A **`ProposedRevision`** — a proposed change to the **one** rubric (a dimension, threshold, or
   add-on), diffed `against_version` (the current rubric `VERSION`), with **cited evidence**.
2. A **`ComparisonReport`** — a per-course report feeding the **`/improve-course` backlog** (FR-018).

## Never a rival rubric (FR-019, SC-008)

- A proposal is a **file in `comparison/`**, never a live rubric. `single_rubric_lint.py` guarantees
  exactly one rubric exists (the proposal does not count as a rival).
- A proposed revision **does not auto-mutate** the live rubric. **Grading uses the current adopted
  rubric version until adoption.**

## Reuses 002's research discipline (not a third method — Assumptions)

- **Candidate selection** ("well-made"): judged with 002's **reliability-weighing** (stars are a
  green flag, not proof — 002 FR-002, Principle II/III), **not** a separate rubric for picking
  candidates.
- **Analysis process**: 002's research method — research → weigh reliability → cite → converge or
  budget-cap. Evidence in a `ProposedRevision` is cited with 002's discipline. It is not a new
  research mechanism, just a different corpus (external courses instead of one topic's sources).

## Minimal adoption protocol (FR-019)

```text
ProposedRevision(proposed)
   │  the factory maintainer reviews it against REAL course evidence (human, deliberate)
   ├─ reject  → status=rejected
   └─ approve → 000 rubric-only re-stamp (MINOR/PATCH VERSION bump, 000 Edge Cases / FR-016)
                provenance → this comparison/ proposal (000 FR-019)
                the stamp bump IS the adoption record
```

- Adoption is **narrow** (000's rubric-only path), **not** a full re-distillation, and **not** a
  silent edit. Provenance points to the `comparison/` proposal, not the reference course.

## SC mapping

SC-008 (100% of comparison outputs target the single rubric; 0 rivals; live rubric unchanged until
deliberately adopted).
