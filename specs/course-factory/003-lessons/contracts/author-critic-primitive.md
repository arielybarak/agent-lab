# Contract — the shared author → critique → refine primitive

**Owner:** spec 003. **Used by:** the skeleton handler (batch mode) and the lesson handler (per-lesson
mode). This is the **single shared** primitive FR-001 mandates — authored **once** as the
`author-critic-loop` skill, invoked by both phases (research R6). The two phases differ only in the
*driver* (batch loop vs. worker pool) and the evaluator's *checklist*; the loop body here is identical.

## The loop

```text
round r (1..3, counter owned by 001's active_loop):
  1. AUTHOR produces (r=1) or refines (r>1) the artifact from the author envelope.
  2. EVALUATOR (author-blind) grades the artifact against its checklist and emits CITED DELTAS.
  3. If the evaluator PASSES → return pass-for-this-artifact.
     Else if r < 3 → AUTHOR refines the cited deltas (targeted revision, NOT a restart, FR-003) → r+1.
     Else (r == 3, no pass) → emit best-effort artifact + unresolved deltas / scorecard (FR-002).
```

The **round counter and cap-at-3 are 001's** (`phase-seam.md` § Round-cap ownership); this primitive
owns what one round *does*. On the cap it produces the best-effort artifact + delta report; **001**
surfaces the accept-or-comment decision (its FR-012) — this primitive never asks the user itself.

## The two envelopes (built by `author_envelope.py`, SC-002)

### Author envelope (fresh context, FR-007)
The author subagent's **entire** input — no other course context:

| Item | Notes |
| :--- | :--- |
| `COURSE_BRIEF.md` | topic/scope, audience, running example, profile, `lesson_format` |
| frozen `SYLLABUS.md` + its `DIFFS.md` entries | canonical frozen-plus-diffs read (001 FR-027) |
| the artifact's approved skeleton + its diffs | *(lesson mode; the batch author drafts skeletons themselves in skeleton mode)* |
| the **relevant** `[Sn]` entries from `SOURCES.md` | selected by the orchestrator, not the full file (Assumptions) |
| the `insights/` digest | may be empty (FR-007) |
| `CALIBRATION.md` | **only** for a lesson beyond the first two, once calibration has run (FR-007/021) |

The author is a **domain mentor**: sources inform, never dictate (FR-004/016).

### Evaluator envelope (author-blind, FR-008)
The evaluator subagent's input:

| Item | Notes |
| :--- | :--- |
| the authored artifact | the skeleton batch (skeleton mode) or the lesson (lesson mode) |
| the grading inputs | the checklist (below), `SOURCES.md` for `[Sn]` resolution, the rubric (lesson mode) |
| its own prior critiques for this artifact | to confirm cited deltas were addressed (Assumptions — artifact history, not author reasoning) |

**MUST NOT contain the author's private reasoning channel** (SC-002). The evaluator is a **separate
fresh-context spawn**; blindness is structural — the author's chain-of-thought is never in the
evaluator envelope by construction (research R4). Honesty boundary: the builder guarantees the
evaluator's *input* is author-blind; it does not scrub what an author embeds *in the artifact itself*
(that is the artifact, which the evaluator is meant to read).

## The evaluator checklist (the phase-specific parameter)

| Phase | Checklist | FR |
| :--- | :--- | :--- |
| Skeletons | (a) topic-match to the lesson, (b) clarity / simple language | FR-005 |
| Lessons | rubric grade (per-dimension threshold, `rubric-gate.md`) **+** exhaustive `[Sn]` traceability (`citation_trace.py`) | FR-010/011 |

The checklist is the **only** phase difference in the evaluation step; the loop body, the cap handling,
and the two-envelope split are identical across phases (FR-001).

## Cited-delta format (what a round must produce to converge)

The evaluator's critique is a list of **cited deltas** — each a specific, addressable revision request
tied to a location in the artifact and (where grounding is at issue) to the `[Sn]` key or rubric
dimension at fault. A round **addresses the cited deltas** (FR-003); it does not rewrite the artifact
from scratch. This is what makes convergence-within-3-rounds achievable and is why the loop is capped
rather than unbounded (FR-002, SC-001).

## Feedback capture (FR-020)

When a critique surfaces a **durable** finding worth carrying forward — not merely a delta the author
already resolved within the cap — the phase appends it to `FEEDBACK.md`. This is 003's write-side of
Principle XII; it is a property of the *phase handler* invoking this primitive, recorded here because it
is triggered by the evaluator's critique.
