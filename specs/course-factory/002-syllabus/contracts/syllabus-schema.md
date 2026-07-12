# Contract — `SYLLABUS.md` shape

**Owner:** spec 002 (the headline artifact). **Consumers:** the **User** (approval gate, via 001), 003
(reads the frozen syllabus **+ its `DIFFS.md`** as canonical input, 003 FR-007), 001 (freezes it,
presents later changes as diffs). **Enforced by:** `syllabus_lint.py` (SC-003/004/005/008). On-disk
identity: `SYLLABUS.md` at the course-folder root (a required delivery artifact, 001 FR-020).

## File shape

Human-readable Markdown — the course shape a user reviews. Two required parts:

### 1. The course shape (phases → lessons → arc)

Organized per the **selected archetype profile's** macro spine and entry point, with the profile's
**advisory** checkpoint notes where it places them (FR-015; profile checkpoints are advisory only, never
gating — Principle IX). Reuses the mandatory-core invariants (lesson arc, running-example thread) without
redefining them (000 FR-024). Sets the course **volume** — approximate phase / lesson count — grounded
in the brief's stated depth (FR-008).

Every **topic** line carries **one** of:
- a `[Sn]` citation resolving into `SOURCES.md` (a grounded topic), **or**
- a `mentor-added` tag (judgment the sources did not supply — FR-006/007).

There is **no** third option: a topic with neither **fails** the lint (SC-003, 0 silently ungrounded).

### 2. Composition notes (the audit trail)

A dedicated section carrying, on **every** run:

| Note | Rule | SC |
| :--- | :--- | :--- |
| **Divergence assessment** | `converged` or `diverged`, **naming the top-weighted sources compared**. Present on every run — the fire/no-fire decision for ask-moment #2 is auditable after the fact (FR-012). | SC-005 |
| **Grounding-stop note** | How research halted: `converged` (sources stopped adding topics) or `budget-capped` (the FR-005 cap hit first). When `budget-capped`, the syllabus notes grounding was **capped, not converged** (edge case). A separate axis from thin-grounding: a capped run may still be well-grounded, and a converged run may still be thin. | — |
| **Thin-grounding flag** | If research yielded too little reliable grounding, flag the course (or the named affected sections) as `thinly-grounded` (FR-011). | SC-008 |
| **Pending directional question** | While an ask-moment-#2 question is open (diverged, not yet answered), record it here so a resumed session re-asks (R3). Removed once answered. | — |
| **Volume-deviation note** | If the topic cannot support (or vastly exceeds) the brief's requested depth, record the corrected volume + the deviation (edge case, FR-008). | — |

## What `syllabus_lint.py` enforces

1. **SC-003** — every topic line has a `[Sn]` **or** a `mentor-added` tag; else fail. A cited `[Sn]`
   must **resolve** — the key must exist in the course's `SOURCES.md` (a cross-file check, not just a
   `[Sn]`-shaped token). A topic citing a **non-existent** key (e.g. `[S99]` absent from `SOURCES.md`)
   fails: "traceable" (SC-003) means the trace actually lands, so a dangling citation is not grounding.
2. **SC-008** — if a `thinly-grounded` flag is present, **every** topic in the flagged scope is
   `mentor-added`; a sourced claim under a thin flag fails (thin grounding never fabricates sourced
   claims, FR-011).
3. **SC-005** — a divergence assessment naming the compared sources is present.
4. **SC-004** — `COURSE_BRIEF.md.lesson_format` is set to `.md` or `.ipynb` (checked here because the
   format decision is part of the syllabus-phase output, FR-009).

## Freeze & forward-diff compatibility (001-owned mechanics)

002 keeps `SYLLABUS.md` in a form that supports 001's **diff-based** change presentation after freezing
(FR-014): stable topic identifiers (the `[Sn]`/`mentor-added` line structure) so a later forward diff
(001 FR-023/027) reads cleanly against the frozen file. 002 **does not** freeze, re-open, or edit a
frozen syllabus itself — a post-freeze gap surfaces as a `DIFFS.md` entry at the current phase (001's
act), and the canonical downstream read is always **frozen `SYLLABUS.md` + its `DIFFS.md`** (never the
frozen file alone).
