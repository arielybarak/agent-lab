---
name: mentor-research
description: >-
  Research-curation discipline for building a cited knowledge base: weigh source
  reliability over popularity, record keeps under stable citation keys ([Sn]/[Pn]-style,
  append-only, deduped per work), tier claims with qualified caveats instead of one
  bucket word, always record boundary conditions/failure modes, identity-verify
  citations via Crossref/ERIC before recording, and stop at convergence or a budget
  cap. USE WHEN researching sources for a syllabus or catalog, curating deep-research
  output (Perplexity-style dumps) into a SOURCES.md, assigning citation keys, tiering
  evidence, or auditing an existing citation list for orphaned/misattributed entries.
---

# Mentor research (search → weigh → key → tier → bound)

One discipline, two entry modes: **inline research** (you run the search loop yourself) or
**curation of external output** (a deep-research dump lands in your lap). The weighing, keying,
tiering, and stopping rules are identical; only the source of raw material differs.

> Re-home note: authored at repo-root `skills/`; copy into `course-factory/.claude/skills/`
> once spec 001 scaffolds the factory's own environment.

## When to Activate This Skill

- "Research X and record what you keep" / building or populating a `SOURCES.md`
- "Turn this deep-research output into cited entries"
- "Assign citation keys / tier this evidence / check these citations"

## The method

1. **Weigh reliability over popularity.** Stars, shares, and rank are green flags, not proof.
   Prefer meta-analyses/primary literature > single studies > practitioner guides > blogs.
   Record the judgment with the entry, not just the link.
2. **Key what you keep — stable and deduped.** Sequential keys in a declared namespace
   (`[S1]`, `[P1]`, …), append-only, never reused. **Dedupe by work, not by URL**: two links to
   the same paper (publisher page + author-lab PDF) are one key. Separate namespaces that will be
   cited side-by-side (e.g. per-course vs. cross-course) must not collide.
3. **Identity-verify before recording.** Resolve each citation's identity (authors, year, title,
   venue) against a registry — `curl https://api.crossref.org/works/<DOI>`, ERIC
   `api.ies.ed.gov/eric/?search=id:<ID>`, NCBI eutils — not against the summary that cited it.
   Prefer the DOI/journal link over mirrors (Scribd, random PDF hosts, course-hosted copies).
4. **Mark what you couldn't verify.** A source known only through another source is
   *(indirect)*; a third-party summary link is *(secondary)*; a weak venue or study type is
   *(supporting)*. Marked-but-kept beats silently-presented-as-verified.
5. **Tier with caveats, not bucket words.** Evidence is rarely uniform. Write
   "High for X, ambiguous for Y" — the qualifier is the payload; downstream consumers make
   decisions on the boundary, not the headline.
6. **Boundary conditions are mandatory.** For every claim kept, record when it fails or
   backfires. An entry with only upside is a red flag: either the research was shallow or the
   claim is too good to be true.
7. **Stop at convergence or the budget cap.** When new sources stop adding material, stop; a
   hard query/tool-call budget backstops the loop. Never run unbounded.
8. **Trace, don't re-prove.** Downstream verification checks that a claim maps to its cited
   source — it does not re-verify the source's own correctness. Say so where the policy applies.

## Curating an external deep-research dump (extra rules)

- **Import only body-referenced citations.** Export formats hide unreferenced footnote spans
  (e.g. a trailing `display:none` block of links). If the body text never cites it, it does not
  enter the sources file.
- **Assume misattribution until verified.** In practice deep-research tools get a meaningful
  fraction of citations wrong — wrong author, wrong year, paraphrased title, wrong venue, even a
  wrong DOI on a correctly-named paper. Step 3 is non-negotiable here; note each correction next
  to the entry so provenance stays auditable.
- **Two footnotes may be one work** (repository page + university press release). Collapse them.
- **Separate provenance from evidence.** When cataloging a debunked/contested claim, cite both
  the popular origin (marked as provenance, never evidence) and the debunking source.

## Gotchas

- The most tempting shortcut — copying the dump's bibliography wholesale into `SOURCES.md` — is
  exactly the failure mode: orphaned links, duplicate works, and misattributions imported as if
  verified.
- Registry APIs are cheap and scriptable; a dozen Crossref lookups cost seconds. There is no
  budget excuse for skipping identity verification of keeper citations.
- Don't let tiers flatten in transcription: if the literature says "strong here, absent there,"
  a lone "High" in the output is a curation bug.
