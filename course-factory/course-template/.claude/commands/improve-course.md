---
description: Run one gated iteration of the analyze → plan → author → grade loop that improves this course. Use when you want to work the course toward the rubric's bar.
argument-hint: "<scope, e.g. 'whole course' or a unit name>"
---

Run the course-improvement loop for: **$ARGUMENTS**

You are the **main thread orchestrator** — subagents cannot spawn subagents, so you drive the loop
and you are the **only writer**. Run ONE iteration, stopping at each gate.

```
N = 1    MAX_ROUNDS = 3    (hard cap — never thrash the same files past this)
```

1. **ANALYZE** — survey the current material against the syllabus using skill `backward-design`'s
   coverage check: which outcomes are unserved, which units are orphaned, what is used before it is
   taught. Return the gap list, **highest-leverage gap first**. Name gaps; do not pad them.
2. **PLAN** — propose the smallest change that closes the top gap: which lesson to **deepen** (
   preferred) or, only if the ground is genuinely uncovered, which lesson to add and where. State
   the outcome(s) the change serves.
   - ⛔ **GATE A** — show the proposal; wait for approve / edit / reject before writing anything.
3. **AUTHOR** — *you* (main thread) write **only** the approved change, in the shape the course
   already uses (skill `lesson-arc`; `/new-lesson` for a new lesson). Agents never write files.
4. **REVIEW** — delegate to **`lesson-consistency-reviewer`** for house-form drift on what you
   touched, then to **`course-evaluator`** (author-blind) for the graded assessment against skill
   `quality-rubric` and the factory's grading spec.
   - ⛔ **GATE B** — show the consistency findings, the score table, and the add-on findings.
5. **EXIT TEST** — STOP when the grading spec's pass condition is met, **OR** `N == MAX_ROUNDS`,
   **OR** the user says stop. Otherwise `N += 1` and feed the report's prescribed fixes back into
   step 2.
6. **ON STOP** — on confirmation, write the final report card to `COURSE_REPORT.md` and summarize
   what changed.

Rules: never skip a gate; never let an agent write files; **deepen thin lessons before adding new
ones**; and take the pass condition from the grading spec — do not invent a threshold here.
