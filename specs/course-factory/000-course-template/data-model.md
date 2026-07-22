# Phase 1 Data Model: Course-Template Distillation

The "entities" here are **on-disk artifact schemas**, not runtime objects — this spec produces a
static directory. Each schema below is derived from the spec's Key Entities + Functional
Requirements and is the shape the distillation must emit and the shape spec 001 later reads.

---

## E1 — Classification record (rows of `CLASSIFICATION.md`)

The single auditable ledger (FR-006 + FR-019 merged — D1). One row per reference asset.

| Field | Type | Rule |
| :--- | :--- | :--- |
| `asset_path` | string | Path within the reference `.claude/`, e.g. `skills/pattern-lesson-format/SKILL.md`. Unique. |
| `asset_type` | enum | `agent` \| `command` \| `skill` \| `hook` \| `other` (settings, CLAUDE.md, setup-backlog, rubric doc). |
| `verdict` | enum | `keep-core` \| `demote-module` \| `drop`. Exactly one (FR-006). |
| `rationale` | string | Cites critical-thinking judgment and/or research (FR-002/FR-004); tiered High/Med/Low + caveat per `mentor-research` (D5). MUST NOT be "SD already had it" (SC-009). |
| `provenance` | string | Reference asset and/or research source it derived from, or `new` (FR-019/SC-007). |
| `neutralized` | bool/na | For `keep-core`: `true` once all topic-specifics stripped (FR-007); `n/a` for drop. |
| `target` | string | Where it lands: `core` \| `module:<name>` \| `profile:<name>` \| `—` (dropped). |

**Coverage invariant**: exactly 23 rows for the current reference (4 agents · 10 commands · 1 hook ·
5 skills · `settings.json` · `setup-backlog.md` · `CLAUDE.md`) — **0 unclassified** (SC-001).
**Merge rule**: two assets that neutralize to the same capability collapse to one core row with both
paths noted in `provenance` (FR-008; e.g. `pattern-lesson-format` + `system-design-curriculum`
lesson-arc).

## E2 — Template manifest (`manifest.yaml`)

Self-description so 001 honors a profile + module selection without inferring it (FR-018 — D2). Full
schema in [`contracts/template-manifest.md`](contracts/template-manifest.md).

| Field | Type | Rule |
| :--- | :--- | :--- |
| `version` | string | Mirrors `VERSION` (semver). |
| `core` | list[path] | The mandatory tier — always shipped, never toggleable. |
| `profiles` | map | `name → {default: bool, pieces: [path]}`. Exactly one `default: true` (FR-025). MVP: only `default`. |
| `modules` | map | `name → {pieces: [path], depends_on: []}`. Each independently toggleable (FR-012); `depends_on` MUST be empty for core (no hidden core dependency, SC-004). |

## E3 — Version stamp (`VERSION`)

Single semver identifier naming the distillation snapshot (FR-016 — D3).

| Field | Type | Rule |
| :--- | :--- | :--- |
| value | `MAJOR.MINOR.PATCH` | Full re-distillation → MAJOR bump; rubric-only re-stamp → MINOR/PATCH. Also the rubric's version identity (004 FR-005) — one counter. Copies record it; 001 compares it for drift (SC-006). |

## E4 — Mandatory core (tier)

Topic-neutral, evidence-invariant machinery present in every course (FR-010). Members:

- Backward-design backbone (outcomes → assessment/evidence → learning experiences).
- Canonical lesson arc (framing → activation → demonstration → practice+feedback → integration/transfer).
- Formative-feedback loops, **including** a topic-neutral lesson-consistency check (arc-order,
  running-example consistency, numbering, file:line findings ranked Critical/Warning/Nit — generalized
  from `lesson-consistency-reviewer`, FR-010).
- Quality-rubric asset (E7).
- Operational commands: `/improve-course`, `/new-lesson`, `/course-report`.

**Invariant**: 0 topic-specific terms after the neutrality gate (E6/SC-002); no member may be a
hidden dependency on any module (SC-004).

## E5 — Archetype profile (tier)

Named, evidence-based configuration **over the one core** (FR-022/024). Sets: macro organizing spine,
entry point (theory-first vs problem-first), checkpoint placement/frequency (**advisory only** — no
runtime enforcement), unit granularity. MUST reuse core invariants, MUST NOT redefine/bypass one.

- **MVP ships**: `default` (theory / linear-spiral) + the profile *mechanism*.
- **Later, independent increments** (NOT built in this plan): PBL/CBL, CBE/mastery, guided-inquiry
  (FR-023, User Story 4).
- Exactly one selectable per course; a course naming none falls back to `default` (FR-025/SC-012).

## E6 — Neutrality-term denylist (`neutrality-terms.txt`)

Maintained artifact, ships with the template (FR-020 — D4). Seeded: `System Design`, `HomeOS`,
`patterns_v1`, `capacity`, `QPS`. **Grows** as new topic wording is caught during classification. The
gate scans **core only** (modules/profiles may carry topic-specifics) and requires 0 hits (SC-002).

## E7 — Quality-rubric asset (two-layer shape)

One rubric, two layers (FR-013/014/015 — shape only, grading owned by 004).

| Layer | Content | Rule |
| :--- | :--- | :--- |
| Core | Exactly 6 dimensions: Technical Correctness, Grounding/No-Fabrication, Pedagogical Flow, Clarity, Coverage, Practicality | Canonical list (004 FR-001 references it). Flagged "adopted on judgment" — digest silent on rubrics (D8). 0 topic-specific dimensions (SC-005). |
| Add-ons | Requestable per-course slots (e.g. SD's fabricated-capacity check, cargo-cult check) | SD-specific checks land here, never in core (FR-014). |

Weights, per-dimension thresholds, hard-gate / no-aggregate-masking semantics → **deferred to 004**
(FR-015).

## E8 — Optional module (tier)

Opt-in add-on a course enables/disables independently (FR-011/012). Initial set derived from SD's
topic-specifics: **katas, diagrams, socratic, pattern-catalog**. The **diagrams** module inherits the
reference reviewer's diagram-existence check (FR-011); the phase-language rule and
`patterns_v2`/`patterns_v1` drift check are **dropped**. Each module self-contained — toggling any off
leaves a working core (SC-004).

---

**Relationships**: `CLASSIFICATION.md` (E1) is the audit source for every piece; `manifest.yaml`
(E2) is the shipped index of E4/E5/E8 membership; `VERSION` (E3) stamps the whole snapshot and the
rubric (E7); the neutrality gate (E6) guards E4. 001 consumes E2 + E3 (see `contracts/`).
