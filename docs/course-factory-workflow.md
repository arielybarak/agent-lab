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
8. `/speckit-converge` — **"did we actually build everything tasks.md asked for?"**
   Re-reads spec/plan/tasks, checks the code against them, and appends anything
   missing/partial/contradicting as a new task phase (never edits code itself — that's
   `/speckit-implement`'s job on the next pass). Run it after `/speckit-implement`, or any
   time the code and the tasks might have drifted (manual edits, a stalled session). Clean
   result = tasks.md is left untouched and it says so.
9. `/speckit-taskstoissues` — optional alternative to step 7: push tasks as GitHub issues
   instead of implementing locally.

`/speckit-constitution` — separate, project-level (not per-spec). Creates/updates
`.specify/memory/<project>/constitution.md`. Already done for course-factory (currently v1.3.0).

**"Refinement" isn't a separate command.** It means: re-run `/speckit-clarify`, or hand-edit
spec.md/plan.md, or address `/speckit-analyze` findings manually — then re-run whatever step
that touched.

## Current status (as of 2026-07-22)

All five specs are **Tasked** — each has `plan.md`, `research.md`, `data-model.md`, `contracts/`,
`quickstart.md`, and `tasks.md`. Nothing is built yet.

| Spec | Status | Next command |
| :--- | :--- | :--- |
| 000-course-template | Tasked | `/speckit-implement` |
| 001-pipeline-skeleton | Tasked | `/speckit-implement` |
| 002-syllabus | Tasked | `/speckit-implement` |
| 003-lessons | Tasked | `/speckit-implement` |
| 004-grading-delivery | Tasked | `/speckit-implement` (built in two slots — see build order) |

Recommended build order (per `specs/course-factory/README.md`):
**000 → 001 → 002 → 004 (rubric core only) → 003 → 004 (rest: delivery/harvest/comparison)**.
That file also has per-phase model guidance (Opus vs. Sonnet by judgment density) and the two
windows where phases can build in parallel across sessions.

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

## Is there a "review" stage after `/speckit-implement`?

**Split across two different tools — no single command does both halves.**

**(b) "did we build exactly what the plan/tasks called for"** → this is `/speckit-converge`
(step 8 above). It's spec-kit-aware: it reads `spec.md`/`plan.md`/`tasks.md` as the source of
intent and reports `missing` / `partial` / `contradicts` / `unrequested` against them.

**(a) "holes, quality, refinement, optimization opportunities"** → **no spec-kit command covers
this.** `/speckit-analyze` (step 6) is the closest-sounding name, but it runs *before*
`/speckit-implement` and only cross-checks spec ↔ plan ↔ tasks against each other — it never
looks at code. Once code exists, the tools for (a) are generic, not spec-kit-native:

- `/code-review` — reviews the working diff for correctness holes/bugs.
- `/simplify` — quality-only pass: reuse, simplification, efficiency, cleanups (not a bug hunt).
- `/security-review` — security posture of the pending changes.

None of these three read `spec.md`/`plan.md` — they review the diff on its own terms, so they
won't catch "this technically works but drifted from what the spec intended" (that's
`/speckit-converge`'s job) or cross-spec seam issues (that needs a manual pass, as in the
`003`/`004` hardening — see `REVIEW-findings.md`/`findings-FIXES.md`).

**Practical order per spec, once code exists:** `/speckit-implement` → `/speckit-converge`
(completeness) → `/code-review` + `/simplify` (quality) → repeat converge if anything got
added/changed. `/speckit-harden` (the custom skill used to plan 001–004) has no post-implement
counterpart in this repo — worth defining one if this loop gets used often.

## Constitution reminder

- Real file: `.specify/memory/course-factory/constitution.md` — edit this one.
- `.specify/memory/constitution.md` is a **symlink** (= "which project is active" selector).
  Never `Write` to it directly — that replaces the symlink with a real file.
- If broken: `ln -s course-factory/constitution.md .specify/memory/constitution.md`
