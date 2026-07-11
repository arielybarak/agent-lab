<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Research the LANDSCAPE OF STRUCTURES for self-learning courses — how courses and

curricula are architected — across different subject types. I'm mapping the design
space to choose an approach later, NOT building anything yet.

Cover, with evidence and citations:

1. Macro-structures / course architectures. Survey the main ones and when each
fits: linear/sequential, spiral, modular (mix-and-match units), project- or
problem-based (PBL), case-based, mastery/competency-based, Socratic/inquiry,
problem-first. Give strengths, weaknesses, and best-fit subject for each.
2. How structure should change by MATERIAL TYPE: concept/theory-heavy,
procedural/code-heavy, quantitative/math, narrative/history, and
language or skill-drill. What structural choices differ per type?
3. Lesson-level arcs. The common internal structures of a SINGLE lesson, and
how they vary by material type.
4. Invariants vs variables: which structural elements are (near-)universal
across all course types, and which must swap by subject?
5. KEY QUESTION: are these differences best handled as configurations/variants
of ONE common structure, or do some subject types need FUNDAMENTALLY
different architectures? What does the evidence actually say?

Prefer established instructional-design sources (backward design / Understanding
by Design, Merrill's First Principles, Bloom's taxonomy, ADDIE, Gagné's Nine
Events, competency-based education, PBL research) over blog opinion. Flag where
evidence is weak or contested. Output as structured Markdown with a "Sources"
section (author/framework + link) at the end.

Question 5 is the payload — it's what tells us single-core-with-profiles vs multi-template.

Evidence across instructional‑design frameworks and meta‑analyses suggests that effective courses share a small set of structural principles (backward design, problem‑centered tasks, activation, demonstration, application, feedback), while macro‑architectures (linear, spiral, project‑based, competency‑based, etc.) function mostly as configurable variants rather than fundamentally different species—though some models (PBL, CBE, mastery learning) impose stronger structural constraints that your course engine would need to treat as distinct profiles.[^1][^2][^3][^4]

***

## 1. Macro course architectures

### Overview table

| Architecture | Core idea | Strengths | Weaknesses | Best‑fit subjects / contexts |
| :-- | :-- | :-- | :-- | :-- |
| Linear / sequential | Content arranged in a fixed sequence of units or lessons, often building from basics to advanced topics. | Simple, predictable; easy to implement and navigate; aligns with many textbook structures. [^3] | Can be rigid; weak at differentiation and revisiting misconceptions; can assume uniform learner pace. [^5] | Introductory concept‑heavy courses (e.g., “Intro to ML”), compliance training, foundational math where prerequisites are strict. |
| Spiral | Key ideas revisited multiple times with increasing complexity and different representations. [^6] | Supports cumulative understanding; good for long‑term retention; aligns with developmental progression. [^6] | Harder to design; may feel repetitive if not carefully scaffolded; assessment alignment can be tricky. [^6] | Concept‑heavy domains (physics, biology, algorithms), K‑12 curricula, subjects with strong vertical structure. |
| Modular / mix‑and‑match | Course built from relatively self‑contained modules that can be reordered or selected based on learner needs. [^3] | Flexible; supports personalization and micro‑learning; easy to reuse content across programs. [^7] | Risk of fragmentation; knowledge dependencies may be obscured; requires strong metadata about prerequisites and competencies. [^5][^7] | Professional development, skills “stacks” (e.g., specific ML techniques), corporate training, language micro‑skills. |
| Project‑based learning (PjBL) | Long(er) projects as the organizing spine; knowledge taught in service of completing an authentic product. [^8][^9] | Large positive effects on academic achievement in higher education (meta‑analytic g often > 0.6–1.0); strong engagement and transfer. [^8][^9] | Design‑intensive; uneven coverage of foundational knowledge if projects are poorly scoped; assessment can be complex. [^8][^9] | STEM and design fields, engineering, data science, entrepreneurship; best when authentic tasks and technology support are feasible. [^8][^9] |
| Problem‑based learning (PBL, in the medical‑education sense) | Ill‑structured problems first; learners identify what they need to learn, then acquire knowledge and apply it in cycles. [^10][^11] | Robust positive effect on skills (clinical reasoning, problem solving); high student satisfaction; good for retention of applied knowledge. [^10][^11] | Mixed/negative short‑term effects on factual knowledge, especially early in curricula; requires careful tutoring and scaffolding. [^10] | Medicine, health professions, advanced STEM where professional reasoning and self‑directed learning are central. [^10][^11] |
| Case‑based learning (CBL) | Realistic cases (often narratives) provide context and sequence; instruction unfolds by analyzing cases. [^12][^13] | Engages learners; supports integration of theory with practice; strong effects on clinical skills when combined with PBL. [^14] | Evidence base is moderate and sometimes methodologically weak; case design quality is critical. [^12][^13] | Clinical education, law, business, ethics, history (using historical cases). [^12][^14][^13] |
| Mastery‑based | Learners progress only after demonstrating mastery of each unit; includes frequent formative assessments and corrective instruction. [^15] | Large positive effects on achievement in K‑12; reduces failure rates; supports equity by allowing different time‑on‑task. [^15] | Requires robust item banks, feedback and remediation; time‑flexibility can conflict with institutional schedules. [^15][^4] | Foundational math and literacy, skills where minimum proficiency is non‑negotiable (e.g., medication safety). [^15] |
| Competency‑based (CBE) | Curriculum organized around explicit competencies; time is variable, outcomes fixed; assessment of performance is central. [^16][^4] | Strong alignment with workforce needs; frameworks and meta‑analyses show improved performance when competency frameworks guide learning. [^7][^17][^18] | Conceptual debates about definitions; implementation is complex; requires good performance assessment and faculty development. [^4][^7][^19] | Health professions, pharmacy, other regulated professions; also used in vocational and corporate training. [^7][^19][^17] |
| Socratic / inquiry‑based | Learning driven by questions, dialogue, and investigation rather than direct exposition. [^20][^21] | Can improve higher‑order thinking, critical reading, and creativity in language‑rich subjects. [^20] | Minimal guidance versions often underperform guided instruction for novices; risk of misconceptions and cognitive overload. [^21] | Philosophy, literature, ethics, advanced seminars; works best with structured guidance and prior knowledge. [^20][^21] |
| Problem‑first / problem‑centered (Merrill) | Instruction organized around authentic tasks/problems from the outset; theory introduced as needed. [^1][^22][^23] | Merrill’s synthesis argues problem‑centered design is a common feature of highly effective instruction across domains; promotes transfer and engagement. [^1][^22][^23] | If problems are too complex or poorly scaffolded, learners flounder; needs tight alignment with activation, demonstration, practice. [^24] | Broadly applicable; especially strong fit for applied STEM, programming, and professional skills. [^1][^23] |


***

## 2. How structure should change by material type

### Concept / theory‑heavy

- Concepts benefit from spiral or modular architectures that revisit big ideas in different contexts and representations over time.[^2][^6]
- Backward design (UbD) recommends organizing theory courses around “big ideas” and essential questions, then aligning assessments and learning activities—a structure that is domain‑agnostic but particularly suited to concept‑heavy subjects.[^5][^2]
- Supportive micro‑structures include concept mapping, contrasting examples, and retrieval + spacing rather than pure project‑driven sequences.[^25][^26]


### Procedural / code‑heavy

- CLT and worked‑example research suggest sequences that start with explicit demonstration and worked examples, then fade to guided and independent practice (often in linear or modular units).[^27][^28][^29]
- Problem‑centered or project‑based macro‑structures are effective when tasks are authentic (e.g., building an app), but procedural correctness still demands clear progression and mastery checkpoints.[^8][^1]
- For self‑learning code courses, chunking procedures into small, testable units with mastery gates (unit tests, coding challenges) aligns well with mastery and competency‑based logic.[^7][^15]


### Quantitative / math‑heavy

- Math learning benefits from structured progressions of problems (linear or spiral), with mastery learning showing strong gains in achievement and reductions in failure.[^15][^29]
- Interleaving of problem types within practice appears beneficial for long‑term retention and discrimination once basics are known, so practice architecture may differ from teaching architecture (e.g., linear teaching, interleaved practice blocks).[^30][^31]
- PBL in quantitative fields works best for higher‑level applications once foundational procedural fluency is in place; early courses often still rely on sequenced units.[^11][^10]


### Narrative / history / case‑rich

- Narrative and history courses naturally lend themselves to case‑based and inquiry‑oriented structures, organizing lessons around events, primary sources, or decisions.[^12][^13]
- UbD suggests framing units around enduring understandings and essential questions (e.g., “What causes revolutions?”) and using cases as evidence to be weighed, which is empirically linked to deeper conceptual understanding.[^2][^5]
- Spiral revisiting of themes (e.g., democracy, empire) across periods supports transfer better than purely chronological “linear” structures.[^6]


### Language learning / skill‑drill

- Language learning and other skill‑drill domains rely heavily on spaced practice, retrieval, and procedural automatization; structures tend to be modular with repeated cycles of exposure and practice.[^26][^25]
- Competency‑based frameworks in health and pharmacy education show that organizing communication and practical skills as competencies with performance‑based assessment can improve practitioner performance.[^17][^7]
- Project‑ or task‑based sequences (e.g., planning a trip in the target language) can be layered on top of drill‑heavy modules, but drills remain fundamental micro‑components.[^23][^1]

***

## 3. Lesson‑level arcs

Across models, lesson‑level structure is surprisingly consistent, as reflected in Merrill’s First Principles, UbD, and similar frameworks.[^1][^23][^2]

### Common patterns (aligned with Merrill / UbD)

A “canonical” lesson arc that shows up in both theory and empirical syntheses:

1. **Problem / goal framing.** Present a real or realistic problem/task or essential question that the lesson will help learners handle (problem‑centered).[^22][^23][^1]
2. **Activation.** Connect to prior knowledge, experiences, or prerequisite skills; preview what will be learned.[^24][^1]
3. **Demonstration / explanation.** Show the concept or procedure via worked examples, models, cases, or multimedia demonstration, aligned with the type of content.[^24][^23][^27]
4. **Application / practice.** Have learners apply the new knowledge in problems, tasks, or discussions with guidance and feedback.[^1][^24]
5. **Integration / reflection.** Ask learners to reflect, generalize, or transfer the learning to new contexts; often via short projects, explanations, or self‑assessment.[^2][^24][^1]

Gagné’s “Nine Events” (gain attention, inform objectives, recall prior learning, present content, provide guidance, elicit performance, provide feedback, assess performance, enhance retention and transfer) largely overlaps with this arc and is widely used, though the empirical evidence is mostly indirect (via alignment with other validated principles rather than head‑to‑head trials).[^22][^23]

### Variations by material type

- **Concept/theory‑heavy:** More time in activation and demonstration; application may emphasize conceptual questions, comparisons, and retrieval rather than complex performance tasks.[^24][^2]
- **Procedural/code‑heavy:** Heavier emphasis on demonstration and guided practice (worked examples, live coding), with multiple short application cycles within a single lesson.[^29][^27][^24]
- **Quantitative:** Structured progression from example to near‑transfer problems to far‑transfer problems; interleaving may occur at the practice stage.[^31][^29][^30]
- **Narrative/history:** Greater emphasis on problem framing and integration—e.g., “How does this case change our understanding of X?”—with practice in argumentation and source analysis rather than stepwise procedures.[^12][^2]
- **Language/skill‑drill:** Shorter, more frequent activation/demonstration cycles (e.g., micro‑dialogues), with large volumes of application (drills, communicative tasks) and cumulative integration over time; pacing is often faster but built on spaced repetition.[^7][^25][^26]

***

## 4. Invariants vs variables

### Invariants (near‑universal structural elements)

Evidence and cross‑model syntheses suggest several invariants:

- **Outcome alignment.** Backward design (UbD) and competency‑based education both insist that clear goals/competencies, aligned assessments, and aligned learning activities are necessary in any effective course architecture.[^4][^5][^7][^2]
- **Problem/task orientation.** Merrill’s review argues that instruction is most effective when centered on tasks learners will actually perform, regardless of domain (problem‑centered).[^23][^22][^1]
- **Activation of prior knowledge.** Both Merrill and Gagné emphasize connecting new material to what learners already know as a general principle.[^1][^24]
- **Demonstration + application.** Learners need to see models (examples, cases) and then practice with feedback; this holds for theory, procedures, skills, and competencies.[^17][^27][^24][^1]
- **Feedback and formative assessment.** Across mastery learning, formative assessment meta‑analyses, and competency frameworks, diagnostic feedback loops are consistently associated with better performance.[^32][^33][^15][^17]
- **Integration/transfer.** Opportunities to apply learning in new contexts (projects, cases, reflective tasks) are common across PBL, CBL, CBE, and UbD.[^11][^4][^12][^2]

These invariants strongly support the idea of a **single core instructional architecture** at the lesson level, and a shared backbone (goals → evidence → learning experiences) at the course level.[^3][^2][^1]

### Variables (elements that swap by subject or model)

Key dimensions that vary meaningfully:

- **Macro organizing spine.**
    - Theory courses: concept sequences or spirals.[^6][^2]
    - Professional programs: competencies and authentic tasks (CBE, PBL, CBL).[^10][^16][^12][^7]
- **Entry point.**
    - Theory‑first: exposition then problems (traditional linear).[^5]
    - Problem‑first: authentic tasks or cases first, then just‑in‑time theory (PBL, problem‑centered).[^10][^12][^1]
- **Pacing logic.**
    - Time‑based cohorts: fixed schedules and modules (typical HE and corporate).[^3]
    - Mastery/CBE: variable time, fixed outcomes; progress gated by demonstrated competence.[^4][^15][^7]
- **Granularity of units.**
    - Fine‑grained units (micro‑lessons, drills) in language and procedural domains.[^26][^7]
    - Coarser units (cases, projects) in PBL/CBL, CBE.[^12][^10][^4]
- **Social structure.**
    - Individual self‑paced sequences (MOOCs, online self‑learning).[^3]
    - Small‑group problem/case discussions in PBL/CBL.[^13][^10][^12]

These variables are where you’d likely define “profiles” or templates in a course‑generation tool.

***

## 5. Single core vs multiple templates (payload)

### What the evidence and frameworks suggest

1. **Strong convergence at the principle and lesson‑arc level.**
    - Merrill’s First Principles were derived by examining many instructional models (including PBL, CBL, traditional direct instruction) and extracting common elements that appear in successful instruction.[^22][^23][^1]
    - UbD, though originally developed for K‑12, is explicitly framed as cross‑subject and cross‑level: design backward from desired understandings/competencies, then align assessments and learning experiences; this logic is used in concept‑heavy, skills‑heavy, and case‑based settings.[^34][^5][^2]
    - ADDIE and similar ISD frameworks provide a general process (Analysis, Design, Development, Implementation, Evaluation) used in corporate, higher‑ed, and online environments, suggesting that the **design process** itself is domain‑agnostic even when specific architectures differ.[^35][^36][^3]

Taken together, this supports a **single meta‑architecture** built around: outcomes/competencies; problem/task framing; activation; demonstration; practice; feedback; integration—configurable for domain specifics.[^23][^2][^1]
2. **Macro‑architectures act as overlays or instantiations, not entirely separate species.**
    - PBL: meta‑analyses show strong positive effects on skills and satisfaction, but PBL courses still rely on clear outcomes, cases/projects as problems, activation, demonstration, practice, and assessment—just with the problem sequence as the main organizing spine.[^11][^10]
    - CBL: scoping and meta‑analytic reviews propose case design frameworks that specify components such as content, structure, process, and outcomes—again nested within an overarching competency‑based logic in medical education.[^14][^13][^12]
    - CBE: systematic reviews in medicine and pharmacy describe competency frameworks as overlays on curricula that reorient goals and assessments but do not eliminate the need for units, lessons, demonstrations, practice, and feedback.[^16][^19][^18][^37][^4][^7][^17]
    - Mastery learning: Bloom and Guskey’s work treats mastery as a pattern of diagnostic assessment and corrective instruction applied to conventional units, not a wholly different lesson structure.[^15]

These models thus look like **profiles** of the same underlying architecture with different parameter settings (e.g., problem‑first vs theory‑first, time‑flexible vs time‑fixed, competency‑framed outcomes vs content‑framed outcomes).
3. **Where differences may be structurally consequential.**
The literature does highlight some cases where architecture choices have real consequences:
    - **PBL vs traditional for knowledge vs skills.** PBL meta‑analyses show robust positive effects on skills, with more ambiguous effects on immediate factual knowledge; this implies that for pure declarative knowledge objectives, PBL may be suboptimal as the only organizing architecture.[^10][^11]
    - **CBE and mastery vs time‑based progression.** CBE and mastery fundamentally change pacing and assessment logic (competence is the unit of progression), which affects how you architect self‑learning courses (e.g., gating, progression rules).[^4][^7][^15]
    - **Inquiry/minimal guidance vs guided instruction.** Evidence summarized by Kirschner, Sweller, and Clark indicates that minimally guided inquiry is structurally less effective for novices than guided models because of cognitive load; you cannot treat “pure inquiry” as just a lightweight variant of the same template without changing support mechanisms.[^21][^27]

These findings argue for **distinct structural profiles** for at least: PBL/CBL, CBE/mastery, and guided‑inquiry/Socratic modes—while still preserving a common principle‑level core.

### Practical implication for your course‑generation tool

Based on this landscape:

- A **single core architecture** grounded in UbD + Merrill + CLT is defensible and evidence‑aligned:
    - Core backbone: Outcomes/competencies → assessments/evidence → learning experiences.[^5][^2][^4]
    - Lesson arc: problem → activation → demonstration → practice → feedback → integration.[^24][^23][^1]
- On top of that core, your system should support **configurable profiles** that adjust macro structure and pacing for different subject types and pedagogical paradigms, for example:
    - **Theory‑profile:** Spiral or linear concept sequences; theory‑first entry; strong retrieval and spacing; modest projects/cases.[^25][^6][^26]
    - **Procedural/code‑profile:** Linear or modular units; heavy worked examples and guided practice; mastery gates on key procedures.[^27][^29][^15]
    - **PBL/CBL‑profile:** Problem‑first; projects/cases as the spine; knowledge introduced just‑in‑time; emphasis on collaborative tasks and reflection.[^14][^12][^11][^10]
    - **CBE/mastery‑profile:** Competencies as top‑level entities; progression via competency demonstration; rich formative assessment and remediation loops.[^19][^7][^15][^17][^4]
    - **Guided‑inquiry‑profile:** Socratic questioning and investigations, but with explicit scaffolding, checkpoints, and occasional direct instruction to manage cognitive load.[^20][^21][^27]

In other words, the evidence does **not** support completely disconnected architectures per subject type; instead, it supports a **single meta‑model with multiple evidence‑based profiles** that tweak macro‑structure, pacing, and the balance of problem‑first vs theory‑first, while preserving common instructional principles.

***

## Sources

(Author / framework + representative link)

- Merrill, M. D. (2002, 2013). *First Principles of Instruction*. (Problem‑centered, activation, demonstration, application, integration).[^38][^22][^23][^1][^24]
- Wiggins, G., \& McTighe, J. (2005). *Understanding by Design*. (Backward design: goals → evidence → learning plan).[^39][^40][^34][^2][^5]
- ADDIE / IPISD model. Instructional systems design process (Analysis, Design, Development, Implementation, Evaluation).[^36][^41][^35][^3]
- Bruner, J. (1960) / Spiral curriculum synthesized in teacher guides.[^6]
- Sweller, J., Paas, F., van Merrienboer, J. (1998–2019). *Cognitive Load Theory and Instructional Design*.[^42][^43][^29][^27]
- Project‑based learning meta‑analyses in higher education.[^9][^44][^8]
- Problem‑based learning meta‑analyses in tertiary education.[^11][^10]
- Case‑based learning in medical education (scoping reviews and meta‑analysis).[^13][^14][^12]
- Mastery learning (Bloom; Guskey, T. R.).[^15]
- Competency‑based medical education (CBME) conceptual review.[^16][^4]
- Competency‑based education in pharmacy: systematic reviews and meta‑analyses.[^45][^18][^37][^19][^7][^17]
- Formative assessment and feedback: Black \& Wiliam (1998); recent meta‑analyses.[^33][^46][^47][^32]
- Interleaving meta‑analysis and theoretical distinction from spacing.[^48][^30][^31]
- Spacing/distributed practice meta‑analysis.[^49][^26]
- Kirschner, Sweller, \& Clark (2006). *Why Minimal Guidance During Instruction Does Not Work*.[^50][^21]

This gives you a principled foundation for defining your internal course schema as a meta‑architecture with profiles, rather than siloed templates by subject.
<span style="display:none">[^51][^52][^53][^54][^55][^56][^57][^58][^59][^60]</span>

<div align="center">⁂</div>

[^1]: https://mdavidmerrill.files.wordpress.com/2019/04/firstprinciplesbymerrill.pdf

[^2]: https://andymatuschak.org/files/papers/Wiggins, McTighe - 2005 - Understanding by design.pdf

[^3]: https://en.wikipedia.org/wiki/ADDIE_model

[^4]: https://pubmed.ncbi.nlm.nih.gov/20662574/

[^5]: https://edis.ifas.ufl.edu/publication/WC322/pdf

[^6]: https://www.structural-learning.com/post/the-spiral-curriculum-a-teachers-guide

[^7]: https://pubmed.ncbi.nlm.nih.gov/36272964/

[^8]: https://files.eric.ed.gov/fulltext/EJ1485543.pdf

[^9]: https://repository.usfca.edu/diss/668/

[^10]: https://cris.maastrichtuniversity.nl/en/publications/effects-of-problem-based-learning-a-meta-analysis/

[^11]: https://www.tandfonline.com/doi/full/10.1080/03075079.2025.2498084?af=R

[^12]: https://pubmed.ncbi.nlm.nih.gov/42183443/

[^13]: https://pubmed.ncbi.nlm.nih.gov/37559108/

[^14]: https://pubmed.ncbi.nlm.nih.gov/41510950/

[^15]: https://tguskey.com/wp-content/uploads/Mastery-Learning-1-Mastery-Learning.pdf

[^16]: https://pmc.ncbi.nlm.nih.gov/articles/PMC126659/

[^17]: https://www.sciencedirect.com/science/article/pii/S1551741121000681

[^18]: https://pubmed.ncbi.nlm.nih.gov/33640334/

[^19]: https://pubmed.ncbi.nlm.nih.gov/32069376/

[^20]: https://eric.ed.gov/?id=EJ1494257

[^21]: https://eric.ed.gov/?id=EJ736299

[^22]: https://www.yorku.ca/unsdgs/toolkit/wp-content/uploads/sites/617/2023/04/Merrills-First_Principles_of_Instruction_A_synthesis.pdf

[^23]: https://students.tippie.uiowa.edu/tippie-resources/technology/instructional-design/models/merrill

[^24]: https://studylib.net/doc/6880382/instructional-design

[^25]: https://www.learningscientists.org/blog/2017/2/9-1

[^26]: https://www.semanticscholar.org/paper/Distributed-practice-in-verbal-recall-tasks:-A-and-Cepeda-Pashler/634293f80f8e661dc259e4902bca99821bec3014

[^27]: https://www.uky.edu/~gmswan3/544/Cognitive_Load_\&_ID.pdf

[^28]: https://repub.eur.nl/pub/21321/29102010-9.pdf

[^29]: https://files.eric.ed.gov/fulltext/EJ1161818.pdf

[^30]: https://pubmed.ncbi.nlm.nih.gov/31556629/

[^31]: https://onlinelibrary.wiley.com/doi/10.1002/acp.1598

[^32]: https://eric.ed.gov/?id=EJ575146

[^33]: https://scholars.georgiasouthern.edu/en/publications/the-impact-of-formative-assessment-on-k-12-learning-a-meta-analys/

[^34]: https://teachingwithtech.lss.wisc.edu/Documents/UBD_Template.doc

[^35]: https://lemonlearning.com/blog/addie-model-the-5-phases-of-instructional-design

[^36]: https://www.d2l.com/blog/what-is-the-addie-model-of-instructional-design/

[^37]: https://pharmacyeducation.fip.org/pharmacyeducation/article/view/2149

[^38]: https://mdavidmerrill.wordpress.com/wp-content/uploads/2019/07/firstprinciplesreigeluthcarr-1.pdf

[^39]: http://arlingtonplc.pbworks.com/f/LbDDallas05WigginsMcTighe.pdf

[^40]: https://www.michigan.gov/-/media/Project/Websites/mde/Year/2007/12/27/UnderstandingbyDesign.pdf?rev=7a41526fbe0c488da5ee7edc07d71e5f

[^41]: https://elmlearning.com/hub/instructional-design/addie-model/

[^42]: https://psycnet.apa.org/record/2019-03026-001

[^43]: https://education.nsw.gov.au/content/dam/main-education/about-us/educational-data/cese/2017-cognitive-load-theory-practice-guide.pdf

[^44]: https://publicatio.bibl.u-szeged.hu/24564/1/meta-analysispublication2022.06.pdf

[^45]: https://www.sciencedirect.com/science/article/abs/pii/S1877129715300198

[^46]: https://researchonline.nd.edu.au/edu_article/315/

[^47]: https://eric.ed.gov/?id=EJ429465

[^48]: https://eric.ed.gov/?id=EJ1319430

[^49]: https://laplab.ucsd.edu/articles/Cepeda_etal_2006.pdf

[^50]: https://www.usf.edu/atle/documents/handout-kirschner-stop-minimally-guided-instruction.pdf.pdf

[^51]: https://www.youtube.com/watch?v=VQG3h4BMLwU

[^52]: https://repositorio-aberto.up.pt/bitstream/10216/158003/2/611717.pdf

[^53]: https://instructionaldesign.com.au/merrills-instructional-design-principles/

[^54]: https://www.sciencedirect.com/science/article/pii/S1551741122003308

[^55]: https://pubmed.ncbi.nlm.nih.gov/38831271/

[^56]: https://mdc.edu/padron/documents/Work of Grant Wiggins.pdf

[^57]: https://www.youtube.com/watch?v=eYIZOebDTAw

[^58]: https://ris.utwente.nl/ws/files/247731083/Collis2005merrill.pdf

[^59]: https://www.youtube.com/watch?v=ByELW39V3fc

[^60]: https://educationlibrary.org/merrills-principles-of-instruction/

