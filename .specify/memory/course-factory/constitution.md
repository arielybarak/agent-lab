<!--
SYNC IMPACT REPORT
==================
Version change: 1.2.2 → 1.2.3 (2026-07-22)
Bump rationale: PATCH — Principle II still described the evaluator as spot-checking
  traceability. Both consuming specs settled on an EXHAUSTIVE check (003 FR-011/SC-004,
  004 FR-007/SC-004 + contracts/citation-traceability.md), on the rationale that `[Sn]`
  resolution is a cheap mechanical lookup, so sampling buys nothing. The B3-4 fix logged
  in specs/course-factory/findings-FIXES.md reworded the spec bodies but never reached
  this file or DESIGN.md § pipeline step 4 — reconciled here in the settled decision's
  favor, per the governance clause ("disagreement with DESIGN.md is a defect to
  reconcile"). The bar is TIGHTENED, never loosened; no principle redefined.
Templates requiring update: none (no template restates the traceability rule).
Follow-up: DESIGN.md § 4 citation bullet updated in the same pass.

--- Prior: 1.2.1 → 1.2.2 (2026-07-11) ---
Bump rationale: PATCH — Development Workflow steps 1–2 still described a separate
  "clarified spec" file and an "empty" `BUILD_PROGRESS.md`, both superseded when spec 001
  was reconciled (B1-5: `COURSE_BRIEF.md` is the sole on-disk home for intake's output;
  B1-7: `BUILD_PROGRESS.md` is "initialized," not empty, per FR-008). The 1.2.0 pass
  reconciled the Core Principles and Structural Constraints but missed this section.
  Wording only; no principle redefined.

--- Prior: 1.2.0 → 1.2.1 (2026-07-11) ---
Bump rationale: PATCH — Principle IX's mandatory-core command list was missing
  `/course-report`, which every other part of the constitution and DESIGN.md already
  treats as a core template command (Development Workflow step 6 generates it; DESIGN
  step 5 says it's "inherited from the template"). Completing the enumeration to match
  already-settled fact, not expanding scope (specs/course-factory/REVIEW-findings.md
  Part B, finding B0-2). No principle redefined; no new guidance added.

--- Prior: 1.1.0 → 1.2.0 (2026-07-11) ---
Bump rationale: MINOR — guidance materially expanded across five principles and both
  non-principle sections to reconcile the 2026-07-10 deep design review
  (specs/course-factory/REVIEW-findings.md Part A) with specs 000–004; no principle
  removed or redefined incompatibly.
  - IV (Clarify Early): added the ask-moments-vs-gates carve-out — the two-ask-moment
    cap governs open clarifying questions only, not review/accept gates (A9).
  - VI (Match the Reviewer to Competence): added a Delivery row to the reviewer table —
    gate = report generation, verdict informational, not a blocker (A11).
  - VIII (One Rubric, Two Layers): added that the rubric's version identity IS the
    template's version stamp (Principle IX) — one identity, not two (A10).
  - IX (Tiered Templates): pinned the initial profile ship set (default + PBL/CBL +
    CBE/mastery + guided-inquiry); procedural/code deferred to a later increment,
    resolving an inventory mismatch against spec 000 FR-023 (A12).
  - XII (Feedback Compounds): reworded the harvest write-rule to user-invoked-only (no
    automatic/scheduled trigger), reconciling stale "after each course/phase" text
    against the settled 2026-07-08 clarification (004 FR-015/016) (A8a).
  - Development Workflow step 6 (Deliver): course content named explicitly
    (`SYLLABUS.md` + lesson files); "certifies" reworded to "reports" — a needs-work
    verdict is still delivered, not withheld (A11).
  - Structural Constraints: required per-course file list gained `DIFFS.md` (the
    forward-diff ledger, A3) and the course content itself (A6); the factory's own
    `.claude/` is now noted as spec 001's implementation deliverable, not a separate
    spec (A5); `insights/` is now noted to start empty, no corpus seeded from the
    reference course (A16).
  No principle was removed, renumbered, or redefined in a backward-incompatible way.

Templates requiring updates:
  ✅ .specify/templates/plan-template.md / spec-template.md / tasks-template.md — generic;
     no new mandatory sections introduced. No edit required.
  ✅ specs/course-factory/{000,001,002,003,004}/spec.md — updated in the same pass as this
     amendment (REVIEW-findings.md Part A resolution); already in sync.
  ✅ README.md / DESIGN.md — updated in the same pass; already in sync.

Follow-up TODOs: none.

--- Prior: 1.0.0 → 1.1.0 (2026-07-10) ---
Bump rationale: MINOR — Principle IX (Tiered Templates) materially expanded from
  "core + optional modules" to a THREE-tier model "core + archetype profiles +
  optional modules", grounded in specs/course-factory/000-course-template/research-digest.md
  (§5: one core + profiles, not siloed per-subject templates). Synced with spec 000
  (FR-009/010/022–025) and DESIGN.md. No principle removed or redefined incompatibly.

--- Prior: initial ratification (1.0.0) ---
Version change: (template / unversioned) → 1.0.0
Bump rationale: Initial ratification. First concrete constitution derived from
  DESIGN.md "Design principles" — MAJOR baseline (1.0.0).

Principles defined (12, derived directly from DESIGN.md):
  I.    Quality Loop Is Mandatory (NON-NEGOTIABLE)
  II.   Anti-Fabrication First (NON-NEGOTIABLE)   [absorbs "Weigh reliability,
        not popularity alone" + "Citations are mandatory"]
  III.  Mentor, Not Aggregator
  IV.   Clarify Early, Research Before Drafting
  V.    Specialize by Overlay, Not Mutation
  VI.   Match the Reviewer to Competence
  VII.  Big Chunks, Then Batch-Review
  VIII. One Rubric, Two Layers
  IX.   Tiered Templates
  X.    One Running Example Per Course
  XI.   Resumable by Design
  XII.  Feedback Compounds

Added sections:
  - Development Workflow — The Phased Pipeline
  - Structural Constraints
  - Governance

Removed sections: none (initial version)

Templates requiring updates:
  ✅ .specify/templates/plan-template.md — "Constitution Check" reads this file
     at plan time; generic gate placeholder still valid, no edit required.
  ✅ .specify/templates/spec-template.md — generic; constitution adds no new
     mandatory spec sections. No edit required.
  ✅ .specify/templates/tasks-template.md — generic; task categories unaffected.
     No edit required.
  ⚠ README.md / DESIGN.md — source of truth for these principles; keep in sync
     if principles are ever amended (currently aligned).

Follow-up TODOs: none. RATIFICATION_DATE set to today (new project, no prior
  adoption date exists).
-->

# course-factory Constitution

Turn a single user-written `COURSE_SPEC.md` into a complete, quality-hardened course.
These principles govern how the factory is built and how it builds courses. They are
derived from and must stay consistent with [`DESIGN.md`](../../../course-factory/DESIGN.md); where this
document and DESIGN.md disagree, that is a defect to reconcile, not a license to drift.

## Core Principles

### I. Quality Loop Is Mandatory (NON-NEGOTIABLE)

There is **no one-shot course generation**. Every course MUST pass through the phased
review loop (syllabus → skeletons → lessons), and every phase MUST clear its gate before
the next begins. Scaffolding and first drafts SHOULD be automated aggressively, but a
review gate — user, agent, or rubric — is never skipped, disabled, or merged away.

**Rationale**: "Spec → whole course in one shot" manufactures exactly what the
`course-evaluator` is built to catch: fabricated capacity numbers and cargo-cult claims.
The gates are the line between a course factory and a slop factory.

### II. Anti-Fabrication First (NON-NEGOTIABLE)

Every factual claim in a course MUST be grounded in the spec's source material. **No
invented numbers.** Claims carry `[Sn]` citation keys that resolve to the course's
`SOURCES.md`, and the evaluator checks **traceability exhaustively** — **every** key, not
a sample — that a claim maps to a real source (it verifies tracing, not truth).
Resolution is a cheap mechanical lookup, so completeness is affordable and sampling is
not good enough. Sources MUST be weighed for reliability,
not popularity: high stars are a strong green flag, **not proof**; each source is judged
on reliability before it is trusted.

**Rationale**: Ungrounded confidence is the failure mode a course generator is most prone
to. Traceable citations make fabrication visible and fixable.

### III. Mentor, Not Aggregator

The factory composes syllabi and lessons with **real domain judgment**. Sources *inform*;
they never *dictate*. The factory MUST guard against sparse, stale (e.g. 20-year-old), or
industry-irrelevant sources — filling gaps, correcting staleness, and keeping content
relevant to what the industry and the learner actually need *now*. Blindly aggregating
sources is prohibited.

**Rationale**: A pile of averaged sources is not a course. Teaching requires a point of
view and current-industry judgment that no source set supplies on its own.

### IV. Clarify Early, Research Before Drafting

Knowable ambiguities MUST be settled **upfront**, before the expensive research step. The
syllabus MUST be grounded in real, critically-filtered sources **before** it is composed.
The factory asks the user **open-ended clarifying questions** at exactly **two ask-moments**:
*upfront intake* (knowable ambiguities, before research) and *post-research* (only if sources
diverge on the topic's angle). Front-load what is knowable; defer only what research must reveal.

**Ask-moments are a distinct category from review gates.** The two-ask-moment limit governs
*questions that shape content*; it does not count or constrain the pipeline's **review gates** (the
syllabus approval loop, the blocking post-skeleton scan, the round-cap accept-or-comment decision —
Principle VI/VII). A gate is a scheduled decision point on already-produced work; an ask-moment is an
open question about missing content. Both are user interactions, but only the latter is capped at two.

**Rationale**: Settling ambiguity mid-pipeline is expensive and wasteful; some divergence
can only be discovered by looking, so that single question is deferred, not front-loaded.

### V. Specialize by Overlay, Not Mutation

Topic specialization lives in a **generated overlay** (`COURSE_BRIEF.md`) plus a **module
selection** (include/exclude optional modules). The template `.claude` internals MUST stay
**frozen** — the factory does not surgically edit them per course. The copy step stamps the
template version into the course so already-shipped courses can be re-synced manually
(re-copy template + reapply the thin overlay).

**Rationale**: One frozen source of truth plus a thin per-course delta means central
improvements flow forward to every future course, drift stays minimal, and generation is
more reliable (writing one brief is safer than editing many files).

### VI. Match the Reviewer to Competence

Each phase's reviewer MUST be whoever is competent to judge that artifact:

| Phase | Artifact | Reviewer | Loop until |
| :--- | :--- | :--- | :--- |
| Syllabus | course shape / scope | **User** | user is pleased |
| Skeletons | per-lesson plans | **Agent-eval, then user** | agent passes, then user confirms |
| Lessons | lesson content | **Automated eval** (rubric) | passes rubric |
| Delivery | course package + report | **Automated** (report generation) | `COURSE_REPORT.md` is generated — **any** verdict clears this gate; a "needs work" verdict is delivered as-is, never withheld, and feeds `/improve-course` instead of blocking |

The user owns "what I want to learn" (structure, scope). Automated evaluation owns
**correctness of material the user is still learning** — the user MUST NOT be made the
correctness gate on content they came to learn. Users MAY add *learnability* feedback on
lessons ("too fast," "confusing example"), but **correctness ≠ user**.

**Rationale**: A reviewer can only gate what they are equipped to judge. Mismatched gates
either rubber-stamp errors or block on the wrong authority.

### VII. Big Chunks, Then Batch-Review

Generate the **whole batch** (all skeletons; full lessons) before evaluating. An automated
**author → critique → refine** loop runs *first*, capped at **3 rounds**; the user gate (if
any) comes *after*. The factory MUST NOT interrupt the user per-item.

**Rationale**: Per-item interruptions exhaust the user and fragment their judgment. Batch
generation plus an automated convergence loop reserves human attention for whole-batch
review.

### VIII. One Rubric, Two Layers

Quality is defined by **exactly one** rubric: a **generic core** (correctness, grounding,
flow, coverage, practicality) plus **topic add-ons** the spec may request (e.g. a
fabricated-capacity-numbers check). `comparison/` MAY propose revisions to that rubric and
MUST NOT keep a rival one; **nothing else defines quality**. The rubric's **version identity is the
template's version stamp** (Principle IX) — one identity across template and rubric, never two.

**Rationale**: Multiple competing rubrics make "quality" unfalsifiable. A single owned
rubric with an explicit revision path keeps the bar coherent and improvable.

### IX. Tiered Templates (core + profiles + modules)

`course-template/` MUST be **three-tiered**: a **small mandatory core** (the evidence-invariant
backward-design backbone, canonical lesson arc, feedback loops, rubric, `/improve-course`,
`/new-lesson`, `/course-report`), a set of **archetype profiles** (named, evidence-based
configurations *over the one core*), and **opt-in optional modules** (katas, diagrams, Socratic
drills, pattern-catalog). The
profiles' **initial ship set** is **default** (theory/linear-spiral) plus the three research-flagged
structurally-consequential paradigms — **PBL/CBL, CBE/mastery, guided-inquiry** (spec 000 FR-023);
**procedural/code** is a candidate profile for a **later increment**, not part of the initial ship
set. It MUST be **one core with profiles, NOT siloed per-subject templates**. The system-design shape
MUST NOT be forced onto a math, history, or other course that does not want it. Because the factory
emits **static course content** (no runtime), a profile MUST NOT lock or gate learner progress — the
strongest progression mechanism it may embed is an **advisory checkpoint note**, never enforcement.

**Rationale**: One rigid template shape overfits the first domain, but N separate templates
duplicate and diverge. The instructional-design evidence (UbD, Merrill, Gagné, cognitive-load
theory; PBL/CBE meta-analyses — see `specs/course-factory/000-course-template/research-digest.md`)
shows a **strong invariant core** with macro-structures acting as **configurable profiles of that
core**, not separate species — while three paradigms (PBL/CBL, CBE/mastery, guided-inquiry) are
structurally consequential enough to be true profiles, not mere module toggles. A thin core +
evidence-based profiles + opt-in modules lets the factory serve any topic without duplication or
irrelevant scaffolding.

### X. One Running Example Per Course

Every course MUST thread a single concrete **running example / project backbone** (as
System Design used *HomeOS-Cloud*). It is required in the spec and carried in the brief.

**Rationale**: A shared backbone gives lessons continuity and gives the learner one
evolving artifact to reason about, instead of disconnected toy examples.

### XI. Resumable by Design

Pipeline state MUST live in the course's `BUILD_PROGRESS.md` — the current phase plus
per-lesson status — updated as work proceeds, so **any session can resume mid-course**.
The build must never depend on in-memory state that a session boundary would lose.

**Rationale**: Course generation spans many sessions. State on disk is the only thing that
survives a pause, a crash, or a handoff to another session.

### XII. Feedback Compounds

Every course MUST carry a `FEEDBACK.md`, populated during the build (gate-event comments, evaluator
critiques). Its critiques MUST be **harvested up into `insights/`** via exactly **two user-invoked**
paths — a per-insight capture and a `setup-retro`-style bulk harvest — with **no automatic or
scheduled trigger**: harvesting never fires on course completion or a phase transition by itself, only
when the user invokes it. Intake, syllabus composition, and drafting MUST read the resulting insights
digest; an empty digest is a valid input.

**Rationale**: A factory that does not learn repeats its mistakes. Harvesting feedback into
a shared digest makes each course better than the last.

## Development Workflow — The Phased Pipeline

The build follows a fixed sequence; these are the enforceable process rules that implement
the principles above.

1. **Intake / clarify** (Principle IV) — read the spec, ask upfront questions, and produce
   `COURSE_BRIEF.md`: the **single on-disk home** for all of intake's output (topic/scope,
   audience, running example, source pointers, the selected archetype profile, and the
   module selection) — there is no separate clarified-spec file.
2. **Copy** (Principle V) — copy `course-template/` into the new course, apply the overlay
   honoring the selected profile, **stamp the template version**, and initialize
   `BUILD_PROGRESS.md` positioned at the start of the syllabus phase, plus the `SOURCES.md`,
   `FEEDBACK.md`, and `DIFFS.md` stubs.
3. **Syllabus loop** — research (converge sources, hard budget/cost cap as backstop; save to
   `SOURCES.md` under stable `[Sn]` keys), compose as a mentor, ask the user only if sources
   diverge, then user-review to approval. **Once approved the syllabus is frozen**: a later
   gap is shown to the user as an explicit diff, **never changed silently**.
4. **Skeleton loop** — draft **all** skeletons at once, run the agent author→critique→refine
   loop (cap 3 rounds; unresolved deltas surface to the user), then user scans the batch.
5. **Lesson loop** — the **same** author→critique→refine inner loop on full lessons, graded
   against the rubric (cap 3 rounds). Correctness is the automated gate. **Stuck lessons do
   not loop forever**: after the cap, show the user the best version + its scorecard; they
   accept it or request one more pass. `BUILD_PROGRESS.md` is updated after every lesson.
6. **Deliver** (Principle I) — the course content (`SYLLABUS.md` + lesson files) + its `.claude`
   residue + a graded **`COURSE_REPORT.md`** reporting quality to the user (Principle VI). The gate is
   the report's **generation**, not a passing verdict — a "needs work" verdict is still delivered,
   never withheld, and feeds `/improve-course` instead. Distinct from `FEEDBACK.md`, which feeds the
   factory's `insights/`.

**Gate discipline**: the 3-round refine cap, the two user ask-moments (intake +
post-research divergence), and the frozen-syllabus diff rule are hard constraints, not
suggestions. Calibratable knobs (research depth, parallel width, refine cap, fake-student
scope) may be tuned after real runs, but only deliberately and recorded.

## Structural Constraints

These repository invariants exist to keep the principles enforceable:

- **Two `.claude` folders stay distinct.** The factory's own `.claude/` runs the pipeline
  (spec 001's implementation deliverable, DESIGN roadmap task #2 — not a separate spec); the
  `course-template/.claude/` is the **frozen** template copied into each course. They
  MUST NOT be conflated or cross-edited.
- **`courses/` is staging only.** Generated courses land in `courses/<name>/`; after
  delivery the user moves the course out to its own home. Per-course files that MUST exist:
  `COURSE_BRIEF.md`, `SOURCES.md`, `BUILD_PROGRESS.md`, `DIFFS.md` (the forward-diff ledger —
  Principle V/XI), `FEEDBACK.md`, **the course content** (`SYLLABUS.md` + lesson files — Principle I's
  actual deliverable), `COURSE_REPORT.md`, and the `.claude/` residue.
- **`insights/` is knowledge, not tooling** — the shared cross-course digest (Principle XII). It
  **starts empty**: no pre-existing corpus is seeded from the reference course; it grows only from
  this factory's own harvested courses.
- **`comparison/` owns rubric revisions** (Principle VIII) and produces per-course reports
  feeding the `/improve-course` backlog; it never keeps a rival rubric.
- **`meta-env-setup/` is decoupled at runtime.** It is lineage / evolution tooling for
  improving the template itself (`validate_claude_setup.py --score` and friends). It MUST
  NOT be invoked to generate an individual course.

## Governance

This constitution supersedes ad-hoc practice for course-factory. It is the enforceable
distillation of `DESIGN.md`; the two MUST stay consistent.

- **Amendments** require a documented change to this file, a version bump per the policy
  below, and reconciliation with `DESIGN.md` and any dependent `.specify/templates/*`.
- **Versioning policy** (semantic):
  - **MAJOR** — a principle is removed or redefined in a backward-incompatible way, or
    governance is materially changed.
  - **MINOR** — a new principle or section is added, or guidance is materially expanded.
  - **PATCH** — clarifications, wording, or non-semantic refinements.
- **Compliance** — specs, plans, and tasks generated under `.specify/` MUST be checkable
  against these principles. The `/speckit-plan` Constitution Check gate reads this file;
  any violation must be justified in that plan's Complexity Tracking or the design changed.
- **The NON-NEGOTIABLE principles (I, II)** may not be waived by any plan; a plan that
  cannot satisfy them is out of scope, not an exception.

**Version**: 1.2.3 | **Ratified**: 2026-07-07 | **Last Amended**: 2026-07-22
