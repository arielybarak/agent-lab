# Implementation Plan: Lessons Phase — Skeletons, Parallel Author–Critic Authoring & Learnability

**Branch**: `003-lessons` | **Date**: 2026-07-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/course-factory/003-lessons/spec.md`

## Summary

Build the **depth behind the skeleton gate and the lesson gate** that spec 001 orchestrates: how
per-lesson skeletons and full lessons are actually authored, critiqued, and hardened. Three joined
deliverables — a **review-ready skeleton batch** (handed to 001's blocking user-scan gate), a set of
**rubric-passing lessons** each grounded by traceable `[Sn]` citations, and a once-per-course
**learnability calibration** (`CALIBRATION.md`) that tunes the explanation format for the whole
course from real reader confusion.

This spec **replaces 001's `skeletons` and `lessons` stub handlers** against the published phase seam
(`specs/course-factory/001-pipeline-skeleton/contracts/phase-seam.md`): each handler consumes the
fixed input envelope, writes its own artifacts, updates only its owned `BUILD_PROGRESS.md` field
(`lessons[]`), and returns a gate result — **without touching the orchestrator**. 001 owns the state
machine, the `active_loop.round` counter and cap-at-3 enforcement, the freeze/forward-diff rules, and
the park machinery for both gates; 003 owns the *work behind those gates* — the shared
author→critique→refine primitive, the mentor-led skeleton batch, the parallel author–critic worker
pool, and the fake-student calibration.

**Technical approach — the same deliberate hybrid 001 and 002 chose.** The measurable Success
Criteria stated in **100% / 0-exception** terms are guaranteed by a **thin deterministic stdlib tool
layer** rather than left to agent discipline: a **pool scheduler** (SC-003 at-most-`pool_width`
in-flight + SC-010 gate-then-fan-out barrier), an **exhaustive citation-traceability resolver**
(SC-004 every `[Sn]` resolves, honoring 002's mentor-added / thin-grounding tags — the factory's
**canonical** grounding check, reused, not re-authored), and an **author/evaluator envelope builder**
(SC-002 the evaluator's input never carries the author's private reasoning). The **judgment** work —
mentor-authoring skeletons and lessons, critiquing against topic/clarity and against the rubric,
reading like the target student — lives in `.claude/` **skills + agents**. The shared
author→critique→refine primitive is authored **once** as a single skill both phases invoke (FR-001);
the two phases differ only in their *driver* (single batch loop vs. worker pool) and the evaluator's
*checklist* (topic-match + clarity vs. rubric + full traceability).

Because spec 000 (frozen template), 001 (factory `.claude/`), and **004 (the rubric)** are not yet
built, this plan — exactly like 002's against 001 — is validated against **contracts + fixtures**: it
defines only the contracts over the shared artifacts (never re-deriving 001's state machine) and, for
the not-yet-built rubric, publishes a thin **rubric-gate consumption contract**
(`contracts/rubric-gate.md`) plus a minimal rubric fixture, so the lesson gate is testable today and
becomes the live seam the moment 004 lands its rubric core.

## Technical Context

This spec produces a **`.claude/` handler + agents plus a thin deterministic tool layer** that plugs
into the factory build engine spec 001 defines. It is not a conventional application service; the
template fields are answered in that light.

**Language/Version**: Python **3.11**, standard library only (repo convention: stdlib only, zero
deps, pytest if tested) for the deterministic tool layer — including the `.ipynb` markdown-cell scan,
which uses only the stdlib `json` parser (a notebook is JSON). The skeleton/lesson-phase surface
itself is `.claude/` Markdown skills + agents (prose + YAML frontmatter).

**Primary Dependencies**:
- **Spec 001's factory `.claude/` and its published contracts** — `phase-seam.md` (the input
  envelope + gate-result vocabulary both handlers implement, and the round-cap ownership split),
  `build-progress-schema.md` (the `lessons[]` field 003 owns, statuses `not-started` / `in-progress`
  / `passed` / `accepted-at-cap`), `diffs-ledger.md` (the forward-diff append 003 uses for FR-017),
  `course-folder.md` (the `CALIBRATION.md` + `FEEDBACK.md` + lesson-file membership). 001 is not yet
  built; 003 validates against the contracts + fixtures and replaces the two stubs without editing the
  orchestrator.
- **Spec 004's rubric** — consumed as a **pass/fail gate** over a lesson (per-dimension threshold,
  004 FR-004; the canonical citation/grounding check, 004 FR-007/FR-008). 004 has only a `spec.md`
  today, so 003 publishes `contracts/rubric-gate.md` (the thin consumption contract) and a rubric
  fixture, mirroring how 002 stood in a contract for not-yet-built 001. 003 **MUST NOT** redefine the
  rubric's contents (FR-010).
- **Spec 002's `SOURCES.md`** — read for `[Sn]` traceability; its schema
  (`specs/course-factory/002-syllabus/contracts/sources-schema.md`) is the resolution target for the
  citation check, and its **mentor-added / thin-grounding tags** are honored, never re-presented as
  sourced (FR-011). 003 reads and cites into `SOURCES.md`; it never searches or populates it.
- **The `mentor-research` heritage is NOT a dependency here** — 003 authors content, it does not
  research. It reads the frozen syllabus + `SOURCES.md` 002 produced.
- **Harness subagent spawning** — the orchestrating session spawns fresh-context author, author-blind
  evaluator, and fake-student subagents. No external services.

**Storage**: Files on disk inside `courses/<name>/` — the per-lesson skeletons, the lesson files
(`.md` / `.ipynb`, format decided by 002), `CALIBRATION.md` (FR-021), `FEEDBACK.md` appends (FR-020),
`DIFFS.md` forward-diff entries (FR-017, via 001's `diffs.py`), and the `lessons[]` slice of
`BUILD_PROGRESS.md` (written via 001's `progress.py`, never hand-edited). No external state store; a
resuming session reads per-lesson status and the presence of `CALIBRATION.md` from the course folder
alone (FR-021 honors 001's disk-only resume rule, FR-018).

**Testing**: `pytest` over the deterministic tool layer, driven from fixtures:
- **pool scheduler** — a lessons-list + `pool_width` + calibration-done fixture asserting at-most-`N`
  in flight (SC-003) and no lesson≥3 dispatched before `CALIBRATION.md` exists (SC-010); the
  degenerate `pool_width = 1` serial case and the `pool_width = 2` case both covered.
- **citation-traceability resolver** — lesson fixtures (fully-cited, unresolvable-`[Sn]`,
  mentor-added-marked, silently-ungrounded) over a `SOURCES.md` fixture, plus a `.ipynb` fixture whose
  `[Sn]` keys live in markdown cells (SC-004; the `.md`/`.ipynb` parity check).
- **envelope builder** — asserts the author envelope carries exactly the FR-007 input set and the
  evaluator envelope carries the artifact + grading inputs but **no** author-reasoning channel (SC-002).

The agent-judgment paths (mentor authoring, topic/clarity critique, rubric grading, reading-as-student)
are exercised as **scenario walkthroughs** in `quickstart.md`, not asserted by `pytest` — they are
irreducibly judgment (see research R2), the same boundary 002 drew.

**Target Platform**: The `agent-lab` monorepo filesystem, driven by Claude Code. No deploy target.

**Project Type**: Pipeline phase-handlers — a `.claude/` skill+agent surface over a small
deterministic Python tool layer, plugged into 001's build engine. The template's library/web/mobile
source-tree options do not apply; see Project Structure.

**Performance Goals**: N/A — an interactive, multi-session authoring pipeline, not a throughput
system. `pool_width` is a **concurrency** knob (MVP 1 → target 2), not a latency target; the only hard
quantitative bound is the **3-round cap** (a correctness bound owned by 001's counter, FR-002).

**Constraints**: (a) **single shared primitive** — skeleton and lesson phases MUST use one
author→critique→refine loop, authored once (FR-001); (b) **fresh-context author / author-blind
evaluator** split on every lesson — the evaluator never receives the author's private reasoning
(FR-007/008, SC-002); (c) **at-most-`pool_width` pairs in flight**, `pool_width` configurable, **MVP =
1** (fully serial, no concurrent `lessons[]` writes to order), target 2 (FR-009, SC-003);
(d) **gate-then-fan-out** — no lesson beyond the first two begins before the fake-student calibration
completes (FR-018, SC-010); (e) **anti-fabrication** — every claim `[Sn]`-cited or explicitly
mentor-added, every citation traceability-checked (exhaustive, not sampled), no lesson passes on an
unresolvable citation (Principle II / FR-011 / SC-004); (f) **never touch the orchestrator, the
`active_loop` counter, the freeze, or the rubric's contents** — 003 produces artifacts + delta reports
and returns gate results; 001 owns the loop/cap/freeze, 004 owns the rubric (FR-002/010/017);
(g) **skeleton phase never auto-advances** — it returns a review-ready batch and `needs-user`, never
`pass` (FR-006, SC-005); (h) **fake-student runs at most once per course**, gated by `CALIBRATION.md`
presence (FR-015, SC-006).

**Scale/Scope**: One instantiated course with an approved, frozen syllabus in → a review-ready
skeleton batch + a set of rubric-passing lessons + one `CALIBRATION.md` out, produced inside 001's
skeleton and lesson phases. MVP ships `pool_width = 1` and the **default** archetype profile (the only
profile 000 ships initially); every FR/SC is unaffected by the value of `pool_width` (FR-009) and the
profile-consumption mechanism (FR-019) is profile-count-agnostic.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution **v1.2.2**. 003 is where **Principle VII (Big Chunks, Then
Batch-Review)** is first *implemented as a running loop* — 001 carries the counter, 002 has no batch
loop; 003 owns what an author→critique→refine round actually does.

| Principle | How this plan satisfies it | Status |
| :--- | :--- | :--- |
| I. Quality Loop Is Mandatory (NON-NEG) | Neither phase one-shots: the skeleton phase runs the agent loop then returns `needs-user` for the blocking scan (FR-006); the lesson phase grades every lesson against the rubric gate before it is `passed` (FR-010). No path skips a gate | ✅ Pass |
| II. Anti-Fabrication First (NON-NEG) | Every lesson claim is `[Sn]`-cited or explicitly mentor-added; the evaluator checks **every** citation for traceability (exhaustive mechanical lookup, not a sample) and fails any lesson with an unresolvable citation (FR-011, SC-004); 002's thin-grounding flags are preserved, never re-presented as sourced | ✅ Pass |
| III. Mentor, Not Aggregator | Skeletons and lessons are authored **as a domain mentor** — sources inform, never dictate — a factory-wide stance (FR-004 note, FR-016); the evaluator's grounding check is about **traceability**, not parroting sources | ✅ Pass |
| VI. Match the Reviewer | Skeletons: agent-eval (topic-match + clarity) then the **blocking user scan** — 003 returns `needs-user`, never `pass` (FR-006). Lessons: **automated rubric** gate, no mandatory user review; correctness is not made a user gate (FR-010) — exactly the seam's `agent-then-user` / `rubric` mapping | ✅ Pass |
| VII. Big Chunks, Then Batch-Review | The whole skeleton batch is drafted before evaluation (single batch loop, FR-004); lessons are authored then graded; the automated author→critique→refine loop (cap 3) runs first, the user gate (if any) after; no per-item user interruption | ✅ Pass |
| IX. Tiered Templates | Both phases honor the selected archetype profile's scaffolding depth + advisory-checkpoint placement (FR-019) **without** altering the shared primitive (FR-001) or the rubric gate (FR-010), which apply uniformly regardless of profile | ✅ Pass |
| X. One Running Example | Lessons thread the brief's required running example; the evaluator (via the rubric's flow/coverage dimensions) can flag a break in the thread — 003 authors *consistent with* the backbone 001 guaranteed present | ✅ Pass |
| XI. Resumable by Design | Per-lesson status is written to `lessons[]` via `progress.py` before a lesson is treated as done (FR-012, SC-007); `CALIBRATION.md` persists the calibration so a post-calibration death resumes from disk (FR-021); no in-memory cross-session state | ✅ Pass |
| XII. Feedback Compounds | The evaluator's durable findings are appended to `FEEDBACK.md` (FR-020, the write side); authors read the `insights/` digest, empty is valid (FR-007). Harvest into `insights/` stays 004's user-invoked path | ✅ Pass |
| IV. Clarify Early | N/A — 003 has **no ask-moments**. Its only user interactions are 001's **gates** (the blocking skeleton scan, the round-cap accept-or-comment), a separate category from the two-ask-moment cap (constitution IV carve-out); the pool idles on a pending gate rather than asking a content question (FR-018) | ✅ N/A |
| V. Specialize by Overlay | 003 reads `COURSE_BRIEF.md` + the profile overlay; it never edits template internals and never mutates a frozen artifact — earlier-artifact gaps surface as forward diffs (FR-017) | ✅ Pass |
| VIII. One Rubric, Two Layers | 003 defines **no** rubric; it consumes 004's as a pass/fail gate and MUST NOT redefine its contents (FR-010) — one rubric, two consumers | ✅ N/A (owned by 004) |

**No violations.** Complexity Tracking is empty. The deterministic tool layer is the *minimum* that
makes the 100%/0-exception SCs (SC-002/003/004/010) mechanical rather than agent-judged (justified in
`research.md` R1) — the same justification 001 and 002 recorded, not an added abstraction.

**Post-design re-check (after Phase 1)**: re-evaluated after `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md`. The one-shared-primitive decision (R6), the canonical-check reuse
(R2), the pool-scheduler / envelope-builder split (R1/R3/R4), and the not-yet-built-rubric consumption
contract (R5) keep the design inside the anti-fabrication / mentor / big-chunks / resumable model and
inside 001's seam and 004's rubric ownership; no new principle tension introduced, no orchestrator or
rubric change implied. Gate still ✅ Pass.

## Project Structure

### Documentation (this feature)

```text
specs/course-factory/003-lessons/
├── spec.md              # Clarified feature spec (input)
├── plan.md              # This file
├── research.md          # Phase 0 — design decisions (tool/skill split, canonical-check reuse, pool model, author-blindness boundary, rubric-consumption stand-in, one shared primitive, .ipynb citation scan)
├── data-model.md        # Phase 1 — entities + the lesson lifecycle + the worker-pool state + the CALIBRATION.md shape, all over 001's seam
├── quickstart.md        # Phase 1 — validate US1/US2/US3 against fixtures + scenario walkthroughs
├── contracts/           # Phase 1 — the contracts 003 owns + how it plugs into 001's seam and consumes 004's rubric
│   ├── skeleton-handler.md         # how the skeleton handler implements phase-seam.md (batch loop → agent pass → needs-user; change-request re-entry, fresh cap)
│   ├── lesson-handler.md           # how the lesson handler implements phase-seam.md (worker pool, per-lesson rubric gate, lessons[] writes, cap→accept-or-comment)
│   ├── author-critic-primitive.md  # the SHARED author→critique→refine primitive: author envelope, author-blind evaluator envelope, delta format, round semantics (FR-001/002/003, SC-002)
│   ├── rubric-gate.md              # the thin consumption contract 003 needs from 004's not-yet-built rubric (per-dimension threshold + the canonical citation/grounding check)
│   └── calibration.md              # CALIBRATION.md schema + the once-per-course fake-student trigger, fold-in, and mandatory re-grade (FR-013–015/021, SC-006)
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

The deliverable **adds to the factory's own build `.claude/`** (created by 001) plus a thin
deterministic tool layer and its tests. It never edits 001's orchestrator, the frozen
`course-template/.claude/`, or 004's rubric. Concrete target layout:

```text
course-factory/.claude/                        # THE FACTORY'S OWN build engine (001 scaffolds; 003 adds skeleton + lesson depth)
├── skills/
│   ├── author-critic-loop/                     #   the SHARED author→critique→refine primitive — the ONE loop both phases invoke (FR-001/002/003)
│   │   └── SKILL.md                            #     author drafts/refines → author-blind evaluator emits cited deltas → author refines the deltas; caps handled by 001's counter
│   ├── skeleton-phase/                         #   the skeleton handler — replaces 001's phase-stubs skeletons path
│   │   └── SKILL.md                            #     draft ALL skeletons in one batch as a mentor → single batch-level loop (FR-004/005) → present-and-wait, return needs-user (FR-006)
│   └── lesson-phase/                           #   the lesson handler — replaces 001's phase-stubs lessons path
│       └── SKILL.md                            #     worker pool (fan-out/fan-in) → per-lesson rubric gate + full traceability → gate-then-fan-out around calibration (FR-007–018)
├── agents/
│   ├── mentor-author.md                        #   fresh-context "domain mentor": batch mode (all skeletons) OR per-lesson mode (one lesson); sources inform, never dictate (FR-004/007/016)
│   ├── skeleton-evaluator.md                   #   author-blind: topic-match + clarity/simple-language per skeleton (FR-005)
│   ├── lesson-evaluator.md                     #   author-blind: rubric grade (per-dimension threshold) + EXHAUSTIVE [Sn] traceability (FR-008/010/011)
│   └── fake-student.md                         #   once-per-course learnability probe: reads first two lessons as the target audience, attempts the exercise (FR-013)

course-factory/tools/                           # deterministic, SC-critical mechanical ops (stdlib Python) — sibling to 001's / 002's tools/
├── sn_resolve.py                               #   the CANONICAL [Sn]→SOURCES.md resolution primitive (honors 002's mentor-added / thin-grounding tags), imported by 002's syllabus_lint, 003's citation_trace, and 004's evaluator — one resolver, not three (research R2)
├── citation_trace.py                           #   003's thin layer over sn_resolve: format-aware extraction (.md prose + .ipynb markdown cells, research R7) + the EXHAUSTIVE per-lesson sweep (every claim cited-or-mentor-added; every key resolved) (SC-004)
├── pool_scheduler.py                           #   at-most-pool_width in flight (SC-003) + gate-then-fan-out barrier: no lesson≥3 dispatched before CALIBRATION.md exists (SC-010); pool_width=1 is the serial degenerate case
├── author_envelope.py                          #   builds the author input set (FR-007) and the author-blind evaluator input set (no author-reasoning channel) (SC-002)
├── rubric_gate.py                              #   NOT BUILT HERE — 004 owns it (its contracts/rubric-grading-semantics.md); 003's lesson gate IMPORTS it for the pass verdict. One predicate, two consumers (004 SC-009); the evaluator agent supplies the per-dimension scores, this decides passed/not-passed. Built before 003 per the README build order
└── README.md                                   #   UPDATE the existing tools/README.md (append the 003 tools + the canonical-resolver reuse note) — do NOT create a second README

course-factory/tests/                           # pytest + fixtures (sibling to 001's / 002's tests/)
├── fixtures/
│   ├── skeletons/                              #   skeleton-batch samples: topic-matched, topic-mismatched (for the evaluator scenario)
│   ├── lessons/                                #   lesson samples: fully-cited, unresolvable-[Sn], mentor-added-marked, silently-ungrounded, and an .ipynb whose [Sn] keys live in markdown cells
│   ├── sources/                               #   a SOURCES.md fixture (the [Sn] resolution target) — REUSE 002's fixtures where they fit
│   ├── rubric/                                 #   a MINIMAL rubric fixture (per-dimension threshold) standing in for not-yet-built 004 (research R5)
│   ├── brief/                                  #   a COURSE_BRIEF.md fixture with audience + assumed prior knowledge (fake-student input) + running example + profile
│   └── pool-scenarios/                         #   lessons-list + pool_width + calibration-done fixtures: serial(1), parallel(2), pre-calibration barrier, fewer-than-two-lessons
├── test_pool_scheduler.py                      #   SC-003 (never exceeds pool_width) + SC-010 (no lesson≥3 before calibration)
├── test_citation_trace.py                      #   SC-004 (rejects unresolvable [Sn]; accepts mentor-added; .md/.ipynb parity)
└── test_author_envelope.py                     #   SC-002 (evaluator envelope carries no author-reasoning channel; author envelope = the FR-007 set)
```

**Structure Decision**: A `.claude/` judgment surface (author + evaluator + fake-student personas)
over a **thin** `tools/` layer that mechanizes exactly the SCs stated in 100%/0-exception terms,
mirroring 001's and 002's split. The **shared primitive is one skill** (`author-critic-loop`) both
phase handlers invoke — honoring FR-001's "single shared" mandate structurally, not by convention; the
two phases are thin drivers over it (a batch loop, a worker pool). The **`[Sn]` resolution primitive is
one shared module** (`sn_resolve.py`) imported by 002/003/004; 003's `citation_trace.py` is a thin
format-aware, exhaustive layer over it — one canonical grounding check, not re-authored per spec
(research R2). The `mentor-author` agent is invoked in two modes (batch /
per-lesson) so the "sources inform, never dictate" stance is one persona, not two divergent copies. No
source tree beyond these additions; `courses/<name>/` is runtime staging (001's), not part of this
deliverable's tree.

## Complexity Tracking

> No Constitution Check violations — this section intentionally left empty. The deterministic tool
> layer is justified in `research.md` (R1) as the minimum needed to make the 0-exception SCs
> (SC-002/003/004/010) mechanical rather than agent-judged — not added abstraction. Its honesty
> boundaries (the scheduler decides dispatch eligibility but the session does the spawning; the
> envelope builder guarantees the evaluator's *input* is author-blind but cannot police what an author
> embeds in the artifact itself) are stated plainly in `research.md` (R3/R4), not hidden.
