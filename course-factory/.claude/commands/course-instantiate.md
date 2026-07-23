---
description: Copy the frozen course-template into a new course folder, overlaying the intake brief's profile + modules, and initialize BUILD_PROGRESS.md at syllabus start.
argument-hint: "--brief <path to COURSE_BRIEF.md> [--spec <path to COURSE_SPEC.md>] [--template <dir>] [--courses-dir <dir>]"
---

Instantiate a course from: **$ARGUMENTS**

A thin command — the mechanical work (copy-never-mutate, overlay, version stamp, state + stub
init) is `course-factory/tools/instantiate.py` (FR-006/007/008); this command just calls it and
reports the result.

## Steps

1. Resolve defaults if not given in `$ARGUMENTS`: `--template course-factory/course-template`,
   `--courses-dir course-factory/courses`. `--brief` is required (the output of `/course-intake`);
   `--spec` is optional (only used to derive the course-name slug from its title).

2. Run:

   ```bash
   python3 course-factory/tools/instantiate.py \
       --spec <spec path, if you have one> \
       --template <template dir> \
       --brief <brief path> \
       --courses-dir <courses dir>
   ```

3. **On success** — report the created `courses/<name>/` path, the stamped `template_version`, and
   remind the author that `BUILD_PROGRESS.md` is positioned at the start of the syllabus phase;
   `/course-build <name>` is the next step.

4. **On halt** (non-zero exit) — the tool prints the reason to stderr (a missing required brief
   field, or an absent/unversioned template). Report it verbatim; do **not** retry with a guessed
   fix or a hand-edited brief — send the author back to `/course-intake` or point them at the
   template defect. No partial course folder is ever left behind (the tool stages then renames
   atomically, cleaning up on any failure) — there is nothing to clean up on your end.

## Boundaries

- Never hand-edit `BUILD_PROGRESS.md` or copy template files yourself — always go through
  `instantiate.py`, which is what makes SC-002/003/009 mechanically true rather than
  agent-discipline-true (research R1).
- Never invent a missing brief field to get past a halt — that is `/course-intake`'s job to
  re-resolve with the author (Principle II).
