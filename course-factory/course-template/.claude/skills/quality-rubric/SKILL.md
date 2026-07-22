---
name: quality-rubric
description: >-
  The single quality standard for course material — one rubric, two layers: a generic core of six
  dimensions (Technical Correctness, Grounding/No-Fabrication, Pedagogical Flow, Clarity, Coverage,
  Practicality) plus requestable per-course topic add-on slots, and the report-card shape a grader
  emits. USE WHEN grading a lesson or syllabus, defining what "good" means for this course, or
  requesting a topic-specific quality check.
---

# Quality Rubric (one rubric, two layers)

## When to Activate This Skill

- Grading a lesson, a unit, or the whole course
- Writing or reading a course report card
- Deciding whether a course may exit its improvement loop
- Adding a topic-specific quality check for this course

## The shape

**One rubric. Two layers. Nothing else defines quality for this course.**

```
Layer 1 — CORE       the six generic dimensions below. Always graded. Never edited per course.
Layer 2 — ADD-ONS    per-course topic checks the course spec may request. Never core dimensions.
```

A course that wants a domain-specific bar adds an **add-on**; it does not add, rename, or remove a
core dimension, and it does not keep a second rival rubric.

## Layer 1 — the core dimensions

| # | Dimension | What it measures |
| :--- | :--- | :--- |
| 1 | **Technical Correctness** | The claims are *true* for the subject: right facts, right reasoning, right trade-offs, no confidently wrong explanation. |
| 2 | **Grounding / No-Fabrication** | Every factual claim, figure, and quotation traces to a stated source or to visible reasoning from stated assumptions. No invented specifics; no unearned confidence. |
| 3 | **Pedagogical Flow** | Follows the canonical arc (skill `lesson-arc`): frames before it answers, activates prior knowledge, demonstrates before it asks for practice, closes with integration. Names the one thing it teaches. |
| 4 | **Clarity** | The explanation is **understandable on first read by the audience the brief names** — not by an expert, and not on a second pass. Judged against the brief's stated starting point, which is the only definition of "the reader" this course has. |
| 5 | **Coverage** | Serves the outcomes the syllabus promised (skill `backward-design`): outcomes reached, evidence present, gaps **named rather than padded**. |
| 6 | **Practicality** | The material actually works for a learner on their own: exercises are doable and checkable, references resolve, artifacts the lesson points to exist, prerequisites are real. |

This list is the **canonical definition** of the core layer, and it carries **no topic-specific
dimension**. Other assets refer to "the core dimensions" and resolve the list here rather than
restating it — so the set is changed in exactly one place.

### Grading Clarity without hand-waving

"Understandable on first read" is a judgment, so ground it in observable defects rather than taste.
A Clarity finding needs a cited `file:line` and one of these named causes:

- **Undefined term on first use** — jargon, notation, or an acronym used before it is introduced, or
  introduced in terms the brief's audience has not met.
- **Forward dependency** — the sentence only parses once the reader knows something later in the
  lesson (or a later lesson).
- **Unexplained leap** — a step in a derivation, argument, or procedure the reader is expected to
  supply themselves, with no signal that they must.
- **Overloaded sentence** — several ideas packed into one sentence where a reader tracking new
  material has to hold all of them at once.
- **Ambiguous referent** — "this", "it", "the above" pointing at more than one plausible antecedent.

Two rules keep it honest:

- **Grade against the brief's audience, never your own reading.** A lesson that is clear to a
  grader who already knows the subject is not thereby clear. When the brief's audience is a novice,
  read as that novice.
- **"Could be clearer" is not a finding.** Name the cause, cite the location, and prescribe the fix
  — same bar as every other dimension.

**If the brief names no audience, Clarity cannot be scored.** Say so explicitly and report the
missing audience as a defect in the brief. Do **not** substitute your own reader and do **not**
score it as a pass — an unscored dimension is honest, a silently-assumed reader is not. Clarity is
the only dimension with an external dependency like this, which makes the audience statement
load-bearing for the whole rubric.

### Which dimension does a finding belong to?

The six dimensions are deliberately disjoint. **Route each defect to exactly one** — the same defect
counted twice distorts every aggregate computed from these scores.

| The defect is… | Dimension |
| :--- | :--- |
| Wrong | Technical Correctness |
| Right, but unsupported — no source, no shown reasoning | Grounding / No-Fabrication |
| Right and supported, but in the wrong **order** — answer before problem, practice before demonstration | Pedagogical Flow |
| Right, supported, well-ordered, but **hard to understand** as written | Clarity |
| Right and clear, but the promised outcome is **not served** | Coverage |
| Right and clear, but it **does not work** for a learner alone — broken exercise, dead reference, unreal prerequisite | Practicality |

Flow and Clarity are the pair most often confused: **Flow grades sequence, Clarity grades
comprehensibility**. A lesson can be perfectly sequenced and impenetrable, or beautifully written in
the wrong order. If a defect genuinely spans two dimensions, file it under the **earlier** row above
and cross-reference it — do not score it twice.

> **Evidence status: adopted on judgment, not research-validated.** The external research digest
> that grounds this template's course and lesson structure does **not** cover quality-rubric
> evidence — it is silent on rubrics, which is a gap, not thinness. This dimension set therefore
> passed the same critical-thinking filter applied to every other borrowed idea, and is recorded as
> **"unproven, adopted on judgment."** A later research pass scoped specifically to course-quality
> rubrics may supersede it without re-deriving the rest of the template.
>
> **Clarity** carries that flag most strongly: unlike the other five it comes from **neither** the
> reference course **nor** the digest. It is newly added on the argument that comprehensibility is
> already assessed twice while a course is being built, with no gradeable output — so making it a
> dimension routes an existing signal into the scorecard instead of discarding it. Sound reasoning,
> but reasoning, not evidence.

## Layer 2 — topic add-on slots

An add-on is a **requestable, per-course** check declared in the course brief. It is graded and
reported alongside the core, and it is clearly labelled as an add-on so it can never be mistaken
for a core dimension.

Each add-on declares:

- **name** — what it checks, in one line
- **trigger** — the kind of claim/artifact it applies to
- **finding rule** — what counts as a violation, stated so two graders would agree

Two add-ons carried over from the reference course, kept as **examples of the slot**, not as
defaults:

| Add-on | Trigger | Finding rule |
| :--- | :--- | :--- |
| Unsupported-quantity check | Any numeric estimate presented to the learner | The figure does not show the arithmetic from its stated assumptions, or cites no source → finding |
| Cargo-cult-remedy check | Any "just add X to fix it" recommendation | The recommendation does not name the specific problem X removes and the cost X adds → finding |

Both are **topic add-ons**. Neither is a core dimension, and neither is enabled unless a course asks
for it.

## Grading discipline

- **Cite evidence for every score.** Use `file:line`. A dimension with no cited evidence is not
  given the benefit of the doubt.
- **Grade what is on disk**, not what was intended. If the same context wrote and grades the
  material, the grade is theater — grading is **author-blind** (agent `course-evaluator`).
- **A debunked method is a Technical Correctness finding.** If the material presents a teaching
  approach the factory's `pedagogy/MYTHS.md` lists as debunked or overclaimed — style-matched
  instruction, brain-hemisphere typing, mindset or grit as a substitute for instruction — score it
  as wrong, not as a stylistic preference. It is a false claim about how learning works.
- **Score the core dimensions and every enabled add-on**, always in that order.

## The report-card shape

A course report reproduces this structure:

1. **Score table** — one row per core dimension, then one row per enabled add-on, then the overall
   result.
2. **Executive summary** — 2–3 sentences: the verdict and the single highest-leverage gap.
3. **Per-dimension findings** — the cited evidence and a *prescribed* fix (actionable: "do X in Y",
   never "needs work").
4. **Add-on findings** — one block per enabled add-on, or an explicit "none found".
5. **Final verdict** — the result plus the prioritized fix list for the next iteration.

## What this asset does NOT define

This rubric fixes the **shape** only. The following are **owned by the factory's grading spec** and
MUST NOT be fixed here, in a course, or in a report template:

- **Weights** per dimension
- **Per-dimension pass thresholds**
- **Hard-gate semantics** — which dimensions can fail a course outright regardless of the rest, and
  the rule that a strong overall result must never mask a failing dimension
- **The aggregation formula** and the overall pass condition
- **Whether findings carry a severity ranking** — the `lesson-consistency-reviewer` ranks its
  findings Critical / Warning / Nit; this rubric deliberately does **not**, because a severity that
  influenced scoring would be a gate by another name. If the grading spec wants one, it defines the
  vocabulary and what it affects. **Open seam question, left to 004 on purpose** — not an oversight.

If a course needs those numbers, it reads them from the grading spec; it does not invent them.

## One version identity

The rubric's version **is** the template's version stamp (`VERSION` at the template root). The
factory keeps **one** counter across the template and its rubric — never two. A rubric revision
bumps that same file.

## Provenance

Derived from the reference course's `course-quality-rubric` skill by **splitting** it: five of the
six generic dimensions became this core layer; its two subject-specific checks (unsupported
quantities, cargo-cult remedies) were demoted to add-on slots; its weights, thresholds, and
hard-gate rule were **removed** as out of scope for the template. **Clarity is new** — present in
neither the reference rubric nor the digest, added on the judgment recorded above. The whole core
set is flagged *adopted on judgment* because the research digest is silent on rubrics. Author-blind
grading and "cite evidence or don't score" are kept on the critical-thinking filter — both are
anti-collusion disciplines that hold regardless of subject. See `CLASSIFICATION.md`.
