# course-factory

**Feed it a course brief. Get back a complete, quality-checked course.**

`course-factory` takes one file — a `COURSE_SPEC.md` describing the course you want to learn —
then researches the topic, drafts a syllabus, writes the lessons, and hardens them against a
quality rubric. You approve the structure; an automated evaluator grades the content. Out comes the
course **plus a graded report card**.

> **Status:** in active design — the pipeline isn't wired up yet. Full design & build plan:
> **[`DESIGN.md`](DESIGN.md)**.

---

## How you'll use it

1. **Fill the spec** — copy [`templates/COURSE_SPEC.template.md`](templates/COURSE_SPEC.template.md)
   to `COURSE_SPEC.md` and fill it in. Rough is fine — the factory interviews you about anything
   vague or ambiguous before it starts.
2. **Run course-factory** — point it at your spec.
3. **Approve the structure** — it researches and drafts a **syllabus**, then **lesson skeletons**;
   you review each until you're happy.
4. **Get the course** — it drafts and quality-gates the lessons, then delivers the course + a graded
   **`COURSE_REPORT.md`**.

---

## The spec

One file decides everything downstream. The template
([`templates/COURSE_SPEC.template.md`](templates/COURSE_SPEC.template.md)) captures the topic,
scope, audience, depth, a **required running example**, optional modules (katas / diagrams /
Socratic), and source material. From your spec the factory generates the course's
`COURSE_BRIEF.md` overlay.

Don't over-polish it. **Phase 0** of the pipeline is an *intake interview* that resolves gaps and
ambiguities with you **before** spending the expensive research step — so a rough spec is enough
to start.

---

## What you get

- The **course** — phases and lessons, plus (optional) diagrams and hands-on katas.
- **`COURSE_REPORT.md`** — a graded scorecard (rubric scores + verdict) certifying the quality.
- A per-course **`.claude/`** so you can keep iterating with `/new-lesson`, `/improve-course`.

## Under the hood

The pipeline, the overlay-not-mutation model, the phased review loop, and the roadmap all live in
**[`DESIGN.md`](DESIGN.md)**.
