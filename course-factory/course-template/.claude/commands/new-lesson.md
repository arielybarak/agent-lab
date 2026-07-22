---
description: Scaffold a new lesson in the course's canonical arc, threaded through the course's running example. Use when starting a lesson or writing up a concept.
argument-hint: "<lesson topic and its unit, e.g. 'recursion in Unit 3'>"
---

Scaffold a new lesson: **$ARGUMENTS**

Follow skill `lesson-arc` exactly, and skill `backward-design` for what the lesson is *for*.

1. **Place it.** Decide the unit and the number (zero-padded, core vs optional placement) from the
   syllabus. **Name the outcome(s) this lesson serves** — if it serves none, stop and fix the
   syllabus first, do not write the lesson.
2. **Check for existing coverage before writing anything new.** If an existing lesson already
   partly serves this outcome, deepen that lesson instead of adding a parallel one. Say which you
   chose and why.
3. **Write the lesson in the arc, in order:**
   **Framing** (the concrete problem/question this answers — lead with the need) →
   **Activation** (the prerequisite or prior lesson it attaches to) →
   **Demonstration** (worked example / model / walked derivation) →
   **Practice + feedback** (tasks with a reference answer or a stated check) →
   **Integration / transfer** (apply it in a new context; connect back to the running example).
   Include optional sections (a "what breaks without this" motivator, a deep dive, a trade-offs
   note) only where they earn their place — never to fill the shape.
4. **Thread the course's running example.** Use the established cast/parts from the course brief;
   do not invent a fresh unrelated example.
5. **Name the one thing the lesson teaches** — the misconception it fixes, the decision it enables,
   or the failure it prevents. A lesson without one is a topic; rewrite it until it has one.
6. **Show the reasoning behind any figure or result** you present, or cite its source.
7. If the **diagrams module** is enabled and this lesson needs a visual, add it with `/add-diagram`
   so the reference resolves. Skip this step entirely when the module is off.

Teaching-first: motivate before you explain. Do not open with the answer.
