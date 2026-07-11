# pedagogy/ — teaching-technique library (populated)

**Status:** built and populated (2026-07-10) — catalog, myths deny-list, sources registry, and
quality gate all in place. **Not yet wired into any pipeline**: specs 002/003/004 will consume it
once they're implemented; no `course-factory/.claude/` exists yet to wire into. Not one of the
four current specs (001–004); see `course-factory/DESIGN.md` § Deferred extensions.

## What

A library of **teaching techniques + worked examples, with per-material-shape applications**
(concept-heavy, code-heavy, math-heavy, narrative/history) — so course composition draws on
proven pedagogy instead of ad-hoc structure. Includes an explicit deny-list of popular-but-
debunked claims as a guardrail against the model's own training-data priors.

## Contents

| File | Role |
| :--- | :--- |
| `TAXONOMY.md` | The two axes (8 techniques × material shapes), entry schema, tier rules, `[Pn]` namespace decision |
| `CHECKLIST.md` | Quality gate the batch was reviewed against (authored *before* the content) |
| `catalog/*.md` | 8 technique entries: what → evidence tier (qualified) → when → boundary conditions → worked example |
| `MYTHS.md` | 4 debunked/overclaimed ideas (learning styles, neuromyths, growth mindset, grit), each with popular-source + debunking citations |
| `SOURCES.md` | 43 `[Pn]`-keyed citations, identity-verified via Crossref/ERIC, indirect/secondary/supporting marks |
| `perplexity_output.md` | Raw deep-research pass the library was curated from (provenance; superseded by the curated files) |

## Why

Turns "mentor judgment" into a grounded, reusable catalog. Every generated course should inherit
proven teaching methods, and the catalog itself should get better over time — the same compounding
idea `insights/` already applies to *build feedback*, applied here to *pedagogy itself*.

## Relationship to `insights/` — sibling, not the same thing

Both are "knowledge, not tooling" directories read at generation time, but they're populated from
different places:

| | Source | Populated by |
| :--- | :--- | :--- |
| `insights/` | Feedback harvested from courses **we've built** | `FEEDBACK.md` → `insights/` harvest (owned by spec 004) |
| `pedagogy/` | Research into teaching methods **in general** | This library (external deep-research pass + curation) |

## How it was built — 002's method, generalized

This reused spec 002's research discipline at a cross-course level, as planned: research → weigh
reliability over popularity → cite under stable keys → stop at convergence/budget. The research
itself ran externally (Perplexity deep research, saved as `perplexity_output.md`); a curation pass
then keyed, tiered, verified, and deduped it into the files above. That curation discipline is
extracted as the shared **`mentor-research` skill** (repo-root `skills/mentor-research/`, active
copy in `.claude/skills/mentor-research/`) for spec 002's own future research runs.

## Resolved decisions (formerly "Open questions")

- **Taxonomy of material/course-type keys** → resolved in `TAXONOMY.md`: material shape is
  **Axis 2**, expressed as optional in-file "Applying to `<shape>`" subsections (only where the
  application genuinely diverges), not a directory grid. Techniques (Axis 1) are capped at 8.
- **Citation discipline** → resolved: yes, `SOURCES.md`-style keys, but in an own **`[Pn]`
  namespace** — cross-course and stable, distinct from any per-course `[Sn]` file, so lessons can
  cite both without collision.
- **Evidence handling** → qualified tiers (High/Medium/Low + one-clause caveat), myths in their
  own file with their own schema, and a normative rule: **specs 002/003 MUST NOT cite a low-tier
  or `MYTHS.md` entry as justification for a course-design choice.**

## Consumption points (future wiring, unchanged)

- **002** (syllabus compose-as-mentor) — draws on it when composing course structure.
- **003** (skeleton/lesson drafting) — draws on it when authoring content.
- **004** (rubric) — optional candidate input to a method-fit rubric add-on; not required for the
  rubric core.

Wiring happens when those specs are implemented; nothing here blocks on them.

## Why this isn't a spec

Spec-kit's `spec.md` shape (user stories, testable functional requirements, measurable success
criteria) fits *pipeline behavior*. This is a **research/content deliverable** — its output is a
populated catalog gated by its own `CHECKLIST.md`, not a built capability with a pipeline gate.
