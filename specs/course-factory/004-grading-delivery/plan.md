# Implementation Plan: Grading & Delivery — Rubric, Course-Evaluator, Report, Harvest & Comparison

**Branch**: `004-grading-delivery` | **Date**: 2026-07-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/course-factory/004-grading-delivery/spec.md`

## Summary

Build the factory's **only definition of quality and everything that definition feeds**. Four
loosely-coupled subsystems at very different points on the critical path:

- **US1 — the rubric (P1, 003's hard prerequisite).** The one-rubric-two-layers **grading-semantics
  layer** — concrete scale, per-dimension thresholds, weights, the hard-gate rule — filling the
  two-layer *shape* that spec 000 owns, plus the **pass predicate** (every dimension ≥ its threshold,
  no aggregate masking) that spec 003 consumes as the lesson gate and 004's course-evaluator runs as
  the engine.
- **US2 — course-evaluator + `COURSE_REPORT.md` (P2, gates delivery).** The course-level grader that
  applies the rubric, runs the **exhaustive `[Sn]` traceability** check (tracing, not truth) honoring
  002's mentor-added / thin-grounding tags, and **independently grades whole-arc dimensions**; the
  `/course-report` command writes the graded scorecard to `COURSE_REPORT.md`.
- **US3 — the `FEEDBACK.md` → `insights/` harvest (P3, post-MVP).** Two user-invoked paths
  (per-insight capture + `setup-retro`-style bulk harvest) that append-only into the cross-course
  `insights/` digest so the factory compounds. No automatic trigger.
- **US4 — `comparison/` (P4, post-MVP).** Analyze external courses → propose **revisions to the one
  rubric** (never a rival) + a per-course `/improve-course` report.

**Technical approach — a deliberate hybrid, mirroring 001/002/003.** The measurable **0-exception
Success Criteria** are made mechanical by a **thin deterministic `tools/` layer** (stdlib Python,
pytest) so they are *guaranteed by code*, not left to agent discipline: the **pass predicate**
(`rubric_gate.py`, SC-010 — no masking), the **single-rubric invariant** (`single_rubric_lint.py`,
SC-001/008/009 — 0 rival rubrics), the **exhaustive traceability sweep** (`course_trace.py` — a thin
course-scoped layer over the **shared** `sn_resolve.py`, SC-004 — 100% unresolvable flagged, 0
mentor-added false-fails), and the **append-only harvest mechanics** (`harvest.py`, SC-007 — no
clobber, no-op on empty). Everything
that is genuine **judgment** — scoring each rubric dimension, the **independent course-level
verdict**, distilling `FEEDBACK.md` critiques into `insights/`, analyzing external courses — lives in
`.claude/` **agents + commands**.

**004 spans two `.claude/` homes, and it does not re-own shared primitives.** The rubric asset, the
`course-evaluator` agent, and the `/course-report` command are **frozen `course-template/` assets**
(they ship inside every generated course as residue; 000 distills the shells, 004 owns their
**grading behavior/contents**). The harvest and `comparison/` are **factory-level** (they operate
across courses, writing `course-factory/insights/` and `course-factory/comparison/`). The `[Sn]`
resolver is the **one shared `sn_resolve.py`** (spec 003 builds it; 002/003/004 import it — "one
resolver, not three"); 004 reuses it and never authors a second grounding rule. Same deliverable,
same scope — this is the *approach* to the quality layer, not a widening of it.

## Technical Context

This spec produces a **frozen-template asset + a `.claude/` judgment surface + a thin deterministic
tool layer** — the factory's quality engine — not a conventional application service. The template
fields are answered in that light.

**Language/Version**: Python **3.11**, standard library only (repo convention: stdlib only, zero
deps, pytest) for the deterministic tool layer. The grading/harvest/comparison surfaces are `.claude/`
Markdown commands + agents (prose + YAML frontmatter); the rubric asset is Markdown.

**Primary Dependencies** (all are prerequisites *completed before 004's build slot* per the README
build order — `000 → 001 → 002 → 004-rubric-core → 003 → 004-delivery` — but **not built at plan
time**, so this plan targets each as a **contract + fixture**, exactly as spec 001 did for 000):

- **000's rubric-shape asset + version stamp** (000 FR-013/015/016). 000 owns the two-layer *shape* +
  the six core-dimension names + the semver `VERSION`; **004 fills the grading semantics** into that
  shape and shares 000's *single* version identity (never a rubric-only counter). Contract:
  [`contracts/rubric-grading-semantics.md`](contracts/rubric-grading-semantics.md); validated against
  the `tests/fixtures/rubric/` stand-in that 003 already defines.
- **The shared `sn_resolve.py` primitive** (spec 003 builds it; its `plan.md`/`tasks.md` T013/T014).
  The course-evaluator's traceability sweep **imports** it — 004 authors no rival resolver. Contract:
  [`contracts/citation-traceability.md`](contracts/citation-traceability.md).
- **002's `SOURCES.md` + mentor-added / thin-grounding tags** (`[Sn]` entries; `mentor-added` /
  `thinly-grounded` markers). Read for traceability; **never populated**. Consumes 002's
  `sources-schema.md` + `syllabus-schema.md`.
- **001's delivery terminal-state + `course-folder.md` contract** (001 FR-011/020). 001 invokes
  `/course-report` at delivery and owns the folder contract; 004 owns the report's **grading and
  contents**. 001's `DIFFS.md` ledger is where course-level gaps land as forward diffs (001 FR-027).
- Reads the factory `insights/` digest producer/consumer seam (write side = 004; read side =
  001/002/003).

**Storage**: Files on disk. Per-course quality artifacts (`COURSE_REPORT.md`) live in
`courses/<name>/`; the rubric ships in the course's frozen `.claude` residue; the cross-course
`insights/` and `comparison/` live under `course-factory/`. No external state store.

**Testing**: `pytest` over the deterministic tool layer, plus scenario walks driven from the **shared
fixtures** (reusing 003's `tests/fixtures/{rubric,sources,lessons}/`): the pass predicate (masking
rejected), the single-rubric lint (a planted rival fails), the exhaustive traceability sweep
(unresolvable `[Sn]` flagged; mentor-added not failed; thin-grounding flags preserved), the
append-only harvest (empty = no-op; two courses = no clobber), and the independent course-level
verdict (all-lessons-pass + incomplete arc coverage → flagged). Agent-judgment surfaces (dimension
scoring, distillation, comparison analysis) are validated by **scenario fixtures**, not unit-asserted.

**Target Platform**: The `agent-lab` monorepo filesystem, driven by Claude Code. No deploy target.

**Project Type**: Quality tooling — a frozen-template asset + a `.claude/` command+agent surface over
a small deterministic Python tool layer. The template's library/web/mobile source-tree options do not
apply; see Project Structure.

**Performance Goals**: N/A — an interactive, at-delivery / on-demand grading and harvest layer, not a
throughput system. Traceability resolution is O(claims) cheap mechanical lookups; exhaustiveness (not
sampling) is a *correctness* property (SC-004), not a performance concern.

**Constraints**: (a) **exactly one rubric** — 0 rival quality definitions, ever (Principle VIII /
FR-001 / SC-001), enforced by lint; (b) **tracing, not truth** — the grounding check verifies
resolution, never fact (FR-007); (c) **no aggregate masking** — a strong dimension may not mask a
failing one (FR-004 / SC-010), enforced by the pass predicate; (d) **forward-diff only** — a
course-level gap surfaces as a forward diff / `/improve-course` item and **never re-opens a passed
phase** (001 FR-023 / FR-010 / SC-006); (e) **harvest is user-invoked only** — 0 automatic/scheduled
triggers (FR-016 / SC-007); (f) **one version identity** across template and rubric (FR-005); (g)
anti-fabrication — mentor-added claims are honored, not fabricated into sourced ones (Principle II /
FR-008).

**Scale/Scope**: One finished course in → one graded `COURSE_REPORT.md` out, plus the cross-course
`insights/` the factory compounds and the on-demand `comparison/` analyses. US1 (rubric) is the
independently-shippable increment that unblocks 003; US2–US4 build on their own schedule (see
Structure Decision).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution **v1.2.2**. This spec **defines and enforces the quality bar** the
other specs consume; the plan's obligation is that the bar is single, mechanical where the SCs demand
it, and matched to the competent reviewer.

| Principle | How this plan satisfies it | Status |
| :--- | :--- | :--- |
| I. Quality Loop Is Mandatory (NON-NEG) | The rubric **is** the gate the loop enforces; the course-evaluator adds an independent course-level verdict on top of per-lesson passes — no path bypasses grading (FR-006/009) | ✅ Pass |
| II. Anti-Fabrication First (NON-NEG) | Exhaustive `[Sn]` traceability (tracing, not truth) flags every unresolvable citation; a mentor-added claim is honored, never fabricated into a sourced one, and thin-grounding flags are preserved (FR-007/008, SC-004) | ✅ Pass |
| IV. Clarify Early | N/A to this layer — 004 grades finished artifacts and harvests on user invocation; it opens no content-shaping ask-moment. Its user touchpoints (harvest, comparison adoption) are **deliberate actions**, not the two capped ask-moments | ✅ Pass (no ask-moment) |
| V. Specialize by Overlay | The rubric is a **frozen template core asset**, copied never mutated; a `comparison/` revision re-stamps the template via 000's rubric-only path, it never hand-edits a course's copy (FR-005/019) | ✅ Pass |
| VI. Match the Reviewer | Delivery's gate is the report's **generation**, not its verdict — a "needs work" report is delivered as-is and feeds `/improve-course`, never withheld (constitution VI Delivery row, FR-011) | ✅ Pass |
| VIII. One Rubric, Two Layers | Exactly one rubric (generic core + requestable add-ons); `single_rubric_lint.py` mechanically enforces 0 rivals; `comparison/` proposes **revisions**, never a second rubric; the rubric's version identity IS the template stamp (FR-001/005/019, SC-001/008) | ✅ Pass |
| IX. Tiered Templates | The rubric + course-evaluator + `/course-report` are **mandatory-core** template assets (constitution IX list); the topic add-on is the rubric's requestable layer, not a siloed rubric (FR-001/002) | ✅ Pass |
| XI. Resumable by Design | Grading is a stateless read over the finished course; a course records the rubric **version** that graded it so its verdict is reproducible/re-syncable (FR-005/013) | ✅ Pass |
| XII. Feedback Compounds | The harvest is the compounding mechanism — two user-invoked paths, append-only, no automatic trigger, empty = no-op; `insights/` starts empty and is read by 001/002/003 (FR-014–017, SC-007) | ✅ Pass |
| III, VII, X (content-time) | Not gated *by* 004 — mentor-composition (III), batch-review (VII), the running example (X) are exercised by 001/002/003; 004 **grades** their result (coverage, flow, the running-example thread are course-level rubric dimensions, FR-009) rather than producing it | ✅ N/A (graded, not produced) |

**No violations.** Complexity Tracking is empty. The NON-NEGOTIABLE principles (I, II) are the ones
this spec most directly operationalizes — the rubric and the traceability check are their mechanical
embodiment.

**Post-design re-check (after Phase 1)**: re-evaluated after `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md`. The four deterministic tools are the *minimum* needed to make the
0-exception SCs mechanical (justified in `research.md` R1); the two-`.claude`-home split and the
shared-`sn_resolve` reuse keep the design inside the frozen-template / one-rubric / single-resolver
model — no new principle tension introduced. Gate still ✅ Pass.

## Project Structure

### Documentation (this feature)

```text
specs/course-factory/004-grading-delivery/
├── spec.md              # Clarified feature spec (input)
├── plan.md              # This file
├── research.md          # Phase 0 — the tool/judgment split, shared-primitive reuse, 000/002/003 seam decisions
├── data-model.md        # Phase 1 — Rubric, Scorecard, Verdict, Insight, ComparisonReport entities + the schemas
├── quickstart.md        # Phase 1 — validate US1–US4 against the shared fixtures (mechanical SCs + scenario SCs)
├── contracts/           # Phase 1 — the seams 000/001/002/003 and the factory consume
│   ├── rubric-grading-semantics.md   # US1: the grading layer over 000's shape + the pass predicate (producer side of 003's rubric-gate.md)
│   ├── citation-traceability.md      # US2: 004's CANONICAL grounding contract; sn_resolve.py implements it; 002/003 consume
│   ├── course-evaluator.md           # US2: scorecard schema + independent course-level verdict + forward-diff-on-gap
│   ├── course-report.md              # US2: COURSE_REPORT.md structure + the delivery-gate semantics (generation, not verdict)
│   ├── insights-harvest.md           # US3: insights/ digest form + the two user-invoked paths + append-only rules
│   └── comparison.md                 # US4: proposed-revision output + the minimal adoption protocol (re-stamp via 000)
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

The deliverable spans **two `.claude/` homes** plus the shared `tools/` layer and two factory-level
knowledge folders. Concrete target layout (annotated with the owning user story and the SC each piece
makes mechanical):

```text
course-factory/course-template/                   # THE FROZEN TEMPLATE (000 distills; 004 fills grading behavior) — copied into each course, never mutated
├── rubric.md                                      #   US1: 004 fills the GRADING SEMANTICS (scale, per-dim thresholds, weights, hard-gate rule) into 000's two-layer SHAPE; carries the rubric/template version (FR-001/004/005)
└── .claude/
    ├── agents/
    │   └── course-evaluator.md                    #   US2: applies the rubric (scores dims), exhaustive [Sn] traceability (imports sn_resolve), honors mentor-added, INDEPENDENT course-level verdict, emits the scorecard (FR-006/007/008/009)
    └── commands/
        └── course-report.md                       #   US2: writes COURSE_REPORT.md from the scorecard; distinct from FEEDBACK.md; delivered at ANY verdict (FR-011/012/013). 000 distills the shell; 004 owns the contents

course-factory/tools/                             # deterministic, SC-critical mechanical ops (stdlib Python) — APPEND to 001/002/003's existing tools/, never a rival dir
├── rubric_gate.py                                 #   US1: the PASS PREDICATE — every dim ≥ its threshold, no aggregate masking; retains per-dim scores (FR-004, SC-010). SHARED: 003's lesson gate + 004's course-evaluator use this ONE predicate (003's rubric-gate.md already names 004 the owner)
├── single_rubric_lint.py                          #   US1/US4: enumerate quality definitions → assert EXACTLY ONE rubric; 0 rivals (FR-001/019, SC-001/008/009)
├── course_trace.py                                 #   US2: the EXHAUSTIVE course-wide [Sn] sweep — a THIN layer over the shared sn_resolve (extract every key across all lessons + syllabus → resolve each → findings), NOT a rival resolver; analogous to 003's per-lesson citation_trace.py (FR-007, SC-004)
├── harvest.py                                      #   US3: append-only insights/ mechanics — append, no-op on empty, no clobber, dedup-safe (FR-017, SC-007). The DISTILLATION is the agent's; the append MECHANICS are the tool's
└── README.md                                       #   UPDATE 001/002/003's existing file — append the 004 tools + the shared-sn_resolve/rubric_gate reuse notes. Do NOT create a second README

course-factory/.claude/                           # THE FACTORY'S OWN engine (cross-course) — 001's home; 004 appends the harvest + comparison surfaces
├── commands/
│   ├── insight-capture.md                         #   US3: user-triggered per-insight capture → one insights/ entry on demand (FR-015)
│   ├── harvest-feedback.md                         #   US3: setup-retro-style bulk harvest — distill a course's FEEDBACK.md, append via harvest.py (FR-015/017)
│   └── compare-course.md                           #   US4: run comparison/ on an external course → proposed rubric revision(s) + per-course /improve-course report (FR-018)
└── agents/
    └── comparison-analyst.md                       #   US4: external-course analysis persona; REUSES 002's research discipline (weigh reliability → cite → converge/budget), not a third method (Assumptions)

course-factory/insights/                          # US3: the append-only cross-course digest — STARTS EMPTY (Principle XII); topic-organized .md, each entry dated + sourced to its course
└── README.md                                       #   fixes the form (append-only, directory-shaped, empty-is-valid); no seeded corpus

course-factory/comparison/                         # US4: external-course analyses → proposed rubric revisions (never a rival) + per-course /improve-course reports
└── README.md                                       #   fixes the output shape + the minimal adoption protocol (human review → re-stamp via 000's rubric-only path)

course-factory/tests/                             # pytest + fixtures — REUSE 003's shared fixtures; add only 004-specific ones
├── fixtures/
│   ├── rubric/                                    #   REUSE 003's minimal rubric fixture (per-dim thresholds) — the pass-predicate + single-rubric target
│   ├── sources/                                   #   REUSE 003's/002's SOURCES.md fixture — the [Sn] resolution target
│   ├── lessons/                                   #   REUSE 003's lesson fixtures (fully-cited, unresolvable-[Sn], mentor-added, silently-ungrounded)
│   ├── course/                                    #   NEW: a finished-course fixture — all lessons pass + INCOMPLETE arc coverage (the SC-011 independent-verdict scenario)
│   ├── feedback/                                  #   NEW: FEEDBACK.md fixtures — populated, empty (no-op), and a two-course pair (no-clobber)
│   └── external-course/                           #   NEW: a well-made external-course stand-in for the comparison scenario
├── test_rubric_gate.py                            #   SC-010 (masking rejected; all-clear only when every dim ≥ threshold)
├── test_single_rubric_lint.py                     #   SC-001/008/009 (a planted rival fails; exactly one rubric passes)
├── test_course_trace.py                           #   SC-004 (exhaustive: unresolvable [Sn] flagged; mentor-added not failed; thin-grounding preserved) — over the SHARED sn_resolve
└── test_harvest.py                                #   SC-007 (empty = no-op; two courses = no clobber; append-only)
```

**Structure Decision**: A frozen-template quality asset + two `.claude/` judgment surfaces (the
**template's** course-evaluator/report shipped in each course; the **factory's** harvest/comparison
running across courses) over a **thin** `tools/` layer that mechanizes exactly the four 0-exception
SCs — the same hybrid split 001/002/003 use. **Three sharing decisions keep "one definition of
quality" structural, not conventional:** (1) the `[Sn]` resolver is the **one** `sn_resolve.py` (003
builds it; 004 imports it — never a rival, mirroring 003's own reuse note); (2) the **pass predicate**
is the **one** `rubric_gate.py` that both 003's lesson gate and 004's course-evaluator apply (003's
`rubric-gate.md` already names 004 the owner of the dimensions/thresholds/scale); (3) the rubric
itself is enforced-singular by `single_rubric_lint.py`. **Priority-phased delivery, per the spec's
"Plannable increments" framing:** US1 (rubric core + pass predicate) is the independently-shippable
increment that unblocks 003 and is built at the `004-rubric-core` slot **before** 003; US2 (evaluator
+ report), US3 (harvest), US4 (comparison) build at the `004-delivery` slot **after** 003, on their
own schedule, without re-planning US1. `courses/<name>/` is 001's runtime staging (not this
deliverable's tree); `insights/` and `comparison/` start as empty, form-fixing folders 004 owns.

## Complexity Tracking

> No Constitution Check violations — this section intentionally left empty. The deterministic tool
> layer is justified in `research.md` (R1) as the minimum required to make the 0-exception SCs
> (SC-001/004/007/008/009/010) mechanical rather than agent-judged, not as added abstraction. Its
> honesty boundary (the tools guarantee the *predicate*, the *resolution*, the *append*, and the
> *single-rubric enumeration*; the agent still supplies the *dimension scores*, the *course-level
> judgment*, and the *distillation* those tools operate on) is stated plainly in `research.md`
> (R1/R3), not hidden.
