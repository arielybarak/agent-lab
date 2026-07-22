---
name: katas
description: >-
  Optional module — standalone practice exercises alongside the lessons: what makes a good kata,
  the exercise folder shape (brief, hints, reference solution), how katas pair with the lessons
  they reinforce, and the checkable-completion rule. USE WHEN adding practice exercises, designing
  a capstone task, or deciding whether a lesson needs a kata.
---

# Katas (optional module)

> **Optional module.** Enable it for courses where competence is *performed* rather than recalled.
> Disable it and the core is untouched — the core's in-lesson practice stage does not depend on it.

## When to Activate This Skill

- Adding a standalone practice exercise for a lesson or unit
- Designing a larger integration/capstone task
- Deciding whether a lesson needs a kata at all

## Kata vs in-lesson practice

The core arc already requires **practice with feedback inside every lesson** (skill `lesson-arc`).
A kata is different and is only worth adding when the difference matters:

| | In-lesson practice | Kata |
| :--- | :--- | :--- |
| Scope | one move, just demonstrated | the whole idea, applied unaided |
| Guidance | scaffolded, fades within the lesson | none by default; hints on request |
| Timing | immediately after demonstration | after the lesson, and again later (spacing) |
| Purpose | check the step landed | check the learner can do it cold |

If a proposed kata is just the lesson's practice stage moved to another file, drop it — that is
duplication, not reinforcement.

## What makes a good kata

- **One clear task, stated as a goal, not as instructions.** The learner decides the approach.
- **Self-checkable.** There is a reference solution, an expected result, or an explicit criterion.
  A kata with no way to know you were right is a prompt, not practice.
- **Sized honestly.** State the expected effort. Katas that silently take five times longer than
  advertised are abandoned.
- **Traceable to an outcome** (skill `backward-design`). A kata that serves no outcome is a puzzle.
- **Failure-mode-aware.** The best katas are built around the mistake learners actually make, so
  the reference solution teaches something the lesson could not.

## Exercise shape

Each kata is a self-contained folder with a stable identifier that encodes its unit and order, so
katas sort in the sequence they are meant to be attempted:

```
exercises/<unit><NN>-<slug>/
├── brief          the task, the goal, the expected effort, the success criterion
├── hints          progressive hints — each one reveals as little as possible
├── starter        (optional) the scaffolding the learner begins from
└── solution       the reference solution, with the reasoning, not just the answer
```

- **Hints are progressive.** Hint 1 re-frames the problem; the last hint is close to the answer.
  One monolithic hint is a spoiler.
- **The reference solution explains itself.** It shows the reasoning and names the mistake the kata
  is built around. An answer with no explanation teaches only whether you matched it.
- **Never edit generated artifacts.** If any part of the exercise tree is produced by a build step,
  edit the source and re-run it.

## Pairing katas with lessons

- Pair a **warm-up kata** with the lesson that introduces the idea, and the **integration kata**
  with the unit that combines several.
- Sequence katas by dependency, exactly as the lessons are sequenced — a kata must never need an
  idea the learner has not met.
- **Space the revisits.** A kata repeated later, in a slightly different guise, is worth more than a
  second new kata on the same idea.
- Every kata thread the course's **running example** where it plausibly fits; a kata about an
  unrelated toy scenario breaks the continuity the course is built on.

## The completion check

A unit's katas are "done" when: every kata has a reference solution that actually works, every
kata's success criterion is stated, and the whole set is traceable to the unit's outcomes. If the
course has an automated check for exercises, it runs green before the unit is called finished.

## Provenance

Derived from the reference course's practice machinery — the standalone kata/capstone distinction,
the exercise-folder shape (brief + hints + reference solution) with an identifier encoding unit and
order, the pair-a-warm-up-with-the-capstone rule, and the never-hand-edit-generated-artifacts rule —
all carried in that course's curriculum skill and architect agent. Its subject-specific kata list
and build tooling were dropped. Grounded additionally in the research digest §4 (demonstration +
application with feedback is a cross-model invariant) and §2 (spaced, cumulative practice for
procedural and drill-heavy material), which is why practice is **core** and only the *standalone
exercise* layer is optional. See `CLASSIFICATION.md`.
