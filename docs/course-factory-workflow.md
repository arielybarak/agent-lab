# course-factory build workflow — personal notes

## Stage order, per spec (000–004)

1. `/speckit-specify` — write/update `spec.md` from a description.
2. `/speckit-clarify` — up to 5 targeted questions; answers get written into spec.md's
   `## Clarifications` section.
3. *(optional)* `/speckit-checklist` — generate a custom quality checklist for the spec.
4. `/speckit-plan` — generate `plan.md` (+ `research.md`, `data-model.md`, `contracts/`,
   `quickstart.md`). Reads the constitution for the "Constitution Check" gate.
5. `/speckit-tasks` — generate `tasks.md`, dependency-ordered.
6. *(optional)* `/speckit-analyze` — read-only cross-check of spec.md ↔ plan.md ↔ tasks.md
   for contradictions/gaps. Reports findings, doesn't edit anything.
7. `/speckit-implement` — actually executes tasks.md (writes real code).
8. `/speckit-converge` — after manual work or drift, diffs the codebase against
   spec/plan/tasks and appends any remaining work as new tasks.
9. `/speckit-taskstoissues` — optional alternative to step 7: push tasks as GitHub issues
   instead of implementing locally.

`/speckit-constitution` — separate, project-level (not per-spec). Creates/updates
`.specify/memory/<project>/constitution.md`. Already done for course-factory (currently v1.2.2).

**"Refinement" isn't a separate command.** It means: re-run `/speckit-clarify`, or hand-edit
spec.md/plan.md, or address `/speckit-analyze` findings manually — then re-run whatever step
that touched.

## Current status (as of 2026-07-11)

| Spec | Status | Next command |
| :--- | :--- | :--- |
| 000-course-template | Drafted, not yet clarified | `/speckit-clarify` |
| 001-pipeline-skeleton | Clarified | `/speckit-plan` |
| 002-syllabus | Clarified | `/speckit-plan` |
| 003-lessons | Clarified | `/speckit-plan` |
| 004-grading-delivery | Clarified | `/speckit-plan` |

Recommended build order (per `specs/course-factory/README.md`):
**000 → 001 → 002 → 004 (rubric core only) → 003 → 004 (rest: delivery/harvest/comparison)**

## The critical gotcha — "which spec am I planning?"

`/speckit-plan`, `/speckit-tasks`, `/speckit-implement` etc. do **not** take a feature number
as their argument. Whatever you type after the command is just free-text *guidance* — it is
**not** used to pick which spec you're targeting.

They determine the target spec from **`.specify/feature.json`**:
```json
{ "feature_directory": "specs/course-factory/000-course-template" }
```
Whatever this file currently points at is what `/speckit-plan` (etc.) will act on.

Right now (checked this session) it points at **000-course-template**.

So: typing `/speckit-plan 000` in a new session does **not** mean "plan spec 000" — "000" would
just get swallowed as ignored guidance text, and the command would run against whatever
`feature.json` currently says (could be the wrong spec!).

**What to actually type:** say which spec by name, and let Claude switch the pointer first:
- `"Plan spec 001 (specs/course-factory/001-pipeline-skeleton) — run /speckit-plan"`
- `"Switch active feature to 002-syllabus, then run /speckit-plan"`

Either phrasing works — CLAUDE.md's footgun notes auto-load every session in this repo, so a
fresh session already knows to check/update `.specify/feature.json` (or
`SPECIFY_FEATURE_DIRECTORY`) before invoking the skill. You don't need to know the mechanism
yourself, just **name the spec explicitly** instead of assuming a bare number in the slash
command does it.

## Constitution reminder

- Real file: `.specify/memory/course-factory/constitution.md` — edit this one.
- `.specify/memory/constitution.md` is a **symlink** (= "which project is active" selector).
  Never `Write` to it directly — that replaces the symlink with a real file.
- If broken: `ln -s course-factory/constitution.md .specify/memory/constitution.md`
