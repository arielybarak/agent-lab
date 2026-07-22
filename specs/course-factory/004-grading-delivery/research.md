# Phase 0 Research — Grading & Delivery (spec 004)

Design decisions behind `plan.md`. Each is **Decision / Rationale / Alternatives considered**. The
spec is fully clarified (3 Qs, Session 2026-07-08); no `NEEDS CLARIFICATION` markers remain, so this
digest resolves *design* questions the plan raised, not open spec ambiguities.

---

## R1 — What is mechanical (deterministic tool) vs. judgment (agent)?

**Decision.** Split exactly as 001/002/003 do: put in `tools/` **only** the operations whose Success
Criteria are stated in **100% / 0-exception** terms, so the SC is guaranteed by code; leave every
graded judgment to `.claude/` agents. Concretely:

| Operation | Home | SC it makes mechanical |
| :--- | :--- | :--- |
| Pass predicate: *every dimension ≥ its threshold* (no aggregate masking) | `rubric_gate.py` | SC-010 |
| Single-rubric invariant: enumerate quality definitions → exactly one | `single_rubric_lint.py` | SC-001, SC-008, SC-009 |
| Exhaustive `[Sn]` traceability sweep (a thin course-scoped layer over the **shared** `sn_resolve.py`) | `course_trace.py` | SC-004 |
| Append-only harvest into `insights/` (append / no-op-on-empty / no-clobber) | `harvest.py` | SC-007 |
| Score each rubric dimension; the independent course-level verdict | `course-evaluator` agent | SC-003, SC-011 (scenario) |
| Distill `FEEDBACK.md` critiques into `insights/` | `harvest-feedback` command + agent | SC-007 (representation) |
| Analyze external courses → propose rubric revisions | `comparison-analyst` agent | SC-008 (scenario) |

**Rationale.** The 0-exception SCs are precisely the ones an agent cannot be *trusted* to hit every
time (a strong dimension quietly masking a weak one; a sampled rather than exhaustive citation check;
a harvest that clobbers a prior course). A ~10–40-line pure function turns each into a mechanical
guarantee. This is the identical discipline 001 (`progress.py` transition function), 002
(`sources_lint.py`), and 003 (`pool_scheduler.py`, `citation_trace.py`) already apply — 004 is not
inventing a pattern, it is completing it for the quality layer.

**Honesty boundary (stated, not hidden).** The tools guarantee the *predicate*, the *resolution*, the
*append*, and the *single-rubric enumeration*. They do **not** and cannot supply the *dimension
scores* (a mentor-grade judgment), the *course-level verdict* (whole-arc coverage/flow reasoning), or
the *distillation* of a critique into an insight. `rubric_gate.py` answers "given these scores, does
it pass?" — not "what is the correctness score?" That division is the whole design: mechanize the
gate, keep the grading human-in-the-agent.

**Alternatives considered.** (a) *All-agent* — the course-evaluator judges pass/fail holistically.
Rejected: makes SC-010's "0 aggregate masking" and SC-004's "exhaustive, not sampled" unfalsifiable,
which is exactly the failure mode Principle I names ("a slop factory"). (b) *All-tool grading* —
score dimensions numerically by regex/heuristics. Rejected: correctness/flow/practicality are
irreducibly judgment; a heuristic score is cargo-cult quality, the thing the rubric exists to catch.

---

## R2 — Who owns the `[Sn]` resolver, and does 004 build one?

**Decision.** **004 does not build a resolver.** The course-evaluator's traceability sweep **imports
the one shared `sn_resolve.py`** — the canonical `[Sn]`→`SOURCES.md` primitive that spec **003
builds** (003 `plan.md` line "one resolver, not three… imported by 002's syllabus_lint, 003's
citation_trace, and 004's evaluator"). 004 owns the **canonical grounding *contract*** (the
semantics: exhaustive, tracing-not-truth, mentor-added exemption, thin-grounding preservation — spec
FR-007/008) and publishes it as [`contracts/citation-traceability.md`](contracts/citation-traceability.md);
`sn_resolve.py` is its shared *implementation*.

**Rationale.** 004's spec FR-007 declares 004 the factory's **canonical** citation/grounding contract
("002 and 003 apply it at their own granularity rather than re-deriving it"), and 003's
`rubric-gate.md` Property 2 already routes 003's lesson gate through `sn_resolve` and points at this
canonical check. Two forces meet cleanly here: 004 owns the *definition*; the *code* is shared and —
because the README build order runs `004-delivery` **after** 003 — already exists by the time 004's
course-evaluator is built. Course-scope is the only delta from 003's per-lesson use: the sweep runs
over **every** `[Sn]` across all lessons + syllabus, not one lesson. That delta is a **thin
course-scoped module** — `course_trace.py` (extract every key → `sn_resolve` each → findings) — the
exact analogue of 003's per-lesson `citation_trace.py`, **not** a second resolver.

**Alternatives considered.** (a) *004 authors its own resolver* (it "owns canonical"). Rejected:
duplicates 003's module, invites drift between two grounding rules — the exact anti-pattern "one
resolver, not three" prevents; ownership of the *contract* ≠ ownership of a *second copy*. (b) *Fold
the course sweep into 003's `citation_trace.py`.* Viable, but `citation_trace.py` is 003's
per-lesson, format-aware layer; a course-wide sweep is 004's concern (`course_trace.py`). 004 reuses
`sn_resolve` (the primitive) directly and MAY reuse `citation_trace`'s extraction helpers; it does
not enlarge 003's per-lesson tool with course-level responsibility.

---

## R3 — Where does each deliverable physically live? (two `.claude/` homes)

**Decision.** Split by *who runs it and when*:

- **Frozen `course-template/` (ships inside every course as residue):** the **rubric asset**
  (`rubric.md`), the **`course-evaluator` agent**, the **`/course-report` command**. These are
  mandatory-core template assets (constitution IX); 000 distills their *shells* from the reference
  course, **004 owns their grading behavior/contents**. They run at delivery *and* remain available
  post-delivery for `/improve-course`.
- **Factory-level `course-factory/.claude/` (runs across courses, never shipped):** the **harvest**
  commands (`insight-capture`, `harvest-feedback`) and the **comparison** command + agent
  (`compare-course`, `comparison-analyst`). These read one course's `FEEDBACK.md` / an external
  course and write the **cross-course** `insights/` and `comparison/` — a factory operation, not a
  per-course one.
- **Shared `course-factory/tools/`:** the three deterministic tools, appended to the existing
  `tools/` (001/002/003's), never a rival directory.

**Rationale.** The litmus test is the constitution's "two `.claude` folders stay distinct": anything
that must *travel with a delivered course* (so the learner can re-grade or run `/improve-course`) is a
template asset; anything that reasons *across* courses (the compounding digest, external comparison)
is factory tooling. `/course-report` being "inherited from the template" (DESIGN step 5) settles the
evaluator+report+rubric as template assets; `insights/` being a cross-course store settles the
harvest+comparison as factory tooling.

**Alternatives considered.** *Put the course-evaluator in the factory's `.claude/`.* Rejected: then a
delivered course could not re-grade itself or run `/improve-course` without the factory present,
breaking the "course is self-contained residue" model (DESIGN "Mental model").

---

## R4 — Is 000 built when 004 is planned? How is the rubric seam handled?

**Decision.** Treat 000/002/003 exactly as 001 treated 000: **not built at plan time**, so the plan
targets each as a **contract + fixture**, but *by 004's build slot they exist* (README order runs
000/001/002 and `004-rubric-core`, then 003, then `004-delivery`). The rubric seam is a clean
division: **000 owns the two-layer *shape* + the six core-dimension names + the semver `VERSION`;
004 fills the *grading semantics* into that shape** (concrete scale, per-dimension thresholds,
weights, the hard-gate rule) and **shares 000's single version identity** (000 FR-016 ↔ 004 FR-005 —
never a rubric-only counter). Validation now uses the `tests/fixtures/rubric/` stand-in 003 already
defines; when 000 ships, the fixture is replaced by the real asset and the pass predicate is
unchanged.

**Rationale.** Planning ahead of a prerequisite is the established repo pattern (001 §Primary
Dependencies). The shape/semantics split is stated verbatim in both specs (000 FR-015, 004 FR-001),
so there is no ownership ambiguity to resolve — only a fixture to stand in until the asset lands.

**Alternatives considered.** *Wait for 000 before planning 004.* Rejected: the README explicitly
decomposes the work so specs can be planned in parallel across sessions; US1 is called out as
independently plannable.

---

## R5 — One pass predicate for both the lesson gate and the course-evaluator?

**Decision.** Yes — `rubric_gate.py` is the **single** pass predicate. Given a mapping of
`dimension → score` and the rubric's `dimension → threshold`, it returns `(passed: bool,
per_dimension: {...})` where `passed` is true **iff every** dimension (core + requested add-ons)
clears its own threshold. No average, no weighted sum that can let a low dimension slide (weights
inform *reporting/ranking* in the scorecard, **not** the gate). Both 003's `lesson-evaluator` (per
lesson) and 004's `course-evaluator` (course-wide dimensions) call it.

**Rationale.** SC-009 ("the same rubric grades both the lesson gate and the course-evaluator — 0
cases of two different quality definitions") and SC-010 ("0 passes with any below-threshold
dimension") are *only* structurally guaranteed if there is literally one predicate. 003's
`rubric-gate.md` already names 004 the owner of "the exact dimensions, their thresholds, and the
scoring scale," so 004 supplying the canonical predicate fulfills a contract 003 already wrote against
— it is not a new imposition on 003's scope. (Coordination note: 003's lesson-evaluator consumes this
predicate; 003's already-planned tasks apply the threshold as agent judgment today, and can import
`rubric_gate.py` when 004's US1 lands — an implementation convergence, not a scope change to 003.)

**Alternatives considered.** *Let each evaluator apply the threshold itself.* Rejected: two copies of
"every dimension ≥ threshold" is two places for the masking rule to drift — SC-009/SC-010 become
convention, not guarantee.

**Weights — a deliberate scope note.** FR-004 pins the *gate* to per-dimension thresholds and lists
weights among the grading semantics 004 owns. Weights therefore exist for **scorecard emphasis /
ranking wins & cleanups**, never to compute the pass/fail gate. Recording them (with the version,
FR-005) keeps a course's grading reproducible; using them in the gate would reintroduce masking. The
plan treats weights as reporting metadata, not gate inputs.

---

## R6 — Harvest: what is mechanical, what is judgment, and how is "user-invoked only" guaranteed?

**Decision.** `harvest.py` owns the **append mechanics**: append a distilled insight file/entry to
`insights/`, **no-op** on an empty `FEEDBACK.md`, **never overwrite** an existing course's insights
(new files or append-only sections keyed by source course + date), dedupe-safe. The **distillation**
(turning a course's critiques into a concise, themed insight) is the `harvest-feedback` command's
agent judgment. "User-invoked only" (FR-016, SC-007: 0 automatic triggers) is guaranteed by
**construction**: the only entry points are the two commands (`insight-capture`, `harvest-feedback`);
there is **no hook, no phase-transition call, no scheduler** wired to them — 001's orchestrator never
invokes the harvest. `insights/` starts **empty** with only a form-fixing `README.md`.

**Rationale.** SC-007 bundles several 0-exception properties (every critique represented; 0 dropped;
0 clobbered; 0 errors on empty; 0 automatic triggers). The append/no-op/no-clobber trio is mechanical
and belongs in the tool; "0 automatic triggers" is an *architectural* guarantee (nothing calls it but
the user's command) — the cleanest way to make "user-invoked only" true is to give the harvest no
non-user caller at all, which also honors the settled 2026-07-08 clarification that decouples 004 from
001's phase transitions.

**Alternatives considered.** (a) *Harvest on course completion.* Rejected outright — contradicts the
clarified FR-016 and re-couples 004 to 001's delivery. (b) *One monolithic `insights.md`.* Rejected:
the spec fixes `insights/` as **directory-shaped** so each harvest is a small diff and append-only is
natural (append a file, not edit a growing one); Key Entities pins this.

---

## R7 — `comparison/`: how does it stay "revisions, never a rival," and how is a revision adopted?

**Decision.** `comparison/` **never writes the live rubric.** `compare-course` + `comparison-analyst`
produce two things into `course-factory/comparison/`: (a) a **proposed revision** targeting the one
rubric (a diff/description against the current rubric version) and (b) a **per-course report** feeding
the `/improve-course` backlog. `single_rubric_lint.py` guarantees no second rubric ever materializes
(a proposal is a proposal file, not a rubric). **Adoption is a deliberate, human-reviewed step**
(FR-019 minimal protocol): the maintainer approves a proposal against real course evidence; adoption
**re-stamps the template** via 000's narrow rubric-only revision path (000 Edge Cases / FR-016) with
provenance to the `comparison/` proposal (000 FR-019) — the stamp bump **is** the adoption record.
The analysis itself **reuses 002's research discipline** (weigh reliability over popularity → cite →
converge-or-budget), not a third method (spec Assumptions).

**Rationale.** SC-008 ("100% of comparison outputs target the single rubric — 0 rivals; live rubric
unchanged until deliberately adopted") is satisfied structurally: proposals live in `comparison/`, the
rubric lives in `course-template/`, and only 000's re-stamp path bridges them, under human review.
Reusing 002's research method (and its `sn_resolve`/citation discipline) avoids inventing a parallel
reliability rubric for *candidate selection* — "well-made" is judged the way 002 judges any source.

**Alternatives considered.** *Auto-apply a strong proposed revision.* Rejected: FR-019 mandates
adoption be reviewed; auto-mutation would silently change the bar mid-factory-life and orphan every
course graded against the prior version without a provenance trail.

---

## Consolidated inputs the plan commits to

- **Reuse, do not re-author:** `sn_resolve.py` (003), the `tests/fixtures/{rubric,sources,lessons}/`
  (003/002), 002's `SOURCES.md`/tag schema, 000's `VERSION` + rubric shape, 001's `course-folder.md`
  + `DIFFS.md`. 004 **adds** the grading semantics, the course-level verdict, the report contents, the
  harvest, and comparison — nothing already owned elsewhere.
- **Four deterministic tools** map 1:1 to the four 0-exception SC clusters (R1 table). Everything else
  is agent judgment behind a scenario fixture.
- **Two `.claude/` homes** (template vs. factory) keep the "self-contained course residue" and "two
  `.claude` folders stay distinct" invariants intact (R3).
