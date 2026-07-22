# Contract — the once-per-course fake-student calibration & `CALIBRATION.md`

**Owner:** spec 003. **Consumed by:** the lesson handler (`lesson-handler.md`) and, indirectly, the
pool scheduler (`CALIBRATION.md` presence is the fan-out barrier, research R3/R8). This contract covers
the fake-student trigger (FR-013), the fix-and-fold-in with mandatory re-grade (FR-014), the
once-per-course guarantee (FR-015), and the persisted `CALIBRATION.md` shape (FR-021).

## Trigger (FR-013, Clarifications)

The check fires when the **first two lessons reach a terminal state** — `passed` **or**
`accepted-at-cap` (cap-surfaced-and-user-accepted), in **syllabus order**. It keys off *terminal state*,
not `passed` alone, so it cannot deadlock on a lesson that never passes. Guarded by **`CALIBRATION.md`
presence**: the check runs **iff `CALIBRATION.md` does not yet exist** (research R8), giving the
once-per-course guarantee across session boundaries (a resumed session sees the file and skips the
check — honors 001's disk-only resume rule, FR-021 cites 001 FR-018).

**Idle-on-pending, not skip (FR-018).** While a cap-surfaced first-or-second lesson awaits the user's
accept-or-comment decision, the pool **idles** — the calibration does not fire on a partial/unaccepted
terminal state. This is a wait; the check fires once both of the first two lessons are genuinely
terminal.

## The fake-student subagent (FR-013)

A **fresh** subagent whose input is **only**:
- the brief's **audience + assumed prior knowledge**, and
- the **first two terminal lessons** (their content).

No author reasoning, no other course context, no rubric. It **reads** the two lessons and **attempts
the exercise**, reporting concrete **confusion points** (undefined terms, too-fast steps).

**No-exercise fallback (edge case).** If a lesson has no exercise (possible under some profiles/modules),
the subagent falls back to **read-and-report-confusion only** — it reads and reports without attempting
an exercise; the calibration still fixes and folds in the points (FR-014).

**Fewer-than-two-lessons (edge case).** If the course has fewer than two lessons, the check runs **once**
on the lesson(s) that exist rather than being skipped; it still runs at most once and never blocks
waiting for a second lesson that will never exist (FR-013).

## Fix, fold-in, and the MANDATORY re-grade (FR-014, SC-006)

1. **Fix** the confusion points **in the two lessons**.
2. Because this **edits an already-terminal (often already-`passed`) lesson**, each edited lesson is
   **re-graded against the rubric** (`rubric-gate.md`, FR-010) **before the calibration is considered
   complete** — a fix MUST NOT silently regress a previously-passed dimension (SC-006: **0** unregraded
   edits to a passed lesson).
3. If a re-grade **fails**, the edited lesson **re-enters** the shared author→critique→refine primitive
   (`author-critic-primitive.md`) under a **fresh** 3-round cap (mirrors 001's change-request pattern),
   until it is terminal again.
4. **Fold** the confusion points into the **drafting guidance** for **every remaining lesson** — this is
   the calibration's whole purpose (it calibrates the explanation format once, not per lesson, FR-015).

## `CALIBRATION.md` — persisted output (FR-021)

Written **once**, when the check (including all re-grades) completes. Human-readable Markdown in
`course_dir`. Its **presence** is (a) the once-per-course guard and (b) the scheduler's fan-out barrier.
Required sections:

| Section | Content |
| :--- | :--- |
| `## Audience snapshot` | the audience + assumed prior knowledge the fake-student was given (FR-013) |
| `## Lessons probed` | the two lesson ids + whether an exercise was attempted or the read-only fallback was used |
| `## Confusion points` | the concrete findings (undefined terms, too-fast steps) (FR-014) |
| `## Fixes applied` | how each confusion point was fixed in the two lessons **+ the re-grade result per edited lesson** (SC-006) |
| `## Drafting guidance` | the explanation-format guidance folded into every remaining lesson's author input (FR-014/021) |

Every author subagent for a lesson beyond the first two reads `CALIBRATION.md` as an FR-007 input
(built into the author envelope by `author_envelope.py`). A session dying post-calibration resumes from
this file rather than losing the guidance (FR-021).

## Ordering guarantee (SC-010, restated at this seam)

The scheduler treats `CALIBRATION.md` presence as `calibration_done`. Until it exists, **no lesson at
`syllabus_index ≥ 3` is eligible** (gate-then-fan-out, FR-018) — so the calibration provably completes
before any remaining lesson is authored, and every remaining lesson is authored **with the calibration
folded in** (SC-006: folded into 100% of remaining lessons; SC-010: 0 lessons beyond the first two
begun before calibration).
