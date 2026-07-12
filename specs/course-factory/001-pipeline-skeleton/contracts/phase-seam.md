# Contract — phase seam (the black box the orchestrator drives)

**Owner:** spec 001. **Implementers:** 002 (syllabus handler), 003 (skeleton + lesson handlers), 004
(deliver handler / report). 001 ships **stub** handlers against this contract so the spine is testable
now (US2/US3); each later spec replaces its stub **without touching the orchestrator**.

## The seam

The orchestrator (`/course-build`) treats each phase's internal work as opaque. For the current
phase it invokes that phase's handler with a fixed **input envelope** and consumes a fixed **gate
result**. It never inspects the handler's internals.

### Input envelope (orchestrator → handler)

| Field | Meaning |
| :--- | :--- |
| `course_dir` | Path to `courses/<name>/`. |
| `brief` | The parsed `COURSE_BRIEF.md` (topic/scope, audience, running example, `archetype_profile`, `modules`). |
| `prior_artifacts` | Each already-gated upstream artifact **paired with its `DIFFS.md` entries** (FR-027) — never the frozen artifact alone. |
| `insights` | The `insights/` digest (may be empty — valid, FR-025). |
| `resume_state` | The relevant slice of `BUILD_PROGRESS.md`: `syllabus_subphase` / `lessons[]` / `active_loop.round`, so a handler resumes mid-phase and skips completed units. |

### Gate result (handler → orchestrator)

| Value | Orchestrator's action |
| :--- | :--- |
| `pass` | Record the gate `cleared`, advance `current_phase`. |
| `needs-user` | Park: clear the lock, stop, and report the pending user decision (syllabus approval, the blocking post-skeleton scan FR-024, or the round-cap accept-or-comment FR-012). |
| `loop` | If `active_loop.round < 3`, increment and re-invoke the handler; at the cap, convert to `needs-user` (accept-or-comment). |
| `failed` | Halt and surface (FR-022); no advance. |

The handler is responsible for **writing its own artifact(s)** into `course_dir` and for updating its
**owned** `BUILD_PROGRESS.md` fields (002 → `syllabus_subphase`; 003 → `lessons[]`) via `progress.py`
before returning. The orchestrator owns `current_phase`, `phases[].gate_status`, `active_loop`, and
the `lock`.

The envelope is the orchestrator's **push**; `course_dir` additionally grants the handler **read**
access to the course-folder files the driver maintains — notably **`FEEDBACK.md`** (gate-event
feedback, FR-026), which the syllabus handler reads to revise after a change request (see the
`user-approval` gate-type semantics below). Reading a driver-maintained course-folder file via
`course_dir` is a ratified handler input, not a private side channel.

## Gate-type semantics the orchestrator enforces (FR-011)

- **syllabus / `user-approval`** — handler composes; orchestrator parks for the user; approval
  recorded before advance. On a **change request** (not approval) the orchestrator **re-invokes** the
  handler, which reads the user's revision comments from **`FEEDBACK.md`** in `course_dir` (the driver
  appended them there as the gate event occurred — FR-026 / data-model rule 9), revises, and re-parks.
  Post-freeze changes are forward diffs (FR-023).
- **skeletons / `agent-then-user`** — handler runs the agent review loop (cap 3); on agent pass the
  orchestrator parks for the **blocking** user scan (FR-024). A change request re-enters the handler
  with a **fresh** 3-round cap, then re-parks for another scan.
- **lessons / `rubric`** — handler grades each lesson against the rubric (cap 3, then one
  accept-or-comment pass); no mandatory user review. Per-lesson status is `lessons[]`.
- **deliver / `report-generated`** — handler generates `COURSE_REPORT.md`; the orchestrator clears
  the gate on the report's **presence**, **any** verdict (FR-011/021).

## Round-cap ownership (FR-012)

- **001 owns**: the `active_loop.round` counter, cap-at-3 enforcement, and the accept-or-comment
  surfacing (a single extension pass, never more).
- **003 owns**: what one author→critique→refine round *does* (the primitive's internals).

The counter is state (001's `BUILD_PROGRESS.md`); the round body is behind this seam (003's).

## Stubs shipped by 001

Each stub (in `course-factory/.claude/skills/phase-stubs/`) writes a minimal placeholder artifact
(e.g. a `SYLLABUS.md` stub) and returns a **scripted** gate result so every path is exercised: a
straight `pass`, a `loop`→`loop`→`pass`, a cap-hit `needs-user`, and a `failed`. This is what US2's
"each phase's work stubbed to 'produced + gate cleared'" runs against.

**How this is tested without an agent.** The orchestrator's *transition legality* lives in
`progress.py`'s pure transition function (research R1). `test_phase_walk.py` feeds the stubs' scripted
gate results directly into that function and asserts the observable spine properties — phases run in
order, no advance without a recorded gate pass (SC-006), the matched `gate_type` per phase (SC-007),
and the full delivery set at `done` (SC-008) — with no agent in the test loop. The `.claude/` driver
is the thin narrative that, in a live run, obtains those same gate results from the real (or stub)
handlers and calls the same function.
