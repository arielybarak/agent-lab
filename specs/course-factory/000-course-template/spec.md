# Feature Specification: Course-Template Distillation

**Feature Branch**: `000-course-template`

**Created**: 2026-07-10

**Status**: Draft

**Input**: User description: "Distill the frozen, versioned, tiered `course-template/` asset from the hand-built `System_Design_SelfLearn/.claude/` reference course — course-factory roadmap task #1 and the foundational prerequisite behind spec 001's copy/overlay/version contract (001 FR-001). Classify every reference asset (KEEP-as-generic-core / DEMOTE-to-optional-module / DROP), strip every System-Design / HomeOS-Cloud / patterns_v1 specific, sort the survivors into a small mandatory core plus opt-in optional modules per constitution Principle IX, keep the rubric to the one-rubric-two-layers model (Principle VIII), and freeze + version-stamp the result so instantiation copies but never mutates it."

## Overview

This is the **foundational asset** for the course factory — **roadmap task #1** in
`course-factory/DESIGN.md` — and the hard prerequisite that spec 001's copy/overlay/version
contract depends on (001 FR-001). Specs 001–004 explicitly treat the **pedagogical content** of
`course-template/` as out of scope; **this spec owns producing that content.** It has no number
peer among 001–004 because it precedes them — hence `000`.

It owns three joined subjects:

1. **Sourcing & critical filtering (the inputs)** — gather teaching ideas from **two** kinds of
   source: the reference course `System_Design_SelfLearn/.claude/` **and** an **external research
   digest** (see the reliability warning below). The reference course is an **unvalidated** artifact,
   so nothing is inherited from it by authority — every idea taken from it MUST pass a
   **critical-thinking filter** and be **cross-checked against the external research** (Principle III,
   "Mentor, Not Aggregator" / weigh reliability, not existence).
2. **Distillation into a three-tier template (the extraction)** — reverse-engineer the topic-neutral
   teaching machinery from the critically-filtered ideas and sort it into **three tiers**: a **small
   mandatory core** (the evidence-invariant backbone + lesson arc + feedback loops), a set of
   **archetype profiles** (evidence-based configurations of that core for structurally-different
   course types) — the **initial ship set** is **default** (theory / linear-spiral) plus the three
   research-flagged structurally-consequential paradigms, **PBL/CBL, CBE/mastery, guided-inquiry**
   (FR-023); **procedural/code** is a candidate profile for a **later increment**, not part of the
   initial ship set (see Assumptions) — and **opt-in optional modules** (add-ons like katas,
   diagrams, retrieval packs). Classify every reference asset
   (agents, commands, skills, hooks) as **keep-as-core / demote-to-module / drop** and strip every
   System-Design / HomeOS-Cloud / `patterns_v1` specific from anything kept (Principle IX, extended
   with profiles per the research digest below).
3. **Freeze & version (the artifact)** — emit the result as a **frozen, version-stamped** template
   directory that instantiation (001) copies and specializes **by overlay, never by mutation**
   (Principle V), and that is **self-describing** about which pieces are core, which profile is
   selected, and which optional modules are enabled.

> **⚠️ The reference course is NOT a proof-of-concept and NOT a reliable reference.**
> `/home/barak/System_Design_SelfLearn/` was **never delivered to or validated by a real learner /
> customer**, so its structure carries **no evidence** that it teaches well. Treat it strictly as a
> **source of ideas to weigh with critical thinking**, never as a proven template to copy. It MUST
> **not** be the sole reference: this spec pairs it with an **external research digest** (a
> Perplexity-style search saved as an `.md` in this feature folder) on how strong, topic-neutral
> course templates and quality rubrics are actually structured, and where the two disagree the
> **better-grounded** guidance wins. Its root `.claude/` (agents/commands/skills/rubric) is the
> starting *idea pool*, not the answer (DESIGN § "Reference: the course we're generalizing from").

**Research grounding (the tiering model).** The external research digest —
[`research-digest.md`](research-digest.md) — resolves the "one template vs many" question: the
evidence (UbD / backward design, Merrill's First Principles, Gagné, cognitive-load theory, PBL/CBE
meta-analyses) shows a **strong invariant core** with macro-structures acting as **configurable
profiles of that core, not separate species** — so the template is **one core + evidence-based
profiles + optional modules**, *not* siloed per-subject templates. Three paradigms are flagged
**structurally consequential** and MUST be true profiles rather than mere module toggles:
**PBL/CBL**, **CBE/mastery** (they reorganize units around competencies + mastery checkpoints), and
**guided-inquiry/Socratic** (it changes required scaffolding — minimal guidance underperforms for
novices).

> **No enforcement — the factory emits static course content.** A profile canNOT *lock* or *gate* a
> learner's progress (there is no runtime to enforce it, and we don't want to block the user). The
> strongest a profile may embed is an **advisory checkpoint note** — e.g., "*recommended: pass this
> check before continuing*". So what actually differs between profiles is the **content
> organization, sequencing, scaffolding depth, and the placement/frequency of (advisory)
> checkpoints** — never a hard gate.

### Out of Scope (owned by other specs / assets)

- **The copy / overlay / version-check contract at build time** — how instantiation copies the
  frozen template, applies the overlay, includes enabled modules, stamps and later diffs the
  version. This spec produces the **artifact and its version stamp**; consuming them is 001
  (FR-006/007). → **001**
- **The rubric's grading engine** — weights, per-dimension pass thresholds, the hard-gate /
  no-aggregate-masking semantics, and the course-evaluator internals. This spec fixes only the
  rubric asset's **two-layer shape** (core dimensions + add-on slots); its grading behavior is
  owned by 004. → **004**
- **Syllabus research method** (web / `gh` / course-platform search → `SOURCES.md`) → **002**.
- **The lesson author–critic worker pool and fake-student check** → **003**.
- **The factory's own build `.claude/`** — the pipeline commands + build agents that *run* the
  phased loop (DESIGN roadmap task #2) are a **distinct** `.claude/` from the template this spec
  produces; the two MUST NOT be conflated (constitution § Structural Constraints). → **001**,
  produced as that spec's `/speckit-plan` + `/speckit-tasks` implementation deliverable, not a
  separate spec (see 001's Assumptions).
- **`meta-env-setup/` involvement** — it is **lineage / scoring tooling only** (`validate_claude_setup.py
  --score` to *improve the template later*), never a build-time dependency of *producing* it
  (DESIGN § "Relationship to meta-env-setup").

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Distill a topic-neutral, tiered template from critically-filtered, research-backed ideas (Priority: P1)

A factory maintainer feeds the distillation **both** the reference course `System_Design_SelfLearn/.claude/`
**and** the external research digest (`.md` in this feature folder). Ideas from the **unvalidated**
reference course are taken only after a **critical-thinking filter** and a **cross-check against the
research** — never inherited just because SD happened to have them. Every reference asset is then
classified **keep-core / demote-module / drop** with a recorded rationale that cites the critical
judgment or the research; each asset kept in the core has all System-Design / HomeOS-Cloud /
`patterns_v1` specifics stripped; and the survivors are sorted into a **small mandatory core**
(syllabus, lesson arc, quality rubric, `/improve-course`, `/new-lesson`) plus **opt-in optional
modules**. Out comes a `course-template/` whose mandatory core carries **no topic assumptions** and
whose shape is **grounded in the research, not in one untested course**.

**Why this priority**: This is the MVP. Nothing downstream can run without a topic-neutral,
tiered template to copy — 001's whole contract is "copy *this*." Built alone it delivers the core
value: a reusable teaching skeleton that no longer assumes System Design **and** does not rest on an
unvalidated reference. Independently demonstrable by inspecting the produced template.

**Independent Test**: Run the distillation against the reference `.claude/` **and** the research
digest; confirm every reference asset has a classification verdict + rationale, and that each
**kept** element records a critical-thinking / research-cross-check justification (no element kept
solely because SD had it); confirm the mandatory core contains zero topic-specific terms (scan for
"System Design", "HomeOS", "patterns_v1", "capacity estimation"); confirm the core covers the
backward-design backbone, lesson arc, feedback loops, rubric, `/improve-course`, `/new-lesson`,
`/course-report`;
confirm the SD-specific capabilities appear only as optional modules or profiles, never in the core;
and confirm the shipped archetype profiles are configurations over the one core, not forked
templates.

**Acceptance Scenarios**:

1. **Given** the reference `.claude/` (every agent, command, skill, hook, and other file it contains
   — FR-006) **and** the research digest, **When** the distillation runs, **Then** every asset
   receives a recorded verdict of keep-core / demote-module / drop with a rationale grounded in
   critical judgment and/or the research — **not** in "SD already had it."
2. **Given** an idea present in the reference course but **contradicted or unsupported** by the
   research, **When** it is evaluated, **Then** it is dropped or explicitly flagged as unvalidated,
   never silently carried into the template.
3. **Given** an asset kept in the core (e.g., the quality rubric), **When** it is inspected, **Then**
   it carries no System-Design / HomeOS-Cloud / `patterns_v1` wording and reads topic-neutrally.
4. **Given** the produced template, **When** its tiers are listed, **Then** a small mandatory core
   (backbone, lesson arc, feedback loops, quality rubric, `/improve-course`, `/new-lesson`,
   `/course-report`) is present, the **archetype profiles** (PBL/CBL, CBE/mastery, guided-inquiry, +
   default) are present
   as configurations over that one core, and the SD-specific capabilities (katas, diagrams,
   pattern-catalog) are optional modules — **not** siloed per-subject templates.
5. **Given** a course type that needs problem-first sequencing with mastery checkpoints, **When** the
   matching profile is selected, **Then** it reconfigures the macro spine + checkpoint placement
   (advisory notes, not enforced) **without** redefining or bypassing any core invariant (backbone,
   lesson arc, feedback loops, rubric core).
6. **Given** two reference assets that encode the same generic capability after neutralization
   (e.g., `pattern-lesson-format` and `system-design-curriculum` both carrying a "lesson arc"),
   **When** they are distilled, **Then** the shared capability lands as **one** core asset rather
   than duplicated.

---

### User Story 2 - Freeze and version-stamp the template as a copyable, immutable artifact (Priority: P2)

The produced template is emitted as a **frozen, version-stamped** directory. It carries a version
identifier a copy can record and later compare against, and it is **self-describing** about which
pieces are mandatory vs optional so instantiation can honor a module selection. Specialization is by
overlay; the template itself is never edited per course.

**Why this priority**: The freeze + version stamp is what makes the template safe to copy across
many courses and lets 001 detect version drift on resume. It builds on the US1 artifact and turns it
into a durable, copyable contract. Testable on its own against the produced template.

**Independent Test**: Inspect the produced template; confirm it carries a version stamp; confirm a
manifest (or equivalent self-description) marks each piece mandatory vs optional; simulate a copy
recording the stamp, bump the template version, and confirm the stamp comparison flags the mismatch.

**Acceptance Scenarios**:

1. **Given** the produced template, **When** it is inspected, **Then** it carries a single version
   identifier (stamp) that uniquely names this distillation snapshot.
2. **Given** the template, **When** its self-description is read, **Then** every piece is marked
   mandatory (core) or optional (module), enabling a downstream module selection without guessing.
3. **Given** a recorded copy stamp and a later template whose version differs, **When** the two are
   compared, **Then** the mismatch is detectable (supporting 001's drift check).
4. **Given** any number of downstream builds, **When** the source template is inspected afterward,
   **Then** it is byte-for-byte unchanged (overlay, not mutation — Principle V).

---

### User Story 3 - Shape the quality rubric as one-rubric-two-layers (Priority: P3)

The template's quality-rubric asset is structured as **one rubric, two layers**: a generic **core**
(Technical Correctness, Grounding / No-Fabrication, Pedagogical Flow, Coverage, Practicality) plus
**requestable topic add-ons**. The reference course's SD-specific checks (fabricated capacity
numbers, cargo-cult "just add X") become **add-ons**, not core dimensions — and the rubric asset
fixes only the *shape*, leaving grading weights and thresholds to spec 004.

**Why this priority**: The rubric is the seam every later spec leans on (the gate in 003, the engine
in 004). Getting its two-layer shape right in the template — generic core, topic specifics demoted
to add-ons — is what lets the same template grade a math course and a systems course. Separable and
inspectable on the produced rubric asset alone.

**Independent Test**: Inspect the template's rubric asset; confirm its core layer holds exactly the
five generic dimensions; confirm every SD-specific check is expressed as an add-on slot, not a core
dimension; confirm the asset defines shape only and states that weights/thresholds/hard-gate
semantics are owned by 004.

**Acceptance Scenarios**:

1. **Given** the template's rubric asset, **When** its core layer is read, **Then** it holds exactly
   the five generic dimensions (Technical Correctness, Grounding / No-Fabrication, Pedagogical Flow,
   Coverage, Practicality) and no topic-specific dimension.
2. **Given** the reference rubric's SD-specific checks (capacity-number fabrication, cargo-cult),
   **When** they are distilled, **Then** they appear as **requestable topic add-ons**, selectable per
   course, not baked into the core.
3. **Given** the produced rubric asset, **When** it is inspected for grading behavior, **Then** it
   defines the two-layer **shape** only and defers weights, per-dimension thresholds, and the
   hard-gate rule to spec 004.

---

### User Story 4 - Ship the structurally-consequential profiles as later, independent increments (Priority: P4)

After the MVP (core + profile mechanism + default profile, User Story 1) ships, the three
research-flagged structurally-consequential profiles — **PBL/CBL**, **CBE/mastery**, and
**guided-inquiry/Socratic** — are validated and shipped as separate, later increments. Each is
independently plannable and testable; none blocks another, and none is required before a first course
can be generated from the default profile alone.

**Why this priority**: FR-023 originally required all three before any course had ever been
generated — three paradigms no course had yet requested, each needing its own SC-012 sample-topic
validation. Phasing them out of the MVP keeps the settled one-core+profiles model intact while
letting the factory validate against real course demand instead of speculative upfront coverage.

**Independent Test**: With only the MVP (core + mechanism + default) shipped, confirm a course can
already be generated end-to-end (US1's own test). Then, for each of PBL/CBL, CBE/mastery, and
guided-inquiry independently: confirm the profile reconfigures the macro spine per FR-022, reuses the
core invariants per FR-024, and passes its own SC-012 sample-topic validation — without needing the
other two profiles to exist.

**Acceptance Scenarios**:

1. **Given** only the MVP profile set (mechanism + default) shipped, **When** a course is generated,
   **Then** it succeeds using the default profile alone — no later-increment profile is a hidden
   dependency of the MVP.
2. **Given** the **PBL/CBL** profile is validated and shipped, **When** a matching sample topic
   selects it, **Then** it reconfigures the macro spine to problem-first sequencing without redefining
   a core invariant (FR-024), independent of whether CBE/mastery or guided-inquiry have shipped.
3. **Given** the **CBE/mastery** profile is validated and shipped, **When** a matching sample topic
   selects it, **Then** it reorganizes units around competencies + mastery checkpoints (advisory
   only, FR-022), independent of the other two.
4. **Given** the **guided-inquiry/Socratic** profile is validated and shipped, **When** a matching
   sample topic selects it, **Then** it applies the required minimum-guidance scaffolding for
   novices (FR-022), independent of the other two.

---

### Edge Cases

- **The reference course has a slick-looking pattern with no grounding in the research** (it exists
  only because one untested course happened to do it that way) — it is treated as **unvalidated**:
  dropped, or kept only with an explicit "unproven, adopted on judgment" flag; it is **never**
  inherited on the strength of SD's existence alone.
- **The research digest is thin, missing, or low-quality** — the distillation MUST **halt or flag**
  rather than silently fall back to treating the unvalidated reference course as authoritative; a
  template grounded only in SD is not acceptable.
- **The research contradicts the reference course** — the **better-grounded** guidance wins and the
  reasoning is recorded (weigh reliability, not the fact that SD exists — Principle III).
- **A reference asset intertwines a generic core with topic specifics** (e.g., the quality rubric
  mixes the five generic dimensions with an SD capacity-number check) — the distillation **splits**
  it: the generic part goes to the core, the specific part becomes an add-on or module; it is not
  dropped wholesale nor kept with the specifics baked in.
- **A reference asset is purely topic-specific with no generalizable core** (e.g.,
  `design-pattern-catalog`, `architecture-diagrams`) — it becomes an **optional module** or is
  dropped; it is **never** forced into the mandatory core.
- **Two reference assets overlap after neutralization** — they are **merged** into one core asset
  rather than duplicated (the "lesson arc" carried by both `pattern-lesson-format` and
  `system-design-curriculum`).
- **A future non-SD course enables none of the optional modules** — the **mandatory core alone**
  MUST still produce a viable course shape; no optional module is a hidden dependency of the core.
- **A topic assumption leaks into the mandatory core** (e.g., "estimate capacity / QPS") — the
  neutrality gate MUST catch it and reject the core as not-yet-neutral.
- **A reference asset belongs to the factory's build tooling, not a course** (e.g., a
  `FEEDBACK.md`-harvest command) — it is **excluded** from the template (it belongs to the separate
  factory build `.claude/`), and the exclusion is recorded as a verdict.
- **The reference course changes after distillation** — the template is a **snapshot**; its version
  stamp records the provenance, and re-distillation (not silent editing) is how a newer snapshot is
  produced.
- **A rubric revision proposed by `comparison/` (004 FR-018/019) is adopted after v1** — updating the
  rubric asset within `course-template/` and bumping the template's version stamp (FR-016) is a
  **narrower, rubric-only re-stamping**, not a full SD-sourced re-distillation: it records provenance
  to the `comparison/` proposal (FR-019) rather than the reference course, and does **not** require
  re-running the FR-002 critical-thinking filter over the whole reference `.claude/`.

## Requirements *(mandatory)*

### Functional Requirements

**Sourcing & critical filtering**

- **FR-001**: The distillation MUST treat `System_Design_SelfLearn/.claude/` as an **unvalidated
  source of ideas, not a proven reference** — it was never delivered to or validated by a real
  learner. It MUST be read-only (never copied wholesale or mutated), and **no** element may be
  carried into the template **solely because the reference course contains it**.
- **FR-002**: Every idea taken from the reference course MUST pass an explicit **critical-thinking
  filter** — a recorded judgment of whether it is genuinely sound pedagogy versus an untested
  artifact of one hand-built course (Principle III, weigh reliability not existence).
- **FR-003**: The distillation MUST NOT rely on the reference course as its **sole** input. It MUST
  also consume an **external research digest** (a Perplexity-style search saved as an `.md` in this
  feature folder) on how strong, topic-neutral course templates and quality rubrics are structured,
  and MUST ground the template's shape in that research — not in the reference course alone.
- **FR-004**: Where the reference course and the external research **disagree**, the distillation
  MUST favor the **better-grounded** guidance and MUST record the reasoning; SD's version does not
  win by default.
- **FR-005**: If the external research digest is **absent**, the distillation MUST **halt** — there
  is nothing to cross-check the reference course against (FR-003 requires pairing, not SD alone). If
  the digest is present but **thin or low-quality on a specific distillation subject** (structures,
  lesson arcs, invariants, or the rubric — see FR-013's rubric carve-out), the distillation MUST
  **flag** that subject as judgment-based rather than research-validated (mirroring FR-013's pattern)
  and continue — it MUST NOT halt over one thin subject when the digest is substantively useful
  elsewhere. **Minimal quality bar**: a subject counts as adequately covered if the digest devotes at
  least one distinct section to it with a citation to a named source (not a passing mention);
  anything less is "thin" for that subject.

**Classification**

- **FR-006**: The distillation MUST assign **every** reference asset — each agent, command, skill,
  hook, **and any other file in the reference `.claude/`** (`CLAUDE.md`, settings, templates, the
  rubric doc, the insights corpus, etc.) — exactly one verdict — **keep-as-generic-core**,
  **demote-to-optional-module**, or **drop** — and MUST record a rationale for each verdict that
  cites the critical judgment and/or the research (per FR-002/FR-004). **This verdict + rationale,
  together with each piece's provenance (FR-019), form one classification table** — a single
  per-asset record, not two separate ledgers.
- **FR-007**: Any asset kept in the core MUST have **all** topic-specifics removed (System Design,
  HomeOS-Cloud, `patterns_v1`, capacity/QPS estimation, and any other domain wording), leaving a
  topic-neutral capability.
- **FR-008**: When two or more reference assets encode the **same** capability after neutralization,
  the distillation MUST consolidate them into a **single** template asset rather than carrying
  duplicates.

**Tiering (Principle IX, extended with profiles)**

- **FR-009**: The template MUST be **three-tiered**: (a) a **small mandatory core**, (b) a set of
  **archetype profiles** (FR-022–FR-025), and (c) **opt-in optional modules**. It MUST be **one core
  with profiles**, **not** a set of siloed per-subject templates (research digest §5).
- **FR-010**: The **mandatory core** MUST be **topic-neutral** (usable by a course in any domain —
  math, history, … — with no System-Design assumption) and MUST hold the evidence-**invariant**
  machinery: at minimum the backward-design backbone (outcomes → assessment/evidence → learning
  experiences), the canonical lesson arc (problem/goal framing → activation → demonstration →
  practice + feedback → integration/transfer), formative-feedback loops, and the quality rubric —
  **grounded in the research digest** (UbD, Merrill, Gagné), not adopted from the reference course on
  faith — **plus** `/improve-course`, `/new-lesson`, and `/course-report` as operational tooling kept
  via the **critical-thinking filter** (FR-002) as sound practice, since the research digest does not
  independently cover command-level tooling. Neither path admits an element solely because the
  reference course had it (FR-001).
- **FR-011**: The reference course's SD-specific capabilities (katas, diagrams, Socratic teaching,
  pattern-catalog) MUST be expressed as **optional modules** (or, where structurally consequential, a
  **profile** per FR-022), never as mandatory core.
- **FR-012**: Each optional module MUST be **self-contained** — enabling or disabling it MUST NOT
  break the mandatory core, a profile, or any other module (no module is a hidden dependency of the
  core).

**Rubric two-layer shape (Principle VIII)**

- **FR-013**: The template's quality-rubric asset MUST follow **one rubric, two layers**: a generic
  **core** of exactly five dimensions — **Technical Correctness, Grounding / No-Fabrication,
  Pedagogical Flow, Coverage, Practicality** — plus a mechanism for **requestable topic add-ons**.
  This is the **canonical definition** of the core dimension list; spec 004 references it rather than
  re-deriving it (see 004 FR-001). The external research digest (FR-003) grounds the course/lesson-arc
  structure (FR-010) but does **not** independently research quality-rubric evidence — it is silent on
  rubrics, not thin. Because of that gap, the core dimension set MUST instead pass the
  **critical-thinking filter** (FR-002) and be recorded with the same **"unproven, adopted on
  judgment"** flag used elsewhere in this spec (see Edge Cases) rather than presented as
  research-validated; it MUST NOT be adopted from the reference rubric on faith either. A future
  research pass scoped specifically to course-quality rubrics MAY supersede this judgment-based
  adoption without requiring a full re-distillation (see the rubric-revision edge case under Edge
  Cases and FR-016).
- **FR-014**: The reference rubric's SD-specific checks (fabricated capacity numbers, cargo-cult
  "just add X") MUST be expressed as **topic add-ons**, selectable per course, and MUST NOT appear as
  core dimensions.
- **FR-015**: The rubric asset MUST define the two-layer **shape only**; grading weights,
  per-dimension pass thresholds, and the hard-gate / no-aggregate-masking semantics are owned by
  spec 004 and MUST NOT be fixed by this spec.

**Freeze, version & self-description (Principle V)**

- **FR-016**: The template MUST carry a **single version identifier (stamp)** that uniquely names the
  distillation snapshot and that a copy can record and later compare against. **This same stamp IS the
  rubric's version identity** (004 FR-005) — the factory maintains **one** version identity across the
  template and its rubric asset, never two independent counters.
- **FR-017**: The template MUST be a **frozen artifact**: per-course specialization happens by
  overlay (001), and the template MUST NOT be edited to serve an individual course.
- **FR-018**: The template MUST be **self-describing** about which pieces are **core**, which belong
  to each **profile**, and which are **optional modules**, so instantiation (001) can honor a profile
  choice + module selection without inferring it.

**Provenance & neutrality gate**

- **FR-019**: Every piece of the produced template MUST record its **provenance** — which reference
  asset and/or research source it derived from, or that it is newly authored. **This is the same
  per-asset record as FR-006's verdict + rationale** (one classification table, not a duplicate
  ledger) — so the distillation is auditable from a single source.
- **FR-020**: The distillation MUST apply a **neutrality gate**: it MUST verify that **no** residual
  topic-specific term remains in the mandatory core before the template is considered done. The
  gate's **term list is a maintained artifact of the distillation**, not fixed by this spec — it
  starts from the known SD-specific terms (FR-007: "System Design", "HomeOS", `patterns_v1`,
  capacity/QPS) and grows as new topic-specific wording is caught during classification; the
  maintained list ships alongside the template as part of its provenance record (FR-019) so
  re-distillation can re-run the same gate.

**Distinctness**

- **FR-021**: The produced `course-template/.claude/` MUST be **distinct** from the factory's own
  build `.claude/`; this spec produces only the template, and any reference asset that is build
  tooling (not course-teaching machinery) MUST be excluded from the template.

**Archetype profiles (research digest §5)**

- **FR-022**: The template MUST express macro-structural variation as **archetype profiles** —
  named, evidence-based configurations **over the single mandatory core** — and MUST NOT fork the
  core into separate per-subject templates. Each profile sets the macro organizing spine, the entry
  point (theory-first vs problem-first), the placement/frequency of checkpoints, and unit
  granularity. Because the factory emits **static course content**, a profile MUST NOT assume any
  runtime enforcement: it MUST NOT lock or gate learner progress — the strongest progression
  mechanism it may embed is an **advisory checkpoint note** ("recommended: pass this check before
  continuing").
- **FR-023**: The template's profile set ships in **priority-ordered increments** (User Stories 1 &
  4): **P1/MVP** — the profile **mechanism** (FR-022/FR-024/FR-025) plus a **default** profile
  (theory / linear-spiral) for concept-first courses, sufficient on its own to generate a course.
  **P4, later, independent increments** — the three profiles the research flags as **structurally
  consequential**: **PBL/CBL**, **CBE/mastery**, and **guided-inquiry/Socratic** — as true profiles
  (not mere module toggles), because each changes content organization, checkpoint placement, and/or
  the required scaffolding. Each later-increment profile MAY ship independently of the other two, in
  any order convenient to real course demand; none blocks the MVP or another increment.
- **FR-024**: Each profile MUST reuse the mandatory core's invariants (backbone, lesson arc, feedback
  loops, rubric core) and MUST only **reconfigure** the variable dimensions — a profile MUST NOT
  redefine or bypass a core invariant.
- **FR-025**: Exactly **one** profile MUST be selectable per course (an intake/overlay decision made
  by 001), and the template MUST carry a **safe default** profile so a course that names none still
  gets an evidence-grounded structure.

### Key Entities

- **Reference course** — `System_Design_SelfLearn/`, the hand-built first course; **read-only,
  UNVALIDATED source material** (never delivered to a real learner), external to the factory. Its
  root `.claude/` is an **idea pool weighed with critical thinking**, not an authoritative input.
- **External research digest** — the Perplexity-style search results (an `.md` in this feature
  folder) on how strong, topic-neutral course templates and quality rubrics are structured; the
  reliability anchor the reference course is cross-checked against, so SD is not the sole source.
- **Reference asset** — one agent, command, skill, or hook in the reference `.claude/`; the unit the
  distillation classifies.
- **Critical-thinking filter** — the recorded judgment (per idea) of whether it is genuinely sound
  pedagogy versus an untested artifact of one hand-built course; what an idea must pass before entry.
- **Classification verdict** — the per-asset decision (**keep-core / demote-module / drop**) plus its
  recorded rationale, citing the critical judgment and/or the research.
- **course-template** — the produced **frozen, versioned, three-tiered** artifact (core + profiles +
  optional modules) that instantiation (001) copies; the deliverable of this spec.
- **Mandatory core** — the evidence-invariant, topic-neutral tier present in every course: the
  backward-design backbone, the canonical lesson arc, feedback loops, quality rubric,
  `/improve-course`, `/new-lesson`, `/course-report`.
- **Archetype profile** — a named, evidence-based configuration **over the one core** that sets the
  macro spine, entry point, checkpoint placement (**advisory only — static content can't enforce
  progression**), and unit granularity; exactly one is chosen per course, with a safe default. **Not**
  a separate template. **Initial ship set**: default (theory/linear-spiral), PBL/CBL, CBE/mastery,
  guided-inquiry (FR-023); **procedural/code** is deferred to a later increment (Assumptions).
- **Optional module** — an opt-in add-on unit (katas, diagrams, Socratic drills, pattern-catalog,
  retrieval/spacing packs) a course may enable or disable independently of the core and profile.
- **Quality-rubric asset** — the template's two-layer rubric: a generic **core** of five dimensions
  plus **topic add-on** slots; shape here, grading semantics in 004.
- **Topic add-on** — a requestable, per-course rubric dimension (e.g., SD's fabricated-capacity
  check) that lives outside the generic core.
- **Template version stamp** — the single identifier naming the distillation snapshot; the anchor for
  001's later drift check.
- **Provenance record** — the mapping from each template piece back to its reference asset and/or
  research source (or "new"), making the distillation auditable.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **100%** of reference `.claude/` assets (every agent, command, skill, hook) have a
  recorded classification verdict **and** a rationale — **0** assets left unclassified.
- **SC-002**: The mandatory core contains **0** topic-specific terms (verifiable by scanning for
  "System Design", "HomeOS", "patterns_v1", "capacity"/"QPS", and other domain wording).
- **SC-003**: The **mandatory core alone** (all optional modules disabled) produces a viable course
  shape for at least **1** unrelated sample topic, with **0** optional modules required. **Before 001
  exists to drive this end-to-end**, "produces a viable course shape" is verified by a **structured
  paper-walkthrough**: manually apply the core's backward-design backbone, lesson arc, and rubric to
  the sample topic and confirm each step produces a sensible artifact (outcomes → assessment →
  lesson-arc outline → rubric-checkable draft), recorded as a checklist — not requiring the pipeline
  to run. Once 001 exists, re-verify by actually driving the pipeline; the paper-walkthrough is a
  pre-pipeline proxy, not a permanent substitute.
- **SC-004**: Every optional module can be independently enabled or disabled with **0** breakage of
  the mandatory core (each module toggled off leaves a working core).
- **SC-005**: The rubric asset's core layer holds **exactly the 5** generic dimensions, and **100%**
  of the reference rubric's SD-specific checks are expressed as topic add-ons — **0** SD-specific
  dimensions in the core.
- **SC-006**: The template carries a version stamp, and a copy that recorded an older stamp detects a
  version mismatch **100%** of the time (supporting 001's drift check).
- **SC-007**: **100%** of template pieces record provenance to a reference asset, a research source,
  or "new" — the distillation is fully auditable, with **0** unexplained pieces.
- **SC-008**: Ownership of "the template is never mutated" belongs to **001 SC-003** — 001 is the
  actor that could violate it, via a bad copy step. This spec's contribution is producing an
  immutable, versioned artifact in the first place (FR-016/FR-017) for 001 to copy from; this criterion
  is not independently re-asserted here to avoid a duplicate, driftable claim.
- **SC-009**: **0** template elements are carried over **solely because the reference course had
  them** — **100%** of kept elements record either a research-grounded justification or an explicit
  critical-thinking judgment (the reference course never wins by existence alone).
- **SC-010**: The distillation consumes an external research digest for **100%** of runs; a run with a
  missing, thin, or low-quality digest halts or flags **100%** of the time rather than proceeding on
  the unvalidated reference course alone.
- **SC-011**: **At MVP**, the template ships **one** shared core, the profile **mechanism**, and the
  **default** profile, with **0** forked per-subject templates (verifiable: disabling the profile
  leaves the one core intact). **At full delivery** (User Story 4's increments landed), the template
  ships **≥4** archetype profiles total (default + the 3 structurally-consequential ones); every
  profile — MVP or later-increment — reuses the core invariants and reconfigures only the variable
  dimensions.
- **SC-012**: Selecting any **shipped** profile (MVP: default only; growing as User Story 4
  increments land) yields a coherent course structure for a matching sample topic — each
  later-increment profile is validated **independently at the time it ships**, not en masse — and a
  course that names **no** profile falls back to the default **100%** of the time (never an undefined
  structure). **Before 001 exists**, "coherent course structure" is verified by the same
  structured-paper-walkthrough proxy as SC-003 (applied per profile, checking that the profile's
  macro-spine/checkpoint reconfiguration produces a sensible outline); re-verified by an actual
  pipeline run once 001 exists.

## Assumptions

- **The reference course is unvalidated, not authoritative.** `System_Design_SelfLearn/` was never
  delivered to or validated by a real learner/customer, so it carries no evidence it teaches well. It
  is an **idea pool weighed with critical thinking**, and MUST be paired with an external research
  digest (FR-003) — it is explicitly **not** the sole source.
- **The external research digest is supplied as an `.md` in this feature folder** (a Perplexity-style
  search the maintainer runs and drops in). Its quality caps how well-grounded the template can be; a
  thin digest halts or flags the distillation (FR-005) rather than silently trusting SD. The current
  digest ([`research-digest.md`](research-digest.md)) resolves the tiering model → **one core +
  profiles**, not siloed templates.
- **The template is one core + archetype profiles, not many templates** (FR-022–FR-025, per the
  research digest §5). The initial profile set is the 3 structurally-consequential ones (PBL/CBL,
  CBE/mastery, guided-inquiry) plus a default (theory / linear-spiral); the set may grow. Which
  concrete elements each profile flips (spine, entry point, advisory checkpoints, granularity) is
  left to the plan. Profiles configure **content**, not runtime enforcement — no locking/gating.
- **"Frozen / versioned" = stamped snapshot.** The version stamp names a snapshot; the *re-sync*
  mechanism (pulling later template improvements into already-built courses) is out of scope here and
  is a later manual step noted in 001.
- **The factory's build `.claude/` is a separate deliverable** (DESIGN roadmap task #2); reference
  assets that are build tooling rather than course-teaching machinery are excluded from the template
  (FR-021) and are not authored here.
- **Rubric grading semantics belong to 004.** This spec fixes only the two-layer *shape*; weights,
  per-dimension thresholds, and the hard-gate rule are 004's (mirrors the 004 seam in the specs
  index).
- **`meta-env-setup/` is lineage / scoring tooling only** (`validate_claude_setup.py --score` to
  improve the template *later*) — not a build-time dependency of producing the template.
- **The initial optional-module set is derived from the reference course's SD-specific
  capabilities** (katas, diagrams, Socratic, pattern-catalog); the module set may grow as later
  courses need new ones.
- **Module granularity is an implementation detail** — what counts as one module is left to the plan,
  provided each module is independently toggleable (FR-012) and self-described (FR-018).
- **A viable "course shape"** (SC-003) means the core's syllabus + lesson-arc + rubric +
  `/improve-course` + `/new-lesson` machinery can drive a course end-to-end for a non-SD topic, not
  that a full course is authored as part of this spec.
- **The critical-thinking filter's recording format (FR-002) reuses the `mentor-research` skill's
  discipline** (`skills/mentor-research/`, already extracted per `pedagogy/README.md`) — tiered
  judgment (High/Medium/Low + one-clause caveat) with a citation trail — rather than inventing a new
  recording scheme for this spec's per-idea judgments.
