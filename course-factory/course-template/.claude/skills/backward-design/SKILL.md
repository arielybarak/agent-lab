---
name: backward-design
description: >-
  The course-level backbone every course is built on — outcomes first, then the evidence that
  proves them, then the learning experiences that get there (backward design). Covers writing
  observable outcomes, choosing evidence, sequencing units by dependency, and the coverage check
  that keeps a syllabus honest. USE WHEN planning or revising a syllabus, sequencing modules,
  deciding what a unit is for, or checking that lessons actually serve the stated outcomes.
---

# Backward Design (the course backbone)

## When to Activate This Skill

- Planning a syllabus or re-sequencing its units
- Deciding what a module/lesson is *for* before writing any of it
- Checking whether the drafted material actually reaches the stated outcomes
- Judging a coverage gap: real gap, or padding?

## The one rule

**Design in this order, never the reverse:**

```
1. OUTCOMES     what the learner must be able to DO afterwards
2. EVIDENCE     how we would know they can do it (assessment / artifact)
3. EXPERIENCES  the lessons, practice, and feedback that get them there
```

Content chosen before outcomes is a reading list, not a course. If you cannot name the evidence
for an outcome, the outcome is not yet written well enough to teach.

## Stage 1 — Outcomes

- State each outcome as an **observable learner action** ("derive X from Y", "explain when A beats
  B", "build a working Z"), not as a topic ("databases", "the Renaissance").
- Separate the **few enduring outcomes** (worth remembering years later) from the **supporting
  ones** (needed to reach them). Sequence supporting outcomes as prerequisites of enduring ones.
- Each outcome gets a **difficulty level**: recall / apply / analyze / create. A course that is all
  recall teaches nothing transferable; a course that is all create has no floor.
- Anchor the whole set to the **audience's starting point**. Write down what is assumed known —
  that assumption is the contract the lessons must honor.
- **Name the misconceptions each outcome must defeat.** For every enduring outcome, write down what
  learners typically get wrong on the way to it — the plausible-but-false belief, the step everyone
  skips, the confusion between two neighbouring ideas. This list is the most reusable artifact in
  the whole design: it tells lessons what to frame against, and it is what makes assessment
  *diagnostic* rather than merely scored (Stage 2).

## Stage 2 — Evidence

For every outcome, name the artifact that would demonstrate it *before* you draft the lesson:

| Outcome level | Typical evidence |
| :--- | :--- |
| Recall | short-answer / retrieval prompts inside the lesson |
| Apply | a worked task the learner completes with the method just shown |
| Analyze | compare two options and justify a choice, with the trade-off named |
| Create | a produced artifact judged against stated criteria |

Rules:

- **Every outcome has at least one piece of evidence**, and every assessment traces to an outcome.
  An assessment with no outcome is scope creep; an outcome with no evidence is a wish.
- **Build the evidence around the misconceptions** named in Stage 1. An item a learner can miss for
  several unrelated reasons tells you nothing; an item designed so that *one specific* wrong belief
  produces *one specific* wrong answer tells you exactly what to reteach. Distractors are where the
  diagnosis lives — choose them, don't fill them.
- Evidence is **formative first** — inside the lesson, cheap, repeatable, feedback-bearing. Reserve
  end-of-unit evidence for integration.
- The rubric (skill `quality-rubric`) grades the *material*; this stage defines what the *learner*
  is asked to produce. They are different objects — do not collapse them.

## Stage 3 — Learning experiences

- Every lesson instantiates the canonical arc (skill `lesson-arc`) in service of one or two
  outcomes. A lesson serving no named outcome is cut, not kept "for context".
- **Choose teaching techniques from the library, not from instinct.** `course-factory/pedagogy/
  DIGEST.md` holds all 8 techniques on one screen with their evidence tiers and — more importantly
  — their **boundary conditions**: when each one stops working. Match the technique to the
  outcome's level and the material's shape; open the full `pedagogy/catalog/` entry when you need
  its worked example or shape-specific guidance. Never justify a choice with an entry from
  `pedagogy/MYTHS.md` (see skill `lesson-arc` § Grounding, which also states the rule standalone).
- **Two of the techniques are course-level decisions, not lesson-level ones.** **Spacing** and
  **interleaving** are settled here, in the syllabus — where each enduring idea returns, and where
  problem types get mixed. A lesson cannot retrofit them. Plan them with the revisit schedule
  (see the profile's spine), not per lesson.
- **Sequence by dependency, not by tidiness.** Order units so nothing is used before it is taught;
  where a concept must recur, plan the revisit deliberately (see the profile's spine) instead of
  repeating it by accident.
- **Deepen before adding.** If an outcome is already partly served by an existing lesson, extend
  that lesson; a new lesson is justified only by genuinely uncovered ground.
- **One running example threads the whole course.** Pick a single concrete artifact/scenario the
  course keeps returning to, and reuse it. Continuity is what makes lessons cumulative rather than
  a pile of unrelated toys.

## The coverage check

Before a syllabus is called done, verify all four:

1. **Every outcome** maps to ≥1 unit and ≥1 piece of evidence.
2. **Every unit** maps to ≥1 outcome (no orphan content).
3. **Nothing is used before it is taught** (walk the dependency order once, in reader order).
4. **Gaps are named, not padded.** An uncovered outcome is written down as a gap; it is never
   papered over with adjacent material that does not actually serve it.

## Gotchas

- **Topic lists masquerading as outcomes.** "Covers recursion" is a topic. "Traces a recursive
  call to its base case and predicts the result" is an outcome. Only the second can be assessed.
- **Assessment drift.** Rewriting a lesson without re-checking its evidence silently breaks the
  outcome→evidence→experience chain. Re-run the coverage check after any structural edit.
- **Coverage padding.** Adding material because the syllabus "looks thin" inflates the course
  without serving an outcome. Name the gap instead — an honest gap is a better artifact than
  filler.
- **The audience assumption is load-bearing.** Most incoherent courses are coherent for a
  *different* learner than the one stated. When a lesson feels too fast or too slow, re-read the
  assumed starting point before rewriting the lesson.

## Provenance

Grounded in the external research digest: backward design (Wiggins & McTighe, *Understanding by
Design*) supplies the outcomes → evidence → experiences backbone; outcome/assessment alignment is
one of the digest's cross-model **invariants** (§4), shared by competency-framed and
project-framed courses alike. The "deepen before adding" and "name gaps, don't pad" rules are
adopted from the reference course on the **critical-thinking filter** (sound authoring discipline,
not research-derived) — see `CLASSIFICATION.md`.
