# Contract — `BUILD_PROGRESS.md` state schema

**Owner:** spec 001. **Consumers:** 002 (writes `syllabus_subphase`, its FR-018), 003 (writes
`lessons[]`, its FR-012). This schema is a **first-class deliverable of 001's plan** (spec
Assumptions) so the three specs share one vocabulary instead of inventing incompatible ones. Any
change here is a forward-diff event against this contract — update all three consumers together.

## File shape

`BUILD_PROGRESS.md` is human-readable Markdown containing **exactly one** fenced ` ```json ` block.
`progress.py` reads/writes only that block; the surrounding prose is regenerated from it and is
advisory. The block is the authoritative state.

```json
{
  "schema_version": 1,
  "course_name": "intro-to-x",
  "template_version": "1.0.0",
  "current_phase": "syllabus",
  "phases": [
    { "name": "syllabus",  "gate_type": "user-approval",   "gate_status": "in-progress", "cleared_at": null },
    { "name": "skeletons", "gate_type": "agent-then-user", "gate_status": "pending",      "cleared_at": null },
    { "name": "lessons",   "gate_type": "rubric",          "gate_status": "pending",      "cleared_at": null },
    { "name": "deliver",   "gate_type": "report-generated","gate_status": "pending",      "cleared_at": null }
  ],
  "syllabus_subphase": null,
  "lessons": [],
  "active_loop": null,
  "lock": { "holder": "cb-3f9a1c7e-8123-4b0a", "acquired_at": "2026-07-11T10:00:00Z", "last_progress_at": "2026-07-11T10:04:00Z" },
  "diffs_ref": "DIFFS.md"
}
```

## Field definitions

| Field | Type | Owner writes | Meaning |
| :--- | :--- | :--- | :--- |
| `schema_version` | int | 001 | Bumped only by a 001 schema change; consumers assert the value they expect. |
| `course_name` | string | 001 | The `courses/<name>/` slug; identifies this build (FR-019). |
| `template_version` | semver string | 001 | Stamped at copy (FR-006); drift-checked on resume (000 FR-016). |
| `current_phase` | Phase enum | 001 | `syllabus` · `skeletons` · `lessons` · `deliver` · `done`. Forward-only. |
| `phases[]` | ordered list | 001 | Each `{ name, gate_type, gate_status, cleared_at }`. `gate_status` ∈ `pending` · `in-progress` · `cleared`. `cleared_at` is an ISO-8601 UTC timestamp or null. |
| `syllabus_subphase` | enum or null | **002** | 002's checkpointable states (`research-in-progress` · `research-done` · `composed` · `presented`, 002 FR-018). Null unless `current_phase == syllabus`. |
| `lessons[]` | list | **003** | Each `{ id, status }`. `status` ∈ `not-started` · `in-progress` · `passed` · `accepted-at-cap` (spec Assumptions: at minimum distinguish done from to-do; these four are the shared set — `accepted-at-cap` is a terminal "done" per 003 FR-013). |
| `active_loop` | object or null | 001 | `{ phase, round }` for the capped refine loop (FR-012); null when no loop is active. `round` ∈ 1..3, then a single accept-or-comment extension. |
| `lock` | object or null | 001 | `{ holder, acquired_at, last_progress_at }` (FR-028); null when the build is parked at a gate or exited cleanly. `holder` is a **per-invocation token** (see below), not a stable session id. |
| `diffs_ref` | string | 001 | Relative path to the forward-diff ledger (`DIFFS.md`). |

### The `lock.holder` token

A Claude Code session exposes no stable, tool-visible session id, so **`/course-build` mints a fresh
`holder` token on each invocation** — a short random value (e.g. `cb-` + a `uuid4` hex slice) — and
passes it to `progress.py` when acquiring the lock. This is sufficient for FR-028/SC-012: the token
only has to be **unique per active invocation** so a concurrent second invocation sees a *different*
live holder and is refused. Because the lock is **cleared at every park / clean exit** (data-model
rule 8), a resuming invocation simply mints a new token and re-acquires — the token is never expected
to persist or be recognized across a park boundary. `acquired_at` / `last_progress_at` are ISO-8601
UTC; the stale-reclaim decision uses `last_progress_at` vs the configured timeout, not the token.

## Rules consumers must honor

1. **Never hand-edit the JSON block** — go through `progress.py`, which enforces legal transitions
   (no advance without a recorded gate pass; no phase skip).
2. **Write only your owned fields.** 002 writes `syllabus_subphase`; 003 writes `lessons[]`. Neither
   advances `current_phase` — that is the orchestrator's (001's) act after the gate result.
3. **Persist before advancing** (FR-016): a sub-phase or lesson status change is written before the
   next unit begins.
4. **A missing/corrupt/inconsistent block halts the pipeline** (FR-022) — consumers must not "repair"
   it silently.
