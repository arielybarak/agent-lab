# Contract — Citation traceability (004's CANONICAL grounding check)

**Owner:** spec 004 (FR-007 — "the factory's **canonical** citation/grounding contract; 002 and 003
apply it at their own granularity rather than re-deriving it"). **Implemented by:** the **shared**
`sn_resolve.py` primitive (spec 003 builds it; 002/003/004 import it — "one resolver, not three").
**Consumers:** 002 (syllabus topic grounding), 003 (per-lesson gate), 004 (course-evaluator).

004 owns the **contract** (the semantics below). It does **not** author a second resolver — the
course-evaluator runs the shared `sn_resolve.py` **course-wide** via a thin course-scoped module,
`course_trace.py` (the exact analogue of 003's per-lesson `citation_trace.py`), R2.

## The rule (tracing, not truth)

For **every** `[Sn]` key in the course (all lessons + `SYLLABUS.md` — exhaustive, not sampled):

1. **Resolve** the key against the course's `SOURCES.md` (002's `sources-schema.md`). Resolution is a
   cheap **mechanical lookup** — that is why it is exhaustive, not a spot-check (FR-007, SC-004).
2. An **unresolvable** key (no such `[Sn]` entry, or a `SOURCES.md` entry flagged `unresolvable`
   after the fact) → a **`TraceabilityFinding`** in the scorecard.
3. This verifies **that a claim maps to a real source** — it does **not** verify the claim is *true*.

## Mentor-added / thin-grounding (002's compose-and-flag policy)

- A claim explicitly marked **`mentor-added`** MUST NOT be flagged merely for lacking an `[Sn]`
  (FR-008, 002 FR-011). Mentor judgment the sources did not supply is a valid, non-fabricated claim.
- A **`thinly-grounded`** flag is **preserved** in the scorecard, never re-presented as if the claim
  were sourced. 004 reports thin grounding; it does not launder it.

## Course scope vs. per-lesson scope

| | 003 (`citation_trace.py`) | 004 (`course_trace.py`) |
| :--- | :--- | :--- |
| Granularity | one lesson (gate) | the whole course (delivery grade) |
| Resolver | `sn_resolve.py` (shared) | `sn_resolve.py` (shared) — **same** |
| Extraction | `.md` prose + `.ipynb` markdown cells (R7) | reuses the same extraction; sweeps all lessons + syllabus |
| On unresolvable | hard gate failure (lesson doesn't pass) | `TraceabilityFinding` in the scorecard → forward diff / `/improve-course` at delivery (FR-010) — **not** a phase re-open |

The delta at course scope is only the **loop over the course's files** — not a second grounding rule.

## SC mapping

- **SC-004** — 100% of unresolvable `[Sn]` flagged; 0 mentor-added claims failed for missing
  grounding; thin-grounding flags preserved.

## Fixture stand-in

Validated against 003's/002's shared `tests/fixtures/{sources,lessons}/` (fully-cited,
`unresolvable-[Sn]`, `mentor-added`, `silently-ungrounded`, and an `.ipynb` whose keys live in
markdown cells). 004 adds no new resolver fixture — it exercises the shared one course-wide.
