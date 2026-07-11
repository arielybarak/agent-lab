# Phase 1 Data Model — Pipeline & Instantiation

Entities and their on-disk shapes, plus the phase/gate state machine. Field-level schemas that other
specs consume are the **contracts** (`contracts/`); this file is the conceptual model and the state
transitions. Entity names track the spec's Key Entities.

---

## Entities

### COURSE_SPEC.md (input, author-written)
The rough input. Not produced by this feature; read by intake. Required fields (per
`templates/COURSE_SPEC.template.md`): topic, scope in/out, audience + assumed prior knowledge,
**running example** (required, Principle X), optional-module wishes, source material. Its quality caps
the course's quality.

### COURSE_BRIEF.md (produced by intake — the single on-disk home for intake output)
The factory-generated overlay and the **only** persisted form of the clarified spec (FR-004 — there
is no separate clarified-spec file). Captures, at minimum:
- `topic_scope` — topic + in/out scope
- `audience` — target learner + assumed prior knowledge
- `running_example` — the required backbone (blocking if absent, FR-003)
- `source_pointers` — pointers to the spec's source material
- `archetype_profile` — exactly one of the template's shipped profiles; defaults to the safe default
  (000 FR-025) when the spec names none (FR-005)
- `modules` — explicit enabled/disabled selection over the template's optional modules (FR-005)
- `lesson_format` — **written later by 002** (`.md`/`.ipynb`); intake leaves it unset
Schema: `contracts/course-folder.md`.

### course-template (dependency, frozen — spec 000)
The frozen, versioned, three-tiered skeleton (core + archetype profiles + optional modules)
instantiation copies. Read-only; never authored or mutated here (FR-001/007). Carries a `VERSION`
(semver, 000 FR-016) and a self-describing manifest. Represented in tests by the minimal fixture (R6).

### Course folder — `courses/<name>/`
The staging instance (one per course), holding every per-course artifact and the `.claude/` residue
copied from the template. Name derived from the course title slug; collisions suffixed, never
overwritten (spec Assumptions). Required contents at delivery are fixed by `contracts/course-folder.md`.

### BUILD_PROGRESS.md (produced at instantiation — the sole source of truth for resume)
The pipeline's on-disk state machine. Human Markdown wrapping one fenced **JSON** state block (R3).
The state block is the authoritative record; the prose is regenerated from it. Full field schema:
`contracts/build-progress-schema.md`. Core fields:
- `template_version` — the semver stamped at copy time (drift check on resume)
- `current_phase` — one of the Phase enum below
- `phases[]` — ordered, each `{ name, gate_type, gate_status, cleared_at }`
- `syllabus_subphase` — 002's sub-phase state while `current_phase == syllabus`
- `lessons[]` — per-lesson `{ id, status }` while in the lesson phases
- `active_loop` — `{ phase, round }` round counter for the capped refine loop (FR-012)
- `lock` — `{ holder, acquired_at, last_progress_at }` (FR-028), or null when parked
- `diffs_ref` — pointer to `DIFFS.md`

### DIFFS.md (produced empty at instantiation — the forward-diff ledger)
Append-only chronological log; one entry per forward diff applied under FR-023:
`{ target_phase_or_artifact, what_changed, why, applied_at }`. Never edited retroactively (FR-027).
Read together with the frozen artifact it annotates. Schema: `contracts/diffs-ledger.md`.

### SOURCES.md / FEEDBACK.md (produced as stubs at instantiation)
`SOURCES.md` — anti-fabrication grounding store; created + referenced here, **populated by 002**.
`FEEDBACK.md` — per-course critique file; created empty here, **written during the build** by gate-event
comments (FR-026) and by 003's evaluator; harvested to `insights/` by 004 (user-invoked only).

### COURSE_REPORT.md (produced at delivery)
The final graded scorecard (rubric scores + verdict). Its **presence** clears the delivery gate
(FR-011/021) — **any** verdict; a "needs work" verdict is delivered as-is, never withheld.

### insights/ digest (read at intake)
Cross-course knowledge store (004's harvest output). Read as an intake input (FR-025); an **empty or
missing digest is a valid input**, not a blocker.

### Lock marker
The `lock` object inside `BUILD_PROGRESS.md` (FR-028) — session identity + timestamps showing who
holds the build. The minimal mechanism resolving concurrent-session conflicts (R5).

---

## Phase enum & gate mapping

The fixed, ordered sequence (FR-009). `intake` and `instantiate` precede the resumable state (a
pre-copy interruption simply re-runs intake — spec Assumptions); the state machine proper begins at
`syllabus`.

| Phase | Gate type | Gate clears when | Reviewer (FR-011) |
| :--- | :--- | :--- | :--- |
| `intake` | — | brief authored, profile + modules selected | (pre-state) |
| `instantiate` | — | folder copied, overlaid, stamped, state + stubs initialized | (pre-state) |
| `syllabus` | `user-approval` | user explicitly approves the syllabus | **User** |
| `skeletons` | `agent-then-user` | agent review passes (cap 3), **then** blocking user scan approves (FR-024) | **Agent, then user** |
| `lessons` | `rubric` | every lesson passes the rubric (cap 3, then accept-or-comment one extra pass) | **Automated rubric** |
| `deliver` | `report-generated` | `COURSE_REPORT.md` is generated — **any** verdict | **Automated** |
| `done` | — | terminal | — |

**Gate result vocabulary** (what a phase handler returns across the seam, `contracts/phase-seam.md`):
`pass` · `needs-user` (park for a user gate) · `loop` (another refine round, if under cap) · `failed`
(halt + surface). The orchestrator maps these onto `gate_status` and either advances, parks, loops,
or halts.

---

## State transitions (the spine's rules)

These rules are enforced by a **pure transition function in `progress.py`** — `(current state, phase
gate result) → next state` — that rejects any illegal move. The `.claude/` driver supplies the gate
result and narrative; the *legality* of every move lives in this function, which is what makes the
transition rules `pytest`-assertable with no agent in the test loop (research R1).

1. **Forward-only.** `current_phase` moves strictly down the enum. A gate MUST be recorded `cleared`
   before `current_phase` advances (FR-010, SC-006). The transition function **refuses** an advance
   whose prior phase has no recorded gate pass — the no-silent-skip guarantee is mechanical, not
   narrative.
2. **Persist-before-advance.** Every unit of progress (a phase clearing, or a lesson changing status)
   is written to `BUILD_PROGRESS.md` **before** the next unit begins (FR-016, SC-004).
3. **Resume.** On start, read `BUILD_PROGRESS.md`, drift-check `template_version`, re-acquire the
   lock, and continue at `current_phase` + the unfinished `lessons[]` — performing no unit the file
   records as done (FR-017, SC-004/005). Passed lessons are never re-worked.
4. **Refine cap (FR-012).** `active_loop.round` increments per refine round; at 3 without clearing,
   the orchestrator parks (`needs-user`) with the best artifact + status for **accept-or-comment**:
   accept → gate clears as-is; comment → **exactly one** more pass, then accepted regardless. The
   accept-or-comment cycle never repeats beyond that single extension.
5. **Blocking post-skeleton scan (FR-024).** After the skeleton agent review passes, park
   (`needs-user`) for the blocking user scan before `lessons` starts. A **change request** re-enters
   003's skeleton loop with a **fresh 3-round cap**, then re-presents for another blocking scan.
6. **Forward diff (FR-023).** A requested change to an already-gated earlier phase never re-opens it;
   it is applied at `current_phase` and appended to `DIFFS.md`. `current_phase` never moves backward
   (SC-010).
7. **Integrity halt (FR-022).** If `BUILD_PROGRESS.md` is missing, corrupt, or internally
   inconsistent — or `template_version` drift is detected, or the frozen template is absent/unversioned
   — the pipeline **halts and reports**, never guesses (SC-009).
8. **Lock (FR-028).** `/course-build` mints a **per-invocation `holder` token** (a short random value
   — a Claude Code session has no stable tool-visible id) and passes it to `progress.py` on entry.
   Acquire on entry; refuse entry if another holder is live within the **liveness window** (surface the
   conflict, SC-012); refresh on each persisted unit; clear on park/clean exit; a **stale** lock (no
   progress within a **generous timeout**) may be reclaimed with the reclaim recorded. The token need
   only be unique per active invocation (the lock is cleared at each park, so it is never expected to
   persist across a park boundary). Both windows are configurable constants with sensible defaults —
   calibratable after real runs, like the round cap (spec Assumptions), not per-course variability.
   (`holder` token details: `contracts/build-progress-schema.md`.)
9. **Feedback capture (FR-026).** Durable gate-event author feedback (round-cap comments; syllabus
   revision feedback) is appended to `FEEDBACK.md` by the **driver** (`/course-build`) as the gate
   event occurs — this is judgment content (free-form user comments), so it is agent-appended, not a
   tool op. The write side of Principle XII; harvest stays 004's user-invoked path.

---

## Validation rules (enforced by the tool layer)

- **Copy-never-mutate**: after instantiation the source `course-template/` is byte-for-byte unchanged
  (SC-003) — `instantiate.py` copies into `courses/<name>/` and touches nothing under the source.
- **Required-field blocking**: intake emits a blocking question for any missing required field and
  never fabricates (FR-003, SC-001).
- **Legal-transition-only**: `progress.py` rejects any `current_phase` advance without the prior
  phase's recorded gate pass, and any write that would skip a phase (SC-006).
- **Artifact-presence at delivery**: `deliver_check.py` verifies the full required set
  (`contracts/course-folder.md`) is present before `done` (SC-008).
- **Append-only ledger**: `diffs.py` only appends; it never rewrites existing `DIFFS.md` entries
  (FR-027).
