# Contract — syllabus phase handler (how 002 implements 001's seam)

**Owner:** spec 002. **Consumes:** 001's `phase-seam.md` (the envelope + gate-result vocabulary),
`build-progress-schema.md` (the `syllabus_subphase` field), `course-folder.md` (the `SOURCES.md` /
`SYLLABUS.md` stubs + delivery membership). 002 **replaces 001's syllabus stub** with this handler and
**changes nothing in the orchestrator** — same input envelope in, same gate-result vocabulary out.

## Input envelope consumed (orchestrator → handler)

Per `phase-seam.md`, the handler reads exactly:

| Field | 002's use |
| :--- | :--- |
| `course_dir` | Where `SOURCES.md` / `SYLLABUS.md` are written and `COURSE_BRIEF.md` is augmented. |
| `brief` | Reads `topic_scope`, `audience`, `running_example`, `archetype_profile`, `source_pointers`, `modules`; keeps the syllabus consistent (FR-010/015). Writes back **only** `lesson_format` (FR-009). |
| `prior_artifacts` | Each gated upstream artifact **paired with its `DIFFS.md` entries** (FR-017). At first syllabus compose this is **empty** — syllabus is the first gated phase (R7); the pairing is honored structurally for the downstream/forward-diff case. |
| `insights` | Read as a composition input alongside `SOURCES.md`; **empty/missing is valid** (FR-016). |
| `resume_state` | The `syllabus_subphase` slice — the handler skips any sub-step the file records as done (FR-018). |

The handler **never** inspects orchestrator-owned state (`current_phase`, `phases[]`, `active_loop`,
`lock`) beyond what the envelope hands it.

## Gate result returned (handler → orchestrator)

| Return | When | Orchestrator action (001) |
| :--- | :--- | :--- |
| `needs-user` | The syllabus reached `presented` and awaits **user approval**; **or** a revision was re-presented after feedback. | Park for the user-approval gate; on approval record it + freeze (001 FR-023), then advance. |
| `failed` | An input is corrupt/inconsistent (e.g. a malformed `BUILD_PROGRESS.md` block, an unreadable brief) such that the phase cannot proceed. | Halt + surface (FR-022). 002 never silently repairs. |

**002 does NOT return `pass`** — the syllabus gate is `user-approval`; the *user's* approval (mediated
by 001) is what clears it, not a handler verdict. **002 does NOT return `loop`** — the 3-round
author→critique→refine cap is 003's primitive, not the syllabus phase's; the syllabus revises against
open-ended user feedback under 001's approval loop, not a capped agent loop.

### Where the revision feedback comes from (the change-request channel)

On a change request the orchestrator **re-invokes** the handler; the envelope carries no `user_feedback`
field, so the handler reads the user's latest syllabus-revision comments from **`FEEDBACK.md`** in
`course_dir`. This read is **ratified by 001's phase-seam** (its `user-approval` gate-type semantics +
the envelope note: `course_dir` grants read access to driver-maintained course-folder files) — it is not
a private side channel. The file is the one 001's driver appends gate-event feedback to as the gate
event occurs (001 FR-026, 001 data-model rule 9, which names "syllabus revision feedback" explicitly).
This reuses 001's existing write side rather than inventing a second feedback channel; 002 only **reads**
`FEEDBACK.md`, never writes it (the harvest to `insights/` stays 004's user-invoked path). A revision
re-enters at `composed`, applies the feedback, re-presents, and returns `needs-user`.

## Sub-phase writes (the only `BUILD_PROGRESS.md` field 002 owns)

The handler writes `syllabus_subphase` via 001's `progress.py` (**never hand-edits** the JSON block,
build-progress-schema rule 1) after each sub-step, in this order:
`research-in-progress → research-done → composed → presented`. Persist-before-advance (rule 3): the new
sub-phase is written before the next sub-step begins, so a session death resumes at the right sub-step.
002 does **not** advance `current_phase` (rule 2 — that is the orchestrator's act after the gate).

## The divergence ask (inline, not a seam park)

Ask-moment #2 (FR-012) is asked **inside the handler's run** while `syllabus_subphase == composed`
(design decision R3) — it is **not** a `needs-user` return. It fires **only** when the top-weighted
sources diverge on the course's core arc (Assumptions); on no divergence it is not asked (SC-005). The
divergence assessment is written to `SYLLABUS.md` composition notes on **every** run regardless. A
pending (unanswered) question is recorded there so a mid-ask resume at `composed` re-asks cheaply. After
the answer the handler **MAY** re-research against the **same** budget (FR-019) and re-compose.

**Persist-before-block (lock safety).** The handler writes `syllabus_subphase = composed` (and records
the pending question) **before** asking, so the inline ask may safely outlive 001's lock stale-reclaim
window (001 build-progress-schema § "Blocking on inline user input vs. the lock"): if the lock is
reclaimed during a long ask, a resuming invocation continues at `composed` and re-asks — no lost or
double-applied answer.

Post-divergence re-research stays within `syllabus_subphase == composed` (it does **not** rewind to
`research-in-progress`): the persistent budget log carries the query count across the session boundary,
so a death during re-research resumes against the same remaining budget, and `exhausted()` forces the
thin-grounding path (FR-011) rather than a fresh budget (R4).

## Ordering & degradation guarantees

- **Research precedes composition** — the handler never composes before `research-done` (Principle IV).
- **Platform search runs last and is degradable** — web → GitHub → platform; if platform syllabi need a
  login or are blocked, the handler completes on web + GitHub grounding and records the limitation
  (FR-001, SC-006); it never scrapes, logs in, or pays.
- **Pre-return validation** — before returning `needs-user`, the handler runs `sources_lint.py` and
  `syllabus_lint.py`; a lint failure is a defect to fix in-phase, not something to surface to the user.
