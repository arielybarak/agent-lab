---
name: diagrams
description: >-
  Optional module — generated visual assets for lessons: when a diagram earns its place, the
  generate-don't-hand-draw pipeline, the house visual conventions, and the check that every
  referenced image actually exists. USE WHEN adding or updating a lesson's diagram, or when a
  lesson's image reference does not resolve.
---

# Diagrams (optional module)

> **Optional module.** Enable it for courses whose material is genuinely structural or spatial.
> Disable it and the core is untouched — no core asset depends on this module.

## When to Activate This Skill

- Adding or updating a lesson's diagram
- Wiring a new lesson that needs a visual
- A lesson's image reference does not resolve

## When a diagram earns its place

A diagram is worth its cost when the idea is **structural** (parts and how they connect),
**spatial**, or **a flow over time** — something prose has to serialize and the reader has to
re-assemble. If the idea is a definition, a comparison, or a sequence of steps, prose or a table is
usually better. A decorative diagram costs maintenance and teaches nothing.

Pair the diagram with the text: the lesson must still make sense without it, and the diagram must
not introduce parts the prose never names.

## Generate, don't hand-draw

Diagrams are **produced by a script checked into the course**, not drawn by hand:

- One generator script per course (or per unit), with **one function per diagram**, named after the
  lesson it serves.
- Output goes to the lesson's own image directory, under the **exact filename the lesson
  references**.
- Re-running the generator reproduces every image from scratch. No image is edited after
  generation.

Why: hand-drawn images drift from the lessons that reference them and cannot be re-styled or
regenerated in bulk. A generated set stays consistent and diffable.

## House conventions

- **One visual language across the course** — the same shapes, the same layout direction, and one
  small colour scheme used to mean the same thing in every diagram. Pick it once; match siblings.
- **Highlight one thing.** A diagram whose every element is emphasized emphasizes nothing.
- **Label with the lesson's vocabulary** — the running example's parts, named exactly as the prose
  names them.
- **Keep it small.** If a diagram needs a legend to be read, it is doing two lessons' work.

## Adding a diagram for a lesson

1. Write a generator function mirroring an existing one, so the new diagram matches its siblings.
2. Output to the lesson's image directory with the **exact filename the lesson references**.
3. Wire the function into the script's driver and run it; confirm the image renders.
4. Confirm the lesson's reference now resolves.

## The image-existence check (this module's contribution to review)

When this module is enabled, the `lesson-consistency-reviewer` additionally checks that **every
image a lesson references exists on disk**. A reference to a missing image is a **Critical**
finding — it is invisible in the source and broken for every reader.

The usual cause is adding a lesson without adding its generator function. Check both directions:

- every image reference in a lesson resolves to a real file, **and**
- every generator function's output is actually referenced by some lesson (an orphan image means a
  renamed or deleted lesson).

If the course's tooling supports an editor hook, a post-edit advisory reminder ("this lesson
references an image that does not exist yet") is a cheap way to catch this at authoring time rather
than at review time. It stays **advisory** — it must never block an edit.

## Gotchas

- **Adding the lesson but not the generator function** is the single most common failure — the
  reference 404s silently.
- **Renaming a lesson** breaks its image path in both directions. Rename the generator function and
  the output file in the same change.
- **Hard-coded environment paths** in the generator (a tool location, a platform-specific path)
  break it on other machines. Guard the platform-specific branch; do not delete the working case.

## Provenance

Derived from the reference course's `architecture-diagrams` skill (the generate-don't-hand-draw
pipeline, the house visual conventions, the add-a-diagram procedure, and the
lesson-without-a-diagram-function failure), with that course's specific tool, colour values, script
paths, and its own list of broken images stripped as topic- and repo-specific. The
image-existence check is inherited from the reference `lesson-consistency-reviewer`'s checklist,
which is where it belongs once the module is optional. The advisory post-edit reminder is
generalized from that course's editor hook; the hook's other job — a hard-coded duplicate-file table
for that repo's own trees — was **dropped**. See `CLASSIFICATION.md`.
