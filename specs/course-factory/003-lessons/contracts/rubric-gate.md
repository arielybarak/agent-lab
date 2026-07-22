# Contract — rubric-gate consumption (what 003 needs from 004's rubric)

**Owner of the rubric:** spec 004 (Principle VIII — the one rubric, two layers). **This file** is
003's **thin consumption contract**: the minimum the lesson evaluator needs from the rubric to gate a
lesson, published now because 004 has only a `spec.md` and no machine-readable rubric yet. 003 validates
its lesson gate against a **rubric fixture** shaped to this contract (research R5), and this contract is
the seam 004's rubric core must satisfy when it lands. **003 MUST NOT define or redefine the rubric's
contents** (FR-010) — it consumes the two properties below and nothing more.

## Property 1 — a pass is a per-dimension threshold (004 FR-004)

- The rubric is a **generic core** (correctness, grounding, flow, coverage, practicality) **plus** any
  **topic add-ons** the course spec requested (Principle VIII, 004 US1).
- A lesson **passes** only if **every** dimension (core + requested add-ons) clears **its own** minimum
  bar. A strong dimension **MUST NOT** mask a failing one — there is no aggregate/average that lets a
  low dimension slide (004 FR-004, README seam log).
- Per-dimension scores are **retained** even though the gate is the all-clear boolean — the lesson
  evaluator carries them into the best-effort scorecard it emits at the cap (FR-002).

003's use: `lesson-evaluator` treats "rubric passes" as *every dimension ≥ its threshold*. It reads the
dimensions + thresholds from the rubric (fixture today, 004's real rubric later); it never invents a
dimension or a threshold.

**The predicate is 004's code, not 003's prose.** 004 implements this rule once, as
`course-factory/tools/rubric_gate.py` (004 `contracts/rubric-grading-semantics.md`), and 004 SC-009
requires exactly one copy of it: *"003's lesson gate and 004's course-evaluator call this **same**
function — there is not a second copy of 'every dim ≥ threshold.'"* So the division of labour is:

| Side | Responsibility |
| :--- | :--- |
| 003's `lesson-evaluator` (agent) | supplies the **per-dimension scores** — judgment |
| 004's `rubric_gate.py` (tool) | decides **passed / not passed** from those scores — mechanics |

003's `lesson-phase` skill calls the tool and gates on its result. It MUST NOT restate the rule in
agent prose: a prose copy cannot guarantee the no-aggregate-masking invariant (004 SC-010) and drifts
the moment 004 revises a threshold. 004's rubric core is built **before** 003 (README build order), so
the tool is available at 003's build slot; before that it runs against `tests/fixtures/rubric/`.

**Where the rubric physically lives.** The rubric is a **mandatory-core asset of the frozen template**
(Principle IX; its version identity *is* the template's version stamp, Principle VIII / 000 FR-016), so
it is **copied into the course** at instantiation (001's copy step) and read from the course's `.claude`
residue in `course_dir` — the lesson evaluator does **not** fetch it from 004's spec or a central
location. Until 000/004 ship, the fixture under `tests/fixtures/rubric/` stands in for that copied
asset.

## Property 2 — grounding is part of grading, via the canonical citation check (004 FR-007/FR-008)

- The evaluator checks **citation traceability for every `[Sn]` key** in the lesson — that each resolves
  to a real `SOURCES.md` entry — verifying **tracing, not truth**. Exhaustive, not sampled, because
  resolution is a cheap mechanical lookup (004 FR-007, 003 FR-011, SC-004).
- A claim explicitly marked **mentor-added** MUST NOT be failed merely for lacking an `[Sn]`; 002's
  **thin-grounding flags** are preserved, never re-presented as sourced (004 FR-008, 002 FR-011).

003's use: this is the **same canonical check** implemented in `citation_trace.py` and shared across
002/003/004 (research R2) — 003 does not author a second grounding rule. An unresolvable citation is a
**hard gate failure**: the lesson does not pass until the citation resolves or the claim is removed
(SC-004), independent of the rubric's per-dimension scores.

## What this contract deliberately leaves to 004

- The **exact dimensions**, their **thresholds**, and the **scoring scale** — 004's, not 003's.
- The **topic add-on mechanism** (how a spec requests an add-on dimension) — 004's US1.
- The **course-level** verdict (whole-arc coverage/flow/running-example, 004 FR-009) — that is
  delivery-time grading, not the per-lesson gate 003 consumes.

## Fixture stand-in (until 004 ships)

`tests/fixtures/rubric/` holds a **minimal** rubric shaped to Properties 1–2: a handful of named
generic-core dimensions each with a threshold, and one requested topic add-on, expressed so the lesson
evaluator's pass predicate (*every dimension ≥ threshold* **and** *every `[Sn]` resolves*) is testable
today. When 004 lands its rubric core, the fixture is replaced by 004's rubric; the pass predicate and
the citation check are unchanged (that is the point of pinning only these two properties).
