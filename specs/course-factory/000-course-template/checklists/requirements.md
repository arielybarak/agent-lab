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
- Two open decisions remain for `/speckit-clarify` (house style — kept as questions, not embedded
  `[NEEDS CLARIFICATION]` markers):
  1. **Distillation validation depth** — is SC-003/SC-012's "viable course shape / coherent per
     profile" proven by an actual dry-run generation, or by a structural/neutrality inspection only?
  2. **`lesson-consistency-reviewer` placement** — core (topic-neutral consistency check) vs an
     optional module; the spec assumes core by default but this is worth confirming.
  3. **Initial profile set** — ship exactly the 4 (3 consequential + default), or also include
     theory-vs-procedural as distinct profiles from the start? (FR-023 sets the floor, not the cap.)
