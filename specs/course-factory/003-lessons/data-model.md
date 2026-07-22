# Phase 1 Data Model — Lessons Phase

003 owns **no new persistent state schema of its own** except `CALIBRATION.md` — its authoritative
runtime state (`lessons[]`, `active_loop`) lives in 001's `BUILD_PROGRESS.md`, and its content
artifacts (skeletons, lesson files) are shaped by 000's template + 002's format decision. This
data-model therefore describes: the **entities** 003 reads and produces, the **lesson lifecycle** it
drives inside 001's `lessons` phase, the **worker-pool state** the scheduler reasons over, the
**`CALIBRATION.md`** shape 003 does own, and the **validation rules** the tool layer enforces. Field
schemas 001 owns are referenced, not restated (see `contracts/`).

## Entities

### Skeleton (batch artifact; the skeleton phase's output)
A per-lesson plan. Drafted **all at once, in one batch** as a domain mentor (FR-004), checked for
(a) topic-match to its lesson and (b) clarity / simple language (FR-005). One skeleton per syllabus
lesson. The batch is presented review-ready; 001's blocking scan (FR-024) records approval. 003 does
not define the skeleton's internal format beyond "matches its lesson topic, reads clearly" — the
template (000) shapes it.

### Lesson (headline output; the lesson phase's product)
A full lesson in the decided format (`.md` / `.ipynb`, 002's decision in `COURSE_BRIEF.md`). Graded
against 004's rubric (FR-010) and grounded by `[Sn]` citations or explicit mentor-added marks (FR-011).
Threads the brief's running example (Principle X). Terminal state = `passed` or `accepted-at-cap`.

### Author subagent (fresh context)
Drafts/refines one skeleton batch **or** one lesson from a **fixed input set** (FR-007), carrying no
cross-lesson context. Authored as a domain mentor — sources inform, never dictate (FR-004/016). One
persona (`mentor-author`) invoked in batch mode (all skeletons) or per-lesson mode.

### Evaluator subagent (author-blind)
Critiques an artifact against its **checklist** and never sees the author's private reasoning (FR-008,
SC-002). Two checklists over one blindness contract:
- **skeleton-evaluator** — topic-match + clarity/simple-language (FR-005).
- **lesson-evaluator** — rubric grade (per-dimension threshold, `rubric-gate.md`) + **exhaustive**
  `[Sn]` traceability (FR-010/011).
May re-read the artifact and its own prior critiques (to confirm cited deltas were addressed); this is
artifact history, not author reasoning (Assumptions).

### Author–critic pair
One author + one evaluator running the shared primitive over a single artifact for up to 3 rounds.

### Worker pool
The fan-out / fan-in orchestration keeping **at most `pool_width`** pairs in flight over the lesson set
(FR-009). `pool_width` configurable: MVP = 1 (serial), target = 2. State is derived from `lessons[]` +
`CALIBRATION.md` presence, not a separate store (research R3).

### Author → critique → refine primitive (the shared loop)
Author produces/refines → evaluator emits **cited deltas** → author refines the deltas (targeted, not a
restart — FR-003) → repeat until pass or cap. Authored **once** (`author-critic-loop`), both phases
drive it (FR-001, research R6). See `contracts/author-critic-primitive.md`.

### Round cap (owned by 001, honored here)
Hard limit of **3** refine rounds. The counter (`active_loop.round`) and cap-at-3 enforcement are
001's (`phase-seam.md` § Round-cap ownership); 003 owns the round *body* and, on the cap, emits the
best-effort artifact + its unresolved deltas / scorecard (FR-002) for 001 to surface. **At MVP
`pool_width = 1`** (and for the single batch-level skeleton loop) exactly one loop is active at a time,
so 001's single `active_loop` counter is authoritative verbatim. **At target `pool_width = 2`**, two
lessons carry independent round counts that a single `{ phase, round }` cannot hold — an explicit open
item of FR-009's deferred concurrency model, resolved (schema forward-diff to 001 **or** 003-internal
per-lesson rounds) only when target-2 lands; it affects **no** MVP FR/SC (research R9).

### Rubric (consumed, owned by 004)
The lesson gate. 003 consumes it as pass/fail (per-dimension threshold) and MUST NOT redefine its
contents (FR-010). Represented here by the consumption contract `contracts/rubric-gate.md` + a fixture
until 004 ships it.

### `[Sn]` citation & Traceability check
A claim's pointer into `SOURCES.md`. **Every** citation is resolved (not sampled) because resolution is
a cheap mechanical lookup (FR-011, SC-004); `citation_trace.py` is the canonical resolver
(research R2), reading `.md` prose and `.ipynb` markdown cells alike (research R7). Verifies **tracing,
not truth**.

### Fake-student subagent + Confusion points + Calibration
The once-per-course learnability probe: a fresh subagent given **only** the brief's audience + assumed
prior knowledge and the first two terminal lessons (FR-013). Its confusion points are fixed in those
two lessons and folded into the drafting guidance for the rest (FR-014); persisted to `CALIBRATION.md`
(FR-021). Runs at most once (FR-015), guarded by `CALIBRATION.md` presence (research R8).

### Drafting guidance
The shared explanation-format guidance lesson authors receive; updated **once** by the calibration and
carried in `CALIBRATION.md`. Author subagents for lessons beyond the first two read it (FR-007/021).

### Read dependencies (not produced here)
- **`COURSE_BRIEF.md`** — topic/scope, audience + assumed prior knowledge, running example,
  `archetype_profile`, `modules`, `lesson_format` (002's augmentation). Read only.
- **Frozen `SYLLABUS.md` + its `DIFFS.md` entries** — the canonical syllabus read (001 FR-027); never
  the frozen artifact alone.
- **Approved skeleton + its diffs** — once the lesson phase begins, the skeleton is a gated artifact;
  read frozen-plus-diffs (FR-007).
- **`SOURCES.md`** — the `[Sn]` resolution target (002's `sources-schema.md`); mentor-added /
  thin-grounding tags honored (FR-011).
- **`insights/` digest** — cross-course learnings; may be empty, a valid input (FR-007).
- **Selected archetype profile** — 000's mechanism, 001's overlay decision; shapes scaffolding depth +
  advisory-checkpoint placement (FR-019) without touching the primitive or the rubric gate.

### Write side (produced / appended here)
- **`lessons[]`** in `BUILD_PROGRESS.md` — per-lesson status, via `progress.py` (FR-012). Owned field
  per `build-progress-schema.md`; 003 never advances `current_phase`.
- **`CALIBRATION.md`** — the calibration output (FR-021). 003 owns this file.
- **`FEEDBACK.md`** — durable evaluator findings **appended** (FR-020); harvest into `insights/` stays
  004's user-invoked path.
- **`DIFFS.md`** — forward diffs on earlier-artifact gaps, via 001's `diffs.py` (FR-017); 003 never
  mutates a frozen artifact.

## The lesson lifecycle (inside `current_phase == lessons`)

Per-lesson `status` values are 001's (`build-progress-schema.md`): `not-started` · `in-progress` ·
`passed` · `accepted-at-cap`. 003 drives the transitions; 001's `progress.py` enforces their legality.

```text
                 scheduler marks eligible + author spawned
   not-started ───────────────────────────────────────────▶ in-progress
                                                                 │
                          author→critique→refine (shared primitive, 001's cap counter)
                                                                 │
                     ┌───────────── evaluator passes (rubric ✓ + every [Sn] resolves) ──────────────┐
                     ▼                                                                                │
                  passed  ◀── re-grade ✓ (calibration edit, FR-014) ──┐                               │
                     │                                                │                               │
   (write lessons[] before "done")                                   │                               │
                     │                                    calibration edits lesson 1/2 (FR-014)       │
                     │                                    → re-enter primitive, FRESH cap             │
                     │                                                ▲                               │
                     │                                                └── re-grade ✗ ─────────────────┘
                     │
        cap reached without pass ──▶ emit best artifact + delta (FR-002) ──▶ 001 surfaces accept-or-comment (FR-012)
                                                                                   │
                                                        user accepts ──▶ accepted-at-cap  (terminal, "done")
                                                        user comments ─▶ one extension pass (001), then terminal
```

Rules:
1. A lesson becomes eligible only when the **scheduler** returns it (SC-003 in-flight cap; SC-010
   pre-calibration barrier for index ≥ 3).
2. A lesson's `status` is written to `lessons[]` **before** the pool treats it as done (FR-012,
   SC-007) — persist-before-advance (001's rule 3).
3. A lesson **passes** only if the rubric passes **and** every `[Sn]` in it resolves (FR-010/011) —
   an unresolvable citation blocks the pass (SC-004).
4. `passed` and `accepted-at-cap` are both **terminal ("done")** — the fake-student trigger keys off
   *terminal state*, not `passed` alone (FR-013, Clarifications).
5. A calibration edit to an already-`passed` lesson (FR-014) forces a **re-grade**; a failing re-grade
   re-enters the primitive under a **fresh** cap (mirrors 001's change-request pattern).

## The worker-pool state (what the scheduler reasons over)

`pool_scheduler.py` is a **pure function** — no owned state; it reads `lessons[]` + a
`calibration_done` boolean (derived from `CALIBRATION.md` presence) + `pool_width`:

| Input | Source | Role |
| :--- | :--- | :--- |
| `lessons[]` (each `{ id, status }`) | `BUILD_PROGRESS.md` (001) | which are terminal, which in flight, ordering |
| `pool_width` | config (MVP 1, target 2) | max non-terminal dispatched at once (SC-003) |
| `calibration_done` | `CALIBRATION.md` presence (research R8) | the gate-then-fan-out barrier (SC-010) |

**`syllabus_index` is derived, not a new field.** 001's `lessons[]` entries are `{ id, status }`
(`build-progress-schema.md`) and the list is in **syllabus order**; the scheduler uses each lesson's
**1-based list position** as its `syllabus_index` (lessons 1–2 = "the first two"; ≥ 3 = "beyond the
first two"). 003 therefore needs **no schema change** to 001's `lessons[]` — the ordering it depends on
is already guaranteed by the list order. (If the `id`s already encode order, position and `id` agree;
position is the authoritative source either way.)

Eligibility predicate (the two invariants, as one function):
- **In-flight cap**: `count(status == in-progress) < pool_width` before a `not-started` lesson may be
  dispatched.
- **Fan-out barrier**: a lesson with `syllabus_index >= 3` (i.e. beyond the first two) is **never**
  eligible while `calibration_done == false`.

MVP `pool_width = 1` ⇒ at most one `in-progress` at a time ⇒ a fully serial walk; the first two lessons
(indices 1–2) are drafted serially, calibration runs, then indices ≥ 3 become eligible one at a time.
At `pool_width = 2` the first two run as a pair and, post-calibration, the remainder fan out two at a
time — same function, config flip (FR-009).

## `CALIBRATION.md` (003's owned artifact)

Created **once**, when the fake-student check completes (FR-021). Human-readable Markdown; its presence
is the once-per-course guard **and** the scheduler's fan-out barrier (research R8). Minimal required
shape (full schema in `contracts/calibration.md`):

| Section | Content | FR |
| :--- | :--- | :--- |
| Audience snapshot | the brief's audience + assumed prior knowledge the fake-student was given | FR-013 |
| Lessons probed | the first two terminal lessons (ids) + whether an exercise was attempted or read-only fallback | FR-013, edge case |
| Confusion points | concrete findings (undefined terms, too-fast steps) | FR-014 |
| Fixes applied | how the confusion points were fixed in the two lessons + the re-grade result per edited lesson | FR-014, SC-006 |
| Drafting guidance | the explanation-format guidance folded into every remaining lesson's author input | FR-014/021 |

## Validation rules (enforced by the tool layer)

| Rule | Enforced by | SC |
| :--- | :--- | :--- |
| Never more than `pool_width` lessons `in-progress` at once | `pool_scheduler.py` | SC-003 |
| No lesson with `syllabus_index ≥ 3` dispatched before `CALIBRATION.md` exists | `pool_scheduler.py` | SC-010 |
| Every `[Sn]` in a passing lesson resolves to a real `SOURCES.md` entry (exhaustive; `.md` + `.ipynb` markdown cells) | `citation_trace.py` | SC-004 |
| Every factual claim is `[Sn]`-cited or explicitly mentor-added; thin-grounding / mentor-added tags preserved | `citation_trace.py` + lesson-evaluator | SC-004 |
| The evaluator envelope carries the artifact + grading inputs but **no** author-reasoning channel | `author_envelope.py` | SC-002 |
| The author envelope is exactly the FR-007 input set (incl. `CALIBRATION.md` for lessons > 2) | `author_envelope.py` | SC-002 (author side) |
| Per-lesson status written to `lessons[]` before the lesson is "done" | handler via `progress.py` (001) | SC-007 |
| Skeleton phase returns `needs-user`, never `pass` (no auto-advance) | `skeleton-phase` handler contract | SC-005 |
| Fake-student runs iff `CALIBRATION.md` absent; writes it on completion | `lesson-phase` handler + presence guard | SC-006 |

Rows the tool layer does **not** enforce (irreducibly judgment — asserted via `quickstart.md`
walkthroughs, not `pytest`): topic-match + clarity of a skeleton (SC-009), whether a rubric dimension
actually clears its bar (the rubric's grading, 004's), whether a confusion point is real, whether a
claim is *true* (tracing ≠ truth). See research R2.
