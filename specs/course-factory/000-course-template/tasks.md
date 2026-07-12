---
description: "Task list for Course-Template Distillation"
---

# Tasks: Course-Template Distillation

**Input**: Design documents from `specs/course-factory/000-course-template/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: This spec requests **no code tests** (TDD not asked for). Its acceptance is **artifact
inspection + one agent-performed paper-walkthrough** — captured as validation tasks that map to the
`quickstart.md` checks and the spec's Success Criteria. No pytest suite unless the optional
neutrality scanner is scripted (T-P3).

**Organization**: Tasks grouped by the spec's four user stories. This is a **distillation/authoring
run**, not a software build — "file path" below is the artifact the task produces under
`course-factory/course-template/`. `$REF` = `${COURSE_FACTORY_REFERENCE_DIR:-/home/barak/System_Design_SelfLearn}`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: US1–US4 (setup/foundational/polish carry no story label)

---

## Phase 1: Setup (Shared Prerequisites)

**Purpose**: Confirm inputs exist and stand up the empty deliverable skeleton.

- [ ] T001 Verify `specs/course-factory/000-course-template/research-digest.md` is present and substantive; **halt the run if absent** (FR-005). Confirm the reference course is reachable at `$REF/.claude` (FR-001).
- [ ] T002 Inventory every reference asset under `$REF/.claude` (4 agents, 10 commands, 1 hook, 5 skills, `settings.json`, `setup-backlog.md`, `$REF/CLAUDE.md` = 23) into the row skeleton (path + type only) of `course-factory/course-template/CLASSIFICATION.md`.
- [ ] T003 [P] Create the deliverable skeleton: `course-factory/course-template/` with `.claude/{skills,commands,agents}/`, `profiles/default/`, and empty `VERSION`, `manifest.yaml`, `neutrality-terms.txt`, `CLASSIFICATION.md`.

**Checkpoint**: Inputs verified, empty template tree exists.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared artifacts every user story writes into. **⚠️ No story work begins until these exist.**

- [ ] T004 Seed `course-factory/course-template/neutrality-terms.txt` with the known SD terms (`System Design`, `HomeOS`, `patterns_v1`, `capacity`, `QPS`); document that the list **grows** as classification catches new topic wording (FR-020, data-model E6).
- [ ] T005 Establish the `CLASSIFICATION.md` table schema — columns `asset_path · asset_type · verdict · rationale · provenance · neutralized · target` (data-model E1); one table, not two ledgers (FR-006/FR-019). Rationale format follows the `mentor-research` discipline (research D5).
- [ ] T006 [P] Establish the `manifest.yaml` skeleton with `version / core / profiles / modules` keys per [`contracts/template-manifest.md`](contracts/template-manifest.md) (leave members empty for now).

**Checkpoint**: Denylist seeded, classification table + manifest scaffolds ready.

---

## Phase 3: User Story 1 - Distill a topic-neutral, tiered template (Priority: P1) 🎯 MVP

**Goal**: Classify all 23 assets, strip topic-specifics from kept ones, and sort survivors into a
small mandatory core + the profile mechanism + a default profile + opt-in modules — grounded in the
research, not in the unvalidated reference.

**Independent Test**: `quickstart.md` Checks 1, 2, 5 pass — every asset classified with rationale +
provenance (0 unclassified), core scans clean against the denylist, and the 2-topic paper-walkthrough
produces a viable course shape from the core alone.

### Classification (every asset gets a verdict — FR-006)

- [ ] T007 [US1] Classify the **4 agents** (`course-evaluator`, `curriculum-architect`, `lesson-consistency-reviewer`, `socratic-mentor`) — apply the critical-thinking filter + research cross-check, record verdict + rationale + provenance rows in `CLASSIFICATION.md`. Note the `lesson-consistency-reviewer` **split** (generic → core, diagram-existence → diagrams module, phase-language + patterns-drift → drop) per FR-010/FR-011.
- [ ] T008 [US1] Classify the **10 commands** into `CLASSIFICATION.md`: `improve-course`/`new-lesson`/`course-report` → core; `add-diagram` → diagrams module; `new-sd-lesson`/`review-pattern-impl` and other SD-specifics → drop or merge; `setup-retro` → **excluded as factory build-tooling** (FR-021), recorded as a verdict.
- [ ] T009 [US1] Classify the **5 skills** into `CLASSIFICATION.md`: `pattern-lesson-format` + `system-design-curriculum` → **merge** their shared lesson-arc into one core asset (FR-008); `course-quality-rubric` → core (shape, US3); `architecture-diagrams` → diagrams module; `design-pattern-catalog` → pattern-catalog module.
- [ ] T010 [P] [US1] Classify the remaining assets (`settings.json`, `setup-backlog.md`, `$REF/CLAUDE.md`, the hook `lesson_diagram_reminder.py`) into `CLASSIFICATION.md` — most are SD/build-specific → drop or module, each with a recorded rationale (FR-006).

### Author the mandatory core (FR-010, topic-neutral)

- [ ] T011 [US1] Author the **backward-design backbone** (outcomes → assessment/evidence → learning experiences) as a core skill in `course-factory/course-template/.claude/skills/backward-design/SKILL.md`, grounded in the research digest (UbD/Merrill/Gagné), topic-neutral.
- [ ] T012 [US1] Author the **canonical lesson arc** (framing → activation → demonstration → practice+feedback → integration/transfer) as `.../.claude/skills/lesson-arc/SKILL.md`, merged from the two reference skills, all SD/HomeOS/patterns_v1 wording stripped (FR-007/FR-008).
- [ ] T013 [US1] Author the **topic-neutral lesson-consistency check** (arc-order, running-example consistency, numbering, file:line findings ranked Critical/Warning/Nit) as `.../.claude/agents/lesson-consistency-reviewer.md`, generalized per the T007 split (FR-010).
- [ ] T014 [P] [US1] Bring the **core commands** into `.../.claude/commands/` — `improve-course.md`, `new-lesson.md`, `course-report.md` — topic-neutralized (FR-010).

### Profiles & modules (mechanism + MVP default; SD-specifics demoted)

- [ ] T015 [US1] Author the **profile mechanism + `default` profile** (theory/linear-spiral) in `course-factory/course-template/profiles/default/` — sets macro spine, theory-first entry point, advisory-checkpoint placement, granularity; reuses core invariants, redefines none (FR-022/FR-024/FR-025).
- [ ] T016 [P] [US1] Build the **optional modules** under `.../.claude/` — `diagrams` (inherits the diagram-existence check, FR-011), `katas`, `pattern-catalog`, `socratic` — each self-contained with empty `depends_on` toward core (FR-011/FR-012).

### Neutrality gate & MVP validation

- [ ] T017 [US1] Run the **neutrality gate** over the mandatory core against `neutrality-terms.txt`; grow the term list for any new topic wording caught; require **0** hits in core paths before proceeding (FR-020, quickstart Check 2). Set every kept-core row's `neutralized = true`.
- [ ] T018 [US1] **2-topic paper-walkthrough** (agent-performed, no pipeline): for *Introduction to Psychology* and *Python Programming* (no-prior-programming), with all modules off, sketch outcomes → assessment → one-lesson arc → rubric-checkable draft; record as a checklist file in the feature folder (SC-003, quickstart Check 5).

**Checkpoint**: MVP template — core + mechanism + default profile + modules — exists, scans neutral, and drives both sample topics on paper. **This is the shippable increment.**

---

## Phase 4: User Story 2 - Freeze and version-stamp the template (Priority: P2)

**Goal**: Make the template a frozen, self-describing, semver-stamped artifact 001 can copy and
drift-check.

**Independent Test**: `quickstart.md` Check 4 passes — `manifest.yaml` version == `VERSION`, exactly
one default profile, every manifest path has a `CLASSIFICATION.md` target, and the drift simulation
flags a bumped stamp.

- [ ] T019 [US2] Write `course-factory/course-template/VERSION` = `1.0.0` (semver); document bump semantics (full re-distillation → MAJOR; rubric-only re-stamp → MINOR/PATCH) per [`contracts/version-stamp.md`](contracts/version-stamp.md) (FR-016).
- [ ] T020 [US2] Complete `manifest.yaml` self-description — populate `core`, `profiles.default` (`default: true`), and `modules.*` (each `depends_on: []` toward core), every path matching a `CLASSIFICATION.md` `target` (FR-018, contract invariants 1–5).
- [ ] T021 [US2] **Drift-check simulation**: record the current `VERSION`, bump it, confirm a recorded-vs-current string compare flags the mismatch (SC-006, quickstart Check 4); confirm the template tree is otherwise byte-frozen (US2 AC-4 / FR-017).

**Checkpoint**: Template is frozen, versioned, and self-describing — ready for 001 to copy.

---

## Phase 5: User Story 3 - Shape the quality rubric as one-rubric-two-layers (Priority: P3)

**Goal**: The rubric asset is a 5-dimension generic core + requestable add-on slots, shape only,
grading deferred to 004.

**Independent Test**: `quickstart.md` Check 3 passes — core layer holds exactly the 5 dimensions, SD
checks are add-ons, and the asset states weights/thresholds are 004's.

- [ ] T022 [US3] Author the **rubric core** — exactly the 5 dimensions (Technical Correctness, Grounding/No-Fabrication, Pedagogical Flow, Coverage, Practicality) — as `.../.claude/skills/quality-rubric/SKILL.md`, recorded with the **"adopted on judgment"** flag since the digest is silent on rubrics (FR-013, research D8); this is the canonical list 004 FR-001 references.
- [ ] T023 [US3] Express the reference rubric's **SD-specific checks** (fabricated-capacity, cargo-cult) as **requestable topic add-on slots**, never core dimensions (FR-014, SC-005).
- [ ] T024 [US3] State in the rubric asset that **weights, per-dimension thresholds, and hard-gate / no-aggregate-masking semantics are owned by spec 004** and MUST NOT be fixed here (FR-015); confirm `VERSION` is the rubric's sole version identity (FR-016 ↔ 004 FR-005).

**Checkpoint**: Rubric shape is set; grading semantics cleanly deferred to 004.

---

## Phase 6: User Story 4 - Ship the structurally-consequential profiles as later increments (Priority: P4)

**Goal**: Add PBL/CBL, CBE/mastery, and guided-inquiry as **separate, later, independent**
increments. **⚠️ NOT part of the MVP** — none blocks a first course; each ships and validates on its
own (FR-023, User Story 4). Do these only when real course demand calls for them.

**Independent Test**: With only the MVP shipped, a course still generates from `default` alone; then
each profile independently reconfigures the spine (FR-022), reuses core invariants (FR-024), and
passes its own 2-topic walkthrough (SC-012) — without the other two existing.

- [ ] T025 [P] [US4] Author the **PBL/CBL** profile (problem-first sequencing) under `profiles/pbl-cbl/`; add to `manifest.yaml`; validate independently via the SC-012 walkthrough (FR-023, US4 AC-2).
- [ ] T026 [P] [US4] Author the **CBE/mastery** profile (units around competencies + advisory mastery checkpoints) under `profiles/cbe-mastery/`; add to `manifest.yaml`; validate independently (FR-022/FR-023, US4 AC-3).
- [ ] T027 [P] [US4] Author the **guided-inquiry/Socratic** profile (minimum-guidance scaffolding for novices) under `profiles/guided-inquiry/`; add to `manifest.yaml`; validate independently (FR-022/FR-023, US4 AC-4).

**Checkpoint**: At full delivery the template ships ≥4 profiles, each reusing the one core (SC-011).

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Full-spec validation and auditability.

- [ ] T028 Run the **full `quickstart.md` validation** (Checks 1–6): classification completeness (SC-001/007/009), neutrality (SC-002), rubric shape (SC-005), manifest+version (SC-006/004), 2-topic walkthrough (SC-003/012), digest-dependency + no-forked-templates (SC-010/011).
- [ ] T029 [P] **Optional**: script the neutrality gate as `course-factory/tools/neutrality_scan.py` (stdlib) with a small pytest, if a repeatable scan is wanted over the manual `grep` recipe (research D4).
- [ ] T030 **Provenance audit**: confirm **100%** of template pieces record provenance to a reference asset, a research source, or `new` — 0 unexplained pieces (SC-007); confirm 0 pieces kept "solely because SD had it" (SC-009).

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (P1)** → no deps, start immediately.
- **Foundational (P2)** → depends on Setup; **blocks all user stories** (they all write into `CLASSIFICATION.md`, `manifest.yaml`, `neutrality-terms.txt`).
- **US1 (P3)** → the MVP; depends only on Foundational.
- **US2 (P4)** → depends on US1 (versions/manifests the pieces US1 produced).
- **US3 (P5)** → depends on Foundational; the rubric core (T022) is referenced by US1's walkthrough, so ideally land T022 alongside US1, but it is independently testable.
- **US4 (P6)** → **later increments**, depend on US1's mechanism+default; each of T025/T026/T027 is independent of the other two.
- **Polish (P7)** → depends on all desired stories complete.

### Within each story

- Classify (T007–T010) before authoring the pieces those verdicts create.
- Author core (T011–T014) before the neutrality gate (T017).
- Neutrality gate (T017) before the MVP walkthrough (T018).

### Parallel opportunities

- T003 (skeleton) ∥ input verification.
- T010 classification ∥ T007–T009 (different asset groups, same file — coordinate row appends).
- T014 core commands ∥ T011–T013; T016 modules ∥ core authoring.
- T025 ∥ T026 ∥ T027 — the three later-increment profiles are fully independent.

---

## Implementation Strategy

### MVP first (User Story 1 only)

1. Phase 1 Setup → 2. Phase 2 Foundational → 3. Phase 3 US1 → **STOP and validate** (quickstart
   Checks 1, 2, 5). A neutral, tiered template that drives both sample topics on paper is the MVP.

### Incremental delivery

1. Setup + Foundational → skeleton ready.
2. **US1 → MVP** (core + mechanism + default + modules), validate, ship.
3. **US2** → freeze + version, so 001 can copy it.
4. **US3** → rubric two-layer shape (land T022 early — US1's walkthrough leans on it).
5. **US4** → PBL/CBL, CBE/mastery, guided-inquiry as demand appears, each independently.
6. **Polish** → full quickstart + provenance audit.

---

## Notes

- [P] = different files / independent. Classification rows share `CLASSIFICATION.md`, so append-coordinate.
- This is authoring, not coding — most "tasks" produce Markdown/YAML assets, not code.
- The only optional code is `neutrality_scan.py` (T029), stdlib + pytest per repo convention.
- US4 is deferred by design — do not treat it as MVP scope (FR-023).
- Once 001 exists, re-run quickstart Checks 3–5 by driving the real pipeline; the paper-walkthrough is a pre-pipeline proxy.
