# course-template

The **frozen, versioned, three-tiered** teaching skeleton every generated course is copied from.

> **Frozen artifact.** Per-course specialization happens by **overlay** — a generated brief plus a
> profile and module selection. Nothing in here is edited to serve an individual course. Central
> improvements flow forward by re-distillation and a version bump, never by surgical per-course
> edits.

## The three tiers

| Tier | What it is | Toggleable? |
| :--- | :--- | :--- |
| **Core** | The evidence-invariant, subject-neutral machinery every course gets: the backward-design backbone, the canonical lesson arc, the feedback loops (consistency check + author-blind evaluator), the quality rubric, and `/improve-course`, `/new-lesson`, `/course-report` | No — always copied |
| **Profiles** | Named configurations *over the one core* — macro spine, entry point, checkpoint placement, unit granularity. Exactly one per course; `default` is the fallback. See `profiles/README.md` | Choose exactly one |
| **Modules** | Opt-in add-ons: `diagrams`, `katas`, `pattern-catalog`, `socratic` | Each independently on/off |

**One core with profiles — never siloed per-subject templates.** There is exactly one `.claude/`
here; `profiles/` holds configuration, not a duplicate core. Disabling every profile and module
leaves a complete, working course template.

## Layout

```
VERSION                  semver stamp for this distillation snapshot
manifest.yaml            self-description: which piece is core / profile / module
CLASSIFICATION.md        the audit ledger — every reference asset's verdict + provenance
neutrality-terms.txt     the maintained denylist the neutrality gate scans core against
README.md                this file
.claude/                 the course-teaching environment (skills, commands, agents)
profiles/                the profile mechanism + the shipped profiles
```

> The `.claude/` **here** is the template copied into each course. It is deliberately **distinct**
> from the factory's own build `.claude/` that runs the generation pipeline. The two are never
> conflated or cross-edited.

## What gets copied

The copy step (spec 001) must not have to *guess* which files land in a generated course. Two
classes of file live at this root:

- **Tier pieces** — everything under `.claude/`, the selected `profiles/` entry, and any enabled
  `modules` pieces. These are the course template; 001 copies them (honoring the profile + module
  selection in `manifest.yaml`).
- **Template-root metadata** — `VERSION`, `manifest.yaml`, `CLASSIFICATION.md`,
  `neutrality-terms.txt`, and this `README.md`. **None is copied into a course.** They describe or
  maintain the *template*: 001 *reads* `VERSION` (to record the drift stamp) and `manifest.yaml`
  (the tier map) at build time but copies neither; the other three exist only for the distillation
  audit and re-distillation. A generated course gets its own equivalent docs via 001's overlay, not
  by inheriting these.

This disposition is declared machine-readably in `manifest.yaml`'s `metadata:` block (each entry
`copied: false`), so 001 reads it rather than inferring it (FR-018). Metadata files are a **distinct
class** from the three tiers — they are not tier pieces, so the "a piece is in exactly one tier"
manifest invariant is unaffected. **This `README.md` is itself ratified as one such declared
template-root metadata file** (it was added during the distillation to document these rules for the
copy consumer); it stays here rather than folding into the manifest, since prose belongs in a README
and the manifest carries only the machine-readable declaration.

## `VERSION` and drift

`VERSION` holds one `MAJOR.MINOR.PATCH` value that names this distillation snapshot, and it is
**also the rubric's version identity** — one counter across the template and its rubric, never two.

| Change | Bump |
| :--- | :--- |
| Full re-distillation (the whole reference re-filtered) | **MAJOR** |
| Rubric-only re-stamp adopted from a review proposal | **MINOR** / **PATCH** |
| No content change | none — the template is byte-frozen between distillations |

A course records this stamp when it is copied and compares it on resume; a mismatch flags drift and
prompts a manual re-sync (re-copy the template, reapply the thin overlay).

## `manifest.yaml`

The seam the copy step reads so it can honor a profile + module selection **without inferring**
tiers from directory layout. Its invariants: `version` equals `VERSION`; exactly one profile has
`default: true`; every listed path exists and has a matching `CLASSIFICATION.md` target; every
module's `depends_on` toward core is empty; and a piece belongs to exactly one tier.

## `neutrality-terms.txt` — the neutrality gate

A **maintained artifact that ships with the template**, so a re-distillation re-runs the same gate.
One term per line, no comment syntax (which keeps it usable verbatim with `grep -f`).

- It **scans the mandatory core only.** Modules and profiles MAY carry subject-specific wording;
  the core may not. The bar is **0 hits**.
- It **grows.** It was seeded from the subject terms named in the spec and gained new entries as
  classification caught more subject wording — 5 seeded, 18 today (see `CLASSIFICATION.md` § The
  neutrality gate). Any future distillation that catches new wording adds it here rather than
  fixing it silently in one file.

```bash
python course-factory/tools/neutrality_scan.py          # gate: exit 1 on any core hit
python course-factory/tools/neutrality_scan.py --all    # also list module/profile hits (advisory)
```

## Provenance

Distilled from a hand-built reference course — treated as an **unvalidated idea pool**, never as a
proven template — cross-checked against an external instructional-design research digest, with the
better-grounded guidance winning. Every one of the 23 reference assets carries a recorded verdict,
a tiered rationale, and its provenance in `CLASSIFICATION.md`; nothing was carried over merely
because the reference course had it. Where the research is silent — notably on quality-rubric
evidence — the adopted choice is flagged **"adopted on judgment"** rather than presented as
research-backed.
