# Classification & Provenance

The single auditable ledger for this distillation. **One table, not two** — each reference asset's
verdict, its rationale, and its provenance are the *same* record.

- **Reference**: `$COURSE_FACTORY_REFERENCE_DIR` (default `/home/barak/System_Design_SelfLearn/`) —
  read-only, and **unvalidated**: never delivered to or validated by a real learner. Nothing was
  carried into this template on the strength of its existing there.
- **Distillation snapshot**: this ledger reflects the reference course at commit
  **`5dd7056`** (`5dd705676f5dc1a5b49e8e34a5dfe4e19f4ca9ef`, dated 2026-07-05), distilled
  **2026-07-23** into `VERSION` 1.0.0. Recording *which state* was read (not just the path) lets a
  later re-distillation `git diff` the reference against this commit and re-filter only what
  actually changed, rather than re-reading the whole `.claude/` blind (Edge Case: "the reference
  course changes after distillation").
- **Research**: `specs/course-factory/000-course-template/research-digest.md` — cited as
  `digest §N`. The distillation halts without it.
- **Rationale format** follows the `mentor-research` discipline: a tiered reliability call
  (**High** / **Medium** / **Low**) plus a one-clause caveat, with the citation trail in
  *provenance*.
  - **High** — the digest supports it directly, as a cross-model invariant or a cited finding.
  - **Medium** — sound authoring discipline the digest does not cover; kept on the
    critical-thinking filter, not on research.
  - **Low** — kept only with an explicit "adopted on judgment" flag, or an artifact of the one
    reference course.

**Verdicts**: `keep-core` · `demote-module` · `drop`. Exactly one per asset.
**Targets**: `core` · `module:<name>` · `profile:<name>` · `—` (dropped).

---

## Table 1 — Reference assets (23 of 23 classified, 0 unclassified)

| # | asset_path | asset_type | verdict | rationale | provenance | neutralized | target |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `agents/course-evaluator.md` | agent | **keep-core** | **High** — an author-blind, evidence-citing grading loop instantiates the digest's *feedback and formative assessment* invariant, and author-blindness is an anti-collusion property independent of subject; caveat: only the **shape** survives — its hard-coded weights, thresholds and pass bar were stripped as owned by the grading spec, and the rubric *content* it grades is judgment-based (row 17). | `ref:agents/course-evaluator.md` + `digest §4` (feedback/formative assessment invariant) | true | `core` |
| 2 | `agents/curriculum-architect.md` | agent | **keep-core** | **High** — its generic contribution (design the spine before the content, sequence by dependency, check existing coverage before adding, name what each lesson teaches) *is* backward design and is a digest invariant; caveat: **merged into the `backward-design` skill rather than kept as an agent** (FR-008), and everything else in it — the subject taxonomy, the fixed table formats, the running-example vocabulary — was dropped as topic-specific. | `ref:agents/curriculum-architect.md` + `digest §4` (outcome alignment), `digest §5.1` (UbD is cross-subject) | true | `core` |
| 3 | `agents/lesson-consistency-reviewer.md` | agent | **keep-core** | **High** — a structural consistency check (arc order, running-example continuity, numbering, `file:line` findings ranked Critical/Warning/Nit) applies to any course whose lessons share a house form; caveat: **split** — the image-existence check went to `module:diagrams` (FR-011), and its per-unit programming-language rule and cross-tree duplication-drift check were **dropped** as artifacts of that repo's own history. | `ref:agents/lesson-consistency-reviewer.md` + `digest §3` (canonical arc = the thing being checked) | true | `core` (+ image check → `module:diagrams`) |
| 4 | `agents/socratic-mentor.md` | agent | **demote-module** | **High** — the digest is explicit that **minimally guided inquiry underperforms guided instruction for novices** (cognitive load), so a Socratic mode cannot be a core default; caveat: kept as an opt-in module *with scaffolding rules added that the reference lacked*; guided-inquiry as a full **profile** is a later, independent increment. | `ref:agents/socratic-mentor.md` + `digest §1` (Socratic/inquiry row), `digest §5.3` (Kirschner/Sweller/Clark) | n/a | `module:socratic` |
| 5 | `commands/add-diagram.md` | command | **demote-module** | **Medium** — a wire-the-diagram-and-verify-the-reference procedure is sound authoring hygiene, but only for courses whose material is structural; caveat: the digest supports multimedia demonstration generally (§3) but gives no basis for diagrams as a universal course component. | `ref:commands/add-diagram.md` | n/a | `module:diagrams` |
| 6 | `commands/course-report.md` | command | **keep-core** | **Medium** — delegating to an author-blind grader and *delivering the verdict as it came back* is the operational surface of the feedback invariant, and is named core tooling by this factory's own governance; caveat: the digest does not cover command-level tooling, so this is the critical-thinking filter, not research; its pass numbers were stripped (owned by the grading spec). | `ref:commands/course-report.md` + `digest §4` (feedback invariant, indirect) | true | `core` |
| 7 | `commands/improve-course.md` | command | **keep-core** | **Medium** — an analyze → plan → author → grade loop with gates and a hard round cap is the mechanism that makes "no one-shot generation" real; caveat: command-level tooling is uncovered by the digest, so this is judgment; the reference's numeric exit condition was stripped and replaced by a reference to the grading spec. | `ref:commands/improve-course.md` | true | `core` |
| 8 | `commands/new-lesson.md` | command | **keep-core** | **Medium** — scaffolding a lesson *in the canonical arc* is the arc's operational surface, and "deepen before adding" prevents the commonest syllabus failure; caveat: judgment-based as tooling, though the arc it scaffolds is High-confidence (row 19/20). | `ref:commands/new-lesson.md` + `digest §3` (the arc it enforces) | true | `core` |
| 9 | `commands/new-sd-lesson.md` | command | **drop** | **High** — after neutralization it is the *same capability* as `/new-lesson` differing only in section names, and the digest reports lesson structure as **consistent across models, varying in emphasis, not in kind** (§3); caveat: consolidated per FR-008 — keeping both would fork the one canonical arc; its "state assumptions, show the reasoning behind any figure" rule was **absorbed** into `lesson-arc` and the rubric's Grounding dimension. | `ref:commands/new-sd-lesson.md` + `digest §3` | n/a | `—` |
| 10 | `commands/plan-curriculum.md` | command | **drop** | **Medium** — its capability (draft/re-sequence the syllabus skeleton) is fully covered by the `backward-design` core skill plus `/improve-course`'s plan step; caveat: dropped as a *surface*, not as a capability — a third command for it would grow the core without adding one, against the "small mandatory core" constraint. | `ref:commands/plan-curriculum.md` | n/a | `—` |
| 11 | `commands/review-lesson.md` | command | **drop** | **Medium** — a thin wrapper that only delegates to the consistency reviewer, which `/improve-course` already invokes; caveat: the capability is preserved intact in the core agent (row 3); only the duplicate entry point is cut. | `ref:commands/review-lesson.md` | n/a | `—` |
| 12 | `commands/review-pattern-impl.md` | command | **drop** | **Low** — reviews learner code for one subject's idioms; the generic residue ("does the artifact do what the lesson asked?") is already the consistency reviewer's practice-closes-the-loop check; caveat: no generalizable home — a code-idiom review is not a course-template concern. | `ref:commands/review-pattern-impl.md` | n/a | `—` |
| 13 | `commands/setup-retro.md` | command | **drop** | **High** — build tooling, not course-teaching machinery: it authors a backlog for improving a repo's own AI setup; caveat: **excluded by FR-021** — it belongs to the factory's own build `.claude/`, which must stay distinct from the template; the exclusion is recorded here as a verdict. | `ref:commands/setup-retro.md` | n/a | `—` |
| 14 | `commands/teach.md` | command | **demote-module** | **High** — the entry point for the Socratic mode; it follows row 4 wherever that lands; caveat: same evidence and the same scaffolding caveat as row 4. | `ref:commands/teach.md` + `digest §5.3` | n/a | `module:socratic` |
| 15 | `hooks/lesson_diagram_reminder.py` | hook | **demote-module** | **Medium** — one of its two jobs generalizes: an *advisory* post-edit reminder that a lesson references an image that does not exist yet, catching at authoring time what review would catch later; caveat: its other job — a hard-coded 16-entry duplicate-file table for that repo's two lesson trees — was **dropped** outright, and the reminder ships as **documented guidance in the diagrams module, not as shipped hook code**, so the template stays content-only. | `ref:hooks/lesson_diagram_reminder.py` | n/a | `module:diagrams` |
| 16 | `skills/architecture-diagrams/SKILL.md` | skill | **demote-module** | **Medium** — the generate-don't-hand-draw pipeline, one visual language across a course, and the add-a-diagram procedure are sound and reusable; caveat: purely topic-specific as delivered (one tool, one colour set, that repo's own broken-image list, all stripped), and the digest gives no basis for diagrams as a universal component — so module, never core. | `ref:skills/architecture-diagrams/SKILL.md` | n/a | `module:diagrams` |
| 17 | `skills/course-quality-rubric/SKILL.md` | skill | **keep-core** | **Low (adopted on judgment)** — **split**: its five generic dimensions became five of the rubric's six core dimensions, its two subject-specific checks became **add-on slots** (FR-014), and its weights/thresholds/hard-gate rule were **removed** as owned by the grading spec (FR-015); caveat: the digest is **silent on rubric evidence** — a gap, not thinness — so the dimension set is flagged *"unproven, adopted on judgment"* and is explicitly **not** presented as research-backed. The sixth dimension, **Clarity, is not from this asset** — see the Clarity row in Table 2. Author-blind grading is kept at **Medium** (anti-collusion, subject-independent). | `ref:skills/course-quality-rubric/SKILL.md` | true | `core` (+ subject checks → rubric add-on slots) |
| 18 | `skills/design-pattern-catalog/SKILL.md` | skill | **demote-module** | **Medium** — the entry shape (intent · role in the running example · common misuse) and the "name the change you want to absorb / if nothing varies you need none" heuristic generalize to any subject with a bounded named solution set; caveat: **most subjects have no such set**, and the digest gives no support for a catalog as a universal component — so opt-in module only, with its subject-specific entries dropped. | `ref:skills/design-pattern-catalog/SKILL.md` | n/a | `module:pattern-catalog` |
| 19 | `skills/pattern-lesson-format/SKILL.md` | skill | **keep-core** | **High** — carries a lesson arc that maps onto the digest's canonical arc (framing → activation → demonstration → practice → integration), plus the *one running example* and *required-vs-optional sections* disciplines; caveat: **merged with row 20 into one `lesson-arc` core asset** (FR-008), with its subject vocabulary, numbering examples and language rules stripped. | `ref:skills/pattern-lesson-format/SKILL.md` + `digest §3` (Merrill/Gagné arc) | true | `core` |
| 20 | `skills/system-design-curriculum/SKILL.md` | skill | **keep-core** | **High** — carries the *same* arc capability as row 19 under different section names, confirming the digest's finding that lesson structure varies in emphasis, not in kind; caveat: **merged into the one `lesson-arc`** (FR-008); its "never assert an unexplained figure" rule was absorbed into `lesson-arc` + the rubric's Grounding dimension, its practice/exercise machinery went to `module:katas`, and its subject taxonomy, estimation method and build pipeline were dropped. | `ref:skills/system-design-curriculum/SKILL.md` + `digest §3`, `digest §4` | true | `core` (+ practice machinery → `module:katas`) |
| 21 | `.claude/settings.json` | other | **drop** | **High** — tool permissions, an allow/deny list, and a wiring entry for row 15's hook: environment configuration for one machine and one repo, not course-teaching machinery; caveat: **excluded by FR-021**; a generated course's own settings are 001's overlay concern, not the frozen template's. | `ref:.claude/settings.json` | n/a | `—` |
| 22 | `.claude/setup-backlog.md` | other | **drop** | **High** — a dated, repo-specific backlog of that setup's own pain, explicitly written to be consumed by the setup-improvement tooling; caveat: **excluded by FR-021** (build/lineage tooling), and it is a point-in-time diary — the opposite of a frozen, reusable template asset. | `ref:.claude/setup-backlog.md` | n/a | `—` |
| 23 | `CLAUDE.md` (reference repo root) | other | **drop** | **Medium** — its transferable content is exactly two rules already captured elsewhere ("teach, don't spoil" → `module:socratic` + `lesson-arc`'s framing-first rule; "one running example" → `lesson-arc` house conventions); caveat: everything remaining is that repo's layout, its duplicate-tree trap and its build commands, and a generated course's equivalent file is 001's **overlay**, not a frozen template piece. | `ref:CLAUDE.md` | n/a | `—` |

### Coverage

| Verdict | Count |
| :--- | :--- |
| `keep-core` | 9 |
| `demote-module` | 6 |
| `drop` | 8 |
| **Total** | **23 of 23 — 0 unclassified** |

**Merges applied (FR-008)**: rows 19 + 20 → one `lesson-arc` core asset; row 2 → merged into
`backward-design` rather than kept as a separate agent; rows 9, 10, 11 dropped as duplicate
surfaces of capabilities already core.

**Splits applied**: row 3 (generic → core, image check → `module:diagrams`, two checks dropped);
row 17 (its five dimensions → core, subject checks → add-on slots, grading semantics → removed);
row 15 (advisory reminder → `module:diagrams`, duplicate-file table → dropped).

---

## Table 2 — Produced pieces → provenance

The complement to Table 1, not a second ledger: Table 1 records what happened to each **input**;
this records where each **output** came from, so no shipped piece is unexplained (SC-007). Rows
tracing to a reference asset name its Table 1 row; rows with no reference origin are grounded in
the digest or marked `new`.

| Produced piece | Tier | Provenance |
| :--- | :--- | :--- |
| `.claude/skills/backward-design/SKILL.md` | core | Table 1 row 2 (generic contribution, merged) + `digest §4` (outcome alignment invariant), `digest §5.1` (UbD is cross-subject) |
| └ its **misconception** rules (Stage 1 + Stage 2) | core | **new** — `digest §4` (feedback/formative assessment invariant) applied at design time; the diagnostic-item rule follows `pedagogy/catalog/formative-assessment.md` ("non-diagnostic items produce no actionable signal") |
| └ its **technique-selection** rule | core | **new** — routes authoring to `course-factory/pedagogy/DIGEST.md` (choose) and `catalog/` (author) for evidence tiers and **boundary conditions**, and forbids justifying a choice from `pedagogy/MYTHS.md` |
| `.claude/skills/lesson-arc/SKILL.md` | core | Table 1 rows 19 + 20 (merged, FR-008) + `digest §3` (canonical arc; per-material-type emphasis) |
| └ its **feedback-quality** rules (diagnostic / how-to-improve / timely / no vague praise) | core | **new** — `digest §4` names feedback + formative assessment a cross-model invariant; the specific rules follow `pedagogy/catalog/formative-assessment.md`. The reference course had no equivalent |
| └ its **retrieval, spacing, worked-example-fading, working-memory** conventions | core | **new** — `digest §2` (spaced practice; worked examples then faded guidance), `digest §4` (demonstration + application invariant), `digest §5` (theory-profile: "strong retrieval and spacing"); corresponds to `pedagogy/catalog/{retrieval-practice,spaced-repetition,worked-examples,scaffolding-cognitive-load}.md` |
| └ its **§ Grounding** pointer + debunked-methods rule | core | **new** — wires the core to `course-factory/pedagogy/` (`DIGEST.md` → `catalog/` + `MYTHS.md`). Stated standalone as well, so the rule survives the template being copied out of the factory where that path does not resolve |
| `.claude/skills/quality-rubric/SKILL.md` | core | Table 1 row 17 (split) — core dimension set flagged **"unproven, adopted on judgment"**; digest silent on rubrics |
| └ its **Clarity** dimension | core | **new** — from neither the reference course nor the digest. Added on the judgment that comprehensibility is already assessed twice during a course build with no gradeable output, so grading it routes an existing signal into the scorecard rather than discarding it. The strongest "adopted on judgment" flag in the template |
| └ its finding-routing table | core | **new** — added so a defect is scored under exactly one dimension; six dimensions overlap more than five did, and double-counting would distort any aggregate |
| `.claude/agents/lesson-consistency-reviewer.md` | core | Table 1 row 3 (split) |
| `.claude/agents/course-evaluator.md` | core | Table 1 row 1 (shape only; weights/gates removed) |
| `.claude/commands/improve-course.md` | core | Table 1 row 7 (numeric exit condition removed) |
| `.claude/commands/new-lesson.md` | core | Table 1 row 8 |
| `.claude/commands/course-report.md` | core | Table 1 row 6 |
| `profiles/README.md` | profile mechanism | **new** — the FR-022/024/025 mechanism, with the four variable dimensions taken from `digest §4` ("Variables") |
| `profiles/default/spine.md` | `profile:default` | **new** — `digest §1` (linear + spiral rows), `digest §2` (concept/theory-heavy), `digest §5` ("theory-profile": spiral/linear, theory-first, retrieval and spacing). Advisory-only checkpoints are this factory's static-content constraint, not the digest's |
| `.claude/skills/diagrams/SKILL.md` | `module:diagrams` | Table 1 rows 16 + 15 (advisory reminder) + row 3's image-existence check |
| `.claude/commands/add-diagram.md` | `module:diagrams` | Table 1 row 5 |
| `.claude/skills/katas/SKILL.md` | `module:katas` | Table 1 row 20 (practice/exercise machinery) + row 2 (warm-up pairing) + `digest §4` (demonstration + application), `digest §2` (spaced practice) |
| `.claude/skills/pattern-catalog/SKILL.md` | `module:pattern-catalog` | Table 1 row 18 |
| `.claude/agents/socratic-mentor.md` | `module:socratic` | Table 1 row 4 + `digest §5.3` — the scaffolding rules are **added**, not inherited |
| `.claude/commands/teach.md` | `module:socratic` | Table 1 row 14 |
| `neutrality-terms.txt` | template metadata | **new** — seeded from FR-007's named terms, grown during this classification (see below) |
| `manifest.yaml`, `VERSION`, `CLASSIFICATION.md`, `README.md` | template metadata | **new** — this spec's own contracts |

**0 unexplained pieces.** **0 pieces kept solely because the reference course had them** — every
`keep-core` row above cites either a digest section or an explicit critical-thinking judgment with
its reliability tier.

---

## The neutrality gate

`neutrality-terms.txt` is a **maintained artifact** that ships with the template, so a
re-distillation re-runs the same gate. It scans the **mandatory core only** — modules and profiles
are allowed to carry subject-specific wording; the core is not. The bar is **0 hits**.

The list is **seeded** from the terms named in FR-007 and **grows** whenever classification catches
new subject wording. This run grew it from 5 seed terms to 18:

- **Seeded (5)**: `System Design`, `HomeOS`, `patterns_v1`, `capacity`, `QPS`
- **Grown during classification (13)**: `System_Design_v1`, `HomeOS-Cloud`, `Smart Home OS`,
  `HomeHub`, `patterns_v2`, `GoF`, `Gang of Four`, `design pattern`, `Micro-Do`, `graphviz`,
  `Zigbee`, `Course_Syllabus.ipynb`, `autodidact`

Run it with `course-factory/tools/neutrality_scan.py`, or with the `grep -f` recipe in the
feature's `quickstart.md` — same contract.
