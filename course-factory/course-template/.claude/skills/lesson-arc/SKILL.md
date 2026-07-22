---
name: lesson-arc
description: >-
  The canonical structure of a single lesson — framing → activation → demonstration → practice
  with feedback → integration/transfer — plus the house conventions that keep lessons consistent
  (one running example, numbering, section order, optional-vs-required sections). USE WHEN
  writing, scaffolding, or reviewing a lesson, or when checking that a draft matches the course's
  house arc.
---

# Lesson Arc (the canonical lesson structure)

## When to Activate This Skill

- Writing or editing any lesson
- Scaffolding a new lesson before its content exists
- Checking a draft matches the house arc (see agent `lesson-consistency-reviewer`)
- Deciding whether a section is missing or legitimately absent

## The arc (match section order and voice)

Every lesson runs these five moves, in order:

1. **Framing** — the concrete problem, goal, or question this lesson answers. Lead with the *need*,
   not the answer. A lesson that opens with the solution teaches *what* without *why*.
2. **Activation** — connect to what the learner already knows: the prerequisite, the prior lesson,
   or the experience the new idea attaches to. Name the prerequisite explicitly if it is missing.
3. **Demonstration** — show the idea worked through: a worked example, a model, a case, a walked
   derivation. Demonstration is *shown*, not asserted.
4. **Practice + feedback** — the learner does it, with guidance that fades. Practice with no
   feedback is exposure, not learning. Feedback that actually teaches is:
   - **Diagnostic** — the item isolates *one* specific misunderstanding, so a wrong answer names
     which one. An item that can be missed for four different reasons produces no usable signal.
   - **About how to improve**, not just whether it was right. A bare ✅/❌ closes the loop far less
     than one line saying what the error was and what to do differently.
   - **Timely** — attached to the practice item itself, not deferred to an answer key at the end of
     the unit.
   - Never vague praise. "Good job" is not feedback.
5. **Integration / transfer** — apply it to a new context, connect it back to the running example,
   or ask the learner to generalize. This is where the lesson stops being local.

**The order is the contract.** Sections may be sized very differently by material type (below), and
some are optional (below), but a lesson that practices before it demonstrates, or frames after it
explains, is out of arc — that is a finding, not a style choice.

## Required vs optional

- **Required:** framing, demonstration, practice+feedback. A lesson missing one of these is
  incomplete.
- **Optional but common:** an explicit "what breaks without this" motivator inside framing; a
  deep-dive section on cost/mechanics after demonstration; a trade-offs / when-*not*-to-use section
  before integration.
- **Do not manufacture an optional section** just to fill the shape. Match the nearest canonical
  lesson in the course rather than inventing structure. An absent optional section is a Warning at
  most; an out-of-order required section is Critical.

## How the arc bends by material type

The moves never change; their **weight** does.

| Material type | Where the time goes |
| :--- | :--- |
| Concept / theory-heavy | Longer activation and demonstration; practice leans on comparison, explanation, and retrieval rather than production |
| Procedural / skill-heavy | Heavier demonstration (worked examples) then several short practice cycles inside one lesson, with guidance fading each cycle |
| Quantitative | Demonstration → near-transfer practice → far-transfer practice; mixed problem types belong in the practice stage, not the teaching stage |
| Narrative / case-rich | Framing and integration carry the lesson; practice is argument and source-weighing rather than stepwise procedure |
| Drill / fluency | Short, frequent activation–demonstration cycles with a large volume of spaced practice; integration accumulates across lessons rather than inside one |

The **archetype profile** (see `profiles/`) sets the macro spine and entry point around these
lessons. It never changes the arc itself.

## House conventions

- **One running example, all course long.** Every lesson teaches through the *same* concrete
  scenario/artifact chosen for the course. Do not invent a fresh unrelated example per lesson —
  continuity is what makes the course cumulative. Name the example's recurring cast/parts once and
  reuse them.
- **Numbering and placement.** Lessons are zero-padded and ordered (`NN_name`), core material at
  the unit root and optional material clearly marked as optional. Each unit opens with its own
  overview/toolkit piece so the framing exists before the first lesson.
- **Signposting is consistent, not decorative.** If the course marks definitions, warnings, or
  hands-on tasks with a convention, that convention is used the same way everywhere or not at all.
- **State assumptions where a claim depends on them.** Any figure, estimate, or result presented to
  the learner shows the reasoning that produced it, or is cited. An unexplained number that *looks*
  rigorous is the most damaging kind of error in a course — see skill `quality-rubric`, Grounding.
- **Write for the audience the brief names, not for yourself.** Define each term at its first use in
  language that audience already has, and do not leave a step in a derivation for the reader to
  supply silently. Correct, well-ordered material that the stated reader cannot follow still fails —
  see skill `quality-rubric`, Clarity, for the specific defects that get cited.
- **Every lesson names the specific thing it teaches.** A lesson that cannot name its one idea —
  the misconception it fixes, the decision it enables, the failure it prevents — is a topic, not a
  lesson. Flag it.
- **Make the learner retrieve, don't just re-present.** Activation should ask the learner to
  *recall* the prerequisite before the lesson restates it, and integration should ask them to
  produce the idea from memory rather than recognize it. Re-reading feels like learning and mostly
  is not; retrieving is what makes it stick.
- **Space and revisit deliberately.** An idea met once is an idea lost. Plan where each enduring
  idea returns — later, in a different context — at syllabus time (skill `backward-design`, and the
  profile's spine), rather than hoping repetition happens by accident.
- **Demonstrate with worked examples, then fade the support.** For anything procedural, show a
  fully worked case before asking for an unaided one, and reduce the scaffolding across successive
  practice items rather than dropping it all at once. Fade it as competence appears — continuing to
  over-support a learner who no longer needs it wastes their attention.
- **Budget the learner's working memory.** Introduce one new idea at a time, keep each practice
  item focused on what was just taught, and put anything the learner must hold in mind next to
  where it is used rather than pages away. Most "too hard" lessons are overloaded, not too advanced.

## Grounding: the teaching-methods library

The factory maintains a curated, cited library of teaching techniques at
**`course-factory/pedagogy/`**. Consult it rather than reasoning from first principles or from
whatever "everyone knows" about teaching:

- **Start at `pedagogy/DIGEST.md`** — all 8 techniques on one screen (retrieval practice, worked
  examples, spacing, interleaving, scaffolding/cognitive load, dual coding, formative assessment,
  guided questioning), each with its **evidence tier and its boundary conditions**. Read the
  boundary conditions, not just the technique: most of these have a regime where they stop helping
  or start hurting. The digest also carries a **§ How they interact** section — a typical lesson
  composes 3–4 of these, and the couplings between them are where misuse comes from.
- **Open `pedagogy/catalog/<name>.md`** when you need the worked example, the full per-material-shape
  guidance, or the citation trail — i.e. when authoring the material, not when choosing the
  approach. The catalog is canonical; the digest is a derived view of it.
- **`pedagogy/MYTHS.md`** — popular but debunked or overclaimed ideas (the digest carries a compact
  version). **A course design choice MUST NOT be justified by an entry in this file.**

> **If that path is not reachable** — for example inside an already-generated course, where the
> library lives back in the factory — the normative rule still applies and does not depend on the
> file being present: **do not build teaching on matching a learner's "style"
> (visual/auditory/kinesthetic or similar), on left/right-brain typing, or on mindset or grit
> messaging used as a substitute for good instruction.** Offer multiple representations because
> *the material* benefits from them, never because a learner carries a style label. These are the
> most likely wrong ideas to arrive by default; naming them is cheaper than catching them later.

## Gotchas

- **Jumping to the answer.** The single most common failure. Framing exists to make the learner
  *want* the idea; skipping it produces material that is correct and unmemorable.
- **Practice without feedback.** Exercises with no reference answer, check, or self-assessment
  criterion do not close the loop. Add the check or cut the exercise.
- **Example drift.** A one-off unrelated example inside an otherwise-threaded course reads as a
  gap in the course, not a variation. Route it back to the running example or justify it in-line.
- **Structure imposed over the course's own shape.** When an existing lesson family has a settled
  house form, match it; do not overwrite it with a generic template.

## Provenance

Merged from **two** reference skills that encoded the same capability after neutralization
(`pattern-lesson-format` and `system-design-curriculum` — consolidated per FR-008; see
`CLASSIFICATION.md`). Grounded in the external research digest §3: the canonical arc (problem/goal
framing → activation → demonstration → application/practice → integration) is Merrill's First
Principles, corroborated by Gagné's events, and the digest reports it as **structurally consistent
across models** while varying in emphasis by material type (§3 "Variations by material type"). The
"one running example" and "name the specific thing it teaches" rules are adopted from the reference
course on the **critical-thinking filter** rather than research: they are sound authoring
discipline, and the digest does not cover lesson-level house conventions.
