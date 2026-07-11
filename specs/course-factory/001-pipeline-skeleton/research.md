# Phase 0 Research — Pipeline & Instantiation spine

Design decisions for the factory's build spine. Each is stated as Decision / Rationale / Alternatives.
These resolve the plan's Technical Context; there are **no open `NEEDS CLARIFICATION` markers** — the
spec is Clarified (2 Qs, 2026-07-07) and its Assumptions settle the rest.

---

## R1 — Hybrid: deterministic tools for mechanical ops, `.claude/` commands for judgment

**Decision.** Split the deliverable in two. The **correctness-critical mechanical operations** —
copy-never-mutate + overlay + version stamp (FR-006/007), `BUILD_PROGRESS.md` read/validate/update
with legal-transition enforcement (FR-010/015/016/022), the lock marker (FR-028), version-stamp drift
compare, `DIFFS.md` append (FR-027), and delivery artifact-presence (FR-020) — are **stdlib Python
tools** under `course-factory/tools/`. The **judgment work** — the intake clarify interview, brief
authoring, profile/module selection, and the orchestration narrative — lives in `.claude/` commands
and agents that *call* those tools.

**Rationale.** The measurable Success Criteria are phrased as hard zeros: template modified **0**
times (SC-003), **0** completed units repeated on resume (SC-004), advance past a gate without a
recorded pass **0** times (SC-006), **0** concurrent advances (SC-012), halt-and-report **100%** on
bad state (SC-009). Those guarantees are only as strong as whatever enforces them. Leaving them to
agent free-form prose is precisely the anti-fabrication failure mode the constitution exists to catch
(Principle I/II). Mechanical operations are deterministic by nature; scripting them makes the SCs
*true by construction* and testable with `pytest`, and matches the repo's established shape
(`meta-env-setup/` = stdlib `tools/` called by `.claude/` commands). Judgment work is the opposite —
it *needs* the agent — so it stays in commands/agents.

**The pipeline state machine itself is part of the deterministic layer.** `progress.py` owns a pure
**transition function** — `(current state, phase gate result) → next state` — that *rejects* any
illegal move (an advance with no recorded gate pass, a phase skip, a backward move). This is what
makes an otherwise agent-driven pipeline mechanically verifiable: SC-006 (no silent skip), SC-007
(matched gate per phase), SC-010 (no re-opened phase), and SC-012 (no concurrent advance) are all
asserted by `pytest` feeding scripted gate results into this function — **no agent in the test
loop**. The `.claude/` driver (R2) supplies the gate results and the narrative; the *legality* of
every transition lives here.

**Alternatives considered.**
- *Pure-markdown pipeline (agent does everything, including file copies).* Rejected: the hard-zero
  SCs become "as reliable as the agent was careful this run"; not testable, not enforceable, directly
  the slop-factory risk.
- *Heavy framework / a real workflow engine.* Rejected: over-engineering for a single-machine,
  multi-session, file-backed pipeline; violates the repo's stdlib-only, simplicity-over-abstraction
  convention. The tool layer is kept to the four scripts above, nothing more.

This split is the plan's single load-bearing decision; the rest follow from it.

---

## R2 — Orchestration model: run-to-gate, then stop and persist (session-boundary-safe)

**Decision.** `/course-build <name>` is **not** a long-running daemon. It is a **single
start-or-continue entry** (no separate resume command — starting and resuming are the same act: read
state, do the next unit). On each invocation it: reads `BUILD_PROGRESS.md`, determines the current
phase, runs the next **unit of progress** (one phase's work via the seam, or one lesson), calls
`progress.py`'s transition function to compute + persist the next legal state **before** starting the
next unit, then either continues to the next unit or — when it reaches a gate that needs the user
(syllabus approval, the blocking post-skeleton scan, the round-cap accept-or-comment) — **stops and
reports**, leaving the build parked at that gate. The user re-invokes `/course-build <name>` to
continue. A fresh session with no memory resumes identically from `BUILD_PROGRESS.md` alone.

**Rationale.** Claude Code commands are prompt invocations, not processes that can block for hours
waiting on a human across a session boundary. "Pause and resume across sessions" (US3, FR-017/018)
therefore *is* the natural execution model, not a bolt-on: persist-before-advance (FR-016) means an
interruption at any point loses no progress (SC-004), and "stop at a user gate" is how a user gate is
honored without a blocking process. This also makes the two-session concurrency story concrete: the
lock marker is checked on entry and released at each parked point (R5).

**Alternatives considered.**
- *One monolithic command that tries to carry a whole build in a single turn.* Rejected: fragile
  across the long, multi-session reality; a crash mid-turn risks a half-written state file.
- *A polling loop that re-checks for user approval on a timer.* Rejected: there is no daemon to poll;
  the re-invocation *is* the resume signal.

---

## R3 — `BUILD_PROGRESS.md` format: human Markdown wrapping one fenced JSON state block

**Decision.** `BUILD_PROGRESS.md` is Markdown (human-scannable narrative) containing **exactly one
fenced ` ```json ` block** that is the machine-readable state: `template_version`, `current_phase`,
the ordered phase list with each phase's `gate_status`, the syllabus **sub-phase** status, the
per-lesson status list, the round counter for the active loop, the `lock` marker, and a `diffs_ref`
pointer. `progress.py` reads/writes **only** that block; the surrounding prose is regenerated from it
for human eyes. The full schema is published as `contracts/build-progress-schema.md` — a **first-class
deliverable of this plan** (spec Assumptions) so 002 (syllabus sub-phase status, its FR-018) and 003
(per-lesson status, its FR-012) write into a **shared, agreed vocabulary** instead of inventing
incompatible ones.

**Rationale.** Two consumers read this file: humans/agents (the narrative, when skimming) and
`progress.py` (the state). A fenced JSON block serves both — `json` is **stdlib** (repo convention:
no third-party deps), the schema is small and flat, and JSON forbids the whitespace/type ambiguity
that makes a hand-rolled YAML parser risky. The Markdown prose around the block stays human-first and
is regenerated from the block, so the two never disagree.

**Alternatives considered.**
- *YAML frontmatter parsed with PyYAML.* Rejected: PyYAML is a third-party dep; repo convention is
  stdlib-only. A hand-rolled YAML subset parser is more fragile than just using `json`.
- *A separate `.json` state file next to the Markdown.* Rejected: two files drift; the single
  `BUILD_PROGRESS.md` is the spec's named sole-source-of-truth (Key Entities), so state lives *in* it.

---

## R4 — Phase internals are a black box behind a seam; this spec ships stubs

**Decision.** Define one **phase-seam contract** (`contracts/phase-seam.md`) that every phase handler
honors: given the course folder + brief + prior gated artifacts (each read together with its
`DIFFS.md` entries, FR-027), the handler produces/updates its artifact(s) in the course folder and
returns a structured **gate result** (`pass` | `needs-user` | `loop` | `failed`, plus the round
count for looped phases). The orchestrator consumes only the gate result; it never looks inside a
phase. This spec ships **stub handlers** (write a placeholder artifact, return a scripted gate
result) for syllabus/skeleton/lesson/deliver. 002/003/004 replace the stubs **against the same
seam**, leaving the spine untouched.

**Rationale.** The spec's own US2 Independent Test says to "drive it through the phases with each
phase's work stubbed to 'produced + gate cleared'." A stable seam is what lets the four specs be
built in separate sessions (README's whole decomposition premise) and what makes the spine testable
today. It also encodes the ownership split for the refine loop: **001 owns** the round **counter**,
the cap-at-3 enforcement, and the accept-or-comment surfacing (FR-012); **003 owns** what one
author→critique→refine round *does*. The counter is state (001's `BUILD_PROGRESS.md`); the round
body is behind the seam (003's).

**Alternatives considered.**
- *Bake syllabus/lesson logic into the orchestrator now.* Rejected: that is 002/003/004's scope and
  would couple the spine to phase internals, breaking the split-across-sessions premise.

---

## R5 — Concurrency: an in-file lock marker, checked on entry, released at each parked point

**Decision.** The lock is a `lock: {holder, acquired_at, last_progress_at}` object inside
`BUILD_PROGRESS.md`'s state block (FR-028). Because a Claude Code session exposes no stable
tool-visible id, `/course-build <name>` **mints a per-invocation `holder` token** (short random value)
and acquires the lock with it via `progress.py`; it is refreshed on every persisted unit and
**cleared** when the build parks at a gate or exits cleanly. A session MUST NOT begin advancing a
course whose lock shows another holder within the **liveness window**; it surfaces the conflict
instead (SC-012). A **stale** lock (no `last_progress_at` update within a generous timeout) MAY be
reclaimed, and the reclaim is recorded. The token need only be unique per active invocation — the
lock is cleared at each park, so it is never expected to persist across a park boundary
(`contracts/build-progress-schema.md`).

**Rationale.** FR-028 asks for exactly this minimal marker, no more. Because state already lives in
`BUILD_PROGRESS.md` and is written after every unit (R2), the lock rides the same file and the same
write — no separate lockfile, no OS-level advisory lock (which wouldn't survive the file-is-truth,
resume-from-disk model anyway). Determinism in `progress.py` gives the 100% conflict-surfacing SC-012.

**Alternatives considered.**
- *OS file lock (`flock`).* Rejected: doesn't cross session/host boundaries and isn't reflected in
  the on-disk source of truth; a resumed cold session couldn't see it.
- *No lock (trust one-at-a-time).* Rejected: FR-028/SC-012 require an enforced, surfaced conflict.

---

## R6 — Template dependency + testability: a minimal frozen-template fixture

**Decision.** Spec 000 (the real `course-template/`) is not built yet, and 001 must not block on it
or define its content. Instantiation is coded against the **copy/overlay/version contract only**, and
tested against a **minimal template fixture** (`tests/fixtures/template-min/`: a `VERSION`, a
`manifest`, a `default` profile, and a couple of `.claude/` files with one topic-neutral placeholder
each). The fixture exercises: copy-byte-for-byte (SC-003), overlay-for-selected-profile (SC-002),
enabled-module inclusion, version stamping, and the **absent/unversioned → halt** edge (FR-001/SC-009).

**Rationale.** Mirrors how US2 stubs phase work: an in-repo stand-in lets the spine be built and
proven now, on the real recommended build order (000 → 001), without a circular wait. When 000 lands,
the same tool runs against the real template unchanged — the contract is what's fixed, not the
fixture.

**Alternatives considered.**
- *Wait for spec 000.* Rejected: needlessly serial; the copy contract is independent of the
  template's content.
- *Point tests at `System_Design_SelfLearn`.* Rejected: that's the unvalidated reference course, not
  a frozen template, and not topic-neutral; wrong shape for a copy-contract fixture.

---

## R7 — Forward-only movement: `DIFFS.md` is the ledger, gated phases never re-open

**Decision.** Once a phase's gate clears it is **immutable** (FR-023). Any later change to an earlier
gated artifact is applied as an **explicit forward diff at the current phase** and appended to
`DIFFS.md` via `diffs.py` — never by re-opening the phase. `DIFFS.md` is created as an empty stub at
instantiation (FR-008) and is append-only (FR-027). Downstream consumers (002/003/004) MUST read a
gated artifact **together with** its `DIFFS.md` entries, never the frozen artifact alone.

**Rationale.** This keeps the pipeline a strict forward sequence (SC-010) and gives a single audit
trail for every post-freeze change. The frozen-syllabus rule (FR-013) is just the first instance of
this general rule, so there is one mechanism, not two. Append-only + deterministic writer means the
ledger can't be silently rewritten.

**Alternatives considered.**
- *Allow re-entering a passed phase to edit in place.* Rejected: violates FR-023/immutability and
  loses the audit trail; re-flow risk on long multi-session builds.
