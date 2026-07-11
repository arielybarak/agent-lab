# Implementation Plan: Course-Factory Pipeline & Instantiation

**Branch**: `001-pipeline-skeleton` | **Date**: 2026-07-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/course-factory/001-pipeline-skeleton/spec.md`

## Summary

Build the **factory's own build `.claude/`** (DESIGN roadmap task #2) — the pipeline that turns a
rough author-written `COURSE_SPEC.md` into an instantiated, resumable course build and walks it
through the fixed phase sequence to delivery. Two joined subjects: **instantiation** (intake clarify
interview → `COURSE_BRIEF.md` overlay + archetype-profile + module selection → copy the frozen
`course-template/` into `courses/<name>/` with the overlay applied + version stamped) and
**orchestration** (the fixed phase sequence, the per-phase gates matched to the competent reviewer,
and the on-disk `BUILD_PROGRESS.md` state machine that makes a build pausable/resumable across
sessions).

**Technical approach — a deliberate hybrid**: the correctness-critical *mechanical* operations
(copy-never-mutate, `BUILD_PROGRESS.md` read/write + legal-transition enforcement, the lock marker,
version-stamp drift compare, `DIFFS.md` append, artifact-presence check) are **deterministic stdlib
Python tools** so the measurable Success Criteria (`SC-003` 0 template mutations, `SC-004`/`SC-006`
0 repeats / 0 silent skips, `SC-012` 0 concurrent advances) are *mechanically* guaranteed rather than
left to agent discipline. The *judgment* work (intake interview, brief authoring, orchestration
narrative) lives in `.claude/` **commands + agents**. Each **phase's internal work is a black box
behind a seam**; this spec ships **stub handlers** (produce placeholder artifact + return a gate
result) so US2/US3 are testable end-to-end today, and 002/003/004 replace the stubs against the same
seam contract without touching the spine. Same deliverable, same scope — this is the *approach* to
the factory `.claude/`, not a widening of it.

## Technical Context

This spec produces a **`.claude/` environment plus a thin deterministic tool layer** (the factory's
own build engine), not a conventional application service. The template fields are answered in that
light.

**Language/Version**: Python **3.11**, standard library only (repo convention: stdlib only, zero
deps, pytest if tested) for the deterministic tool layer. The pipeline surface itself is `.claude/`
Markdown commands + agents (prose + YAML frontmatter).

**Primary Dependencies**: The frozen, versioned, three-tiered `course-factory/course-template/`
asset (**spec 000**, FR-001) — read-only at build time; instantiation **halts** if it is absent or
unversioned. Spec 000 is not yet built, so this plan is validated against a **minimal template
fixture** (see Testing) and defines only the copy/overlay/version *contract* over the template, never
its content. Also reads the factory `insights/` digest (FR-025) and — as black boxes behind the seam
— the syllabus/lesson/grading phase handlers owned by 002/003/004.

**Storage**: Files on disk. Per-course state lives entirely in `courses/<name>/` (chiefly
`BUILD_PROGRESS.md`); there is **no external state store** — a fresh session resumes from the course
folder alone (FR-018/SC-005).

**Testing**: `pytest` over the deterministic tool layer, plus scenario tests driven from fixtures:
(1) a **minimal frozen `course-template/` fixture** (VERSION + manifest + a couple of `.claude/`
files) so instantiation is testable without spec 000; (2) **stub phase handlers** that emit
"produced + gate result" so the phase walk (US2) and resume (US3) run end-to-end. Tests assert the
SCs directly (template byte-unchanged, no repeated units on resume, no advance without a recorded
gate pass, lock refusal on concurrent advance).

**Target Platform**: The `agent-lab` monorepo filesystem, driven by Claude Code. No deploy target.

**Project Type**: Pipeline/tooling — a `.claude/` command+agent environment over a small
deterministic Python tool layer. The template's library/web/mobile source-tree options do not apply;
see Project Structure.

**Performance Goals**: N/A — an interactive, multi-session authoring pipeline, not a throughput
system. The only hard timing concept is the lock **liveness/stale window** (FR-028), a correctness
bound, not a performance target.

**Constraints**: (a) **copy, never mutate** the source template (Principle V / FR-007 / SC-003);
(b) **resumable from disk alone** — no in-memory cross-session state (Principle XI / FR-018);
(c) **strict forward-only** phase sequence — gated phases immutable, changes as forward diffs
(FR-023/027); (d) the factory's own build `.claude/` MUST stay **distinct from** the copied
`course-template/.claude/` (constitution § Structural Constraints); (e) anti-fabrication — intake
never invents a missing required field (Principle II / FR-003 / SC-001).

**Scale/Scope**: One `COURSE_SPEC.md` in → one instantiated, resumable `courses/<name>/` out, walked
to delivery. Multiple courses coexist in staging, each independently resumable (FR-019). MVP walks
the phases with **stubbed** phase internals and the **default** archetype profile (the only profile
000 ships initially); the profile/module *mechanism* is profile-count-agnostic.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution **v1.2.2**. This spec builds the **spine that enforces** the
principles; the plan's obligation is that the spine makes each one mechanically observable.

| Principle | How this plan satisfies it | Status |
| :--- | :--- | :--- |
| I. Quality Loop Is Mandatory (NON-NEG) | No one-shot path exists; the orchestrator advances **only** through the fixed phase sequence and refuses to advance without a recorded gate pass (FR-009/010, SC-006) | ✅ Pass |
| II. Anti-Fabrication First (NON-NEG) | Intake surfaces every missing required field as a **blocking question**, never a fabricated default (FR-003, SC-001); state integrity is deterministic, not guessed (FR-022, SC-009) | ✅ Pass |
| IV. Clarify Early | Upfront intake interview is ask-moment #1 (FR-002); gates are a **separate** category, not counted against the two-ask-moment cap (FR-014) | ✅ Pass |
| V. Specialize by Overlay | Instantiation copies + overlays + version-stamps; the source template is byte-unchanged, enforced by tooling (FR-006/007, SC-003) | ✅ Pass |
| VI. Match the Reviewer | Per-phase gate mapping is encoded in the state machine: user / agent-then-user / rubric / report-generated (FR-011, SC-007) | ✅ Pass |
| VII. Big Chunks, Then Batch-Review | The orchestrator runs the automated loop (cap 3) before any user gate and never interrupts per-item (FR-012/014) | ✅ Pass |
| IX. Tiered Templates | Intake makes an explicit archetype-profile + module selection; instantiation overlays **honoring** the selected profile and includes enabled modules (FR-005/006). The *content* of profiles/modules is 000's; the spine enforces the selection + overlay | ✅ Pass |
| X. One Running Example | The brief captures the required running example; intake **blocks** (never fabricates) if it is absent (FR-003/004, SC-001) — the spine guarantees its presence, 002/003 thread it | ✅ Pass |
| XI. Resumable by Design | `BUILD_PROGRESS.md` is the sole source of truth; persisted after every unit before the next begins; resume from disk alone (FR-015/016/017/018, SC-004/005) | ✅ Pass |
| XII. Feedback Compounds | Intake reads `insights/` (empty is valid, FR-025); gate-event comments are appended to `FEEDBACK.md` (FR-026); harvest stays 004's user-invoked path | ✅ Pass |
| III, VIII (content-time) | Not gated by the spine — mentor-composition (III) and the rubric (VIII) are exercised by 002/003/004 behind the phase seam; the core they act on is carried, not enforced here | ✅ N/A (behind the seam) |

**No violations.** Complexity Tracking is empty.

**Post-design re-check (after Phase 1)**: re-evaluated after `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md`. The hybrid tool/command split and the stubbed-seam strategy keep
the design inside the frozen-template / overlay / resumable-state model; no new principle tension
introduced. The deterministic tool layer is the *minimum* needed to make the NON-NEGOTIABLE and
measurable SCs mechanical rather than agent-judged (justified in `research.md` R1), not an added
abstraction. Gate still ✅ Pass.

## Project Structure

### Documentation (this feature)

```text
specs/course-factory/001-pipeline-skeleton/
├── spec.md              # Clarified feature spec (input)
├── plan.md              # This file
├── research.md          # Phase 0 output — spine design decisions (tool/command split, run-to-gate model, state format)
├── data-model.md        # Phase 1 output — entities + the BUILD_PROGRESS.md / COURSE_BRIEF.md / DIFFS.md schemas + phase/gate state machine
├── quickstart.md        # Phase 1 output — validate US1/US2/US3 with the fixture + stubs
├── contracts/           # Phase 1 output — the seams 002/003/004 consume
│   ├── build-progress-schema.md   # the published state schema (first-class deliverable, spec Assumptions)
│   ├── phase-seam.md              # how the orchestrator invokes a phase's black-box work + gate result
│   ├── diffs-ledger.md            # DIFFS.md forward-diff append contract (FR-027)
│   └── course-folder.md           # the delivered per-course artifact set (FR-020)
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

The deliverable is the **factory's own build environment** — a `.claude/` command+agent surface over
a thin deterministic Python tool layer. Concrete target layout (distinct from, and never conflated
with, the copied `course-template/.claude/`):

```text
course-factory/.claude/                   # THE FACTORY'S OWN build engine (this spec's deliverable)
├── commands/
│   ├── course-intake.md                  #   intake interview → COURSE_BRIEF.md + profile + module selection (FR-002/003/004/005)
│   ├── course-instantiate.md             #   copy frozen template → courses/<name>/, overlay, stamp, init state + stubs (FR-006/007/008)
│   ├── course-build.md                   #   the orchestrator; start-or-continue <name>: read state → run next unit → persist → gate → advance/park (FR-009–012/017/023/024)
│   └── course-status.md                  #   read-only render of BUILD_PROGRESS.md (no state change)
├── agents/
│   └── intake-interviewer.md             #   conducts the upfront clarify interview; anti-fabrication discipline (FR-002/003)
└── skills/
    └── phase-stubs/                      #   001's stub handlers implementing contracts/phase-seam.md (syllabus/skeleton/lesson/deliver)
        └── SKILL.md                      #   what the driver invokes per phase until 002/003/004 replace it

course-factory/tools/                     # deterministic, correctness-critical mechanical ops (stdlib Python)
├── instantiate.py                        #   copy-never-mutate + overlay + version stamp + init state/stubs + name/collision resolve (FR-006/007/008, SC-003)
├── progress.py                           #   read/validate/serialize BUILD_PROGRESS.md + the pure transition function (legal-move-only) + lock (FR-010/015/016/022/028)
├── diffs.py                              #   append-only DIFFS.md writer (FR-027)
├── deliver_check.py                      #   required-artifact-presence check at delivery (FR-020, SC-008)
└── README.md                             #   what each tool guarantees and which command calls it

course-factory/tests/                     # pytest + fixtures
├── fixtures/
│   ├── template-min/                     #   minimal frozen course-template stand-in (VERSION + manifest + .claude/) — unblocks US1 without spec 000
│   └── specs/                            #   sample COURSE_SPEC.md files (well-formed, missing-required-field, malformed)
├── test_instantiate.py                   #   SC-002/003 (overlay applied, template byte-unchanged)
├── test_progress.py                      #   SC-004/005/006/009/010/012 (resume, no-repeat, no-silent-skip, integrity halt, lock)
├── test_phase_walk.py                    #   US2 end-to-end with stub handlers (SC-007/008)
└── test_diffs.py                         #   FR-023/027 forward-diff ledger
```

**Structure Decision**: A `.claude/` engine (judgment surface) over a **thin** `tools/` layer
(mechanical guarantees), with **stubbed phase handlers behind a documented seam**. The Python surface
is deliberately minimal — only the operations whose measurable SCs demand determinism live there;
everything requiring domain judgment stays in commands/agents. The `courses/` staging area is created
at first instantiation and is **not** part of this deliverable's tree (it holds generated courses,
gitignored). `course-factory/insights/` exists as an **empty** sibling (start-empty per Principle
XII) that intake **reads** (FR-025, empty is valid); 001 never writes it — 004 does. This layout
keeps the factory's own `.claude/` structurally separate from the `course-template/.claude/` that
instantiation copies (Structural Constraints).

## Complexity Tracking

> No Constitution Check violations — this section intentionally left empty. The deterministic tool
> layer is justified in `research.md` (R1) as the minimum required to make the NON-NEGOTIABLE
> principles and measurable SCs mechanical rather than agent-judged, not as added abstraction.
