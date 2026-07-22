# Pedagogy digest — all 8 techniques on one screen

**Derived file. `catalog/*.md` is canonical.** This is a condensed view for pipeline consumption,
regenerated from the catalog — **never hand-edited**. If this and a `catalog/` entry disagree, the
catalog wins and this file is stale.

**What was kept:** each technique's definition, its qualified evidence tier, when to use it, and its
**boundary conditions verbatim** — the part that stops a technique being applied wrongly.
**What was dropped:** worked examples, citation prose, full `Applying to <shape>` sections. Open the
catalog entry when you need one. `[Pn]` keys resolve to [`SOURCES.md`](SOURCES.md).

**Why one file:** a single lesson normally composes **3–4** of these at once — they map onto
different moves of the lesson arc, not onto competing choices. Reading them separately also hides
the couplings in [§ How they interact](#how-they-interact), which is where most misuse comes from.

---

## 1. Retrieval practice · `catalog/retrieval-practice.md`

**Is** — low-stakes prompts that make the learner *pull* knowledge from memory instead of re-reading it.
**Tier** — **High.** 217-study meta-analysis: practice testing beats restudy across lab and classroom, including transfer `[P1][P2][P3]`. Overt (written/spoken) retrieval beats covert `[P4]`.
**Use when** — factual/conceptual material with judgeable answers · ≥1 day between study and final test · mixed recall + recognition formats.
**Fails when**
- **No feedback on hard items** — repeated failure without correction reinforces errors and discourages `[P1][P4]`.
- **High stakes** — graded or competitive testing raises anxiety and shifts attention to performance `[P1][P2]`.
- **Left optional** — restudy *feels* easier, so learners under-use it; the course must schedule retrieval, not offer it `[P2][P3]`.

**Code-heavy:** recall becomes *production* — "write the signature from memory", "predict this output". Running the code supplies the required feedback.

## 2. Worked examples · `catalog/worked-examples.md`

**Is** — fully solved problems with step-by-step rationale, studied before independent practice.
**Tier** — **High.** The worked-example effect: novices learn more from studying examples than from unguided problem solving `[P5][P6][P7][P8]`.
**Use when** — novice/intermediate meeting a new complex procedure · high element-interactivity material · segmented, key steps highlighted, followed by a few forced-processing problems.
**Fails when**
- **Expertise reversal** — as skill grows, detailed examples become redundant, add load, and *hinder* problem solving. Fade them `[P6][P7][P19]`.
- **Passive skimming** — without self-explanation prompts or a move to independent practice, learners copy surface steps and don't transfer `[P7]`.
- **Bad examples backfire** — steps without the *why*, or irrelevant detail mixed in, erase the effect `[P7][P10]`.

**Narrative/history:** the "problem" is interpretive — an annotated model analysis (claim → evidence → counter-evidence → conclusion), then a partially completed parallel case. Fading logic identical.

## 3. Spaced repetition · `catalog/spaced-repetition.md`

**Is** — the same material revisited across gaps rather than massed into one session.
**Tier** — **High.** 317-experiment meta-analysis; optimal gap depends on the target retention interval, and the gap effect is non-monotonic `[P12][P13][P14][P15]`.
**Use when** — durable retention over weeks/months is the goal · paired with *retrieval* at each review (spaced testing ≫ spaced re-reading) · declarative and procedural alike.
**Fails when**
- **Too-short gaps** approximate massing and shrink the benefit; **too-long gaps** cause full forgetting and costly relearning `[P12]`.
- **Passive reviews** — spacing helps re-reading far less than it helps retrieval `[P12][P15]`.
- **Opaque schedules** — a spacing plan the learner can't understand or trust loses adherence `[P12]`.

**Code-heavy:** rarely flashcards — **structured reuse**. Later lessons deliberately re-invoke earlier constructs. *The syllabus is the spacing schedule; plan the reuse chain when composing it.*

## 4. Interleaving · `catalog/interleaving.md`

**Is** — mixing problem types within a practice session so the learner must first decide *which* applies.
**Tier** — **High for inductive/discriminative learning; medium overall; ambiguous for expository text.** 59-study meta-analysis, g ≈ 0.42; strongest for visual material, smaller-but-positive in math, **nonsignificant-to-negative for expository text** `[P16][P17][P14]`.
**Use when** — learners must discriminate between confusable strategies or categories · optimizing delayed retention and transfer · *after* baseline familiarity with each type individually.
**Fails when**
- **Feels worse than it is** — practice performance drops; unwarned learners read the mix as confusing. Tell them why it's mixed `[P14]`.
- **No discrimination demand, no benefit** — word lists and expository text show no advantage, sometimes worse than blocking `[P16]`.
- **Novice overload** — heavy interleaving of complex topics before schemas exist interacts badly with cognitive load `[P17][P6]`.

**Narrative/history:** mostly **don't**. Interleave only where a real discrimination target exists; otherwise keep it blocked and get durability from spacing + retrieval.

## 5. Scaffolding / cognitive-load management · `catalog/scaffolding-cognitive-load.md`

**Is** — structuring tasks and explanations to control working-memory load, with **fading** of support as expertise grows.
**Tier** — **High.** Decades of Cognitive Load Theory experiments; the minimal-guidance critique reaches the same conclusion from the failure side `[P19][P6][P20][P21]`.
**Use when** — introductory or high-complexity material where learners lack schemas · **always paired with fading**: high guidance → completion problems → open problem solving · multimedia design choices count as load management.
**Fails when**
- **Over-scaffolding** — support outliving its need creates dependency, removes productive struggle, triggers expertise reversal `[P19][P7]`.
- **Load mismanagement** — redundant parallel explanations, or a diagram split from the text explaining it, *add* extraneous load `[P26][P27]`.
- **The opposite failure** — minimal-guidance/pure discovery for novices overloads memory and breeds misconceptions `[P21]`.

## 6. Dual coding · `catalog/dual-coding.md`

**Is** — meaningfully aligned visual + verbal representations, so the learner builds linked codes.
**Tier** — **High for well-designed combinations — gains vanish when multimedia design principles are violated.** `[P22][P23][P24][P25][P28]`
**Use when** — visuals are directly relevant (never decorative) and aligned in time and space with the words · complex spatial, causal, or procedural content · strongest for **lower prior knowledge** · signal key parts, strip extraneous detail.
**Fails when**
- **Redundancy effect** — on-screen text + identical narration + a busy diagram *impairs* learning `[P26][P27]`.
- **Decorative images distract**, especially low-prior-knowledge learners `[P24][P25]`.
- **Split attention** — explanation far (in space or time) from the diagram it explains erases the benefit `[P25][P26]`.

**Narrative/history:** the payoff visuals are **timelines, maps, causal chains** — structures prose hides. Portraits and scene art are decoration unless the lesson's claim is *about* them.

## 7. Formative assessment · `catalog/formative-assessment.md`

**Is** — low-stakes checks *during* learning whose results change what happens next. The defining feature is the closed loop.
**Tier** — **Medium-to-high, with methodological caveats.** K-12 meta-analyses g ≈ 0.16–0.31 after publication-bias adjustment; classic syntheses rank feedback among the largest influences, but reviewers flag low-certainty primary evidence `[P30][P31][P32][P33][P34]`.
**Use when** — feedback is timely, specific, and about *how to improve* · the system actually acts on the data (reteach, adjust difficulty, regenerate practice) · learner self-assessment and goal setting amplify it.
**Fails when**
- **Summative creep** — heavily graded or ranking-oriented "formative" checks lose the benefit and can harm motivation; vague praise does nothing `[P30][P33]`.
- **Non-diagnostic items** — questions that don't isolate a specific misunderstanding produce no actionable signal. "More quizzes" is not the mechanism `[P32]`.
- **Overclaiming** — the evidence base has known quality problems; treat headline effect sizes as directional `[P32]`.

## 8. Socratic / guided-discovery questioning · `catalog/socratic-guided-discovery.md`

**Is** — structured, sequenced questions leading the learner to construct understanding. **Guided only.**
**Tier** — **Medium, with important caveats — the weakest-evidenced technique here.** One supporting quasi-experimental study `[P29]`; against it, the cognitive-load literature finds minimally guided approaches less effective for novices `[P21]`. Net: works when questions are highly structured and load is managed; **never as unguided discovery**.
**Use when** — intermediate learners with some prior knowledge · higher-order goals (critical thinking, argumentation) · discussion-shaped material · always with clear objectives and occasional direct explanation.
**Fails when**
- **The macro-stance trap** — adopting "discovery" as a course-wide stance for novices overloads memory and entrenches misconceptions. Questioning is a technique *inside* well-guided instruction, not a replacement for it `[P21]`.
- **Poor sequencing stalls** — questions assuming knowledge the learner lacks derail the dialogue `[P21][P29]`.
- **No synthesis, no takeaway** — questioning without a closing summary leaves fragmented understanding `[P21]`.

**Code-heavy:** maps onto debugging and code reading — "what do you expect this line to return?" The program's behavior is the corrective feedback, keeping the dialogue anchored to ground truth.

---

## How they interact

Reading these as eight independent options is the commonest way to misuse them. The couplings:

- **Retrieval needs formative feedback.** Retrieval *backfires* on hard items without correction (#1) — so a retrieval schedule without a feedback path (#7) is actively harmful, not merely weak.
- **Spacing is a retrieval schedule, not a re-reading schedule.** Spaced *testing* ≫ spaced review (#3 + #1). Spacing alone leaves most of the effect on the table.
- **Worked examples and scaffolding are one mechanism.** Both live or die on **fading** (#2 + #5). Failing to fade produces expertise reversal from either direction.
- **Interleaving fights cognitive load early.** It needs baseline schemas first (#4 + #5) — interleave *after* the scaffold has faded, not during.
- **Dual coding is a load decision, not a decoration decision.** Its failure modes (redundancy, split attention) are load failures (#6 + #5).
- **Socratic questioning presupposes scaffolding.** Unguided, it *is* the minimal-guidance failure mode (#8 + #5).

Practical consequence: **#5 (load/scaffolding) is a precondition for #2, #4, #6, #8**, and **#7 (feedback) is a precondition for #1 and #3.** Choose those two first.

## Myths — never justify a design choice with these

Full entries, with popular-source *and* debunking citations, in [`MYTHS.md`](MYTHS.md). **Normative
rule:** specs 002/003 MUST NOT cite any of these — or a low-tier entry — as justification.

| Myth | Status | Use instead |
| :--- | :--- | :--- |
| **Learning styles** (VAK/VARK, style-matched instruction) | No adequate evidence for the meshing hypothesis `[P35][P36]` | General principles for everyone; multiple representations because the *material* benefits — not because learners carry style labels |
| **"Brain-based" neuromyths** (left/right-brain, Brain Gym) | Prevalent among teachers, scientifically unsupported `[P37]` | Spacing, retrieval, feedback |
| **Growth mindset as a big lever** | Over*claimed* — meta-analytic effects trivial-to-small; meaningful only in some at-risk subgroups `[P38]` | Structural improvements (practice, feedback, scaffolding); mindset messaging at most a modest adjunct |
| **Grit as a uniquely powerful predictor** | Over*claimed* — r ≈ .18, largely redundant with conscientiousness `[P39]` | Supportive design + broader self-regulation skills |

Two of these are **overclaims, not fabrications** — the debunked part is "big lever", not "the thing exists". Don't overcorrect into denying them.

## When to open the full catalog entry

This digest is enough to **choose** a technique and avoid its main failure mode. Open
`catalog/<name>.md` when you need the **worked example**, the **full `Applying to <shape>` guidance**,
or the **citation trail** behind a tier — i.e. when authoring the actual material, not when deciding
the approach.
