# findings-FIXES — resolution log for REVIEW-findings.md

> **Repaired 2026-07-22.** Entries A8–A14 were corrupted by terminal column-wrapping when this log
> was first pasted in (padding spaces overwrote characters; A9, A10, and A14 were swallowed into
> neighbouring lines). They have been reconstructed from `REVIEW-findings.md`'s Direction fields and
> verified against the specs as they stand. Wording is a reconstruction; the resolutions themselves
> were spot-checked on disk and are accurate.
>
> **Status: closed.** Every Part A / B / C finding is resolved or explicitly judgment-called. Treat
> this file as historical record, not open work. **One exception, found 2026-07-22 —** see
> "Incomplete sweep" at the end.

Summary

Resolved all Part A findings (A1–A16) across 000-004 spec.md, README.md, DESIGN.md, and constitution.md. Constitution bumped 1.1.0 → 1.2.0 (MINOR).

Critical
- A1 — Wired the profile seam: 001 FR-004/005/006 now select a profile at intake; 002 FR-015 and 003 FR-019 consume it. Fixed 001's stale two-tier course-template language (FR-001, Key Entities) that A1 flagged.
- A2 — 000 FR-013's rubric-dimension list is now explicitly judgment-based (critical-thinking filter + "unproven, adopted on judgment" flag), since the digest has no rubric coverage — not silently claimed research-validated.
- A3 — New DIFFS.md forward-diff ledger, owned by 001 (FR-027), stubbed at instantiation (FR-008). 002/003 now read "frozen artifact + DIFFS.md" as canonical input.

Major
- A4 — FEEDBACK.md now has writers: 001 FR-026 (gate-event comments), 003 FR-020 (evaluator critiques).
- A5 — Factory's own .claude/ declared 001's implementation deliverable (not a separate spec) — judgment call, the other option was a standalone spec entry.
- A6 — SYLLABUS.md + lesson files added to 001's delivery contract and constitution's file list.
- A7 — Insights digest wired as an input to 001 intake (FR-025) and 002 composition (FR-016).
- A8 — Constitution/DESIGN reconciled to the settled decisions: the harvest is user-invoked-only, and the fake-student trigger is the first two lessons reaching a terminal state, not "pass the rubric."
- A9 — Ask-moments (open questions) vs. gates (approvals) made explicitly distinct in 001 FR-014 and constitution Principle IV.
- A10 — Rubric version IS the template stamp (000 owns the single version identity). Added a narrower rubric-only re-stamp path in 000's Edge Cases so comparison/ revisions have a landing spot without a full re-distillation. Judgment call, matches Part C's C4-2 suggestion.
- A11 — Delivery's gate = report generation, verdict informational. Reworded "certify" → "report" throughout (001, 004, constitution, DESIGN) so a needs-work verdict still reaches the delivered terminal state.

Minor
- A12 — procedural/code pinned as a later-increment profile, not part of the initial ship set (already true in 000's FR-023/Assumptions; fixed the inconsistent Overview text).
- A13 — 000 FR-013 is now the canonical rubric-dimension list; 004 FR-001 references it instead of re-deriving.
- A14 — README seam #3 reworded to match reality (002 has no sub-phase state yet).
- A15 — DESIGN's pedagogy/ row updated to built/populated/not-wired; added a forward-pointer in 003 for the [Pn] citation slot needed at wiring time.
- A16 — insights/ declared to start empty (confirmed on disk — no pre-existing corpus exists).

Also added 6 new "Seams to watch" entries in README so a cold session can find these cross-spec contracts without re-deriving them.


- B1-1 (=A1), B1-2 (=A3), B2-2 (=A7), B4-1 (=A11) — exactly as flagged.
- Also caught two more during re-check that Part A had silently already fixed: B2-7 (syllabus artifact named SYLLABUS.md — done via A6) and B1-7 (BUILD_PROGRESS.md "empty"→"initialized" — done as a side effect of A3's FR-008 edit).
- B3-2 was only half-resolved by A9 (the ask-moment carve-out) — completed the remaining half here (003 FR-018 now states the pool idles, not proceeds, while a cap-accept decision is pending).
- C4-2 (fold rubric versioning into template stamp) — already done by A10. C2-3, C4-4 — affirmations, no defect, no edit.

Bug caught in passing

001 FR-008 cited FR-025 for the DIFFS.md stub, but that FR is actually FR-027 (a leftover from the Part A pass) — fixed.

By spec

000: B0-1 (paper-walkthrough proxy for SC-003/SC-012 pre-pipeline), B0-2 (/course-report added to core list, 4 spots + constitution + DESIGN), B0-3 (halt only if digest absent; flag if thin-on-a-subject, with a minimal quality bar), B0-4 (neutrality term list is a maintained artifact), B0-5 (classify every file, dropped hardcoded 4/10/5/1 counts), B0-6 (/improve-course//new-lesson//course-report grounded via critical-thinking filter, not the research digest), C0-2 (FR-006/FR-019 merged into one classification-table concept), C0-3 (mentor-research skill reuse), C0-4 (SC-008 defers to 001 SC-003).

001: B1-3/C1-2 (new FR-028 lock marker + SC-012), B1-4 (FR-024 defines the change-request loop: fresh 3-round cap), B1-5 (FR-004 folds module selection in; COURSE_BRIEF.md is the sole home, no separate clarified-spec file), B1-6 (FR-012 capped at exactly one extra pass), B1-8 (intake-interruption assumption), C1-1 (FR-013 turned into a pointer to FR-023, number kept for cross-refs), C1-3 (BUILD_PROGRESS.md schema flagged as a first-class plan deliverable).

002: B2-1 (new FR-018 sub-phase status), B2-3 (SC-005 reframed around a recorded divergence assessment), B2-4 (new FR-019, post-divergence research reuses the same budget), B2-5 (new edge case, depth-vs-reality conflict), B2-6 (dead-[Sn] ownership resolved: flag-at-discovery only, no recurring liveness check), C2-1 (mentor-research skill reuse), C2-2 (platform search sequenced last, degradable).

003: B3-1 (calibration-edited lessons must be re-graded), B3-2 (completed — pool idles while cap-accept pending), B3-3 (new CALIBRATION.md artifact, FR-021), B3-4 (spot-check → full traceability check, since resolution is cheap — reworded everywhere including mirrored fix in 004), B3-5 (.ipynb citation assumption), B3-6 (no-exercise fallback edge case), B3-7 (orchestrator mis-selection edge case), C3-1 (pool_width config, MVP=1/target=2 — also fixed in DESIGN.md), C3-2 (004 marked canonical citation contract, 002/003 reference it), C3-3 (FR-016 merged into FR-004), C3-4 (fake-student flagged as first knob to revisit).

004: B4-2 (SC-007 reworded to "every critique represented," not content volume), B4-3 (FR-004: scale/thresholds owned by plan, recorded with version), B4-4 (FR-019: minimal adoption protocol — maintainer approves, logged via 000's provenance/stamp), B4-5 (insights digest form specified in Key Entities), B4-6 (comparison/'s source selection reuses 002's reliability weighing), C4-3 (comparison/ names reuse of 002's research method), plus swept remaining stale "certifies"/"spot-check" wording the Part A pass had missed in a few spots.

The two judgment calls

1. C0-1 (000): Added a new User Story 4 ("Ship the structurally-consequential profiles as later, independent increments," P4) and rephrased FR-023/SC-011/SC-012 so the MVP is core+mechanism+default only; PBL/CBL, CBE/mastery, and guided-inquiry each ship as independent later increments. Purely additive — no existing FR/US renumbered.
2. C4-1 (004): Did not split into two spec-kit features. Added a "Plannable increments" note under Overview stating US1 is independently plannable/taskable ahead of US2–US4, strengthened US1's "Why this priority," and left an explicit recommendation that a real split (004-rubric-core + 004a-delivery-harvest-comparison) is a follow-up decision for the user, not executed here.

Constitution bumped 1.2.0 → 1.2.1 (PATCH) for B0-2's /course-report completion — no principle redefined, just an enumeration fixed to match already-settled fact.

---

## Incomplete sweep — found 2026-07-22

**B3-4 (spot-check → exhaustive traceability) was reported "reworded everywhere" but stopped at the
spec bodies.** `003/spec.md` and `004/spec.md` were correctly updated, and 004 published
`contracts/citation-traceability.md` making the exhaustive rule canonical. But the two *governing*
documents were never touched:

- `.specify/memory/constitution.md` Principle II — still read "the evaluator spot-checks traceability"
- `course-factory/DESIGN.md` § pipeline step 4 — same wording

This mattered because the constitution's own governance clause makes a DESIGN/constitution
disagreement "a defect to reconcile," and the A8 pass had already established that pattern for the
other two stale items. Reconciled in the settled decision's favor (constitution **1.2.2 → 1.2.3**,
DESIGN step 4 citation bullet). The bar was tightened, never loosened, so no spec was in violation
while the wording lagged.

**Lesson for future sweeps:** a "reworded everywhere" claim should grep `.specify/memory/` and
`DESIGN.md`, not just `specs/*/spec.md`. The `**Input**:` blocks at the top of each spec.md are
verbatim historical records of the original user description and are correctly left unswept.
