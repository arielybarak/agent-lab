# Phase 1 Data Model — Syllabus Phase

Entities and on-disk shapes, plus the syllabus-phase **sub-state machine** that runs *inside* one node
(`current_phase == syllabus`) of 001's phase machine. Field-level schemas other specs or the tool layer
consume are the **contracts** (`contracts/`); this file is the conceptual model and the sub-transitions.
Entity names track the spec's Key Entities.

---

## Entities

### SOURCES.md (002's primary durable output; 001 ships the stub)
The anti-fabrication grounding store for the **whole course** (FR-004). Populated during the research
sub-phase. Each entry is an `[Sn]`-keyed record: `{ key, type, citation, reliability_judgment,
topics_covered, flags? }`. `type ∈ course · repo · syllabus · post`. `citation` is a **link** for heavy
sources, an **inline citation** for posts/comments/tips (FR-003). `reliability_judgment` is prose
weighing reliability over popularity (stars = green flag, not proof) — **required, non-empty** (SC-001).
`topics_covered` feeds the convergence signal. `flags` may mark `(indirect)`, `(secondary)`,
`(supporting)`, or `unresolvable` (a dead link found *during this phase* — flagged once, not re-checked;
edge case). Keys are **append-stable**: assigned sequentially, never reused (FR-004, Assumptions).
Full schema: `contracts/sources-schema.md`.

### SYLLABUS.md (002's headline artifact; frozen on approval)
The composed course shape + scope (phases, lessons, arc), at the course-folder root; a required delivery
artifact (001 FR-020, `course-folder.md`). Written by the composer. Every **topic** either carries a
`[Sn]` citation or a `mentor-added` tag (FR-007, SC-003) — no silently ungrounded topic. Carries a
**composition-notes** section holding: the **divergence assessment** (converged/diverged + the sources
compared, SC-005), any **thin-grounding flag** at course or section scope (FR-011, SC-008), and a
recorded **pending directional question** while one is open (R3). Frozen by 001 on approval; later
changes are forward diffs against it (001 FR-023/027) — 002 keeps it in a form that supports 001's
diff presentation (FR-014). Full schema: `contracts/syllabus-schema.md`.

### COURSE_BRIEF.md (read; augmented with one field)
001's overlay. 002 **reads** `topic_scope`, `audience`, `running_example`, `archetype_profile`,
`source_pointers`, `modules` (kept consistent with the syllabus, FR-010/015) and **writes** exactly one
field, `lesson_format` (`.md` | `.ipynb`, FR-009), which intake left unset (001 data-model). The
write-back is an agent append of a single declared field; its **presence** is asserted by
`syllabus_lint.py` (SC-004). 002 touches no other brief field.

### Source (conceptual)
A single kept research find: its `type`, `citation`, `reliability_judgment`, and `topics_covered`. The
unit weighed (FR-002) and recorded (FR-003); its `topics_covered` drives convergence.

### Convergence signal (conceptual)
The condition that new sources stop adding **topics_covered** not already captured (Assumptions:
convergence is judged by topic coverage). One of the two research-stop triggers; an agent judgment (R2),
its firing recorded so the research-done transition is auditable. **Which** of the two triggers fired
(`converged` vs `budget-capped`) is recorded as the **Grounding-stop note** in SYLLABUS.md composition
notes (edge case: a budget-capped run notes grounding was capped, not converged) — a distinct axis from
thin-grounding.

### Research budget (state; the hard backstop)
A persistent query/tool-call counter in the course folder (e.g. `.syllabus-research-log`), incremented
before each web/`gh`/platform query; `research_budget.py` reads it to decide stop (FR-005, SC-002). The
backstop that halts research even without convergence. **One budget per course syllabus phase** —
post-divergence re-research (FR-019) continues the same count; there is no reset (R4).

### Lesson-format decision (state)
`.md` by default, `.ipynb` when the course is code-heavy (FR-009). Decided by the composer from the
course's nature once the syllabus shape is clear; written into `COURSE_BRIEF.md.lesson_format`.

### Divergence (conceptual + recorded assessment)
Wide disagreement across the **top-weighted** sources on the course's core arc/angle (Assumptions), not
minor topic-ordering differences. The trigger for ask-moment #2 (FR-012). **Every run** records an
explicit divergence assessment in SYLLABUS.md composition notes — converged or diverged, naming the
sources compared — so the fire/no-fire decision is auditable even though the judgment is agent-rendered
(SC-005).

### Selected profile (read dependency — 000's mechanism)
The course's chosen archetype profile (001's overlay decision, 000's content). Shapes the syllabus's
**macro spine**, **entry point** (theory-first vs problem-first), and **checkpoint placement/frequency**
— **advisory only** (000 FR-022) — while the mandatory-core invariants are reused unchanged and never
bypassed (FR-015, 000 FR-024). Represented by a fixture until 000 ships (R6).

### Insights digest (read input — Principle XII read side)
004's cross-course harvest output, read at composition alongside SOURCES.md (FR-016). **Empty or missing
is a valid input**, not a blocker (mirrors 003's precedent).

### Syllabus sub-phase status (002's owned `BUILD_PROGRESS.md` field)
The phase's checkpoint state — `research-in-progress` · `research-done` · `composed` · `presented` —
written via 001's `progress.py` after each sub-step so a mid-phase interruption resumes at the right
sub-step (FR-018). The **only** `BUILD_PROGRESS.md` field 002 writes (001 owns the rest;
`build-progress-schema.md`). Enum is **fixed by 001's schema** — 002 does not add states (R3).

---

## The syllabus sub-state machine (inside `current_phase == syllabus`)

001's orchestrator invokes the handler with the input envelope and consumes one gate result
(`contracts/phase-seam.md`). *Within* that invocation the handler walks these sub-states, persisting
`syllabus_subphase` before each transition (FR-018) so a resumed session skips completed sub-steps:

| From → To | Sub-step work | Persist |
| :--- | :--- | :--- |
| *(start)* → `research-in-progress` | Begin `mentor-research`: web → GitHub → **platform last, degradable** (FR-001). Increment the budget log per query. | `research-in-progress` |
| `research-in-progress` → `research-done` | Stop on **convergence or budget** (FR-005, SC-002); write kept sources to `SOURCES.md` (`[Sn]` + reliability, SC-001). `sources_lint.py` must pass. | `research-done` |
| `research-done` → `composed` | Compose-as-mentor honoring the profile (FR-006/015), correcting staleness, filling gaps; decide **volume** (FR-008) + **format** (FR-009, write brief); every topic `[Sn]` or `mentor-added` (SC-003); flag thin grounding if applicable (FR-011, SC-008); **write the divergence assessment** (SC-005). | `composed` |
| `composed` → `composed` *(if diverged)* | **Inline ask-moment #2** (R3): ask the directional question; on answer, **MAY** re-research against the **same** budget (FR-019) → re-compose. Sub-phase stays `composed`; the pending question is recorded until answered. | `composed` |
| `composed` → `presented` | Present the review-ready syllabus (FR-013); `syllabus_lint.py` must pass (SC-003/004/005/008) before returning to the orchestrator. | `presented` |

**Gate-result mapping to the seam** (the handler → orchestrator return, `contracts/syllabus-handler.md`):

- Reaching `presented` → return **`needs-user`**: the orchestrator parks for the user-approval gate
  (syllabus review). This is the **only** seam park 002 triggers.
- Orchestrator re-invokes the handler on a **change request** → the handler **revises** (re-enters at
  `composed`, re-presents) and returns `needs-user` again (FR-014). It never returns `pass` for a
  user-approval gate — approval is the orchestrator's determination; freeze is 001's act.
- A hard failure (e.g. `sources_lint`/`syllabus_lint` cannot pass because an upstream input is
  corrupt) → return **`failed`** (halt + surface, seam semantics). 002 never "repairs" a corrupt
  `BUILD_PROGRESS.md` block silently (build-progress-schema rule 4).

**Divergence ask vs. approval gate — kept distinct (constitution IV, README seam #8).** The inline ask
(`composed`, R3) is an **ask-moment**: an open directional question about missing content, capped at two
across the pipeline (intake + here). The `presented`→`needs-user` park is a **gate**: a review decision
on produced work, uncapped. They are different categories and use different mechanisms on purpose.

---

## Validation rules (enforced by the tool layer)

- **Every source keyed + judged** (`sources_lint.py`, SC-001): reject any `SOURCES.md` entry lacking a
  stable `[Sn]` key or a non-empty `reliability_judgment`; reject a reused key (append-stable, FR-004);
  a `duplicate-work` (two links, one work) collapses to one key (mentor-research dedupe-by-work).
- **Every topic grounded or tagged** (`syllabus_lint.py`, SC-003): reject any syllabus topic with
  neither a `[Sn]` citation nor a `mentor-added` tag — 0 silently ungrounded topics. A cited `[Sn]`
  must **resolve** into the course's `SOURCES.md` (cross-file); a dangling citation to a non-existent
  key fails — "traceable" means the trace lands, not merely that a `[Sn]`-shaped token is present.
- **Thin-grounding consistency** (`syllabus_lint.py`, SC-008): if a course/section is flagged
  thinly-grounded, **every** affected topic must be `mentor-added` — no silently thin course.
- **Divergence assessment present** (`syllabus_lint.py`, SC-005): the composition notes must contain a
  divergence assessment naming the sources compared, on **every** run (converged or diverged).
- **Format recorded** (`syllabus_lint.py`, SC-004): `COURSE_BRIEF.md.lesson_format` is set to `.md` or
  `.ipynb` before the handler returns `needs-user`.
- **Budget bounded** (`research_budget.py`, SC-002): `exhausted()` is a pure function of the query log;
  once true, the research skill must stop; re-research after a divergence answer shares the same count
  (FR-019) — no reset path exists.
