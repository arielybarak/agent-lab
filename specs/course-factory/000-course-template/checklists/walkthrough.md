# Checklist: 2-topic paper-walkthrough (SC-003 / SC-012)

**Performed**: 2026-07-22, agent-performed (no pipeline — 001 does not exist yet).
**Template under test**: `course-factory/course-template/` at `VERSION` 1.0.0.
**Re-run 2026-07-22** for the six-dimension rubric core (Clarity added to FR-013 after the first pass);
steps 1–3 were unaffected, step 4 was re-graded for both topics.
**Configuration**: **mandatory core only — all four optional modules (diagrams, katas,
pattern-catalog, socratic) DISABLED.** Part B repeats step 4's sizing with the `default` profile.

The question this answers: does the core alone — `backward-design`, `lesson-arc`, `quality-rubric`,
the two review agents, the three commands — produce a viable course shape for two topics of
**different material shape**, with no subject assumption leaking in? Two topics, not one, so the
neutrality claim is not validated against a single easy fit.

---

## Topic 1 — *Introduction to Psychology* (concept / theory-heavy)

Assumed audience: a curious adult with no background in psychology or research methods.

### Step 1 — Outcomes (skill `backward-design`, Stage 1)

Enduring outcomes (the few worth keeping years later):

1. Explain a given behaviour using **more than one** level of analysis (biological, cognitive,
   social) and say what each level does and does not account for.
2. Given a claim about human behaviour, judge **what evidence would be needed** to support it, and
   identify what the cited study actually establishes.
3. Distinguish **correlation from causation** in a real reported finding, and name the design that
   would be needed to make the causal claim.

Supporting outcomes (prerequisites of the above): name the major sub-fields and what each studies ·
read a study description and identify sample, measure, and design · describe two classic findings
and their replication status · define reliability and validity in plain terms.

- ✅ **Sensible?** Yes. Every outcome is an observable learner action ("explain", "judge",
  "distinguish… and name"), not a topic label — exactly what Stage 1 demands.
- ✅ **Levels present.** Mixed recall / apply / analyze; not all-recall, not all-create.
- ✅ **Audience contract written down.** "No background in psychology or research methods" is the
  assumption the lessons must honor.

### Step 2 — Evidence (Stage 2)

| Outcome | Evidence |
| :--- | :--- |
| 1 (multi-level explanation) | Given a short behaviour vignette, write one paragraph per level and one sentence on what that level misses — graded against stated criteria (analyze) |
| 2 (evidence judgment) | Given a popular-press summary of a study, list what the study can and cannot support (analyze) |
| 3 (correlation/causation) | Given a real reported correlation, state the causal claim being smuggled in and the design that would test it (analyze) |
| Supporting | In-lesson retrieval prompts; label sample/measure/design on three study descriptions (recall / apply) |

- ✅ **Every outcome has ≥1 evidence; every assessment traces to an outcome.** No orphans.
- ✅ **Formative-first.** The retrieval and labelling work sits inside lessons; the vignette and
  press-summary tasks are the end-of-unit integration.
- ✅ **No subject assumption from the template.** The evidence table in `backward-design` is
  keyed by *outcome level*, not by subject; recall/apply/analyze mapped cleanly.

### Step 3 — One lesson in the canonical arc (skill `lesson-arc`)

Lesson: **"The correlation that wasn't causation."**

| Arc move | Content |
| :--- | :--- |
| **Framing** | A real headline of the form "people who do X live longer." What would you have to believe for the headline's implied advice to be good advice? |
| **Activation** | Learners have already labelled sample/measure/design on three studies. Recall: which of those three could support an intervention claim? |
| **Demonstration** | Walk one published correlation to its three competing explanations (X→Y, Y→X, Z→both), each made concrete for that finding. Then show the study design that separates them. |
| **Practice + feedback** | Three fresh correlations; for each, name the most plausible third variable and the design that would settle it. Reference answers name the third variable and explain *why it is plausible*, not just what it is. |
| **Integration / transfer** | Return to the course's running example (a single recurring behaviour the whole course keeps re-explaining) and re-examine one earlier claim about it in this light. |

- ✅ **Arc holds with no subject assumption.** Every move filled naturally; the theory-heavy
  emphasis (longer activation and demonstration, comparison-based practice) is exactly the row
  `lesson-arc` gives for concept/theory-heavy material.
- ✅ **Names the one thing it teaches** — the misconception it fixes.
- ✅ **Practice closes the loop** — reference answers exist and explain.
- ✅ **Running example works for a non-technical subject.** A recurring behaviour serves the same
  continuity role a build-artifact would elsewhere. The core's "one running example" rule did not
  need a technical subject to make sense.

### Step 4 — A rubric-checkable draft (skill `quality-rubric`)

Sketch of the lesson draft, checked against the core dimensions:

| Dimension | Can the core rubric actually grade this draft? |
| :--- | :--- |
| Technical Correctness | ✅ The three competing explanations and the named design are either right or wrong for that finding — checkable against the literature |
| Grounding / No-Fabrication | ✅ Bites immediately: the cited study needs a real reference, and any effect size stated needs a source. A plausible-sounding invented statistic is exactly what this dimension catches |
| Pedagogical Flow | ✅ Arc order is inspectable; framing precedes the answer; the taught idea is named |
| Clarity | ✅ Gradeable against the stated audience ("no background in psychology **or research methods**"). Concrete predicted findings: *"confound"*, *"third variable"* and *"design" used in its technical sense* are **undefined terms on first use** for this reader; "the study could not support an intervention claim" is an **unexplained leap** unless the inference is spelled out. Both are citable defects with named causes, not taste |
| Coverage | ✅ Traces to enduring outcome 3 and supporting outcomes; a gap here would be a named gap |
| Practicality | ✅ Three practice items with reference answers; the headline and study must resolve to real sources |

- ✅ **Zero add-ons required.** The core dimensions graded a psychology lesson with nothing enabled.
- ✅ **Clarity routed cleanly.** No defect above belongs to two dimensions: the undefined-term and
  unexplained-leap findings are comprehension defects in correctly-ordered material, so the routing
  table puts them in Clarity, not Pedagogical Flow.
- ✅ **No subject-specific dimension was missed.** (A course wanting, say, an ethics-of-research
  check would declare it as an **add-on** — the slot exists.)

---

## Topic 2 — *Python Programming* (procedural / code-heavy)

Assumed audience: an intelligent adult with **no prior programming background**.

### Step 1 — Outcomes

Enduring outcomes:

1. Given a described task, write a working program that solves it using values, conditions, loops,
   and functions.
2. Read an error message or wrong output, **form a hypothesis about the cause**, and test it — i.e.
   debug rather than guess.
3. Choose an appropriate built-in data structure for a task and justify the choice.

Supporting: run a program and predict its output before running · trace a loop by hand · write and
call a function with parameters and a return value · read a traceback to the offending line · use
a list, dict, and set for their intended purposes.

- ✅ Observable actions throughout; the levels run recall → apply → create, appropriate for a
  procedural subject.
- ✅ Audience contract ("no prior programming") recorded — the load-bearing assumption.

### Step 2 — Evidence

| Outcome | Evidence |
| :--- | :--- |
| 1 (write a working program) | A small specified program that must run and produce stated output (create) |
| 2 (debug) | Broken programs supplied; learner states the hypothesis, the test, and the fix — the *hypothesis* is graded, not only the fix (analyze) |
| 3 (choose a structure) | Three task descriptions; pick a structure per task and justify against an alternative (analyze) |
| Supporting | Predict-then-run prompts in-lesson; hand-trace a loop; a function with a stated contract (recall / apply) |

- ✅ Every outcome covered; every assessment traces back.
- ✅ **The predict-then-run prompt is formative evidence that costs nothing** — precisely the
  "formative first, cheap, repeatable" rule from Stage 2.

### Step 3 — One lesson in the canonical arc

Lesson: **"Why your loop runs one time too many."**

| Arc move | Content |
| :--- | :--- |
| **Framing** | A short program that should print 5 lines and prints 6. Learner predicts the output before seeing it run. |
| **Activation** | Recall the previous lesson's hand-trace routine. What is the loop variable's value on the last pass? |
| **Demonstration** | Trace the loop step by step, in a table, one row per pass — including the pass that should not have happened. Then the same trace on the corrected version. |
| **Practice + feedback** | Four short loops, guidance fading: (1) trace a given loop, answer supplied; (2) predict output, then run; (3) find the off-by-one, hint available; (4) write a loop to a stated spec, reference solution supplied. |
| **Integration / transfer** | Fold the corrected loop into the course's running program (the single artifact the course builds all the way through) and re-run its checks. |

- ✅ **Arc holds.** Same five moves; the emphasis shifts exactly as `lesson-arc`'s
  procedural/skill-heavy row prescribes — heavy demonstration, several short practice cycles inside
  one lesson, guidance fading each cycle.
- ✅ **Guidance fades within the lesson** — visible in the four-item ladder.
- ✅ **The same running-example rule worked** with a very different artifact (a program being
  built up, versus a recurring behaviour). This is the core neutrality result: two topics of
  opposite shape, same core, no strain.
- ✅ **Katas module not needed.** Practice-with-feedback is core; only the *standalone exercise
  layer* is the optional module, and this lesson did not require it.

### Step 4 — A rubric-checkable draft

| Dimension | Can the core rubric grade this draft? |
| :--- | :--- |
| Technical Correctness | ✅ The trace table is either correct or not; the fix either works or not |
| Grounding / No-Fabrication | ✅ Every output claimed must be the output the code actually produces — a stated-but-wrong output is a Grounding finding |
| Pedagogical Flow | ✅ Framing (predict) precedes demonstration; the named idea is the off-by-one |
| Clarity | ✅ **The dimension that bites hardest here**, and the sharpest evidence for adding it. For a reader with *no prior programming*, "iterable", "index", "zero-based", and range-exclusivity are all **undefined terms on first use**; "the loop variable is 5 on the last pass" is an **unexplained leap** if zero-based counting was never made explicit. A lesson can be correct, grounded, and perfectly sequenced and still lose this reader entirely — which is precisely the failure the other five dimensions all score as PASS |
| Coverage | ✅ Traces to supporting outcome "trace a loop by hand" and enduring outcome 2 |
| Practicality | ✅ Four items with answers/hints; the running program must actually run |

- ✅ **Zero add-ons required**; zero modules required.
- ✅ **Clarity earns its place on this topic.** It is the only dimension that fails a draft which is
  otherwise correct, grounded, well-sequenced, complete, and runnable — the exact gap the
  no-prior-programming audience falls into. On the psychology topic it also fired, but less
  sharply, which is the expected spread for a comprehension dimension across material types.

---

## Part B — the `default` profile (SC-012)

Re-sizing both topics with the **`default` profile** selected (theory-first entry, linear spine
with a planned spiral, one advisory checkpoint per unit, medium 3–6-lesson units):

| | *Introduction to Psychology* | *Python Programming* |
| :--- | :--- | :--- |
| **Spine** | Linear by dependency (methods → levels of analysis → sub-fields → integration), spiralling the two enduring ideas (evidence quality; multi-level explanation) once each in later units | Linear by strict dependency (values → conditions → loops → functions → structures), spiralling "debugging as hypothesis testing" into each later unit as the programs grow |
| **Entry point** | Theory-first — good fit; explain the concept, then apply | Theory-first — **acceptable, not ideal.** Each lesson still frames with a concrete failing program before the explanation, which is what keeps it workable |
| **Advisory checkpoints** | End of each unit, self-checkable retrieval + one applied task | End of each unit, "write this small program cold" |
| **Granularity** | Medium units of 4–5 lessons | Medium units of 4–6 lessons |
| **Coherent outline?** | ✅ Yes — this is the profile's declared best fit | ✅ Yes — coherent and teachable |

- ✅ **Both topics yield a coherent outline under `default`.**
- ✅ **No core invariant was redefined or bypassed** to make either work — the profile touched only
  spine, entry point, checkpoint placement, and granularity.
- ✅ **Fallback verified on paper**: neither topic *named* a profile in this walkthrough, and both
  landed on `default` — the one profile with `default: true` in `manifest.yaml`.
- ⚠️ **Recorded limitation, not a failure**: `default`'s theory-first entry is a *weak* fit for the
  procedural topic (already stated in `profiles/default/spine.md` § Best fit / weak fit). It still
  produces a coherent course, which is the SC-012 bar. A problem-first profile would fit better and
  is exactly what the later, independent PBL/CBL increment is for. Nothing is blocked meanwhile.

---

## Result

| Check | Psychology | Python |
| :--- | :--- | :--- |
| 1. Backward-design backbone yields sensible outcomes | ✅ | ✅ |
| 2. Backbone produces coherent evidence for those outcomes | ✅ | ✅ |
| 3. Canonical arc instantiates without a subject assumption | ✅ | ✅ |
| 4. Draft is gradeable by the core rubric (all 6 dimensions, incl. Clarity) | ✅ | ✅ |
| 5. Achieved with **0** optional modules enabled | ✅ | ✅ |
| 6. `default` profile yields a coherent outline (SC-012) | ✅ | ✅ |

**SC-003 satisfied** — the mandatory core alone produced a viable course shape for two topics of
different material shape, with zero optional modules required.
**SC-012 satisfied at MVP** — the one shipped profile (`default`) produces a coherent structure for
both, and a course naming no profile falls back to it.

**Note on standing.** This is the **pre-pipeline proxy** the spec authorizes (FR/SC-003, research
D7), not a permanent substitute. Once spec 001 exists, re-verify by actually driving the pipeline.
Maintainer review of this checklist is optional by design — there is no human-approval gate here.
