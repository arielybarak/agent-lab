# Implementation Plan: Course-Template Distillation

**Branch**: `000-course-template` | **Date**: 2026-07-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/course-factory/000-course-template/spec.md`

## Summary

Distill the frozen, versioned, three-tiered `course-factory/course-template/` asset from the
hand-built reference course `System_Design_SelfLearn/.claude/` (an **unvalidated idea pool**, read
from a configurable path) **cross-checked against** the external `research-digest.md`. The work is a
**one-time authoring/distillation run**, not a running program: classify all 23 reference assets
(keep-core / demote-module / drop) with recorded rationale + provenance in one classification table,
strip every topic-specific from anything kept, sort survivors into a **small mandatory core + a
default archetype profile + opt-in optional modules**, shape the quality rubric as one-rubric-two-
layers, run a **neutrality gate** over the core, and emit a **semver-stamped, self-describing**
directory that spec 001 copies by overlay and never mutates. Correctness is proven pre-pipeline by a
**2-topic, agent-performed paper-walkthrough** (Introduction to Psychology; Python Programming).

## Technical Context

This spec produces **content assets** (`.claude/` markdown + a manifest + a version stamp), not a
software service. The template-template fields below are answered in that light.

**Language/Version**: N/A for the deliverable (Markdown/YAML `.claude/` assets). One **optional**
supporting check — the neutrality-gate scanner (FR-020/SC-002) — MAY be a stdlib Python 3.11 script
or a plain `grep` recipe; no third-party deps (repo convention: stdlib only, pytest if tested).

**Primary Dependencies**: The reference course `.claude/` at `$COURSE_FACTORY_REFERENCE_DIR`
(default `/home/barak/System_Design_SelfLearn/`, FR-001) — read-only; and
[`research-digest.md`](research-digest.md) in this feature folder (FR-003, distillation halts if
absent — FR-005). The critical-thinking filter reuses the `mentor-research` skill's recording
discipline (spec Assumptions), not a new scheme.

**Storage**: Files on disk — the produced `course-factory/course-template/` directory tree.

**Testing**: Three artifact checks, no runtime harness: (1) classification-completeness (every one
of the 23 assets has a verdict + rationale — SC-001); (2) neutrality-gate term scan over the core
(SC-002); (3) the 2-topic agent-performed structured paper-walkthrough recorded as a checklist
(SC-003/SC-012). Optional pytest only if the neutrality scanner is scripted.

**Target Platform**: Repo filesystem (the `agent-lab` monorepo). No deploy target.

**Project Type**: Content-asset / template authoring (single deliverable directory) — not
library/web/mobile. The template-provided source-tree options do not apply; see Project Structure.

**Performance Goals**: N/A (one-time authoring run).

**Constraints**: (a) topic-neutral core — zero residual topic terms past the gate; (b) frozen +
semver-stamped, copied-never-mutated (Principle V); (c) one core + profiles, never siloed per-subject
templates (Principle IX); (d) the produced `course-template/.claude/` MUST stay distinct from the
factory's own build `.claude/` (FR-021, Structural Constraints).

**Scale/Scope**: 23 reference assets in; MVP out = 1 small core + the profile **mechanism** + **1
default profile** + the optional-module set derived from SD's topic-specifics. The three
structurally-consequential profiles (PBL/CBL, CBE/mastery, guided-inquiry) are **later, independent
increments** (User Story 4 / FR-023), explicitly **out of this plan's MVP delivery**.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution v1.2.2. This spec **produces the template**; several
course-*build*-time principles (I quality loop, VII big-chunks, X running example, XI resumable, XII
feedback) do not gate template production directly — the plan's obligation is that the produced core
**carries** their machinery, which it does.

| Principle | Relevance to this spec | Status |
| :--- | :--- | :--- |
| II. Anti-Fabrication | Template shape grounded in the research digest, not invented; rubric core flagged "adopted on judgment" where the digest is silent (FR-013) | ✅ Pass |
| III. Mentor, Not Aggregator | Critical-thinking filter on every SD-sourced idea (FR-002); research wins ties (FR-004) | ✅ Pass |
| IV. Clarify Early | Spec is Clarified (5 Qs, 2026-07-11); no open `NEEDS CLARIFICATION` | ✅ Pass |
| V. Specialize by Overlay | Deliverable is frozen + semver-stamped + self-describing (FR-016/017/018) | ✅ Pass |
| VIII. One Rubric, Two Layers | Rubric asset is 6-dimension core + add-on slots, shape-only, defers grading to 004 (FR-013/014/015) | ✅ Pass |
| IX. Tiered Templates | The spec's spine: one core + profiles + modules, MVP ships default profile only (FR-009/022–025) | ✅ Pass |
| I, VII, X, XI, XII (build-time) | Not gated at template-production time; core carries the rubric/lesson-arc/feedback-loop machinery these rely on downstream | ✅ N/A (carried, not enforced here) |

**No violations.** Complexity Tracking is empty.

**Post-design re-check (after Phase 1)**: re-evaluated after `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md` were written — the design stays entirely within the
frozen/versioned/tiered, one-core-with-profiles model; no new principle tension introduced. Gate
still ✅ Pass.

## Project Structure

### Documentation (this feature)

```text
specs/course-factory/000-course-template/
├── spec.md              # Clarified feature spec (input)
├── research-digest.md   # External research grounding (input, FR-003)
├── plan.md              # This file
├── research.md          # Phase 0 output — distillation-methodology decisions
├── data-model.md        # Phase 1 output — schemas of the produced artifacts
├── quickstart.md        # Phase 1 output — how to validate the produced template
├── contracts/           # Phase 1 output — the seams spec 001 consumes
│   ├── template-manifest.md   # self-description schema 001 reads (FR-018)
│   └── version-stamp.md       # semver stamp format + drift-check contract (FR-016)
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

The deliverable is a **content directory**, not a `src/` tree. Concrete target layout:

```text
course-factory/course-template/           # produced frozen artifact (the deliverable)
├── VERSION                               # semver stamp, e.g. 1.0.0 (FR-016)
├── manifest.yaml                         # self-description: which pieces are core / profile / module (FR-018)
├── CLASSIFICATION.md                     # ONE table: per-asset verdict + rationale + provenance (FR-006/019)
├── neutrality-terms.txt                  # maintained topic-term denylist for the gate (FR-020)
├── .claude/                              # the topic-neutral course-template env — distinct from the factory's own (FR-021)
│   ├── skills/                           #   core: lesson-arc + backward-design + rubric-shape;  modules: diagrams, katas, pattern-catalog, socratic
│   ├── commands/                         #   core: improve-course, new-lesson, course-report;  module: add-diagram
│   └── agents/                           #   core: consistency-reviewer (generalized), course-evaluator (shape);  module/dropped per CLASSIFICATION.md
└── profiles/
    └── default/                          # MVP: theory / linear-spiral (FR-023/025). PBL·CBE·guided-inquiry = later increments, not built here.

course-factory/tools/                     # OPTIONAL, only if the neutrality gate is scripted
└── neutrality_scan.py                    # stdlib scan of the core against neutrality-terms.txt (SC-002)
```

**Structure Decision**: Single content-asset deliverable under `course-factory/course-template/`.
No application source tree, no test pyramid — the "tests" are the three artifact checks named in
Technical Context. The distillation *procedure* that produces this tree is captured as the ordered
task list in `tasks.md`; it is an authoring run, not persistent code.

## Complexity Tracking

> No Constitution Check violations — this section intentionally left empty.
