# Specification Quality Checklist: Course-Template Distillation

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-07-10
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- Items marked incomplete require spec updates before `/speckit-clarify` or `/speckit-plan`.
- **Resolved (2026-07-10):** the "one template vs several" question is settled by the external
  research digest (`research-digest.md` §5) → **one core + archetype profiles + optional modules**,
  not siloed per-subject templates. Encoded in FR-009/010 + the new **Archetype profiles** group
  (FR-022–FR-025), SC-011/012, and constitution Principle IX (v1.1.0).
- **Resolved (2026-07-11, `/speckit-clarify`):**
  1. **Distillation validation depth** — settled as a 2-topic (*Introduction to Psychology*,
     *Python Programming*), agent-performed, structured paper-walkthrough (no dry-run pipeline
     needed pre-001; no mandatory human-approval gate). See spec's Clarifications + SC-003/SC-012.
  2. **`lesson-consistency-reviewer` placement** — settled as a **split**: the generic
     consistency-check capability → core (FR-010); the diagram-existence check → the `diagrams`
     module (FR-011); the phase-language rule and `patterns_v2`/`patterns_v1` drift check →
     dropped. See spec's Clarifications.
  3. **Initial profile set** — already settled by the Part A/B/C reconciliation pass (2026-07-11,
     predating this clarify session): procedural/code is a later-increment candidate, not part of
     the initial ship set (FR-023, Assumptions, constitution Principle IX). This checklist note was
     stale; no clarify question needed.
  Two other decisions were also resolved this session, not originally tracked here: the reference
  course's on-disk location (now a configurable input, FR-001) and the template version-stamp
  format (now semantic versioning, FR-016).
