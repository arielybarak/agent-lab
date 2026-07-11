# course-factory specs — deep design review

**Date**: 2026-07-10
**Scope**: cross-spec integrity (000–004 + DESIGN.md + constitution) and per-spec holes/optimization,
pre-`/speckit-plan`. Findings only — no spec edited. Every entry in the README "Resolved decisions
(seam log)" is treated as final and not re-litigated.

Ranking: **[Critical]** blocks a correct build · **[Major]** real gap/rework risk · **[Minor]** polish.

---

## Part A — Cross-spec findings

### Critical

**A1 · [Critical] · Profile seam is broken downstream — 000 delegates profile selection to a spec that doesn't know it.**
- Where: 000 FR-025 ("an intake/overlay decision made by 001") + 000 FR-018 vs 001 FR-004/FR-005/FR-006, 002 (whole spec), 003 (whole spec) — the word "profile" appears **zero times** in 001, 002, and 003; 001 FR-001 and its Key Entities still describe a **two-tier** template ("mandatory core plus opt-in optional modules").
- Why: 001/002/003 predate the 2026-07-10 three-tier decision (constitution 1.1.0 sync report says it synced 000 + DESIGN only). Profiles change exactly what 002 composes (macro spine, entry point) and 003 authors (scaffolding depth, checkpoint placement) — as specced, a profile would be selected by no one and consumed by nothing.
- Direction: add profile-selection to 001's intake/brief/copy contract (FR-004/005/006, SC-002), and add profile-consumption FRs to 002 (compose per the selected profile's spine) and 003 (author per its scaffolding/checkpoint rules).

**A2 · [Critical] · The research digest contains no rubric evidence, so 000's rubric-validation requirement is unsatisfiable.**
- Where: 000 FR-013 ("the core dimension set itself MUST be validated against the external research") + FR-003 (digest is "on how... course templates **and quality rubrics** are structured") vs `research-digest.md` — its actual prompt and content cover macro-structures, lesson arcs, and invariants only; quality rubrics are never researched.
- Why: by 000's own FR-005, a digest that is "thin" on a subject must halt/flag the distillation — the rubric subject is not thin, it's absent; FR-013 and SC-005's five-dimension core would be adopted from the SD reference on faith, which FR-001/SC-009 forbid.
- Direction: run a second research pass scoped to course-quality rubrics/evaluation criteria (or explicitly re-scope FR-013 to judgment-based with a recorded "unproven, adopted on judgment" flag per the 000 edge case).

**A3 · [Critical] · Forward-diff mechanics are defined by nobody — and 003's authors never see applied diffs.**
- Where: 001 FR-023 (rule only) vs 003 FR-007 (author inputs = brief + **frozen syllabus** + skeleton + [Sn] entries + insights digest — no diffs) and 003 FR-017 (surfaces diffs, doesn't consume them); no spec says where a diff is recorded, who applies it, or how downstream readers of a frozen artifact see it.
- Why: the settled forward-diff-only rule makes gated artifacts permanently stale; without a diff ledger + a read rule, lessons get authored against a syllabus the user has already amended — silent drift, exactly what the rule exists to prevent.
- Direction: 001 should own the diff artifact (where it lives, its lifecycle in `BUILD_PROGRESS.md` or a sibling file) and every consumer spec (002/003/004) should name "frozen artifact + its applied diffs" as the canonical read.

### Major

**A4 · [Major] · Nobody populates `FEEDBACK.md`.**
- Where: 001 FR-008 creates the stub; 004 Out-of-Scope explicitly disowns "the per-critique writing"; 003 never mentions `FEEDBACK.md` at all.
- Why: Principle XII's compounding loop has an unowned first half — harvest (004) reads a file no spec ever writes.
- Direction: assign per-critique writing (most naturally 003's evaluator loop and 001's gate events) to an owning spec.

**A5 · [Major] · DESIGN roadmap task #2 — the factory's own build `.claude/` — is specced nowhere.**
- Where: DESIGN § Build roadmap #2; 000 Out-of-Scope ("→ separate asset", no owner named); README build order (000→001→002→004→003→004) omits it entirely.
- Why: it's the thing that *runs* the pipeline; if 001's implementation is implicitly it, that's never stated, and its structural-constraint distinctness (constitution) has no spec enforcing it from the build side.
- Direction: either declare it 001's implementation deliverable (in 001's plan) or give it a small spec/asset entry in the README index with a build-order slot.

**A6 · [Major] · The delivery contract omits the course itself.**
- Where: 001 FR-020 + SC-008 and constitution § Structural Constraints list required per-course artifacts as brief/sources/progress/feedback/report/.claude — **no syllabus file, no lessons**; DESIGN's diagram shows "lessons, syllabus, diagrams, katas"; 002 never names the syllabus's on-disk identity either.
- Why: a folder with zero lessons satisfies the letter of every delivery FR/SC; the deliverable ("the course content") is the one thing the contract doesn't require.
- Direction: add the content artifacts (syllabus file + lessons per the format decision) to 001 FR-020/SC-008 and the constitution's file list; have 002 name the syllabus artifact.

**A7 · [Major] · The insights-digest read rule is unimplemented in two of its three readers.**
- Where: constitution XII + 004 FR-017 say intake (001), syllabus compose (002), and drafting (003) read the digest — 003 FR-007 complies; 001's intake FRs (FR-002–005) and all of 002 contain no mention of the insights digest.
- Why: a constitution MUST with no implementing requirement in the owning specs; the compounding loop's read side silently drops two consumers.
- Direction: add digest-as-input FRs to 001 intake and 002 composition (an empty digest is valid, per 003's precedent).

**A8 · [Major] · Constitution & DESIGN are stale against two settled clarifications.**
- Where: (a) constitution XII "harvested… after each course/phase" + DESIGN's insights write-rule vs 004 FR-016 (harvest is **user-invoked only** — settled 2026-07-08); (b) DESIGN pipeline step 4 "when the first two lessons **pass the rubric**" and no gate-then-fan-out vs 003's settled terminal-state trigger + FR-018 ordering.
- Why: the constitution's own governance clause says disagreement with DESIGN is "a defect to reconcile"; XII's "MUST be harvested" is unmeetable if the user never invokes it.
- Direction: reconcile the docs to the seam log (soften XII to user-invoked, update DESIGN step 4) — not a re-litigation, the clarifications win.

**A9 · [Major] · "Only two ask-moments" literally contradicts four other user interactions.**
- Where: 001 FR-014, constitution IV, DESIGN ("Two moments we ask the user") vs the syllabus approval loop, 001 FR-024 blocking scan, FR-012 accept-or-comment at cap, and 003's cap-surfaced-and-user-accepted trigger.
- Why: an implementer honoring FR-014 as written cannot honor FR-024; the intended distinction (clarifying *questions* vs review *gates*) exists nowhere in text, so both FRs are unfalsifiable together.
- Direction: define the carve-out once (ask-moments = open questions; gates/accept-decisions are a different category) in 001 and mirror in the constitution.

**A10 · [Major] · Two version identities, no revision path: rubric version vs template stamp.**
- Where: 004 FR-005/FR-013 (rubric MUST be versioned) vs 000 FR-016 (**single** template stamp) + 000 FR-017/edge case (the only defined change path is full re-distillation, which is sourced from the reference course — not from `comparison/` revisions).
- Why: an adopted rubric revision has no defined landing: the rubric is a frozen template asset, so "extend the single rubric" implies a template change no spec's freeze/version mechanics cover.
- Direction: define template-evolution-after-v1 (who bumps the stamp for a non-distillation change; whether rubric version = template version) — likely a 000/004 joint seam entry.

**A11 · [Major] · Delivery's gate and the "needs work" verdict don't compose.**
- Where: 001 FR-010 (every phase's gate must clear) but FR-011 maps reviewers only for syllabus/skeletons/lessons — delivery has no defined gate; 004 FR-009 lets the course-evaluator return "needs work" while FR-011 says the report "MUST certify the course."
- Why: it's undefined whether a needs-work course still reaches the delivered terminal state, and what a "certification" bearing a failing verdict means to the user.
- Direction: 001 defines delivery's gate condition (likely "report generated," with verdict informational); 004 rewords "certify" to "attest/report" or conditions it on the verdict.

### Minor

**A12 · [Minor] · Profile inventory inconsistency: is procedural/code a profile?** Constitution IX and 000's overview/Key Entities enumerate five profiles (incl. procedural/code); 000 FR-023/SC-011 mandate only 3 + default. Ambiguous ship-set. Direction: pin procedural/code as ship-now, later, or folded into default.

**A13 · [Minor] · Duplicated ownership of the five core rubric dimensions.** 000 FR-013 and 004 FR-001 each assert the list; a future revision must touch both specs in lockstep. Direction: one spec names them, the other references.

**A14 · [Minor] · README seam #3 says 002 updates phase status — 002's spec never mentions `BUILD_PROGRESS.md`.** One side of the seam is prose-only. Direction: fix the README or add the FR to 002 (see B2-1).

**A15 · [Minor] · DESIGN says `pedagogy/` is "Deferred idea, not built" — it's built and populated (2026-07-10).** Also its normative rule ("specs 002/003 MUST NOT cite a low-tier or MYTHS.md entry") and the `[Pn]` namespace live only in `pedagogy/README.md`; 003 FR-011's citation contract ([Sn]-or-mentor-added) has no slot for a `[Pn]` cite. Direction: update DESIGN's status; when wiring, extend the citation contract to admit `[Pn]`.

**A16 · [Minor] · The existing SD-derived `insights/` corpus has no owner.** DESIGN's reliability warning says the caution "applies to the insights/ corpus," but no spec owns importing/filtering the pre-existing corpus (004 owns only the go-forward harvest). Direction: assign the initial seed-and-filter (000's critical filter is the natural discipline) or declare insights/ starts empty.

---

## Part B — Per-spec holes & gaps

### 000 — Course-Template Distillation

- **B0-1 · [Major] · SC-003/SC-012 are untestable before the pipeline exists.** "Viable course shape" / "coherent course structure" for sample topics presuppose driving the machinery end-to-end, which needs 001+ (not yet built). This is the flagged "distillation validation depth" open question — but the SCs as written have no pre-pipeline verification method. Direction: define a paper-walkthrough or checklist-based validation proxy in clarify, or stage the SC until 001 exists.
- **B0-2 · [Major] · `/course-report` is missing from the mandatory core.** 000 FR-010 (and constitution IX) enumerate the core without it, yet 004 FR-011 and DESIGN step 5 say `/course-report` is "inherited from the template." A required template asset has no tier. Direction: add it to FR-010's core list.
- **B0-3 · [Minor] · FR-005's "halt or flag" is two different behaviors with no chooser, and "thin/low-quality" has no criteria or judge.** SC-010 inherits the ambiguity. Direction: pick one behavior and give a minimal quality bar (e.g., digest must cover each distillation subject).
- **B0-4 · [Minor] · The neutrality gate's term list is open-ended.** FR-007/FR-020/SC-002 scan for four named terms "and other domain wording" — the 0-terms criterion is unfalsifiable beyond the enumerated set. Direction: make the term list a maintained artifact of the distillation.
- **B0-5 · [Minor] · The classification universe is agents/commands/skills/hooks only, and US1 hard-codes counts (4/10/5/1).** Loose reference files (CLAUDE.md, settings, templates, the rubric doc, the insights corpus) fall outside FR-006; the counts break if the reference repo changes. Direction: classify "every file in the reference `.claude/`" and drop the literal counts.
- **B0-6 · [Minor] · FR-010 claims the whole core is "grounded in the research digest," but `/improve-course` and `/new-lesson` have no research grounding** — they're SD-derived judgment keeps, which is fine under SC-009's second clause but contradicts FR-010's wording. Direction: word the commands' grounding as explicit critical-thinking judgment.

### 001 — Pipeline & Instantiation

- **B1-1 · [Critical]** — see **A1**: no profile-selection requirement anywhere in intake/brief/copy.
- **B1-2 · [Major]** — see **A3**: forward-diff artifact/lifecycle undefined despite FR-023 owning the rule.
- **B1-3 · [Major] · The concurrent-sessions edge case has no requirement.** Edge Cases say "only one may hold the build," but no FR/SC defines holding, acquiring, or releasing the build — an edge case naming un-specced behavior. Direction: spec a minimal lock convention or explicitly move concurrency to Out of Scope.
- **B1-4 · [Major] · The skeleton-scan change-request path is undefined.** FR-024 allows "approval (or change request)" but nothing says what a change request triggers — re-enter the agent loop? A fresh 3-round cap? Direct edits? Direction: define the post-change-request loop and its cap in clarify.
- **B1-5 · [Minor] · The clarified spec has no persisted home** (and the brief-vs-module-selection split is ambiguous: FR-004 excludes the selection from the brief, SC-002/scenario 3 imply it's in the brief). FR-018 requires all resume state on disk. Direction: name the on-disk home for both.
- **B1-6 · [Minor] · The accept-or-comment cycle is uncapped.** DESIGN/constitution say comments buy "one more pass"; FR-012 drops the limit, permitting an infinite user↔pass loop. Direction: encode the one-more-pass bound.
- **B1-7 · [Minor] · "Create an empty `BUILD_PROGRESS.md` positioned at the start of the syllabus phase"** (FR-008) — "empty" and "positioned" contradict. Direction: "initialized" not "empty."
- **B1-8 · [Minor] · Interruption during intake (before the course folder exists) has no resume story** — state begins at instantiation. Redoing intake is fine, but say so. Direction: one assumption line.

### 002 — Syllabus

- **B2-1 · [Major] · No sub-phase state: expensive research has no recorded resume point.** The spec never touches `BUILD_PROGRESS.md`; a session dying between research-done and compose/approval leaves nothing but an implicit `SOURCES.md`, and the budget spend/convergence status is unrecorded — 001 FR-015 only tracks phase + per-lesson status. Direction: define the syllabus phase's checkpointable sub-states with 001 (research-done, composed, presented).
- **B2-2 · [Major]** — see **A7**: syllabus composition never reads the insights digest despite constitution XII.
- **B2-3 · [Minor] · SC-005's "raised whenever a real angle conflict exists" has no oracle** — the divergence threshold is admitted agent judgment (Assumptions), so the 100% criterion is unmeasurable. Direction: reframe the SC around auditable behavior (a recorded divergence assessment per run).
- **B2-4 · [Minor] · Post-divergence-answer behavior is undefined.** If the user's directional answer pivots the angle, may research resume? Against what budget? Direction: one FR clause on post-ask re-research.
- **B2-5 · [Minor] · Brief-depth vs. source-reality conflict is unhandled.** FR-008 grounds volume "in the brief's stated depth" — no path for when the topic can't support (or vastly exceeds) the requested size. Direction: add the edge case (mentor-corrects + flags, consistent with FR-006).
- **B2-6 · [Minor] · The dead-`[Sn]` edge case has no owning FR.** "Flagged so later lessons do not cite a broken key" — 003/004 verify entry resolution, not link liveness; nobody owns detecting a dead link or when. Direction: either drop liveness (entries outlive links) or assign a check.
- **B2-7 · [Minor] · The syllabus artifact is never named** — no file name/location for the thing 001 freezes and 003 consumes (see A6). Direction: name it in Key Entities.

### 003 — Lessons

- **B3-1 · [Major] · Post-calibration fixes bypass the rubric gate.** FR-014 fixes fake-student confusion points in the two *already-passed* lessons with no re-grade requirement — an edit can regress a passed dimension after the gate recorded a pass. Direction: require re-running the rubric gate (or a scoped delta-check) on calibration-edited lessons.
- **B3-2 · [Major] · Cap-stuck first lessons stall the entire course on a mid-phase user decision.** The settled terminal-state trigger (FR-013) + gate-then-fan-out (FR-018) mean a cap-surfaced lesson 1 blocks all remaining lessons until the user accepts — an interaction 001 FR-014 forbids as written (see A9), with unstated latency implications. Not challenging the settled ordering — the interaction path just has no owner. Direction: 001's ask-moment carve-out must cover the cap-accept decision, and 003 should state the pool idles (not proceeds) while waiting.
- **B3-3 · [Major] · The drafting guidance is unpersisted.** The calibration's output ("folded into the drafting guidance for every remaining lesson") has no on-disk home; a session dying post-calibration violates 001 FR-018's resume-from-disk rule. Direction: name the guidance artifact and its location in the course folder.
- **B3-4 · [Minor] · SC-004's "100% of factual claims" can't be certified by a spot-check.** FR-011 mandates sampling; the SC demands totality (004's SC-004 has the same tension with its FR-007). Direction: align — either full-coverage citation check or a sampled SC.
- **B3-5 · [Minor] · `.ipynb` citation mechanics unspecified** — where `[Sn]` keys live in code cells/outputs and how the traceability check reads notebooks. Direction: one assumption line; plan detail after that.
- **B3-6 · [Minor] · The fake-student "attempts the exercise" assumes one exists** — behavior for a lesson without an exercise (possible under some profiles) is undefined. Direction: fall back to read-and-report-confusion only.
- **B3-7 · [Minor] · Orchestrator mis-selection of "relevant `[Sn]` entries" silently produces false mentor-added tags** (author can't cite a source it wasn't given). Direction: note the failure mode; consider letting the evaluator flag claims that match existing sources.

### 004 — Grading & Delivery

- **B4-1 · [Major]** — see **A11**: needs-work verdict vs. "MUST certify" vs. 001's undefined delivery gate.
- **B4-2 · [Minor] · SC-007 contradicts FR-014.** "100% of the non-empty `FEEDBACK.md` content is appended" vs. harvest as *distillation* — distilling is precisely not appending 100% of content. Direction: measure "every critique is represented," not content volume.
- **B4-3 · [Minor] · The pass contract 003 consumes has no scale or threshold ownership.** FR-004 defines the shape (per-dimension bars) but nobody owns choosing the scale and bar values, and no artifact records them. Direction: assign to 004's plan and record them with the rubric version.
- **B4-4 · [Minor] · Rubric-revision adoption is "a deliberate, reviewed step" with no reviewer, record, or version-bump mechanics** (compounds A10). Direction: minimal adoption protocol (who approves, where logged, stamp effect).
- **B4-5 · [Minor] · The insights digest's form is unowned** though three specs read it as an input — 004 maintains `insights/` but never defines the digest artifact readers load. Direction: name the digest file/shape in Key Entities.
- **B4-6 · [Minor] · "Well-made external GitHub courses" has no selection criteria** for `comparison/`. Direction: one assumption (reuse 002's reliability weighing).

---

## Part C — Per-spec optimization

### 000

- **C0-1 · [Major] · Phase the profile inventory.** FR-023/SC-011 require 4 validated profiles before any course has ever been generated — 3 of them for paradigms no course has requested, each needing its own SC-012 sample-topic validation. Keeps the settled one-core+profiles model intact: MVP = core + profile *mechanism* + default profile; ship PBL/CBL, CBE/mastery, guided-inquiry as later increments inside 000. Direction: split into user stories by profile, priority-ordered.
- **C0-2 · [Minor] · FR-006's verdict-rationale ledger and FR-019's provenance record are near-duplicates** — two auditable per-asset mappings. Direction: one classification table carrying verdict + rationale + provenance.
- **C0-3 · [Minor] · Missed reuse: the `mentor-research` skill** (already extracted, per `pedagogy/README.md`) is exactly the recording/tiering discipline FR-002/FR-004 re-invent for the critical-thinking filter. Direction: adopt it as the filter's recording format at plan time.
- **C0-4 · [Minor] · SC-008 duplicates 001 SC-003 verbatim** (template unchanged across builds) — same criterion owned twice. Direction: keep it in 001 (the actor that could violate it), reference from 000.

### 001

- **C1-1 · [Minor] · FR-013 is a special case of FR-023** (the spec says so: "generalizes the frozen-syllabus diff rule") — fold FR-013 into FR-023 as an example to remove a redundant requirement pair.
- **C1-2 · [Minor] · Decide concurrency's scope explicitly** (see B1-3): specify a minimal lock or move it to Out of Scope — half-owning it via an edge case is the worst position.
- **C1-3 · [Minor] · Name the `BUILD_PROGRESS.md` schema as a first-class deliverable** of 001's plan — 002 (B2-1) and 003 (FR-012) both write into it; a tiny published schema is the cheapest way to keep three specs from inventing incompatible status vocabularies.

### 002

- **C2-1 · [Major] · Missed reuse: the `mentor-research` skill was extracted expressly "for spec 002's own future research runs"** (`pedagogy/README.md`) yet 002 re-specifies the same discipline in FR-002/003/005 and never references it. Direction: make the skill the research method in 002's plan — one research discipline across 002, 000's filter, and 004's `comparison/`.
- **C2-2 · [Minor] · Platform name-search is the most fragile, lowest-yield research leg** (login walls acknowledged in Assumptions). Keep it, but sequence it last and explicitly degradable in the MVP slice — web + `gh` first, matching the DESIGN "prove out shallow research" step.
- **C2-3 · [Minor] · Right-sized otherwise** — 002 is the cleanest of the five; resist growing its side of the approval loop (present + revise only; loop control stays 001's).

### 003

- **C3-1 · [Major] · Build serial-first; make pool width a config.** The two-pairs-in-flight pool (fan-out/fan-in mediation, concurrent loop arbitration, ordered `BUILD_PROGRESS.md` writes) is the spec's largest complexity for what DESIGN itself lists as a calibratable knob ("parallel width (2)"). Direction: spec width as a parameter with MVP=1 and 2 as the target — every FR/SC except SC-003 survives unchanged.
- **C3-2 · [Minor] · The grounding/citation contract is restated three times** (003 FR-011 ≈ 002 FR-007/FR-011 ≈ 004 FR-007/FR-008) — drift risk across the quality owner and two consumers. Direction: make 004 the canonical citation/grounding contract; 002/003 reference it.
- **C3-3 · [Minor] · FR-016 duplicates FR-004's mentor stance** — merge into one requirement.
- **C3-4 · [Minor] · US3 (fake-student) is the only cross-cutting serialization in the phase** — if early real runs show low calibration yield, it's the natural deferral candidate; the settled gate-then-fan-out ordering governs it *given* it runs, not whether it ships in the first increment. Keep, but flag as the first knob to revisit after run #1.

### 004

- **C4-1 · [Major] · Split the spec to match the settled build order.** README already builds 004 in two chunks (rubric core before 003; delivery/harvest/comparison last), but one spec.md gates planning of four loosely-coupled subsystems — US1 (rubric + gate contract) is on 003's critical path; US3/US4 are post-MVP by the spec's own admission. Direction: either split into two features or mark US1 as an independently plannable increment so 003 isn't blocked behind harvest/comparison planning.
- **C4-2 · [Minor] · Fold rubric versioning into the template stamp** unless a rubric genuinely revs independently of the template — one version identity resolves A10 with less machinery.
- **C4-3 · [Minor] · `comparison/` should name its reuse of 002's research method** (weigh reliability, stable keys, converge-or-budget) rather than implying a third research discipline.
- **C4-4 · [Minor] · The harvest is nearly a one-command definition** (two user-invoked paths, append-only, no-op on empty) — keep it thin; FR-014–017 are already close to implementation-level detail.

---

## Challenges to settled decisions

**None.** Every settled seam-log decision holds up under review. Two of them, however, left **stale
text upstream** that must be reconciled *in the settled decision's favor*: the user-invoked-only
harvest vs constitution XII / DESIGN's "after each course/phase" (A8), and the terminal-state
fake-student trigger + gate-then-fan-out vs DESIGN step 4 (A8). And one settled rule
(forward-diff-only) is correct but **mechanically incomplete** — it needs the diff ledger and
consumer read-rule (A3) to be safe.

---

## Executive summary — before `/speckit-plan`

1. **Wire the profile seam downstream (A1):** 001 must select + record the profile, 002/003 must consume it — right now 000 delegates to specs that have never heard of profiles.
2. **Close the rubric evidence gap (A2):** the research digest covers structures only; run a rubric-focused research pass or explicitly re-scope 000 FR-013 before planning 000.
3. **Define forward-diff mechanics and put the course content into the delivery contract (A3, A6):** where diffs live, how 003's authors read them, and syllabus/lessons as required delivery artifacts.
4. Then: give `FEEDBACK.md` population and the factory's own `.claude/` an owner (A4, A5), and reconcile constitution/DESIGN with the settled 003/004 clarifications (A8, A9).
5. Biggest plan-time savings: phase 000's profiles, serial-first 003 pool, split 004 at the rubric/rest boundary (C0-1, C3-1, C4-1).
