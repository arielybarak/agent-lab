# Phase 0 Research: Course-Template Distillation

The feature spec is **Clarified** (5 Qs, 2026-07-11) and the external `research-digest.md` already
resolved the big substantive question (one core + profiles, not siloed templates — §5). So Phase 0
here is not open research; it is the record of the **distillation-methodology decisions** the plan
commits to, in Decision / Rationale / Alternatives form. No `NEEDS CLARIFICATION` markers remain.

---

## D1 — Classification is ONE table, not two ledgers

- **Decision**: Record every reference asset's verdict + rationale **and** its provenance in a single
  `CLASSIFICATION.md` table (columns: asset path · type · verdict · rationale · provenance ·
  neutralized?). One row per asset.
- **Rationale**: FR-006 and FR-019 both explicitly say verdict+rationale and provenance are the
  **same per-asset record** — "one classification table, not a duplicate ledger." A single table is
  auditable from one place (SC-001/SC-007) and cannot drift against itself.
- **Alternatives rejected**: Separate `verdicts.md` + `provenance.md` (two files drift; the spec
  forbids it). Frontmatter-per-asset (not scannable as a whole; hard to prove 100% coverage).

## D2 — Self-description is a YAML manifest at the template root

- **Decision**: `manifest.yaml` lists each shipped piece and tags it `core` / `profile:<name>` /
  `module:<name>`, plus the selectable profile set and the safe default (FR-025).
- **Rationale**: FR-018 requires the template be self-describing so 001 can honor a profile + module
  selection "without inferring it." YAML is human-diffable, parses with stdlib, and matches the
  `.claude/` ecosystem's existing frontmatter conventions. It is the contract 001 reads
  (see `contracts/template-manifest.md`).
- **Alternatives rejected**: Inferring tiers from directory location alone (fragile, unstated —
  violates "without inferring"); JSON (less readable in diffs, no comments for rationale pointers).

## D3 — Version stamp = semantic versioning in a `VERSION` file

- **Decision**: A top-level `VERSION` file holding `MAJOR.MINOR.PATCH`. Full re-distillation → MAJOR;
  rubric-only re-stamp (Edge Cases) → MINOR/PATCH. This single stamp **is also the rubric's version
  identity** (FR-016 ↔ 004 FR-005) — one counter, never two.
- **Rationale**: Settled in clarify (Q3). Mirrors the constitution's own versioning policy, so a
  rubric-only re-stamp is visibly distinguishable from a full re-distillation, and 001's drift check
  (SC-006) compares two well-ordered identifiers.
- **Alternatives rejected**: Content hash (detects drift but can't express "rubric-only vs full" —
  loses the semantic signal the clarify answer asked for); date stamp (no ordering semantics for a
  narrow vs broad change).

## D4 — Neutrality gate = a maintained denylist + a scan

- **Decision**: `neutrality-terms.txt` seeds from the known SD terms (`System Design`, `HomeOS`,
  `patterns_v1`, `capacity`/`QPS`) and **grows** as new topic wording is caught during
  classification. The gate scans the mandatory core (not modules/profiles) and must find **zero**
  hits before the template is "done" (FR-020/SC-002). The scan MAY be a stdlib script
  (`tools/neutrality_scan.py`) or a documented `grep` recipe.
- **Rationale**: FR-020 mandates the term list be a **maintained artifact**, shipped with the
  template (part of provenance) so re-distillation re-runs the same gate. Modules/profiles are
  allowed topic-specifics; only the core must be clean — the scan is scoped accordingly.
- **Alternatives rejected**: A fixed term list frozen in the spec (spec explicitly says it must grow);
  an LLM-judged neutrality pass with no recorded term list (not reproducible; can't re-run
  identically at re-distillation).

## D5 — Critical-thinking filter reuses `mentor-research` discipline

- **Decision**: Each SD-sourced idea's recorded judgment uses the `mentor-research` skill's format —
  a tiered reliability call (High/Medium/Low + one-clause caveat) with a citation trail — rather than
  a new per-idea scheme. Lives in the `rationale`/`provenance` columns of `CLASSIFICATION.md`.
- **Rationale**: Spec Assumptions pin this explicitly; the skill already exists
  (`skills/mentor-research/`). Reusing it avoids inventing a second recording mechanism (DESIGN's
  "reuse research discipline across scopes" principle).
- **Alternatives rejected**: A bespoke rubric for idea-judgment (duplication; drift from the extracted
  skill).

## D6 — Reference location is an env-var input, default preserved

- **Decision**: The distillation reads the reference `.claude/` from
  `$COURSE_FACTORY_REFERENCE_DIR`, defaulting to `/home/barak/System_Design_SelfLearn/` when unset
  (FR-001). It is read-only; nothing is vendored into the repo.
- **Rationale**: Settled in clarify (Q1). Keeps a personal, unvalidated course external and read-only
  instead of hardcoding a path or copying it in.
- **Alternatives rejected**: Hardcoded absolute path (clarify rejected it — not portable, bakes in one
  maintainer's layout); vendoring the reference into the repo (imports an unvalidated course as if
  it were a fixture).

## D7 — Validation is a 2-topic, agent-performed paper-walkthrough

- **Decision**: Pre-001, "produces a viable course shape" (SC-003/SC-012) is proven by an
  **agent** reasoning through a structured walkthrough for **two** topics of different shape —
  *Introduction to Psychology* (theory-heavy) and *Python Programming* for a no-prior-programming
  learner (procedural/code-heavy) — sketching outcomes → assessment → one-lesson arc → rubric-checkable
  draft, recorded as a checklist. No pipeline run, no mandatory human gate.
- **Rationale**: Settled in clarify (Q5). 001 doesn't exist yet, so an end-to-end run is impossible;
  two differently-shaped topics stop the neutrality claim from being validated against one easy fit.
- **Alternatives rejected**: One sample topic (over-fits an easy shape); waiting for 001 (blocks 000's
  own acceptance on a downstream spec); a mandatory human-approval gate (clarify explicitly made it
  optional).

## D8 — Rubric core is flagged "adopted on judgment," not research-validated

- **Decision**: The 5-dimension rubric core (Technical Correctness, Grounding/No-Fabrication,
  Pedagogical Flow, Coverage, Practicality) is recorded with the spec's "unproven, adopted on
  judgment" flag, because `research-digest.md` is **silent on quality-rubric evidence** (a gap, not
  thinness). A future rubric-scoped research pass may supersede it without a full re-distillation.
- **Rationale**: FR-013 spells this out; it prevents the rubric core from being presented as
  research-backed when the digest doesn't cover it, while still letting the template ship.
- **Alternatives rejected**: Presenting the rubric as research-validated (false grounding — violates
  Anti-Fabrication); halting because the digest is silent on rubrics (FR-013 carve-out says silence on
  rubrics is not "thin" and must not halt).

---

**Output**: all methodology decisions resolved; no open unknowns block Phase 1 design.
