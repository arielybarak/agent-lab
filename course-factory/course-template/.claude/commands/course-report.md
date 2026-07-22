---
description: Grade the course — run the course-evaluator and save its report card to disk. Use when you want a fresh, evidence-cited quality assessment of the course.
argument-hint: "<scope, e.g. 'whole course' or a unit name>"
---

Produce a graded course report for: **$ARGUMENTS**

1. Delegate to the **`course-evaluator`** agent (read-only, author-blind). It grades the course
   material against skill `quality-rubric` — its core dimensions plus every **topic add-on** this
   course enabled in its brief — citing `file:line` for each score, and applying the weights,
   thresholds, and gates from the factory's grading spec (the template does not define them).
2. **Show the returned report card** in full: score table (core rows, then add-on rows, then the
   overall result), executive summary, per-dimension findings with prescribed fixes, add-on
   findings, and the final verdict with its prioritized fix list.
3. On confirmation, write it to the course's `COURSE_REPORT.md`.

**Report the verdict as it came back.** A weak verdict is delivered, not withheld and not softened
— it is the input to `/improve-course`. If the grading spec's thresholds were unavailable, say the
overall verdict could not be computed and report the per-dimension scores and findings anyway.
