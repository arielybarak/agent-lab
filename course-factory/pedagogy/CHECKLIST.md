# Quality Checklist: pedagogy/ technique library

**Purpose**: Gate every `catalog/*.md` entry, `MYTHS.md`, and `SOURCES.md` before the library is
considered populated. Authored **before** transcription (Phase 0) so the batch critique reviews
against it, not ad-hoc judgment.
**Created**: 2026-07-10
**Gates**: `catalog/*.md` (8 entries), `MYTHS.md`, `SOURCES.md`, `DIGEST.md`

## Evidence & Citation

- [x] Every catalog entry carries at least one `[Pn]` citation resolving to a real `SOURCES.md` entry
- [x] Every `SOURCES.md` entry has a stable `[Pn]` key, author/year/title, and a link or an explicit "no direct link" mark
- [x] No orphaned links imported — zero entries from `perplexity_output.md`'s unreferenced footnote span (`[^1_48]`–`[^1_73]`)
- [x] Indirect/secondary citations (cited via a summary, mirror, or third-party page — e.g. Sweller & Cooper 1985) are explicitly marked as such, not presented as directly verified
- [x] Where a citation has both a peer-reviewed/DOI link and a mirror (Scribd, random PDF host), the DOI/journal link is the one recorded
- [x] Repeated sources across techniques (e.g. Sweller, Cepeda) are deduplicated to a single `[Pn]` key
- [x] Evidence tiers are qualified where the literature is nuanced (tier + one-clause caveat), not collapsed to one bucket word

## Pedagogical Soundness

- [x] Every catalog entry's "Boundary conditions & pitfalls" section is genuinely populated (documented failure modes), not upside restated
- [x] No myth-laundering: nothing presented as a catalog technique that belongs in `MYTHS.md`, and no catalog entry leans on a debunked mechanism
- [x] Socratic/guided-discovery entry treats *guided* questioning only — unguided/minimal-guidance discovery is flagged as the failure mode, per Kirschner/Sweller/Clark
- [x] Tier calibration is consistent *across* entries (same evidence strength → same tier language)
- [x] Each `MYTHS.md` entry has both a popular-source citation and a debunking citation
- [x] `MYTHS.md` entries state an evidence-based alternative, not just the debunk

## Structure Completeness

- [x] Every catalog entry has all mandatory schema sections (What it is → Evidence tier → When to use → Boundary conditions & pitfalls → Worked example)
- [x] `Applying to <material shape>` subsections appear only where the application genuinely diverges from the worked example — no empty/padded shape sections
- [x] Exactly 8 catalog entries, matching `TAXONOMY.md`'s Axis-1 list
- [x] `MYTHS.md` has all 4 planned entries: learning styles, brain-based neuromyths, growth mindset, grit

## Dogfood Realism

- [x] Every worked example is a concrete, plausible course-generation scenario (a tool composing lessons), not an abstract classroom vignette
- [x] Worked examples span more than one material shape across the catalog (not all programming, not all math)
- [x] No entry depends on or references `System_Design_SelfLearn` or any other unreviewed existing course
- [x] Entries are usable by specs 002/003 as written — self-contained, no "see the full paper" required to apply the technique

## Digest fidelity (`DIGEST.md`)

- [x] Every catalog entry's **"Boundary conditions & pitfalls"** survives into the digest — the digest may compress the definition and drop the worked example, but never a failure mode
- [x] Digest evidence tiers are the catalog's **qualified** tiers verbatim, not collapsed to one bucket word (e.g. interleaving stays "high for inductive/discriminative, ambiguous for expository text")
- [x] Every `[Pn]` key in the digest resolves to `SOURCES.md` and appears in the source it condenses — the digest introduces **no** citation of its own
- [x] All 8 Axis-1 techniques appear, in `TAXONOMY.md`'s order
- [x] Digest is marked **derived, never hand-edited**, and names `catalog/` as canonical on disagreement
- [x] `MYTHS.md` entries appear in the digest with their debunking citations and the "use instead" column — the deny-list is not weakened by compression

## Notes

- Items are checked during Phase 3's batch critique (one fresh-context reviewer over the whole
  batch, capped at 3 rounds); unresolved deltas are noted inline in the affected file rather than
  looped forever.
- Citation checking here is **tracing, not truth** (same policy as spec 004's lesson citations):
  verify the claim maps to the cited source, don't re-verify the source's own correctness.
- **Gate run 2026-07-10**: fresh-context batch review, 2 rounds, verdict PASS. Accepted noted
  delta (do not re-raise): the 8 *primary* worked examples lean STEM/clinical — kept as-is from
  the research pass by design; narrative/history coverage lives in the "Applying to" subsections
  of worked-examples, dual-coding, and interleaving.
