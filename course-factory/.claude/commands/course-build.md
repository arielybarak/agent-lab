---
description: Start-or-continue a course build — read BUILD_PROGRESS.md, run the next unit of work, persist, and either advance, park at a gate, or halt. The only command that drives a course through the pipeline.
argument-hint: "<course name> [--template <dir>, default course-factory/course-template]"
---

Drive the course build for: **$ARGUMENTS**

> **Honesty check before you start.** Until specs 002 (syllabus), 003 (skeletons/lessons), and 004
> (grading/report) are implemented, every phase handler you invoke here is the **`phase-stubs`**
> skill — it writes an honest placeholder, never real course content. A build that reaches `done`
> today is a **proof that the spine works**, not a delivered course. Say this plainly to the author
> before driving a build, and never present stub output (`# Syllabus (stub)`, etc.) as if it were
> real. Once 002/003/004 land and replace the stubs, this file's steps are unchanged — only what
> gets invoked in step 3 differs.

There is **no separate resume command** — starting and resuming are the same act (research R2):
read state, do the next unit, persist, then either continue, park at a gate, or stop. A fresh
session with no memory of prior runs does the same thing this command always does. Never
hand-edit `BUILD_PROGRESS.md` — every state change goes through `course-factory/tools/progress.py`.

## 0. Locate the course

`<name>` is required. `course_dir = course-factory/courses/<name>`. If it doesn't exist, **halt**:
tell the author to run `/course-instantiate` first. This command acts on exactly this one named
course — other courses in staging are untouched (FR-019).

## 1. Acquire the lock (FR-028, SC-012)

```bash
python3 course-factory/tools/progress.py lock-acquire course-factory/courses/<name>
```

- **Success** — prints the freshly minted `holder` token; remember it for this invocation.
- **Refused** (non-zero exit, `LockError` on stderr) — another session holds this build within the
  liveness window. **Stop immediately** and report the conflict to the author (name the holder and
  how long ago it last progressed) — never proceed, never overwrite (SC-012).

## 2. Resume (FR-017/018, SC-004/005/009)

```bash
python3 course-factory/tools/progress.py resume course-factory/courses/<name> \
    --template-version "$(cat <template dir>/VERSION)"
```

- **`IntegrityError`** (missing/corrupt/inconsistent state, or a `template_version` drift) — release
  the lock, **halt**, and report the exact problem to the author. Never guess, never "repair"
  the file (FR-022, SC-009).
- **Success** — you now have the full state: `current_phase`, each phase's `gate_status`, any
  `active_loop`, and `lessons[]`. Resume **from this alone** — no memory of a prior session is
  needed or trusted (SC-005).
- If `current_phase == "done"` — report the course already delivered (point at `COURSE_REPORT.md`),
  release the lock, and stop.

## 3. Run the next unit for the current phase

Invoke the **`phase-stubs`** skill for `current_phase` (until 002/003/004 replace it) against
`contracts/phase-seam.md`'s input envelope: `course_dir`, the parsed `COURSE_BRIEF.md`, every prior
gated artifact **paired with its `DIFFS.md` entries** (FR-027 — never the frozen artifact alone once
a diff exists against it), the `insights/` digest, and the relevant resume slice
(`syllabus_subphase` / `lessons[]` / `active_loop`).

**After every persisted unit, refresh the lock** with the **same holder token** from step 1
(per FR-016's persist-before-advance):

```bash
python3 course-factory/tools/progress.py lock-refresh course-factory/courses/<name> --holder <token>
```

Don't substitute `lock-acquire` here — it resets `acquired_at` on every call, which would erase the
audit trail of when this invocation actually started holding the build; `lock-refresh` only touches
`last_progress_at`.

### `syllabus` (`user-approval`) — no round cap

1. If `SYLLABUS.md` doesn't exist yet, run the stub to write it (a fenced json block with the
   planned `lessons: [{id, title}, ...]` — `contracts/phase-seam.md` / the stub's own shape).
2. Present it to the author (**AskUserQuestion**: approve, or comment with changes).
3. **Approve** →
   ```bash
   python3 course-factory/tools/progress.py transition course-factory/courses/<name> pass
   python3 course-factory/tools/progress.py seed-lessons course-factory/courses/<name> \
       course-factory/courses/<name>/SYLLABUS.md
   ```
   The second call reads the now-frozen `SYLLABUS.md`'s lesson list and seeds `lessons[]` with one
   `not-started` entry per planned lesson — this is what lets the skeleton phase know how many
   skeletons to draft (one per lesson, 003's skeleton-handler.md) and what the lessons phase later
   iterates over. Seeding is idempotent (never resets an already-worked lesson, SC-004), so it's
   safe even if this step is somehow re-run. Report the advance to `skeletons`.
4. **Comment** → append the comment to `FEEDBACK.md` (FR-026), re-run the stub to revise
   `SYLLABUS.md`, go back to step 2. No round cap here (FR-012 scopes the cap to skeletons/lessons
   only) — repeat until the author is pleased.

### `skeletons` (`agent-then-user`) — round-capped agent review, then a **blocking** scan (FR-024)

1. If the skeleton files don't exist yet, run the stub to draft the whole batch — one skeleton
   per lesson seeded in `lessons[]` (see the syllabus step above).
2. Run the agent-review loop: `progress.py transition <dir> loop` once per round.
   - **Passes under the cap** → `progress.py clear-active-loop <dir>`, go to step 3.
   - **Hits the cap** (`active_loop.round` reaches `progress.ROUND_CAP` — check `course-status`'s
     output rather than assuming the number, it's `progress.py`'s constant to own) → present the
     current best batch to the author for **accept-or-comment** (AskUserQuestion): **accept** →
     `accept-round-cap <dir>`; **comment** → **append the author's comment to `FEEDBACK.md`**
     (FR-026 — the round-cap accept-or-comment is the first case that rule names, and it is durable
     author feedback exactly like the syllabus-revision and post-skeleton-scan comments), then
     `extend-round-cap <dir>`, run **exactly one** more stub round, then `progress.py transition
     <dir> loop` again (its outcome settles regardless — FR-012). Either way, go to step 3.
3. **The blocking user scan** — present the agent-cleared batch to the author (AskUserQuestion:
   approve, or request changes). This is a **separate** gate from the round cap above; it is
   **mandatory** even if the agent review passed on round 1 (SC-011).
   - **Approve** → `progress.py transition <dir> pass`. Report the advance to `lessons`.
   - **Change request** → append the comment to `FEEDBACK.md`, re-run the skeleton stub
     incorporating it, and restart step 2 with a **fresh** round cap (FR-024). Re-present for
     another blocking scan afterward.

### `lessons` (`rubric`) — one round-capped cycle per lesson, serial (`pool_width` = 1 at MVP)

For each lesson in `lessons[]` not yet `passed` / `accepted-at-cap` (in order — never re-work one
already terminal, SC-004):

1. Run the lesson stub for that lesson.
2. Run its round-cap cycle exactly like the skeleton agent-review above (`loop` →
   `clear-active-loop` on an early pass, or the accept/extend path at the cap — **including the
   `FEEDBACK.md` append on a cap-`comment`**, FR-026) — **no mandatory user review** here (FR-011);
   a rubric pass is enough.
3. Record it: `progress.py set-lesson-status <dir> <lesson-id> passed` (or `accepted-at-cap` if it
   only cleared via the cap extension).

Once **every** lesson in `lessons[]` is terminal — not before — `progress.py transition <dir> pass`
to clear the phase and advance to `deliver`. A single lesson settling its own round cap never does
this on its own.

### `deliver` (`report-generated`) — unconditional on presence (FR-011/021)

1. Run the deliver stub to write `COURSE_REPORT.md` (any verdict).
2. `progress.py transition <dir> pass`. Report `done`, then run:
   ```bash
   python3 course-factory/tools/deliver_check.py course-factory/courses/<name>
   ```
   and surface its result (it should pass — this is a sanity check, not the gate itself; the gate
   already cleared on the report's presence).

## 4. Forward diffs (FR-023/027, SC-010)

If, at any point, the author's feedback describes a change that belongs to an **already-gated**
earlier phase (e.g. a skeleton-phase note that really means "fix the syllabus"), **never** re-open
that phase. Apply the change at the **current** phase's artifact and log it:

```bash
python3 course-factory/tools/diffs.py course-factory/courses/<name>/DIFFS.md \
    --target <earlier phase or artifact> \
    --what-changed "<the concrete delta>" \
    --why "<the gap it fills>" \
    --applied-at-phase <current_phase>
```

`current_phase` never moves backward, no matter how it's phrased to you.

## 5. Park, release the lock, and stop

Whenever a step above ends at a human gate that hasn't been answered yet in this same
conversation (the author isn't available, or you've reached the end of this turn), release the
lock cleanly:

```bash
python3 course-factory/tools/progress.py lock-release course-factory/courses/<name>
```

Report exactly where the build is parked and what's needed to continue (which gate, which
question). The next `/course-build <name>` — same session or a brand new one — resumes from
`BUILD_PROGRESS.md` alone and re-presents the same pending decision (step 2 handles this
automatically; nothing here needs a special "was I parked?" check).

## Boundaries

- **Never hand-edit `BUILD_PROGRESS.md`.** Every field change goes through `progress.py`.
- **Never call `transition ... pass` for `skeletons` or `lessons` on a single unit's settle.** A
  refine cycle settling (`clear-active-loop` / `accept-round-cap` / `extend-round-cap`) only ever
  clears `active_loop` — the phase itself clears only when its own full condition is met (the
  blocking scan for skeletons; every lesson terminal for lessons).
- **Never ask an open-ended clarifying question mid-batch** (FR-014) — only the two ask-moments
  (intake, and post-research divergence — 002's) and the scheduled gates above interrupt.
- **Never fabricate a gate result.** If a stub or a real handler hasn't actually produced/reviewed
  something, don't report `pass` to make progress look further along than it is.
