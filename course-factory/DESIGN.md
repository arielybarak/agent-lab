# course-factory — design & build plan

**Turn a single course-spec `.md` into a complete, quality-hardened course.**

This is the *design doc + build plan* (not working code yet) — it describes what `course-factory`
is meant to become so we can build it deliberately. For the product-facing overview and the intake
prompt, see [`README.md`](README.md).

---

## The idea in one line

You write a **course spec** (topic, audience, depth, running example). The factory instantiates
a course from a **frozen template**, lays a **topic-brief overlay** on top, then walks a
**phased review loop** — you approve the structure, an automated evaluator hardens the content —
until the course clears the quality rubric. Out comes the **course itself**, with a specialized
`.claude` left inside it as a byproduct.

It is **not** a `.claude` generator. It is a **course generator** that happens to carry a
`.claude` as its engine.

## Two `.claude` folders — don't confuse them

| `.claude` | Lives at | Role |
| :--- | :--- | :--- |
| **Factory's own** | `course-factory/.claude/` | Runs the **build pipeline** — the tooling that helps *us* make courses (scaffold, draft, grade agents/commands). |
| **Course template** | `course-factory/course-template/.claude/` | **Frozen** template copied into the **generated course**, adapted via overlay, shipped as the course's residue env for continued iteration. |

## Mental model

```
COURSE_SPEC.md  ─▶  [ course-factory/.claude ]  ─▶  a finished course/
 (user-written)         runs the pipeline         courses/<name>/  (staging — moved out after delivery)
                              │                         ├── lessons, syllabus, diagrams, katas
                              │                         ├── COURSE_BRIEF.md    (generated topic overlay)
                              │                         ├── SOURCES.md         (research grounding, [Sn] cite targets)
                              │                         ├── BUILD_PROGRESS.md  (pipeline state — resume anywhere)
                              │                         ├── FEEDBACK.md        (critiques → harvested to insights/)
                              │                         ├── COURSE_REPORT.md   (final graded scorecard)
                              ▼                         └── .claude/  (from course-template, frozen)
                   course-template/  (frozen skeleton + generic .claude, copied not mutated)
```

**Deliverable = the course content.** The per-course `.claude` is the *residue*, not the
point — exactly the shape the `System_Design_SelfLearn` repo has today (course content in
`System_Design_v1/` **plus** a repo-root `.claude`).

`courses/` is **staging only**: once delivered, the user moves the course out of this repo to its
own home (like `System_Design_SelfLearn`). That also sidesteps nested-`.claude` command collisions
with the factory's own `.claude`.

## Specialize by overlay, not mutation

**Naming:** `COURSE_SPEC.md` = what the **user writes** (from `templates/COURSE_SPEC.template.md`);
`COURSE_BRIEF.md` = what the **factory generates** from it — the overlay living inside the course.

The spec does **not** edit the template `.claude`'s internals. Instead it produces:

1. **A topic-brief** (`COURSE_BRIEF.md`, a `CLAUDE.md`-style file) that the generic tools *read*
   — running example, audience, scope, source material.
2. **A module selection** — include/exclude *optional modules*. A module is anything from a single
   skill file to a full bundle (skills + commands + hooks + settings fragments + template folders +
   code) — e.g. *diagrams* = skill + reminder hook + `generate_diagrams.py`.

The template `.claude` stays **frozen**. Why overlay beats mutation:

- **Central upgrades flow forward** — improve the generic `.claude` once; every *future* course
  gets it at copy time. Already-shipped courses are re-synced **manually** (re-copy template +
  reapply the thin overlay); the copy step stamps the template version into the course to make
  that easy.
- **Less drift** — one source of truth + a thin per-course delta, not N hand-edited copies.
- **More reliable to generate** — writing one brief is safer than surgically editing many files.

That same brief serves **both** the factory during the build *and* the shipped course afterward.

## Pipeline — the phased review loop

Automate scaffolding and first drafts aggressively; **keep a review gate at each phase**. The
**reviewer changes by phase — matched to whoever is competent to judge that artifact.**

| Phase | Artifact | Reviewer | Loop until | Why them |
| :--- | :--- | :--- | :--- | :--- |
| **1. Syllabus** | course shape / scope | **User** | user is pleased | user owns "what I want to learn" |
| **2. Skeletons** | per-lesson plans | **Agent-eval, then user** | agent passes, *then* user confirms | agent checks topic-fit + clarity first; user then judges structure |
| **3. Lessons** | lesson content | **Automated eval** (course-evaluator + rubric) | passes rubric | user can't grade material they're *learning* |

**Reusable primitive:** an **author → agent-critique → refine** loop powers both the skeleton and
lesson phases. Generate the whole batch (**big chunks** — don't interrupt the user per item), run
the agent loop to convergence (**capped at 3 rounds**), *then* apply the phase's gate. Only the gate differs: a **user
scan** after skeletons, **rubric-only** after lessons.

**Steps:**

0. **Intake / clarify** — read the spec, then ask the user upfront questions to resolve
   ambiguities about the course's *nature* **before** spending the expensive research. Cheaper to
   settle now than mid-pipeline. Produces a clarified spec + `COURSE_BRIEF.md` + module selection.
1. **Copy** `course-template/` into the new course (skeleton + frozen `.claude`), apply overlay,
   stamp the template version, and create an empty `BUILD_PROGRESS.md` (pipeline state: current
   phase + per-lesson status, so any session can resume mid-course).
2. **Syllabus loop:**
   - **a. Research (expensive).** Search the web, **GitHub**, and **course platforms**
     (Udemy, Coursera, edX) for existing courses / accessible syllabi / other sources on the topic.
     **Critically weigh** each for relevance and reliability — high stars are a *strong green flag*
     but not proof. Save what you keep to the course's **`SOURCES.md`** under stable keys
     (`[S1]`, `[S2]`, …) — links for heavy sources, inline citations for posts / comments / tips.
     It is the **anti-fabrication grounding for every lesson later**, not just the syllabus.
     *Tooling stays light: web search + `gh` CLI for GitHub. For Udemy / Coursera / edX, a
     **shallow name-search** only — find similarly-named courses and read the publicly visible
     syllabus (often viewable without registering; verify on first run). No scrapers/pullers
     unless real runs prove repeated cost.* **Stopping rule:** pull until sources **converge**
     (new ones stop adding topics), with a hard **budget / cost cap** as backstop.
   - **b. Compose** the syllabus **as a domain mentor** — sources *inform*, they don't *dictate*.
     Don't blindly aggregate: sources may be sparse, stale (20 years old), or off from what the
     industry / the user actually needs. Apply common sense and current-industry judgment to fill
     gaps, correct staleness, and keep it relevant. Decide course **volume** here, plus the
     **lesson file format** — `.md` by default, `.ipynb` when the course is code-heavy (a judgment
     call from the course's nature once the syllabus takes shape; record it in `COURSE_BRIEF.md`).
   - **c. Diverging sources?** If topics vary widely across sources, ask the user directional
     questions to pick the course's angle. *(This gate can't be front-loaded — you only learn of
     the divergence by looking.)*
   - **d. User reviews** the syllabus; repeat until pleased. Once approved, the syllabus is
     **frozen**: if later drafting reveals a gap, the change is shown to the user as an explicit
     diff — never made silently.
3. **Skeleton loop:**
   - **a.** Draft **all** lesson skeletons at once (big chunk — don't interrupt the user per-lesson).
     Draft them **as a domain mentor** too — not by parroting sources; same critical,
     current-industry judgment as the syllabus.
   - **b. Agent review loop** — an evaluator agent checks every skeleton: *(1)* does it match its
     lesson's topic? *(2)* is it clear, good quality, simple language? — then refines.
     Author ↔ critique ↔ refine until all pass, **capped at 3 rounds**; what's still unresolved
     goes to the user with the open delta.
   - **c. User reviews** the batch (scans as deeply as he likes); repeat if he wants changes.
4. **Lesson loop** — the **same author ↔ critique ↔ refine** inner loop as skeletons, on **full
   lessons**, graded against the **rubric** (same 3-round cap). Correctness is the **automated**
   gate; the user may add *learnability* feedback ("too fast," "confusing example") — but
   **correctness ≠ user**. No mandatory deep user review here.
   - **Execution: parallel author–critic pairs.** Each lesson gets its own **fresh-context author
     subagent** (inputs: brief + syllabus + its skeleton + relevant `SOURCES.md` entries + the
     insights digest) and a **separate author-blind evaluator subagent** (never sees the author's
     reasoning). The orchestrating session mediates each pair's loop and keeps **two pairs in
     flight** at a time (a fan-out/fan-in worker pool), updating `BUILD_PROGRESS.md` after every
     lesson.
   - **Citations are mandatory.** Claims carry `[Sn]` keys resolving to `SOURCES.md`; the
     evaluator spot-checks **traceability** (claim maps to a real source). It verifies tracing,
     not truth.
   - **Fake-student check — once per course, lightweight.** When the **first two lessons** pass
     the rubric, a fresh subagent gets *only* the brief's audience + assumed prior knowledge and
     those two lessons; it reads them and attempts the exercise. Its confusion points (undefined
     terms, too-fast steps) are fixed there **and folded into the drafting guidance for every
     remaining lesson**. One run — it calibrates the explanation format, not each lesson.
   - **Stuck lessons don't loop forever.** After the capped rounds, show the user the current best
     version + its scorecard; they accept it or give comments for one more pass.
5. **Deliver** — the course content + its specialized `.claude` residue + a **`COURSE_REPORT.md`**:
   the final graded scorecard the `course-evaluator` emits (rubric scores, wins, cleanups, verdict),
   like `System_Design_SelfLearn`'s `updated_course_report.md`. Generated by the `/course-report`
   command inherited from the template. It **certifies** the course to the user — distinct from
   `FEEDBACK.md`, which feeds improvement back into the factory's `insights/`.

**Two moments we ask the user:** *upfront intake* (knowable ambiguities, before research) and
*post-research* (only if sources diverge). Front-load what's knowable; defer what research reveals.

> **Why the loop is non-negotiable:** "spec → whole course in one shot" manufactures exactly what
> our `course-evaluator` catches — *fabricated capacity numbers* and *cargo-cult claims*. Keep the
> gates. That's the line between a course factory and a slop factory.

## What will live here (proposed structure)

| Path | Purpose |
| :--- | :--- |
| `.claude/` | The **factory's own** environment — pipeline commands + build agents (scaffold, draft, grade). Runs when *we* build a course. |
| `course-template/` | The **frozen** output-course skeleton: folder layout for phases/lessons **+ its generic `.claude/`**. Copied, never mutated. **Tiered:** mandatory core (syllabus, lesson arc, rubric, `/improve-course`, `/new-lesson`) + optional modules (katas, diagrams, Socratic, pattern-catalog). |
| `courses/` | **Staging area where generated courses land** — one subfolder per course (`courses/<name>/`), each holding the content + `COURSE_BRIEF.md` + `SOURCES.md` + `BUILD_PROGRESS.md` (pipeline state) + a **`FEEDBACK.md`** (empty template; gathers critiques / things-to-fix for *that* course) + a **`COURSE_REPORT.md`** (the final graded scorecard from `course-evaluator`) + its `.claude` residue. After delivery the user moves the course out to its own home. |
| `templates/` | The **course-spec template** (`COURSE_SPEC.template.md`, what the user fills in — initial draft exists) + syllabus/lesson templates. |
| `insights/` | Distilled **lessons learned** across courses — anti-fabrication, the running-example backbone, kata design, estimation method. **Write rule** (two ways): *user-triggered capture* (when an insight surfaces, the user explicitly tells an agent to log it here) + a *`setup-retro`-style harvest* that **pumps each course's `FEEDBACK.md` up into here** after each course/phase. **Read rule:** intake (step 0), syllabus compose (2b), and skeleton/lesson drafting all load this digest. Knowledge, not tooling. |
| `comparison/` | Analyze well-made GitHub courses vs ours. Produces **(a)** proposed revisions to the **one** template rubric (it never keeps a rival rubric) and **(b)** a **per-course report** feeding the `/improve-course` backlog. |

## The spec (the input that decides everything)

`COURSE_SPEC.md` — the file the user feeds in. Its quality caps the course's quality, so it must
capture at least:

- **Topic** and **scope** (what's in / explicitly out)
- **Audience** + assumed prior knowledge
- **Depth & size** — phases, approximate lesson count / hours
- **Running example / project backbone** — every good course of ours has one
  (System Design used *HomeOS-Cloud*). Required.
- **Optional modules** to enable — katas? diagrams? Socratic teaching?
- **Source material / references** to ground against (anti-fabrication anchor)

The template lives at `templates/COURSE_SPEC.template.md` (initial draft exists). From it the
factory generates the per-course `COURSE_BRIEF.md` overlay.

## Relationship to `meta-env-setup/`

**Decoupled at runtime.** `meta-env-setup/` builds a `.claude` *from nothing* for an
*arbitrary* repo (transcript mining, scaffolding, effectiveness scoring). course-factory doesn't
need that at course-generation time — it already carries a crystallized `course-template/.claude`
and only *overlays* it.

Keep meta-env-setup as **lineage / evolution tooling only**: use its `validate_claude_setup.py
--score` and friends when we want to **improve the template itself**, never to generate an
individual course.

## Design principles

- **Clarify early, research before drafting** — settle knowable ambiguities upfront; ground the
  syllabus in real, critically-filtered courses before composing it.
- **Weigh reliability, not popularity alone** — high stars are a strong green flag, not *proof* of
  correctness; still judge each source on reliability.
- **Mentor, not aggregator** — the factory brings real domain judgment; sources inform but never
  dictate. Guard against sparse, stale, or industry-irrelevant sources with common sense and a
  mentor's view of what matters *now*.
- **Big chunks, then batch-review** — generate the whole batch (all skeletons, full lessons)
  before evaluating, so we don't interrupt the user constantly; an automated
  *author → critique → refine* loop runs first, the user gate (if any) comes after.
- **Specialize by overlay, not mutation** — topic specifics live in a generated brief + module
  selection; the template `.claude` internals stay frozen so central improvements flow to every
  course.
- **Match the reviewer to competence** — user judges structure/scope; automated eval judges
  correctness of material the user is still learning.
- **One rubric, two layers** — a **generic core** (correctness, grounding, flow, coverage,
  practicality) plus **topic add-ons** the spec can request (e.g. SD's fabricated-capacity-numbers
  check). `comparison/` proposes revisions to it; nothing else defines quality.
- **Resumable by design** — `BUILD_PROGRESS.md` tracks the phase + per-lesson status; any session
  can pick up mid-course.
- **Feedback compounds** — every course carries a `FEEDBACK.md`; harvest it up into `insights/`
  so the factory gets better with each course it builds.
- **Quality loop is mandatory** — no one-shot course generation.
- **Anti-fabrication first** — ground every claim in the spec's source material; no invented
  numbers.
- **One running example per course** — a concrete backbone the whole course threads through.
- **Tiered templates** — small mandatory core, opt-in modules; don't force system-design shape
  onto a math or history course.

## Build roadmap

1. **Distill `course-template/`** from `System_Design_SelfLearn/.claude` — extract the
   topic-neutral core (syllabus, lesson arc, rubric, `/improve-course`) into the frozen template;
   demote SD-specific pieces (`design-pattern-catalog`, `architecture-diagrams`, katas) to
   **optional modules**. *This is task #1 — the template does not exist yet.*
2. **Stand up the factory's own `.claude/`** — the pipeline commands + build agents that run the
   phased loop.
3. **Finish the course-spec template** (`templates/COURSE_SPEC.template.md` — initial draft exists).
4. **Build `comparison/`** — define the benchmark rubric, then run the first analysis against a
   real GitHub course.
5. **Prove out shallow research** — `gh` + web search + shallow Udemy / Coursera / edX name-search
   (verify their syllabi are readable without registering). Dedicated fetch tools only if real
   runs show repeated cost.
6. **Wire the pipeline** — a thin driver: spec → overlay → syllabus loop → skeleton loop → lesson
   loop → deliver.

## Reference: the course we're generalizing from

`/home/barak/System_Design_SelfLearn/` — the first hand-built course (content in
`System_Design_v1/`) and the source of both the template `.claude` and the `insights/` corpus.
Its `.claude` lives at the **repo root**, not inside `System_Design_v1/`, and already has the
agents, commands, and skills (course-evaluator, curriculum-architect, socratic-mentor,
`/improve-course`, `/new-sd-lesson`, quality rubric) that we will harvest and generalize.

---

## Open decisions

*All settled for now.* Design decisions made during this pass are captured above — after real
runs, calibrate: **research depth** (convergence + budget cap), **parallel width** (2
author–critic pairs), the **refine cap** (3 rounds), and the **fake-student scope** (first 2
lessons only).
