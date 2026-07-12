# Phase 0 Research — Syllabus Phase

The design decisions behind the plan. Each is Decision / Rationale / Alternatives, in the format the
plan workflow prescribes. There were **no `NEEDS CLARIFICATION` markers** in the spec (both were
closed in the 2026-07-07 clarify session — FR-005 budget unit, FR-011 thin-grounding policy); this
Phase 0 instead resolves the *design* unknowns the plan must settle before Phase 1.

---

## R1 — Where determinism earns its place (the tool/skill split)

**Decision.** Put in stdlib Python **only** the checks whose Success Criteria are stated as
**100% / 0-exception** and are therefore falsifiable by inspection of an artifact, and leave every
judgment call in the `.claude/` surface. Concretely, three tools:

| Tool | Guarantees (mechanical) | SC |
| :--- | :--- | :--- |
| `research_budget.py` | Research stops at the cap; the stop decision is a pure function of the logged query count. | SC-002 (0 unbounded) |
| `sources_lint.py` | Every `SOURCES.md` entry has a stable `[Sn]` key **and** a recorded reliability judgment. | SC-001 |
| `syllabus_lint.py` | Every syllabus topic traces to `[Sn]` or is tagged mentor-added; a divergence assessment is present; thin-grounding flags imply every affected topic is mentor-tagged; `lesson_format` is set in the brief. | SC-003, SC-005, SC-008, SC-004 |

**Rationale.** This is the exact discipline 001 recorded in *its* R1: the NON-NEGOTIABLE / measurable
outcomes must be *mechanically* observable, not left to agent good behavior, or the SC is unfalsifiable.
Anti-fabrication (Principle II) is the spec's whole point — "no silently ungrounded topics" is worth a
linter, not a hope. Keeping the tools thin (three small validators + one counter, no framework) honors
the repo's stdlib-only, minimality-over-abstraction convention.

**Alternatives considered.**
- *All-agent, no tools* — rejected: SC-001/002/003/008 become agent-attestation, not verifiable; the
  same reason 001 built `progress.py` instead of trusting narrative.
- *A heavier "syllabus engine"* — rejected: the composition itself is irreducibly judgment (R2); a big
  tool layer would either duplicate agent judgment or falsely mechanize it.

## R2 — What must stay agent judgment (and why it is not a testing gap)

**Decision.** Reliability weighing (FR-002), compose-as-mentor with staleness correction (FR-006), the
convergence call (FR-005), and the divergence call (FR-012) stay in the `.claude/` surface and are
validated by **scenario walkthroughs** in `quickstart.md`, not by `pytest`.

**Rationale.** These are the domain-mentor decisions the whole factory exists to add over a naive
aggregator (Principle III). A unit test asserting "this source is reliable" would just re-encode a
judgment as a fixture and prove nothing. What *can* be mechanized is the **shape** of the judgment's
output — that a reliability judgment was recorded, that the divergence assessment names the sources
compared — and R1's linters do exactly that. So the boundary is: **tools check that judgment happened
and left an auditable trace; humans/scenarios check the judgment was good.** This mirrors 001, whose
intake interview quality is a scenario, while its state legality is a pure function.

## R3 — The divergence ask is inline in the handler, not a seam `needs-user` park

**Decision.** The post-research divergence question (FR-012, ask-moment #2) is asked **inline within
the syllabus-phase handler's own run** (via the interactive harness), **not** surfaced to the
orchestrator as a `needs-user` park. Only the **user-approval review** goes through the seam's
`needs-user`.

**Rationale.** Ask-moments and gates are, by constitution IV's explicit carve-out and README seam #8, a
**distinct category**. 001's seam enumerates the three `needs-user` causes it recognizes — syllabus
approval, the blocking post-skeleton scan, the round-cap accept-or-comment — and the divergence ask is
**not** among them, by design: it is 002-owned content (the spec assigns 002 "the trigger + content of
the post-research divergence question"), not a 001-owned gate. Routing it through 001's park machinery
would (a) require an orchestrator change 002 is forbidden to make and (b) miscategorize an ask-moment as
a gate. Handling it inline keeps the two categories clean and keeps the orchestrator untouched.

**Resumability consequence (handled, not a gap).** The fixed sub-phase enum (`research-in-progress` /
`research-done` / `composed` / `presented`, owned by 001's schema) has **no** distinct
"awaiting-divergence-answer" state — and must not grow one, since that would be a forward-diff against
001's `build-progress-schema.md`. The inline ask therefore happens while the sub-phase reads
`composed`: composition is done, the divergence assessment (converged/diverged + sources compared) is
already written into `SYLLABUS.md`'s composition notes (SC-005), and the pending directional question
is recorded there too. A session that dies mid-ask resumes at `composed`, sees the recorded pending
question, and re-asks — cheap, because the assessment is already on disk. This is the one place the
handler blocks on the user *without* parking; it is deliberate and documented in `contracts/syllabus-handler.md`.

**Lock interaction (persist-before-block).** Because the `composed` checkpoint is persisted *before*
the inline ask, the block is safe against 001's lock **stale-reclaim**: a long ask refreshes no unit, so
another invocation MAY reclaim the stale lock, but it resumes at `composed` and re-asks with no lost or
double-applied answer. 001's lock contract now states this persist-before-block rule explicitly (001
`build-progress-schema.md` § "Blocking on inline user input vs. the lock"), ratifying the coupling
rather than leaving it implicit.

**Alternatives considered.**
- *Route the divergence ask through `needs-user`* — rejected: needs an orchestrator change (out of
  002's scope) and collapses the ask-moment/gate distinction the constitution draws.
- *Add a fifth sub-phase state* — rejected: forward-diff against 001's frozen schema contract; the
  `composed`-with-recorded-pending-question encoding avoids it entirely.

## R4 — The budget counter's honesty boundary (stated, not hidden)

**Decision.** `research_budget.py` maintains a persistent counter (a small JSON/plain-text log in the
course folder, e.g. `.syllabus-research-log`) that the research skill **increments before each
query**; the tool's `remaining()` / `exhausted()` calls are a pure function of that log. The skill is
disciplined to route every web / `gh` / platform query through the increment step; the tool is the
**mechanical backstop** that refuses "continue researching" once the log hits the cap.

**Rationale — and the honest limit.** A Claude Code skill can call `WebSearch` / `gh` directly, so no
tool can *intercept* a query the skill forgets to log — the counter is exactly as complete as the
skill's logging discipline. This is the same class of limit 001 stated plainly for its `lock.holder`
token (no stable session id, so a per-invocation token is "good enough" and the limit is documented).
The mechanical guarantee 002 can honestly claim is therefore: **given the query log, the stop decision
is deterministic and testable (SC-002 asserts stop-at-cap over a log fixture)**; the completeness of
the log is skill discipline, reinforced by making the increment the *same call* that returns the next
query's go/no-go. We do **not** claim the counter magically bounds an undisciplined agent.

**FR-019 consequence.** Post-divergence re-research (FR-019) charges the **same** counter — the tool
exposes no "reset"; re-entry after the divergence answer continues from the existing count, and
`exhausted()` then forces the thin-grounding path (FR-011) instead of a fresh budget. `test_research_budget.py`
asserts a re-research call after a divergence answer cannot exceed the original cap.

## R5 — Reuse `mentor-research`, re-homed; do not author a second research method

**Decision.** The research sub-phase (FR-001–005) is the existing **`mentor-research`** skill applied
to per-course syllabus grounding. It is **copied verbatim** from repo-root `.claude/skills/mentor-research/`
into `course-factory/.claude/skills/mentor-research/` (the skill's own re-home note instructs exactly
this, "once spec 001 scaffolds the factory's own environment"); 002 is that consumer. The
syllabus-phase handler *invokes* it; it is not rewritten.

**Rationale.** The spec's Assumptions name this reuse explicitly ("rather than inventing a second
method"), and DESIGN's "reuse research discipline across scopes" principle says the same. The skill
already encodes weigh-reliability, `[Sn]`/`[Pn]` namespace separation, dedupe-by-work, tier-with-caveats,
boundary-conditions, and converge-or-budget — precisely FR-001–005. `[Sn]` (per-course) and `[Pn]`
(cross-course pedagogy) namespaces are declared non-colliding by the skill itself.

**Boundary note.** `mentor-research`'s identity-verification step (Crossref/ERIC/NCBI) is written for
academic citations; for course-platform and GitHub sources 002 applies the skill's *general* weigh +
mark-what-you-couldn't-verify discipline (a repo's reliability is stars-as-green-flag + inspection, not
a DOI lookup). `contracts/sources-schema.md` states this so `sources_lint.py` does not demand a DOI on
a GitHub entry.

## R6 — Validate against fixtures now; live research is deferred to real runs

**Decision.** Like 001, validate the deterministic layer against **hand-authored fixtures** and the
judgment layer against **scenario walkthroughs**, not a live research run. Fixtures: `SOURCES.md`
samples (well-formed / missing-key / reliability-absent / duplicate-work), `SYLLABUS.md` samples
(fully-traced / silently-ungrounded / thin-grounding / missing-divergence-assessment), a query-log at
and over budget, and a diverging-vs-agreeing source pair for the ask-fires-only-on-divergence scenario.

**Rationale.** 000 (the template/profile) and 001 (the factory `.claude/`) are not built, and DESIGN's
roadmap task #5 ("prove out shallow research") is an explicit *later* step gated on real runs.
Fixtures make every mechanical SC testable today without a network round-trip or a live template, and
keep the plan honest about what is proven now vs. calibrated later (budget value, convergence
heuristic — both flagged calibratable in the spec Assumptions).

## R7 — FR-017's read discipline is honored structurally, though vacuous at first compose

**Decision.** The handler always reads prior gated artifacts **as `frozen + DIFFS.md`** via the seam's
`prior_artifacts` field (FR-017), even though **at initial syllabus composition there is no gated
predecessor** — syllabus is the first gated phase; `COURSE_BRIEF.md` is pre-state, not gated.

**Rationale.** FR-017 is a general read-discipline rule (README seam #6). For 002 its *live* effect is
downstream: 002's own frozen `SYLLABUS.md` + its `DIFFS.md` entries become the paired canonical read
for 003 (003 FR-007) and for any later forward-diff against the syllabus. Encoding the pairing in the
handler now (a) costs nothing when `prior_artifacts` is empty and (b) means the handler is already
correct if a future forward-diff re-enters the syllabus phase carrying diffs. Recorded here so the
apparent "unused" pairing is understood as forward-looking, not dead.
