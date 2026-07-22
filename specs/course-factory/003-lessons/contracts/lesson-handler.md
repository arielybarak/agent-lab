# Contract — lesson phase handler (how 003 implements 001's seam)

**Owner:** spec 003. **Consumes:** 001's `phase-seam.md` (envelope + gate-result vocabulary, the
`rubric` gate-type semantics, the round-cap ownership split), `build-progress-schema.md` (owns
`lessons[]`), `diffs-ledger.md` (forward diffs, FR-017), `course-folder.md` (lesson files,
`CALIBRATION.md`, `FEEDBACK.md`). **Consumes 004's rubric** via `rubric-gate.md`. 003 **replaces 001's
`lessons` stub** with this handler and **changes nothing in the orchestrator**.

## Input envelope consumed (orchestrator → handler)

| Field | 003's use (lesson phase) |
| :--- | :--- |
| `course_dir` | Where lesson files, `CALIBRATION.md`, `FEEDBACK.md`, `DIFFS.md` live. |
| `brief` | `audience` + assumed prior knowledge (fake-student input, FR-013), `running_example`, `lesson_format` (`.md`/`.ipynb`, 002's decision — the pool does not re-decide it), `archetype_profile` (FR-019), `modules`. |
| `prior_artifacts` | The **frozen `SYLLABUS.md`** and each **approved skeleton**, each paired with its `DIFFS.md` entries (001 FR-027, FR-007) — canonical frozen-plus-diffs reads. |
| `insights` | An authoring input; empty is valid (FR-007). |
| `resume_state` | `lessons[]` (skip terminal lessons) + `active_loop.round` (resume a mid-loop lesson at its round). Presence of `CALIBRATION.md` in `course_dir` tells the handler calibration already ran (research R8). |

## The per-lesson inner loop (the shared primitive)

For each lesson the handler runs `author-critic-primitive.md`:
1. Spawn a **fresh-context `mentor-author`** whose input is exactly the FR-007 set, built by
   `author_envelope.py` (brief, frozen syllabus + diffs, that lesson's approved skeleton + diffs, the
   **relevant** `[Sn]` entries, the insights digest, and — for any lesson beyond the first two, once
   calibration has run — `CALIBRATION.md`).
2. Spawn a **separate, author-blind `lesson-evaluator`** (evaluator envelope from
   `author_envelope.py` — the authored lesson + grading inputs, **no** author-reasoning channel, SC-002).
3. The evaluator **grades against the rubric** (per-dimension threshold, `rubric-gate.md`, FR-010) and
   runs the **exhaustive** `[Sn]` traceability check (`citation_trace.py`, FR-011). A lesson **passes**
   only if the rubric passes **and** every citation resolves; an unresolvable citation blocks the pass
   (SC-004). The author refines the **cited deltas** (FR-003), capped at 3 by 001's counter (FR-002).

## The worker pool (fan-out / fan-in) and gate-then-fan-out

The handler dispatches **only** the lessons `pool_scheduler.py` returns eligible (research R3):
- **In-flight cap** — at most `pool_width` lessons `in-progress` at once (SC-003); MVP `pool_width = 1`
  is a fully serial walk (no concurrent `lessons[]` writes to order).
- **Gate-then-fan-out** — the pool authors the **first two lessons first**, runs the fake-student
  calibration (`calibration.md`), and only then are lessons at `syllabus_index ≥ 3` eligible (FR-018,
  SC-010). **No lesson beyond the first two begins before `CALIBRATION.md` exists.**
- **Idle-on-pending-gate** — while a cap-surfaced first-or-second lesson awaits the user's
  accept-or-comment decision (001 FR-012), the pool **idles** — it does not proceed to calibration or
  fan-out on a partial/unaccepted terminal state (FR-018). This is a wait, not a skip.

## Gate result returned (handler → orchestrator)

Because the lesson phase drives many per-lesson loops behind one seam, the handler returns per the
**current** lesson's loop state, using 001's `rubric` gate-type semantics:

| Return | When | Orchestrator action (001) |
| :--- | :--- | :--- |
| `loop` | The current lesson's evaluator did not pass and `active_loop.round < 3`. | Increment the round, re-invoke (`phase-seam.md`). |
| `needs-user` | A lesson hit the cap without passing — best lesson + scorecard surfaced. | Park for the round-cap **accept-or-comment** decision (FR-012); accept → `accepted-at-cap`, comment → one extension pass. |
| `pass` | **All** lessons are terminal (`passed` or `accepted-at-cap`) and calibration has run. | Record the gate cleared, advance `current_phase` to `deliver`. |
| `failed` | An input is corrupt/inconsistent. | Halt + surface (FR-022). |

Unlike the skeleton phase, the lesson gate **is** `rubric`, so the handler **does** return `pass` once
every lesson is terminal — there is no mandatory user review of lesson content (Principle VI: correctness
is the automated gate, not the user).

**One active loop at MVP; the target-2 exception is a flagged seam item.** The `loop` return + 001's
single `active_loop = { phase, round }` model a **serial** loop. At **MVP `pool_width = 1`** exactly one
lesson is in flight, so `active_loop.round` is that lesson's round — the seam works verbatim. At
**target `pool_width = 2`** two lessons carry independent round counts a single counter cannot hold; how
per-lesson rounds are tracked is an **open item of FR-009's deferred concurrency model** (a forward-diff
extension of 001's `active_loop`, or 003-internal per-lesson rounds) — resolved when target-2 is
validated on real runs, not assumed now (research R9). No MVP FR/SC depends on it.

## `lessons[]` writes (the field 003 owns)

The handler writes each lesson's `status` to `lessons[]` via 001's `progress.py` (**never hand-edits**
the JSON block) as the lesson reaches a terminal state, **before** the pool treats it as done (FR-012,
SC-007) — persist-before-advance (build-progress-schema rule 3). Statuses: `not-started` → `in-progress`
→ `passed` | `accepted-at-cap`. 003 does **not** advance `current_phase` (rule 2).

## Calibration trigger (delegated to `calibration.md`)

When the **first two lessons reach a terminal state**, the handler runs the fake-student check **iff**
`CALIBRATION.md` is absent (research R8), fixes the confusion points in those two lessons, **re-grades**
each edited lesson (FR-014, SC-006), folds the guidance into `CALIBRATION.md`, and only then lets the
scheduler fan out the rest. Full contract in `calibration.md`.

## Forward diffs & feedback (write side)

- **Forward diff (FR-017):** a gap found in the frozen syllabus or an approved skeleton surfaces as a
  forward diff via 001's `diffs.py`, applied at the current phase — never a phase re-open, never a silent
  edit of a frozen artifact (001 FR-023, SC-008).
- **Feedback (FR-020):** durable evaluator findings are **appended** to `FEEDBACK.md`; harvest stays
  004's.

## Degradation & format guarantees

- **`.ipynb` lessons** are authored and traceability-checked in that format as decided in
  `COURSE_BRIEF.md`; `[Sn]` keys live in markdown cells and are read by `citation_trace.py`'s
  markdown-cell scan (research R7). The pool never re-decides the format.
- **Thin `SOURCES.md`** — the handler follows 002's compose-and-flag policy: compose from mentor
  judgment, flag the thin grounding, tag affected claims mentor-added, preserve those flags (FR-011);
  a syllabus gap exposed by thin grounding surfaces as a forward diff, not a silent fill.
- **Empty insights digest** — a valid input; authors proceed without it (FR-007).
- **Input-selection miss (edge case)** — when the orchestrator hands an author incomplete `[Sn]`
  entries, the evaluator MAY flag a claim that plausibly matches an *existing-but-unpassed* `SOURCES.md`
  entry as a likely **selection** miss (distinct from a genuinely ungrounded claim), so the
  input-selection step can be corrected rather than only failing the lesson (spec edge case, FR-007).
