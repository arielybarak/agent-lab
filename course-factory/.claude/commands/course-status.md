---
description: Read-only render of a course's BUILD_PROGRESS.md — current phase, gate statuses, lessons, any active refine loop, and lock state. Never changes state.
argument-hint: "<course name>"
---

Report status for: **$ARGUMENTS**

This command **never** advances, parks, or otherwise changes state — it only reads and renders.

## Steps

1. `course_dir = course-factory/courses/<name>`. If it doesn't exist, say so and point at
   `/course-instantiate`.
2. Read the state (read-only, no lock acquired):
   ```bash
   python3 course-factory/tools/progress.py show course-factory/courses/<name>
   ```
   On an `IntegrityError` (missing/corrupt/inconsistent state, `/course-build` would halt too) —
   report the problem plainly; don't attempt a fix here.
3. Render for the author:
   - **Current phase** and its gate type (user-approval / agent-then-user / rubric /
     report-generated), plus each phase's `gate_status` and `cleared_at` if cleared.
   - **`lessons[]`** — a done/todo count and the list of not-yet-terminal lesson ids, if the build
     is in the lessons phase.
   - **`active_loop`** — if set, which phase it belongs to and its `round` count (the cap itself is
     `progress.ROUND_CAP` — read it from the tool rather than restating a number here).
   - **`lock`** — whether the build is currently held (by whom, last progress timestamp) or free.
   - **`template_version`** stamped into this course.
4. If `current_phase == "done"`, point at `COURSE_REPORT.md` instead of a phase status.

## Boundaries

- Read-only: never calls `progress.py transition`, `lock-acquire`, or any other mutating
  subcommand. Use `/course-build <name>` to actually advance a build.
