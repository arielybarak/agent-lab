# Quickstart: Validate the Produced Course-Template

How to confirm the distillation deliverable is correct. There is **no pipeline to run** (001 doesn't
exist yet) — validation is artifact inspection + one agent-performed paper-walkthrough. Each check
maps to a Success Criterion.

## Prerequisites

- The produced `course-factory/course-template/` tree exists (`VERSION`, `manifest.yaml`,
  `CLASSIFICATION.md`, `neutrality-terms.txt`, `.claude/`, `profiles/default/`).
- Reference course reachable at `$COURSE_FACTORY_REFERENCE_DIR` (default
  `/home/barak/System_Design_SelfLearn/`) — only needed to re-check classification coverage.

## Check 1 — Classification completeness (SC-001, SC-007, SC-009)

```bash
# Every reference asset (23 for the current reference) has exactly one row + rationale + provenance.
REF="${COURSE_FACTORY_REFERENCE_DIR:-/home/barak/System_Design_SelfLearn}"
find "$REF/.claude" -type f | wc -l            # expected asset count (agents+commands+hooks+skills+settings+backlog) + CLAUDE.md
```

- Expected: **every** asset has a `CLASSIFICATION.md` row with a non-empty `verdict`, `rationale`,
  and `provenance`; **0 unclassified**.
- No `rationale` reads "SD already had it" — each kept row cites research or a critical-thinking
  judgment (SC-009).

## Check 2 — Neutrality gate: core has 0 topic terms (SC-002)

```bash
# Scan the mandatory core (NOT modules/profiles) against the maintained denylist.
grep -R -n -i -f course-factory/course-template/neutrality-terms.txt \
  course-factory/course-template/.claude   # then filter to core paths per manifest.yaml
# expected: no hits in any `core:` path
```

- Expected: **0** hits in core paths. Hits in `module:`/`profile:` paths are allowed (those tiers may
  carry topic-specifics). If `tools/neutrality_scan.py` exists, run it instead — same contract.

## Check 3 — Rubric two-layer shape (SC-005)

- Open the rubric asset. Confirm the **core layer holds exactly the 5** dimensions (Technical
  Correctness, Grounding/No-Fabrication, Pedagogical Flow, Coverage, Practicality) and **0**
  topic-specific dimensions.
- Confirm SD's checks (fabricated-capacity, cargo-cult) appear as **add-on slots**, not core.
- Confirm the asset states weights/thresholds/hard-gate are **owned by 004** (defines shape only).

## Check 4 — Manifest & version contract (SC-006, SC-004)

- `manifest.yaml` `version` **equals** the `VERSION` file (one identity).
- Exactly **one** `profiles.*.default: true`.
- Every manifest path exists on disk and has a matching `CLASSIFICATION.md` `target`.
- **Drift sim**: record `VERSION`, bump it, confirm a recorded-vs-current string compare flags the
  mismatch (`contracts/version-stamp.md`).
- **Module independence**: for each module, confirm `depends_on` toward core is empty — toggling it
  off leaves a working core (SC-004).

## Check 5 — 2-topic paper-walkthrough (SC-003, SC-012) — the core neutrality proof

Agent-performed, no code. For **each** of the two sample topics —
**Introduction to Psychology** (theory-heavy) and **Python Programming** for a no-prior-programming
learner (procedural/code-heavy) — with **all optional modules disabled**, reason through and record a
checklist:

1. **Outcomes** — apply the backward-design backbone: does it yield sensible learning outcomes?
2. **Assessment** — does the backbone produce coherent evidence/assessment for those outcomes?
3. **One-lesson arc** — instantiate the canonical lesson arc for one lesson: does it hold without a
   System-Design assumption?
4. **Rubric-checkable draft** — sketch a lesson draft the 5-dimension core rubric can actually grade.

- Expected: each step produces a sensible artifact for **both** topics using the **core alone** — no
  optional module required. Record as a checklist (maintainer review optional, not required).
- Then repeat step-4 sizing against the `default` profile (SC-012): its macro-spine/checkpoint
  reconfiguration yields a coherent outline for both topics; a course naming no profile falls back to
  `default`.

## Check 6 — Digest dependency & no forked templates (SC-010, SC-011)

- **Digest consumed (SC-010)**: confirm the run actually consumed `research-digest.md` — every
  research-grounded `CLASSIFICATION.md` provenance resolves to it. Confirm the distillation's
  halt/flag behavior exists: a **missing** digest halts the run (FR-005), and a digest **thin** on a
  specific subject (fewer than one cited section, D-note in `research.md`) flags that subject
  "judgment-based" rather than silently trusting the reference course.
- **No forked templates (SC-011)**: confirm there is **one** `.claude/` core shared across all
  profiles — `profiles/` holds configurations (spine/entry-point/checkpoints), **not** a full
  duplicate `.claude/` per subject. Disabling the profile layer leaves the one core intact. At full
  delivery (User Story 4 landed) expect **≥4** profiles, each reusing the same core.

## Definition of done

All five checks pass and `CLASSIFICATION.md` shows 0 unclassified assets. The later-increment
profiles (PBL/CBL, CBE/mastery, guided-inquiry) are **not** required for this to pass — they ship and
validate independently (User Story 4). Once 001 exists, re-run Checks 3–5 by actually driving the
pipeline; the paper-walkthrough is a pre-pipeline proxy, not a permanent substitute.
