# Taxonomy — how this library is organized

Two axes. Only the first gets its own files; the second lives as optional in-file subsections.
This keeps the catalog a practical tool, not a combinatorial grid.

## Axis 1 — generic technique (one file each, capped at 8)

Domain-general techniques from the cognitive-science literature. **The cap is deliberate**: this
is a practical catalog for a course-generation pipeline, not a literature review. Adding a 9th
entry requires removing one or a strong case that the pipeline needs it.

| # | Technique | File |
| :--- | :--- | :--- |
| 1 | Retrieval practice | `catalog/retrieval-practice.md` |
| 2 | Worked examples | `catalog/worked-examples.md` |
| 3 | Spaced repetition (distributed practice) | `catalog/spaced-repetition.md` |
| 4 | Interleaving | `catalog/interleaving.md` |
| 5 | Scaffolding / cognitive-load management | `catalog/scaffolding-cognitive-load.md` |
| 6 | Dual coding (visual + verbal) | `catalog/dual-coding.md` |
| 7 | Socratic / guided-discovery questioning | `catalog/socratic-guided-discovery.md` |
| 8 | Formative assessment | `catalog/formative-assessment.md` |

**Not a peer entry:** "direct instruction vs. problem-based learning" is a macro instructional
*stance*, not a technique — it is folded into the Socratic entry's boundary conditions (the
Kirschner/Sweller/Clark minimal-guidance critique) rather than listed as a 9th item.

## Axis 2 — material shape (in-file subsections, not a directory grid)

Material shapes: **concept-heavy** (theory, mental models), **code-heavy** (programming,
notebooks), **math-heavy** (proofs, procedures), **narrative/history-heavy** (arcs, events,
interpretation). A technique file adds an `Applying to <shape>` subsection **only where the
application genuinely diverges** from its worked example — most techniques don't need one for
every shape, and an empty subsection is worse than none.

## Entry schema (fixed, all sections mandatory unless marked optional)

1. **What it is** — one-paragraph definition.
2. **Evidence tier** — qualified tier + `[Pn]` citation(s). See tier rules below.
3. **When to use** — conditions, learner level, material type.
4. **Boundary conditions & pitfalls** — one merged section; when it fails or backfires.
   Mandatory: a technique entry with no known failure mode is a red flag, not a feature.
5. **Worked example** — one concrete, plausible scenario of a course-generation tool using it.
6. **Applying to `<material shape>`** — *optional*, only where divergent (Axis 2).

## Evidence tiers — qualified, with teeth

| Tier | Meaning |
| :--- | :--- |
| **High** | Meta-analyses / converging cognitive-science literature. |
| **Medium** | Single studies or strong practitioner consensus. |
| **Low** | Popular but weakly supported — flagged, never excluded silently. |

Rules:

- **Tiers are qualified, not single words.** Evidence is rarely uniform — write
  "High for X, medium for Y" or "Medium, with caveats" plus a one-clause caveat where the
  literature is nuanced (e.g. interleaving: high for inductive/discriminative learning, ambiguous
  for expository text). Collapsing to one bucket word loses the boundary information the pipeline
  needs.
- **Myths are not low-tier techniques.** A debunked claim (e.g. learning styles) has no "when to
  use" — it structurally isn't a technique, so it lives in `MYTHS.md` with its own schema (claim →
  why popular → why wrong → what to use instead → popular-source citation + debunking citation),
  not as a tier tag inside the catalog.
- **Normative rule (mirrors spec 002's FR style):** specs 002/003 MUST NOT cite a low-tier entry
  or a `MYTHS.md` entry as justification for a course-design choice. The low tier and the myths
  file exist only as a deny-list guardrail against training-data priors reaching for a debunked
  claim.

## Citation namespace — `[Pn]`, not `[Sn]`

Pedagogy citations are cross-course and stable, keyed `[P1]`, `[P2]`, … into
`pedagogy/SOURCES.md`. This is deliberately a **separate namespace** from the per-course `[Sn]`
keys of a course's own `SOURCES.md` (spec 002), so a lesson can cite both without collision.
Keys are append-stable: once assigned, never reused for a different source.
