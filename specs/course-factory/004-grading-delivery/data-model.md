# Phase 1 Data Model — Grading & Delivery (spec 004)

Entities the quality layer produces or reads, their fields, the validation rules the deterministic
tools enforce, and the two small state lifecycles (rubric version; course verdict). Schemas that other
specs consume live in [`contracts/`](contracts/); this file is the entity reference behind them.

Legend: **(004)** owned here · **(000/002/003/001)** owned by that spec, read here · **[tool]** the
deterministic module that enforces a rule.

---

## Entities

### Rubric **(shape: 000 · grading semantics: 004)**

The single definition of quality. **Two layers:**

- **Generic core** — the six dimensions **named by 000 FR-013** (Technical Correctness,
  Grounding/No-Fabrication, Pedagogical Flow, Clarity, Coverage, Practicality). 004 does **not** re-derive the
  list.
- **Topic add-ons** — optional extra dimensions a course requests via `COURSE_BRIEF.md` (e.g.
  fabricated-capacity-numbers). Applied **only** when requested; an unknown requested add-on is
  **surfaced, not silently dropped** (FR-002).

**Grading-semantics fields 004 fills into 000's shape** (per dimension, core + add-on):

| Field | Meaning | Rule |
| :--- | :--- | :--- |
| `scale` | The score range, e.g. `1..5` (rubric-wide) | Fixed by 004's plan, recorded with the version (FR-004) |
| `threshold` | The minimum a dimension must reach to clear | Per dimension; the gate input |
| `weight` | Reporting emphasis for wins/cleanups ranking | **Not a gate input** — never averages a low dimension away (R5) |
| `hard_gate` | The rule: pass iff **every** dimension ≥ its threshold | No aggregate masking (FR-004, SC-010) |
| `version` | The rubric's identity = the template's semver `VERSION` (000 FR-016) | One identity, never a rubric-only counter (FR-005) |

- **Physical home:** `course-factory/course-template/rubric.md` (frozen; copied into each course).
- **Uniqueness invariant:** exactly one Rubric exists in the factory — **0 rivals** [`single_rubric_lint.py`] (SC-001).

### Dimension score → **PassResult** **(004)** `[rubric_gate.py]`

The output of the pass predicate over one artifact (a lesson, or the whole course):

```text
PassResult:
  passed: bool                       # true iff EVERY dimension.score >= dimension.threshold
  per_dimension: { name: {score, threshold, cleared: bool} }   # retained for the scorecard (FR-004)
```

- `passed` is the **hard gate** — a single below-threshold dimension makes it `false` regardless of
  how high the others score (SC-010). `per_dimension` is always retained even when `passed` is true.

### Scorecard **(004)** — the course-evaluator's output

```text
Scorecard:
  rubric_version: str                # which rubric graded this course (FR-005/013)
  per_dimension:  PassResult.per_dimension   # core + requested add-ons
  wins:           [str]              # what the course does well (agent judgment)
  cleanups:       [str]              # ranked improvements (weights inform ranking)
  traceability:   [TraceabilityFinding]      # every unresolvable [Sn] (may be empty)
  verdict:        Verdict            # independent course-level judgment
```

- Emitted for **100%** of graded courses with per-dimension scores + wins + cleanups + verdict
  (SC-003).

### Verdict **(004)** — the independent course-level judgment

- Values: **`pass`** | **`needs-work`**.
- **Independent, not a roll-up** (FR-009): the evaluator grades whole-arc dimensions (coverage across
  the syllabus, flow/continuity, the running-example thread) and MAY return `needs-work` **even when
  every lesson already passed** its per-lesson gate (SC-011).
- A `needs-work` verdict is **delivered as-is** in `COURSE_REPORT.md` — never withheld — and its gaps
  feed the forward-diff / `/improve-course` backlog (FR-010/011), **never** re-open a passed phase
  (SC-006).

### TraceabilityFinding **(004)** `[course_trace.py` over the shared `sn_resolve.py` — R2]`

One record per `[Sn]` key that fails to resolve to a *live* `SOURCES.md` entry.

```text
TraceabilityFinding:
  key:     str          # the unresolvable [Sn]
  where:   str          # file:location of the citing claim
  reason:  "no-such-entry"        # the key has no SOURCES.md entry
         | "entry-unresolvable"   # entry EXISTS but 002 flagged it `unresolvable` (dead/removed source) — the spec's dead-source edge case
         | "sources-missing"      # the course has no SOURCES.md at all
```

- `entry-unresolvable` is the spec's **"claim cites an unresolvable `[Sn]` (dead/removed source)"**
  edge case: 002 flags a dead link once during its phase and does not re-check; 004's grading is
  where a *later* death surfaces as a finding.

- The sweep is **exhaustive** — every `[Sn]` in the course, not a sample (FR-007, SC-004).
- A claim explicitly marked **`mentor-added`** is **not** a finding for lacking an `[Sn]`; its
  thin-grounding flag is **preserved**, never re-presented as sourced (FR-008). Tracing, **not truth**.

### Insight **(004)** — a cross-course lesson-learned entry

```text
Insight:
  theme:        str      # e.g. anti-fabrication, running-example-design, estimation-method, kata-design
  body:         str      # the distilled lesson (not a verbatim FEEDBACK.md copy)
  source_course: str     # which course it was harvested from (provenance)
  date:         str      # ISO date captured/harvested
```

- **Home:** `course-factory/insights/<theme>.md` — topic-organized, **directory-shaped** (not one
  monolith), so each harvest is a small append.
- **Append-only** — one course's harvest never clobbers another's [`harvest.py`] (SC-007). Starts
  **empty**; an empty digest is valid input for readers (001/002/003).

### ComparisonReport + ProposedRevision **(004)**

```text
ProposedRevision:            # targets the ONE rubric — never a second rubric (FR-019, SC-008)
  against_version: str       # the rubric version the proposal is diffed against
  change:          str       # the proposed revision to a dimension / threshold / add-on
  evidence:        [cite]    # external-course evidence, cited via 002's discipline (Assumptions)
  status:          "proposed" | "adopted" | "rejected"

ComparisonReport:            # per external course, feeds the /improve-course backlog (FR-018)
  external_course: str
  findings:        [str]
  proposed:        [ProposedRevision]
```

- **Home:** `course-factory/comparison/`. A proposal is a **file**, never a live rubric — the live
  rubric is unchanged until adoption re-stamps the template (below).

---

## Read-only inputs (owned elsewhere)

| Entity | Owner | 004's use |
| :--- | :--- | :--- |
| `SOURCES.md` `[Sn]` entries | 002 | traceability resolution target (read, never populated) |
| `mentor-added` / `thinly-grounded` tags | 002 | honored + preserved by the grounding check (FR-008) |
| Template `VERSION` (semver) | 000 | **is** the rubric version (FR-005); recorded in the scorecard/report |
| `DIFFS.md` forward-diff ledger | 001 | where course-level gaps land (FR-010, never a phase re-open) |
| `course-folder.md` delivery contract | 001 | 001 invokes `/course-report` at delivery; 004 owns its contents |
| Finished course (lessons + `SYLLABUS.md`) | 002/003 | the artifact the course-evaluator grades |

---

## State lifecycles

### Rubric version (shared with the template stamp — 000 FR-016)

```text
v_current ──(comparison/ proposes revision)──▶ ProposedRevision(status=proposed)
                                                      │
                              human review vs. real course evidence (FR-019)
                                        ┌─────────────┴─────────────┐
                                    reject                        adopt
                                        │                           │
                              status=rejected      000 rubric-only re-stamp (MINOR/PATCH bump),
                                                    provenance → the proposal (000 FR-019);
                                                    the stamp bump IS the adoption record
                                                            │
                                                        v_next
```

- A full re-distillation is a MAJOR bump (000's job); a rubric revision is a **narrow** MINOR/PATCH
  re-stamp — **never** a silent edit and **never** a second rubric (SC-008).

### Course verdict (per graded course)

```text
finished course ──course-evaluator──▶ Scorecard{verdict}
   ├─ every lesson passed  &  whole-arc dims clear  ──▶ verdict = pass
   └─ whole-arc gap (coverage/flow/running-example)  ──▶ verdict = needs-work
             (delivered as-is; gap → DIFFS.md / /improve-course; NO phase re-open)
```

---

## Validation rules → tools → SCs

| Rule | Enforced by | SC |
| :--- | :--- | :--- |
| Pass iff every dimension (core + requested add-ons) ≥ its threshold; no aggregate masking | `rubric_gate.py` | SC-010 |
| Exactly one rubric in the factory; 0 rivals | `single_rubric_lint.py` | SC-001, SC-008, SC-009 |
| Generic core applied to 100% of courses; add-on only when requested; unknown add-on surfaced | `course-evaluator` + rubric shape | SC-002 |
| Every graded course → scorecard with per-dim scores + wins + cleanups + verdict | `course-evaluator` | SC-003 |
| 100% of unresolvable `[Sn]` flagged; 0 mentor-added false-fails; thin-grounding preserved | `course_trace.py` over shared `sn_resolve.py` (R2) | SC-004 |
| Every delivered course has `COURSE_REPORT.md` with scores + verdict + rubric version, distinct from `FEEDBACK.md` | `/course-report` + `course-report.md` contract | SC-005 |
| Grading re-opens a passed phase 0 times; every course-level gap → forward diff | `course-evaluator` + 001's `DIFFS.md` | SC-006 |
| Every critique represented in `insights/`; append-only; no-op on empty; 0 automatic triggers | `harvest.py` + command construction (R6) | SC-007 |
| Independent course-level verdict can flag needs-work when all lessons passed | `course-evaluator` (scenario) | SC-011 |
