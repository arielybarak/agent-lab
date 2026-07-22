# Contract — skeleton phase handler (how 003 implements 001's seam)

**Owner:** spec 003. **Consumes:** 001's `phase-seam.md` (envelope + gate-result vocabulary, the
`agent-then-user` gate-type semantics, the round-cap ownership split), `build-progress-schema.md`
(reads `active_loop`; owns no field in this phase — skeletons are a batch, not per-item `lessons[]`),
`diffs-ledger.md` (forward diffs, FR-017), `course-folder.md` (where the skeleton batch is written,
`FEEDBACK.md` append). 003 **replaces 001's `skeletons` stub** with this handler and **changes nothing
in the orchestrator**.

## Input envelope consumed (orchestrator → handler)

| Field | 003's use (skeleton phase) |
| :--- | :--- |
| `course_dir` | Where the per-lesson skeleton batch is written; `FEEDBACK.md` / `DIFFS.md` live here. |
| `brief` | Reads `topic_scope`, `audience`, `running_example`, `archetype_profile` (scaffolding depth + advisory-checkpoint placement, FR-019), `modules`. |
| `prior_artifacts` | The **frozen `SYLLABUS.md` paired with its `DIFFS.md` entries** (001 FR-027) — the canonical read, never the frozen artifact alone. |
| `insights` | Read as an authoring input; **empty/missing is valid** (FR-007's read discipline). |
| `resume_state` | `active_loop.round` for this phase — the handler resumes the batch loop at the recorded round (round-cap counter is 001's). |

The handler never inspects orchestrator-owned state beyond the envelope.

## What the handler does

1. **Draft ALL skeletons in one batch** as a domain mentor (FR-004) — never one interruption per
   lesson, never by parroting sources. A **single batch-level** author→critique→refine loop: one
   `mentor-author` over the whole set, one `skeleton-evaluator` over the batch. The two-pairs-in-flight
   worker pool is **lesson-only** and MUST NOT be used here (FR-004, Clarifications).
2. **Run the shared primitive** (`author-critic-primitive.md`): the evaluator checks every skeleton for
   (a) topic-match and (b) clarity/simple-language (FR-005); the author refines the **cited deltas**
   (FR-003). Capped at 3 rounds by 001's counter (FR-002).
3. On **convergence** (all skeletons pass) *or* **cap-hit** (best batch + unresolved deltas, FR-002),
   **present the batch review-ready** and return `needs-user` — **never** auto-advance (FR-006, SC-005).

## Gate result returned (handler → orchestrator)

| Return | When | Orchestrator action (001) |
| :--- | :--- | :--- |
| `loop` | The evaluator did not pass every skeleton and `active_loop.round < 3`. | Increment the round, re-invoke the handler (`phase-seam.md`). |
| `needs-user` | The batch is review-ready — all skeletons passed, **or** the cap was hit and the best batch + deltas are surfaced. | Park for the **blocking** user scan (FR-024); on a change request re-invoke with a **fresh** 3-round cap, then re-park. |
| `failed` | An input is corrupt/inconsistent (malformed state block, unreadable syllabus). | Halt + surface (FR-022); 003 never silently repairs. |

**003 does NOT return `pass` in the skeleton phase** — the gate is `agent-then-user`; only the *user's*
scan (mediated by 001) clears it after the agent loop passes. This is the mechanical guarantee behind
SC-005: the handler's success path is `needs-user`, so there is no code path that advances to lessons
without a recorded user approval.

## The change-request channel (re-scan after user edits)

On a user change request the orchestrator re-invokes the handler with a **fresh** `active_loop`
(cap reset to 3, per `phase-seam.md` § `agent-then-user`). The handler reads the user's scan comments
from **`FEEDBACK.md`** in `course_dir` (the same driver-maintained channel 002 reads and 001 FR-026
writes — ratified by the seam, not a private side channel), re-runs the batch loop against them, and
re-returns `needs-user` for another scan.

## Forward diffs & feedback (write side)

- **Forward diff (FR-017):** if drafting a skeleton reveals a gap in the **frozen syllabus**, the
  handler appends a forward diff via 001's `diffs.py` and drafts against the diff — it **never** reopens
  the syllabus phase or edits the frozen artifact (honors 001 FR-023, SC-008).
- **Feedback (FR-020):** a durable evaluator finding worth carrying forward (not a delta already
  resolved within the cap) is **appended** to `FEEDBACK.md`. Harvest into `insights/` stays 004's
  user-invoked path.

## Ordering & degradation guarantees

- **Whole batch before evaluation** — the handler drafts every skeleton before the evaluator runs
  (Principle VII, FR-004); it never interrupts the user per skeleton.
- **Profile-respecting, primitive-invariant** — scaffolding depth + advisory-checkpoint placement track
  the selected profile (FR-019); the shared primitive and its cap are unchanged by profile.
- **Pre-return check** — before returning `needs-user`, the handler confirms the batch is complete (one
  skeleton per syllabus lesson) and each carries the evaluator's verdict or, at the cap, its unresolved
  delta; an incomplete batch is a defect to fix in-phase, not surfaced to the user.
