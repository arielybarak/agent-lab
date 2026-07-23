---
description: Intake a rough COURSE_SPEC.md — upfront clarify interview, then author COURSE_BRIEF.md (profile + module selection). Ask-moment #1 of the pipeline's two.
argument-hint: "<path to COURSE_SPEC.md> [path to course-template/, default course-factory/course-template]"
---

Run intake on: **$ARGUMENTS**

This is **ask-moment #1** (FR-002) — resolve knowable ambiguities and obtain any missing required
content **before** any downstream phase (instantiation, syllabus, …) begins. It produces
`COURSE_BRIEF.md` — the single on-disk home for the clarified spec, the archetype-profile
selection, and the module selection (FR-004). It does **not** copy the template or create the
course folder — that is `/course-instantiate`.

## Steps

1. **Locate the spec.** Read the `COURSE_SPEC.md` path from `$ARGUMENTS` (default
   `course-factory/COURSE_SPEC.md` if none given). If it's missing, empty, or has no recognizable
   structure at all, **halt** here and report why — do not proceed, do not write anything
   (edge case: malformed spec).

2. **Delegate to `intake-interviewer`** (read-only) with the spec path, `course-factory/insights/`,
   and the template's `manifest.yaml`. It returns: resolved fields, knowable-ambiguity questions,
   **blocking questions** for any missing required field, and an archetype-profile + module
   recommendation.

3. **Ask the blocking + knowable-ambiguity questions** yourself, using **AskUserQuestion**, batched
   in as few calls as sensible. Never invent an answer for a blocking question (Principle II /
   FR-003) — if the author truly has no running example yet, keep asking/wait; do not fill one in
   to move things along.

4. **Confirm the archetype-profile and module recommendation** with the author (a quick
   confirm-or-adjust, not an open-ended question — FR-014 reserves open questions for the two
   ask-moments, and this is still ask-moment #1's batch). If the template's manifest offers only
   one profile (the MVP state — `course-template/` ships only `default` until 000 adds more), don't
   spend a question on confirming it: state which profile was used and move on. Still confirm the
   module selection whenever the template offers more than one module.

5. **Author `COURSE_BRIEF.md`** at `<course-spec-dir>/COURSE_BRIEF.md` (or a path you tell the
   author, ready for `/course-instantiate --brief <path>`). Shape: human-readable prose (topic,
   audience, running example, source pointers, why this profile/these modules) followed by exactly
   **one** fenced ` ```json ` block instantiate.py reads:

   ```json
   {
     "topic_scope": {"topic": "...", "in_scope": ["..."], "out_of_scope": ["..."]},
     "audience": {"description": "...", "prior_knowledge": "..."},
     "running_example": "...",
     "source_pointers": ["..."],
     "archetype_profile": "default",
     "modules": {"<module-name>": true},
     "lesson_format": null
   }
   ```

   Every field must be **explicit** — no key omitted, no value fabricated. `lesson_format` stays
   `null` (002 writes it later, per data-model.md).

6. **Report** the brief's path and a one-paragraph summary of what was resolved vs. what the author
   answered, so the next step (`/course-instantiate`) has a clear handoff.

## Anti-fabrication (non-negotiable)

If any required field remains unanswered after asking, **do not proceed** to write
`COURSE_BRIEF.md` with a placeholder — stop and tell the author what's still needed. A brief with
an invented running example or an invented source pointer is worse than no brief at all
(Principle II, SC-001).
