---
name: phase-stubs
description: >-
  001's placeholder phase handlers for syllabus/skeletons/lessons/deliver — write a minimal
  artifact and return a scripted gate result against contracts/phase-seam.md, so /course-build is
  testable end-to-end before specs 002/003/004 replace each stub with real content. USE WHEN
  /course-build reaches a phase and needs to invoke that phase's handler.
---

# Phase stubs (the seam 002/003/004 will replace)

Each phase's *internal* work — research, drafting, grading — is a black box behind
`contracts/phase-seam.md`: given the course folder + brief + prior gated artifacts (each read
together with its `DIFFS.md` entries, FR-027), a handler writes its artifact(s) and returns a gate
result. `/course-build` never looks inside a handler; it only consumes the gate result. This skill
is what **001** ships in place of 002/003/004's real handlers, so the spine is provable now.

## What each stub does

A stub never fabricates course content — it writes an explicit placeholder, never invented
subject-matter (Principle II still applies to a stub's *own* output, even though it isn't real
content). Placeholder text always says plainly that it's a stub.

| Phase | Writes | Placeholder shape |
| :--- | :--- | :--- |
| `syllabus` | `SYLLABUS.md` | prose + one fenced ` ```json ` block: `{"lessons": [{"id": "L01", "title": "..."}, ...]}` — `progress.seed_lessons()` reads this to populate `lessons[]` (see `course-build.md`'s syllabus step) |
| `skeletons` | `skeletons/<lesson-id>.md` per lesson already seeded in `lessons[]` | `# Skeleton: <id> (stub)\n` |
| `lessons` | `lessons/<lesson-id>.md` (or `.ipynb` — 002's format decision) | `# Lesson: <id> (stub)\n` |
| `deliver` | `COURSE_REPORT.md` | a minimal scorecard shape with a placeholder verdict |

**On `syllabus`'s json block:** this is the one piece of *structure* a stub must get right even
though its *content* is a placeholder — `parse_syllabus_lessons()` needs a real, non-empty
`lessons` list (even if each title is `"(stub)"`) or `/course-build`'s seed step halts
(`IntegrityError`). A stub may also demonstrate `progress.py set-syllabus-subphase <dir> presented`
once it writes the file — 002's real handler walks all four sub-phases
(`research-in-progress → research-done → composed → presented`); the stub only needs the last one.

## Gate results a stub returns — and who decides them

For a **live demo/manual run**, the invoking session picks the gate result to script (there is no
real agent-review or rubric yet) — state plainly in the transcript that it's scripted, per
`quickstart.md`'s scenario list: a straight `pass`, a `loop`→`loop`→`pass`, a cap-hit
`needs-user`, and a `failed`. For **automated tests**, `test_phase_walk.py` feeds these same
values directly into `progress.transition()` — no handler code runs at all (research R1's "no
agent in the test loop").

**Important: a refine cycle settling (under the cap, or via accept/extend at the cap) is never the
same as the *phase* clearing.** `progress.py`'s `loop`/`clear_active_loop`/`accept_round_cap`/
`extend_round_cap` only ever touch `active_loop` — none of them advance `current_phase`. Only an
explicit `progress.py transition <dir> pass` clears a phase's gate and moves to the next one. This
is what lets `skeletons` (one round-cap cycle, then a *separate* blocking scan) and `lessons`
(**several** round-cap cycles, one per lesson, before the phase itself is done) share the same
mechanism without either one auto-advancing early.

### The one nuance `/course-build` must get right per phase (contracts/phase-seam.md)

- **`syllabus`** (`user-approval`) — the stub always returns `needs-user` once it's written
  `SYLLABUS.md` (never `pass` on its own — a syllabus never self-clears; only the author's
  explicit approval, applied by the driver calling `progress.py transition <dir> pass`, clears it).
  No round cap applies here (FR-012 scopes the cap to skeletons/lessons only) — a change request
  just re-invokes the stub, which rewrites the placeholder and returns `needs-user` again.
- **`skeletons`** (`agent-then-user`) — the stub's *own* agent-review loop uses the round-cap
  mechanism: `progress.py transition <dir> loop` per round. If it passes **under** the cap, settle
  with `progress.py clear-active-loop <dir>`; if it **hits** the cap, ask the author accept-or-comment
  and resolve with `accept-round-cap` or `extend-round-cap`. Either way, once the agent side has
  settled, the stub reports **`needs-user`** to the seam — **never `pass`** — because FR-024's
  blocking user scan still has to happen before the phase itself may clear. Only after the
  author's explicit approval of that scan does `/course-build` call `transition <dir> pass`. A
  change request at the scan re-invokes the stub for a **fresh** round cap (`progress.ROUND_CAP`,
  FR-024).
- **`lessons`** (`rubric`) — the stub works one lesson at a time (MVP is serial, `pool_width`=1 —
  see `course-factory/DESIGN.md`). For **each** lesson: run its own round-cap cycle exactly like
  skeletons above (`loop` → `clear-active-loop` on an early pass, or `accept`/`extend-round-cap`
  at the cap), then record the lesson with `progress.py set-lesson-status <dir> <id> passed` (or
  `accepted-at-cap`). Only once **every** lesson is terminal does `/course-build` itself call
  `transition <dir> pass` to clear the phase — no single lesson's settle does that.
- **`deliver`** (`report-generated`) — the stub writes `COURSE_REPORT.md` with a placeholder
  verdict; `/course-build` then calls `transition <dir> pass` unconditionally once it exists —
  presence, not verdict, clears delivery (FR-011/021). **Note for 004:** this stub writes the file
  itself; the *real* handler differs mechanically, not just in content — `/course-report` is a
  **mandatory-core template command** (004's `contracts/course-report.md`), inherited into the
  *course's own* `.claude/` at instantiation, so the real deliver step is "invoke the course's
  inherited `/course-report`," not a factory-side handler analogous to 002/003's.

## Boundaries

- A stub never invents real subject-matter content — its whole point is to be an honest
  placeholder, not a preview of 002/003/004's output.
- A stub never calls `progress.py transition ... pass` itself — only `/course-build`, once the
  *phase's own* condition is met (not just one unit's refine cycle), does that.
- 002/003/004 replace these stubs **file-for-file** against the same seam; nothing in
  `/course-build` or `progress.py` should need to change when they do.
