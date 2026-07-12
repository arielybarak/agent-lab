# Implementation Plan: Syllabus Phase — Research & Mentor-Led Composition

**Branch**: `002-syllabus` | **Date**: 2026-07-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/course-factory/002-syllabus/spec.md`

## Summary

Build the **depth behind the syllabus gate** that spec 001 orchestrates: the expensive, budget-capped
**research** that grounds a course, and the **mentor-led composition** of the syllabus itself. Two
durable deliverables — a populated **`SOURCES.md`** (the anti-fabrication grounding for *every* later
lesson) and a **review-ready, ultimately-frozen `SYLLABUS.md`** — plus the augmentation of
`COURSE_BRIEF.md` with the `.md`/`.ipynb` lesson-format decision.

This spec **replaces 001's syllabus stub handler** against the published phase seam
(`specs/course-factory/001-pipeline-skeleton/contracts/phase-seam.md`): it consumes the fixed input
envelope, writes its own artifacts, updates only its owned `BUILD_PROGRESS.md` field
(`syllabus_subphase`), and returns a gate result — **without touching the orchestrator**. 001 owns the
loop, the freeze, and the park machinery; 002 owns the *content* — what research finds, how the
syllabus is composed, the volume + format decision, and the trigger + content of the post-research
divergence question.

**Technical approach — the same deliberate hybrid 001 chose.** The measurable Success Criteria stated
in **100% / 0-exception** terms are guaranteed by a **thin deterministic stdlib tool layer** rather
than left to agent discipline: a research **budget counter** (SC-002, 0 unbounded runs), a
**`SOURCES.md` linter** (SC-001, every entry keyed + reliability-judged), and a **syllabus-output
validator** (SC-003 topic traceability, SC-005 divergence-assessment presence, SC-008 thin-grounding
tag consistency, SC-004 format-decision presence). The **judgment** work — weighing reliability,
composing as a domain mentor, judging convergence and divergence — lives in `.claude/` **skills +
agents**, reusing the existing **`mentor-research`** skill as the shared research discipline rather
than inventing a second method. The syllabus-phase handler is the seam between the two: it drives the
tools, invokes the judgment surface, and returns the gate result the orchestrator consumes.

Because spec 000 (the frozen template) and 001 (the factory `.claude/`) are not yet built, this plan —
exactly like 001's — is validated against **fixtures** (a minimal `COURSE_BRIEF.md`, hand-authored
`SOURCES.md`/`SYLLABUS.md` samples with deliberate defects, and a diverging-sources scenario), and
defines only the **contracts** over the shared artifacts, never re-deriving 001's state machine.

## Technical Context

This spec produces a **`.claude/` handler + agents plus a thin deterministic tool layer** that plugs
into the factory build engine spec 001 defines. It is not a conventional application service; the
template fields are answered in that light.

**Language/Version**: Python **3.11**, standard library only (repo convention: stdlib only, zero deps,
pytest if tested) for the deterministic tool layer. The syllabus-phase surface itself is `.claude/`
Markdown skills + agents (prose + YAML frontmatter).

**Primary Dependencies**:
- **Spec 001's factory `.claude/` and its published contracts** — `phase-seam.md` (the input
  envelope + gate-result vocabulary this handler implements), `build-progress-schema.md` (the
  `syllabus_subphase` field 002 owns), `course-folder.md` (the `SOURCES.md`/`SYLLABUS.md` stubs 002
  populates and their delivery-set membership). 001 is not yet built; 002 validates against the
  contracts + fixtures and replaces the syllabus stub without editing the orchestrator.
- **The `mentor-research` skill** (currently at repo-root `.claude/skills/mentor-research/`) — the
  shared research discipline (weigh reliability → key under `[Sn]` → tier → converge-or-budget). Its
  own re-home note says to copy it into `course-factory/.claude/skills/` once 001 scaffolds the
  factory environment; this spec is that consumer.
- **Spec 000's frozen template** — read-only, only its **archetype profile** is consumed at compose
  time (FR-015). Not yet built; represented by a minimal profile fixture, exactly as 001 stands in a
  minimal template fixture.
- **Harness research tools** — `WebSearch`, the `gh` CLI, and shallow public platform name-search —
  invoked by the research skill, counted against the budget. No scrapers, logins, or paid pullers.

**Storage**: Files on disk inside `courses/<name>/` — `SOURCES.md`, `SYLLABUS.md`, the
`lesson_format` augmentation of `COURSE_BRIEF.md`, and the `syllabus_subphase` slice of
`BUILD_PROGRESS.md` (written via 001's `progress.py`, never hand-edited). No external state store; a
resuming session reads sub-phase status from the course folder alone (FR-018).

**Testing**: `pytest` over the deterministic tool layer, driven from fixtures: hand-authored
`SOURCES.md` samples (well-formed + missing-key + reliability-absent) for the linter; `SYLLABUS.md`
samples (fully-traced + a silently-ungrounded topic + a thin-grounding case) for the validator; a
query-log fixture for the budget counter; and a diverging-vs-agreeing source scenario asserting the
divergence-assessment record is always written (SC-005) and the ask fires only on divergence. The
agent-judgment paths (weighing, composing) are exercised as *scenario walkthroughs* in
`quickstart.md`, not asserted by `pytest` (they are irreducibly judgment — see research R2).

**Target Platform**: The `agent-lab` monorepo filesystem, driven by Claude Code. No deploy target.

**Project Type**: Pipeline phase-handler — a `.claude/` skill+agent surface over a small deterministic
Python tool layer, plugged into 001's build engine. The template's library/web/mobile source-tree
options do not apply; see Project Structure.

**Performance Goals**: N/A — an interactive, budget-bounded authoring phase, not a throughput system.
The only hard quantitative concept is the research **budget** (FR-005): a max query/tool-call count,
a *cost* bound, not a latency target.

**Constraints**: (a) **light tooling only** — web + `gh` + shallow public name-search; no scrapers /
logins / paid pullers (FR-001 / SC-006); (b) **anti-fabrication** — no ungrounded topic, no invented
sourced claim; every topic traces to `[Sn]` or is tagged mentor-added (Principle II / FR-007 / SC-003);
(c) **sources inform, never dictate** — mentor composition, staleness corrected (Principle III /
FR-006); (d) **never touch the orchestrator or re-implement the loop/freeze** — 002 writes content and
revises on feedback; 001 owns the gate loop and freeze (FR-014); (e) **stable, append-only `[Sn]`
keys** — a key, once assigned, is never reused (FR-004 / Assumptions); (f) **one research budget** —
post-divergence re-research charges the *same* budget, never a fresh one (FR-019).

**Scale/Scope**: One instantiated course in → a populated `SOURCES.md` + a frozen `SYLLABUS.md` +
the `lesson_format` augmentation out, produced inside 001's syllabus phase. MVP composes against the
**default** archetype profile (the only profile 000 ships initially); the profile-consumption
*mechanism* (FR-015) is profile-count-agnostic.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution **v1.2.2**. 002 is where three content principles (II Anti-Fabrication,
III Mentor-Not-Aggregator, IV Clarify-Before-Drafting) are first *exercised on real content* — 001
carries them behind the seam; 002 makes them observable in the syllabus artifacts.

| Principle | How this plan satisfies it | Status |
| :--- | :--- | :--- |
| I. Quality Loop Is Mandatory (NON-NEG) | 002 never one-shots; it composes, then returns `needs-user` so 001's user-approval gate runs. No path skips the gate (FR-013/014) | ✅ Pass |
| II. Anti-Fabrication First (NON-NEG) | Every kept source is `[Sn]`-keyed with a reliability judgment (FR-002/003, SC-001); every syllabus topic traces to `[Sn]` or is tagged mentor-added, mechanically linted (FR-007, SC-003); thin grounding is flagged, never fabricated (FR-011, SC-008) | ✅ Pass |
| III. Mentor, Not Aggregator | Composition is compose-as-mentor — sources inform, stale/irrelevant material is corrected, gaps filled with current-industry judgment (FR-006, US2 Independent Test with a deliberately stale source) | ✅ Pass |
| IV. Clarify Early, Research Before Drafting | Research fully precedes composition (sub-phase order `research-* → composed`); the divergence ask is ask-moment #2, fired **only** on real divergence (FR-012, SC-005) — an ask-moment, **not** a gate, so outside 001's park machinery (constitution IV carve-out, README seam #8) | ✅ Pass |
| V. Specialize by Overlay | 002 augments `COURSE_BRIEF.md` with one field (`lesson_format`) and reads the profile overlay; it never edits template internals (FR-009/015) | ✅ Pass |
| VI. Match the Reviewer | The syllabus reviewer is the **User** (course shape/scope); 002 presents and revises, 001 loops to approval (FR-013/014) — correctness of learned material is not made a user gate here | ✅ Pass |
| VIII. One Rubric, Two Layers | 002 defines **no** rubric; the syllabus is user-approved, not rubric-graded (Out of Scope; the rubric is 004's) | ✅ N/A (owned by 004) |
| IX. Tiered Templates | Composition honors the selected profile's macro spine / entry point / advisory checkpoints while reusing the mandatory core's invariants — it never redefines or bypasses them (FR-015) | ✅ Pass |
| X. One Running Example | The syllabus stays consistent with the brief's required running example (FR-010, SC-007) — it threads the backbone 001 guaranteed present | ✅ Pass |
| XI. Resumable by Design | `syllabus_subphase` is written via `progress.py` after each sub-step so a mid-phase death resumes at the right sub-step (FR-018); no in-memory cross-session state | ✅ Pass |
| XII. Feedback Compounds | Composition reads the `insights/` digest (empty is valid) alongside `SOURCES.md` (FR-016); the read side of Principle XII | ✅ Pass |
| VII (Big Chunks) | Not exercised here — the batch author→critique→refine loop is 003's; the syllabus is a single artifact behind one user gate | ✅ N/A (003's) |

**No violations.** Complexity Tracking is empty. The deterministic tool layer is the *minimum* that
makes the 100%/0-exception SCs mechanical rather than agent-judged (justified in `research.md` R1) —
the same justification 001 recorded, not an added abstraction.

**Post-design re-check (after Phase 1)**: re-evaluated after `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md`. The tool/skill split, the inline-divergence-ask decision (R3), and
the fixture-based validation keep the design inside the anti-fabrication / mentor / resumable model and
inside 001's seam; no new principle tension introduced, no orchestrator change implied. Gate still
✅ Pass.

## Project Structure

### Documentation (this feature)

```text
specs/course-factory/002-syllabus/
├── spec.md              # Clarified feature spec (input)
├── plan.md              # This file
├── research.md          # Phase 0 — the design decisions (tool/skill split, mechanization boundary, inline-ask, budget honesty, mentor-research reuse)
├── data-model.md        # Phase 1 — entities + the SOURCES.md / SYLLABUS.md shapes + the syllabus-phase sub-state machine over the seam
├── quickstart.md        # Phase 1 — validate US1/US2/US3 against fixtures + scenario walkthroughs
├── contracts/           # Phase 1 — the schemas 002 owns + how it plugs into 001's seam
│   ├── syllabus-handler.md    # how the handler implements phase-seam.md for the syllabus phase (envelope in → gate result out, sub-phase writes)
│   ├── sources-schema.md      # SOURCES.md entry schema — [Sn] keys, citation, reliability judgment (FR-003, SC-001)
│   └── syllabus-schema.md     # SYLLABUS.md shape — topic traceability, mentor-added tags, thin-grounding flags, divergence assessment (FR-007/011/012, SC-003/005/008)
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

The deliverable **adds to the factory's own build `.claude/`** (created by 001) plus a thin
deterministic tool layer and its tests. It never edits 001's orchestrator or the frozen
`course-template/.claude/`. Concrete target layout:

```text
course-factory/.claude/                       # THE FACTORY'S OWN build engine (001 scaffolds; 002 adds the syllabus depth)
├── skills/
│   ├── syllabus-phase/                        #   the syllabus phase handler — replaces 001's phase-stubs syllabus path
│   │   └── SKILL.md                           #     envelope → research (mentor-research) → compose → divergence-ask → present → gate result (FR-001–019)
│   └── mentor-research/                       #   RE-HOMED here from repo-root .claude/skills/ (its own re-home note); the shared research discipline (FR-001–005)
│       └── SKILL.md
├── agents/
│   └── syllabus-composer.md                   #   fresh-context "domain mentor": compose-as-mentor honoring the profile, correcting staleness (FR-006/010/015)

course-factory/tools/                          # deterministic, SC-critical mechanical ops (stdlib Python) — sibling to 001's tools/
├── research_budget.py                         #   persistent query/tool-call counter + cap check; stop decision is deterministic given the log (FR-005, SC-002)
├── sources_lint.py                            #   SOURCES.md validator — every entry has a stable [Sn] key + a recorded reliability judgment (FR-003, SC-001)
├── syllabus_lint.py                           #   syllabus-phase output validator — topic traceability, divergence-assessment presence, thin-grounding tag consistency, lesson_format present (FR-007/011/012/009, SC-003/004/005/008)
└── README.md                                  #   UPDATE 001's existing tools/README.md (append the three 002 tools + the budget-honesty boundary) — do NOT create a second README

course-factory/tests/                          # pytest + fixtures (sibling to 001's tests/)
├── fixtures/
│   ├── brief-min/                             #   minimal COURSE_BRIEF.md (with + without lesson_format) + a default-profile stand-in
│   ├── sources/                               #   SOURCES.md samples: well-formed, missing-[Sn]-key, reliability-absent, duplicate-work
│   ├── syllabi/                               #   SYLLABUS.md samples: fully-traced, silently-ungrounded-topic, thin-grounding, missing-divergence-assessment
│   └── query-log/                             #   research query-log samples at / under / over budget
├── test_research_budget.py                    #   SC-002 (stops at cap; never unbounded; post-divergence re-research shares the same budget, FR-019)
├── test_sources_lint.py                       #   SC-001 (rejects unkeyed / reliability-absent entries; accepts well-formed)
└── test_syllabus_lint.py                      #   SC-003/004/005/008 (rejects ungrounded topic / missing format / missing divergence assessment / silent thin-grounding)
```

**Structure Decision**: A `.claude/` judgment surface (research + compose) over a **thin** `tools/`
layer that mechanizes exactly the SCs stated in 100%/0-exception terms, mirroring 001's split. The
handler is the seam-facing entry point; `mentor-research` is **re-homed, not re-authored** (one
research discipline, per the skill's re-home note); the composer is a fresh-context mentor agent so the
"sources inform, never dictate" stance is a first-class persona, not a buried instruction. No source
tree beyond these additions; `courses/<name>/` is runtime staging (001's), not part of this
deliverable's tree.

## Complexity Tracking

> No Constitution Check violations — this section intentionally left empty. The deterministic tool
> layer is justified in `research.md` (R1) as the minimum needed to make the anti-fabrication SCs
> (SC-001/002/003/008) mechanical rather than agent-judged — not added abstraction. Its honesty
> boundary (the budget counter can only count queries the skill logs) is stated plainly in
> `research.md` (R4), not hidden.
