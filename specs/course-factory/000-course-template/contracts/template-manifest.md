# Contract: Template Manifest (`manifest.yaml`)

**Producer**: spec 000 (this distillation). **Consumer**: spec 001 (copy/overlay/version — 001
FR-001/006/007). This is the seam that lets 001 honor a profile + module selection **without
inferring** tiers from directory layout (FR-018).

## Location

`course-factory/course-template/manifest.yaml` — at the template root, alongside `VERSION`.

## Schema

```yaml
version: "1.0.0"            # MUST equal the VERSION file (semver). Drift here is a defect.

core:                       # mandatory tier — always copied, never toggleable
  - .claude/skills/lesson-arc/SKILL.md
  - .claude/skills/backward-design/SKILL.md
  - .claude/skills/quality-rubric/SKILL.md
  - .claude/agents/lesson-consistency-reviewer.md
  - .claude/agents/course-evaluator.md
  - .claude/commands/improve-course.md
  - .claude/commands/new-lesson.md
  - .claude/commands/course-report.md
  # …every path here also appears as a `target: core` row in CLASSIFICATION.md

profiles:                   # exactly one default:true (FR-025). MVP ships only `default`.
  default:
    default: true
    entry_point: theory-first
    pieces:
      - profiles/default/spine.md
  # pbl-cbl / cbe-mastery / guided-inquiry: added by LATER increments (FR-023), absent at MVP

modules:                    # opt-in, each independently toggleable (FR-012)
  diagrams:
    pieces:
      - .claude/skills/architecture-diagrams/SKILL.md
      - .claude/commands/add-diagram.md
    depends_on: []          # MUST be empty toward core — no module is a hidden core dependency (SC-004)
  katas:
    pieces: [ ... ]
    depends_on: []
  pattern-catalog:
    pieces: [ ... ]
    depends_on: []
  socratic:
    pieces: [ ... ]
    depends_on: []
```

## Invariants 001 relies on

1. **`version` == `VERSION`** — one identity; 001 records this stamp and later drift-checks it (SC-006).
2. **Exactly one `profiles.*.default: true`** — 001's fallback when a course names no profile
   (FR-025/SC-012). Zero or many defaults is a defect.
3. **Every `core`/`profile`/`module` path exists on disk** and has a matching `CLASSIFICATION.md`
   row with the same `target` (SC-001/SC-007) — no manifest entry without provenance.
4. **`modules.*.depends_on` toward core is empty** — 001 may include/exclude any module without
   breaking the core (FR-012/SC-004).
5. **Core is never listed under `modules` or `profiles`** — a piece is in exactly one tier.

## Out of scope for this contract

*How* 001 copies, overlays, and stamps (001 FR-006/007); the grading engine that reads the rubric
(004). This contract fixes only the **shape 001 reads**.
