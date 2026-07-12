# course-factory specs — index & roadmap

The factory is decomposed into a **foundational asset spec (000)** plus **four subject-specs
(001–004)**, ordered by pipeline flow. Each is an independently specifiable / plannable /
implementable unit (`spec.md` → `plan.md` → `tasks.md`), so the work can be split across sessions: a
fresh session reads this index, picks one spec, and works it without re-deriving the decomposition.
**000 is the prerequisite** — it produces the frozen template every downstream spec copies.

Governing doc: [`course-factory/DESIGN.md`](../../course-factory/DESIGN.md) (source of truth) and
the project constitution at [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md).

> **Two "resumabilities" — don't conflate them.**
> - `BUILD_PROGRESS.md` resumes a **course build** (runtime, one per generated course).
> - This index + `specs/**` resumes **our development of the factory** (build-time, across sessions).

## The specs

| # | Spec | Owns | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- |
| **000** | **Course-Template Distillation** | distill the frozen, versioned, **three-tiered** `course-template/` (**core + archetype profiles + optional modules**): gather ideas from `System_Design_SelfLearn/.claude/` (**unvalidated — critical-thinking filter, not authority**) **plus an external research digest**, classify every reference asset (keep-core/demote-module/drop), strip topic-specifics, two-layer rubric shape, version stamp | reference course (unvalidated, read-only) + external research digest | **Clarified** (5 Qs resolved) — ready for `/speckit-plan` |
| **001** | **Pipeline & Instantiation** | intake clarify interview, `COURSE_BRIEF.md` overlay + module selection, frozen-template copy/overlay/version contract, the phase state machine, gates, resume, delivery contract | 000 (course-template asset) | **Clarified** (2 Qs resolved) — ready for `/speckit-plan` |
| **002** | **Syllabus** | research & sourcing → `SOURCES.md`, compose-as-mentor, the `.md`/`.ipynb` lesson-format decision, the user-approval gate's content | 001 | **Clarified** (2 Qs resolved) — ready for `/speckit-plan` |
| **003** | **Lessons** | skeleton & lesson authoring, the parallel author–critic worker pool, the fake-student learnability check | 001, 004 (rubric) | **Clarified** (3 Qs resolved) — ready for `/speckit-plan` |
| **004** | **Grading & Delivery** | the rubric & course-evaluator internals, `COURSE_REPORT.md` scorecard, `FEEDBACK.md` → `insights/` harvest, `comparison/` | 001 | **Clarified** (3 Qs resolved) — ready for `/speckit-plan` |

Status legend: **Not started** → **Drafted** (spec.md written) → **Clarified** → **Planned**
(plan.md) → **Tasked** (tasks.md) → **In progress** → **Done**.

## What each spec covers

### 000 — Course-Template Distillation → [`000-course-template/spec.md`](000-course-template/spec.md)

The foundational asset (DESIGN roadmap task #1). Reverse-engineers the topic-neutral teaching
machinery from the one-topic reference course `System_Design_SelfLearn/.claude/` — which is
**unvalidated (never delivered to a real learner) and therefore NOT a reliable reference**: it is an
**idea pool weighed with critical thinking**, cross-checked against an **external research digest**
(a Perplexity-style `.md` dropped into the feature folder) so SD is **not the sole source**.
Classifies every reference asset **keep-core / demote-module / drop** (never keeping anything just
because SD had it), strips every System-Design / HomeOS-Cloud / `patterns_v1` specific, and sorts
survivors into a **three-tier** template: a **small mandatory core** (evidence-invariant backbone +
lesson arc + feedback loops + quality rubric + `/improve-course` + `/new-lesson`), a set of
**archetype profiles** (PBL/CBL, CBE/mastery, guided-inquiry, + a default — configurations *over the
one core*, **not** siloed per-subject templates), and **opt-in optional modules**; shapes the rubric
as **one-rubric-two-layers** (generic core + requestable topic add-ons); freezes + version-stamps the
result. The tiering model is settled by the research digest (`research-digest.md` §5). **001's copy
contract (FR-001) depends on this existing.** Clarified 2026-07-11 (5 Qs): reference-course
location is configurable (not hardcoded), `lesson-consistency-reviewer` splits core/module/dropped,
version stamp is semantic-versioned, "small" core has no formal size ceiling, and the pre-pipeline
paper-walkthrough runs on 2 named sample topics, agent-performed.

### 001 — Pipeline & Instantiation → [`001-pipeline-skeleton/spec.md`](001-pipeline-skeleton/spec.md)

The front-end + the spine. Turns a rough `COURSE_SPEC.md` into a set-up, resumable course build —
including selecting the course's **archetype profile** (000's mechanism) — and walks it through the
fixed phase sequence to delivery. Treats each phase's *internal work* as a black box behind its gate.
**Its implementation is the factory's own build `.claude/`** (DESIGN roadmap task #2) — not a
separate spec, see 001's Assumptions. Clarified 2026-07-07 (2 Qs): backward transitions are
forward-diff-only (FR-023), and the post-skeleton user scan is a blocking gate (FR-024) — see the
seam log below.

### 002 — Syllabus

The depth behind the **syllabus gate**: shallow research (web + `gh` + Udemy/Coursera/edX
name-search) with a convergence + budget stopping rule, saved to `SOURCES.md` under `[Sn]` keys;
compose-as-mentor (sources inform, never dictate), **consistent with the course's selected profile**;
decide course volume and the `.md`/`.ipynb` format, writing the format back into `COURSE_BRIEF.md`.
Ends at the user-approval gate; approved syllabus (`SYLLABUS.md`) is frozen.

### 003 — Lessons

The depth behind the **skeleton and lesson gates**: the shared author → critique → refine primitive
(3-round cap); the parallel author–critic worker pool (fresh-context authors + author-blind
evaluators, two pairs in flight), authoring **per the selected profile's** scaffolding depth and
checkpoint placement; the once-per-course fake-student learnability check on the first lessons.
Consumes 004's rubric as the lesson gate.

### 004 — Grading & Delivery

The **rubric and everything it feeds**: the one-rubric-two-layers definition (generic core + topic
add-ons) and course-evaluator, the graded `COURSE_REPORT.md`, the `FEEDBACK.md` → `insights/`
harvest so the factory compounds, and `comparison/` (analyze GitHub courses → propose rubric
revisions). It owns the *only* definition of quality.

## Foundational assets

- **`course-template/` distillation** (DESIGN roadmap task #1) — **now spec 000** (above), no longer
  a spec-less prerequisite: extract the topic-neutral core (syllabus, lesson arc, rubric,
  `/improve-course`, `/new-lesson`) into the frozen, tiered template; demote SD-specific pieces to
  optional modules. **`System_Design_SelfLearn` is an unvalidated idea-source, not a proven
  reference** — filter it with critical thinking and cross-check it against an external research
  digest (see 000); never inherit from it by authority. **001's copy contract depends on this
  existing.**
- **`COURSE_SPEC.template.md`** — the author-facing spec template (initial draft exists in
  `../templates/`); still a plain asset, not a spec.

## Seams to watch (cross-spec)

1. **The rubric is shared** — it is the *gate* in 003 but the *engine* in 004. Define it in 004;
   003 consumes it. 004's rubric core likely needs to land (or a thin shared contract) before 003.
2. **`COURSE_BRIEF.md`** — created by 001, augmented by 002 (the format decision), read by 002/003/004.
3. **`BUILD_PROGRESS.md` / phase state** — owned by 001 (FR-015). **002** records the syllabus
   phase's **sub-phase status** (`research-in-progress` / `research-done` / `composed` / `presented`,
   002 FR-018) as it completes each sub-step; **003** updates per-lesson status as lessons complete
   (003 FR-012).
4. **`course-template/`** — the foundational asset above; a hard prerequisite for 001.
5. **Archetype profile** — selected at intake (001 FR-005), defined by 000 (FR-022–025), consumed by
   002 (syllabus spine/checkpoints, FR-015) and 003 (scaffolding depth/checkpoint placement, FR-019).
6. **Forward-diff ledger (`DIFFS.md`)** — owned by 001 (FR-027). "Frozen artifact + its `DIFFS.md`
   entries" is the canonical read for 002 (FR-017), 003 (FR-007), and any other downstream consumer of
   a gated artifact — never the frozen artifact alone once a diff exists against it.
7. **Version identity** — the rubric's version **is** the template's version stamp (000 FR-016 / 004
   FR-005); one identity, not two. A rubric revision from `comparison/` lands via 000's narrower
   rubric-only re-stamping path (000 Edge Cases), not a full re-distillation.
8. **Ask-moments vs. gates** — 001 FR-014's two-ask-moment limit governs open clarifying questions
   only. Review gates (syllabus approval loop, the blocking skeleton scan, the round-cap
   accept-or-comment decision) are a separate, unlimited-count category — they are scheduled decision
   points on already-produced work, not open questions.
9. **`FEEDBACK.md` write side** — populated during the build by 001 (gate-event comments, FR-026) and
   003 (evaluator critiques, FR-020); harvested up into `insights/` by 004, user-invoked only
   (unchanged). Previously unowned (see former finding A4).
10. **Insights digest read side** — read at intake (001 FR-025), syllabus compose (002 FR-016), and
    drafting (003, pre-existing FR-007); an empty digest is valid input everywhere.

## Resolved decisions (seam log)

Clarify outcomes per spec, recorded here so a cold session can honor settled decisions from **this
index alone** — without opening each spec's `Clarifications` section. **Update this whenever
`/speckit-clarify` resolves a marker** (mirror the spec's `Clarifications` entry, and note which
sibling specs it constrains).

### 000 — Course-Template Distillation · Session 2026-07-11

- **Reference-course location = configurable input** (FR-001). The hardcoded absolute path
  (`/home/barak/System_Design_SelfLearn/`) becomes an overridable config value/env var, defaulting
  to that path when unset. → *Self-contained to 000.*
- **`lesson-consistency-reviewer` = split** (FR-010/FR-011). Its generic capability (arc-order +
  running-example consistency + numbering + file:line findings, ranked Critical/Warning/Nit) is
  core; its diagram-existence check joins the `diagrams` module; its phase-language rule and
  `patterns_v2`/`patterns_v1` drift check are dropped (no generalizable home). → *Self-contained to
  000.*
- **Template version stamp = semantic versioning** (FR-016). MAJOR = full re-distillation; MINOR/
  PATCH = a rubric-only re-stamp. → *Constrains 001* (its drift-check compares semver) *and 004*
  (the rubric's version identity is this same stamp).
- **"Small" mandatory core = no formal yardstick.** Judged case-by-case at plan time, not tied to a
  numeric ceiling or `meta-env-setup`'s scoring tool. → *Self-contained to 000.*
- **Pre-pipeline validation = 2-topic, agent-performed paper-walkthrough** (SC-003/SC-012).
  *Introduction to Psychology* (theory-heavy) + *Python Programming* for a non-programmer
  (procedural/code-heavy); an agent reasons through outcomes → assessment → one-lesson-arc outline
  → rubric-checkable draft per topic, no mandatory human-approval gate. → *Self-contained to 000.*

### 001 — Pipeline & Instantiation · Session 2026-07-07

- **Backward transitions = forward-diff only** (FR-023). Gated phases are immutable once passed; a
  change to an earlier phase is applied as an explicit forward diff at the *current* phase — never by
  re-opening it. → *Constrains 002/003/004*: on finding a gap in an earlier artifact, surface a diff;
  do not reopen the phase.
- **Post-skeleton user scan = blocking gate** (FR-024). After agent review of the skeleton batch
  passes, the pipeline pauses for explicit user approval before the lesson phase starts. →
  *Constrains 003*: the skeleton phase presents for approval and waits; it does **not** auto-advance.

### 002 — Syllabus · Session 2026-07-07

- **Research cap unit = search/tool-call budget** (FR-005). Research stops at convergence or a max
  query/tool-call count — never unbounded. (Budget value calibratable; the unit is a query count.)
- **Thin-grounding policy = compose + flag** (FR-011). On near-zero reliable sources, compose from
  mentor judgment, mark the course/sections thinly-grounded, and tag affected topics mentor-added —
  never block or fabricate. → *Constrains 003*: lessons may rely on flagged, mentor-added grounding,
  but MUST preserve the thin-grounding flags and mentor-added tags rather than presenting them as
  sourced.

### 003 — Lessons · Session 2026-07-07

- **Pool ordering = gate-then-fan-out** (FR-018). The lesson worker pool drafts lessons 1 & 2 first,
  runs the once-per-course fake-student calibration, and **only then** fans out the remaining lessons
  (two pairs in flight) with the calibration folded in — no lesson beyond the first two begins before
  the calibration completes. → *Self-contained to 003*; sets the pool's ordering contract.
- **Fake-student trigger = first two to reach a terminal state** (FR-013). The check fires on the
  first two lessons that are rubric-passed **or** cap-surfaced-and-user-accepted (in syllabus order);
  with fewer than two lessons it runs once on what exists, and it never blocks on a lesson that never
  passes. → *Consumes 001's cap-surface/accept contract* (its FR-012) — "terminal state" includes a
  user-accepted-at-cap lesson.
- **Skeleton authoring = single batch-level loop** (FR-004). One author drafts all skeletons at once
  and one evaluator critiques the batch; the two-pairs-in-flight worker pool is **lesson-only**. →
  *Self-contained to 003*; distinguishes the batch skeleton loop from the per-lesson pool.

### 004 — Grading & Delivery · Session 2026-07-08

- **Rubric pass = per-dimension threshold** (FR-004). Every generic-core dimension and every requested
  topic add-on must clear its own minimum bar; a lesson or course passes only if **no** dimension is
  below threshold (no aggregate masking), while per-dimension scores are retained for the scorecard.
  → *Constrains 003*: this is the exact pass contract 003's per-lesson gate consumes — a lesson passes
  only when every rubric dimension clears its bar.
- **Course verdict = independent course-level grading** (FR-009). The course-evaluator additionally
  grades whole-arc dimensions (coverage across the syllabus, flow/continuity, the running-example
  thread) and MAY return a "needs work" verdict **even when every lesson already passed**; such gaps
  feed the `/improve-course` backlog as a forward diff (001 FR-023), never a phase re-open. →
  *Self-contained to 004*; distinguishes the course-level verdict from a per-lesson-pass roll-up.
- **Harvest = user-invoked only** (FR-015/016). No automatic/scheduled `FEEDBACK.md` → `insights/`
  harvest; both the per-insight capture and the `setup-retro`-style bulk harvest run only when the
  user invokes them, keeping 004 decoupled from 001's phase transitions. → *Loosens the 001 seam*: the
  harvest is **not** wired into delivery or phase advancement.

## Deferred extensions

Ideas that touch these specs but are intentionally **not** in their initial scope — each has an
Out-of-Scope bullet in the owning spec(s); the few-words version and full rationale live in
`course-factory/DESIGN.md` § Deferred extensions and `docs/FUTURE_IDEAS.md` § Course-factory.

| Idea | Touches | Depends on |
| :--- | :--- | :--- |
| Multi-format / per-artifact lessons (HTML, slides) | 002 (format decision) | A `course-template/` renderer module |
| Inline mid-lesson MCQ comprehension checks | 003 (authoring), 004 (rubric) | A `course-template/` opt-in module |
| Pedagogy technique library (`pedagogy/`) | 002 (compose), 003 (drafting), 004 (rubric add-on) | 002's research method, generalized |
| Spec-kit-style artifact discipline for course *builds* (status-stamped artifacts, per-phase checklists, an analyze-style check, a decision/seam log) | 001, 002, 003, 004 | None — pick up during each spec's own `/speckit-plan` |

## Recommended build order

**000 (`course-template/` asset)** → **001** → **002** → **004 (rubric core)** → **003** → **004
(delivery, feedback harvest, comparison)**. Rationale: the frozen template must exist before anything
can copy it (000); then the spine and instantiation (001); then the first gate's depth (syllabus,
002); the rubric must exist before lessons can be graded (004 core); lessons (003); delivery/feedback
last.
