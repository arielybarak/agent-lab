# Archetype profiles — the mechanism

A **profile** is a named, evidence-based *configuration over the one core*. It is not a second
template, and there is no per-subject fork of `.claude/`. Exactly **one** profile is selected per
course; a course that names none falls back to the profile marked `default: true` in
`manifest.yaml`.

## What a profile MAY set

Only these four dimensions vary. They are the ones the research digest identifies as genuinely
subject-dependent (§4 "Variables"):

| Dimension | What it decides |
| :--- | :--- |
| **Macro spine** | How units are organized end to end — a concept sequence, a revisiting spiral, a chain of problems/cases, a set of competencies |
| **Entry point** | Theory-first (explain, then apply) vs problem-first (authentic task first, ideas introduced as needed) |
| **Checkpoint placement & frequency** | Where the course pauses to consolidate, and how often — **advisory only** (see below) |
| **Unit granularity** | Fine-grained short units vs coarse units built around a large task or competency |

## What a profile MUST NOT do

- **MUST NOT redefine or bypass a core invariant.** The backward-design backbone, the canonical
  lesson arc, the feedback loops, and the rubric's core layer are the same under every profile. A
  profile that needs to change one of them is not a profile — it is a change to the core.
- **MUST NOT fork the core.** A profile adds configuration files under `profiles/<name>/`; it never
  ships its own copy of a core asset.
- **MUST NOT gate or lock learner progress.** The factory emits **static course content** — there
  is no runtime to enforce progression, and blocking the learner is not wanted. The strongest
  progression device a profile may embed is an **advisory checkpoint note**: *"recommended: work
  through this check before continuing."* Never a hard gate.
- **MUST NOT depend on an optional module.** A profile has to work with every module disabled.

## Adding a profile

1. Create `profiles/<name>/spine.md` stating the four dimensions above, plus the evidence the
   configuration rests on and its best-fit material types.
2. Register it under `profiles:` in `manifest.yaml` with its `entry_point` and `pieces`. Leave
   `default: true` on exactly one profile — zero or several defaults is a defect.
3. Validate it independently: walk two differently-shaped sample topics through it and confirm the
   macro-spine/checkpoint reconfiguration yields a coherent outline **without** touching a core
   invariant.

## Shipped profiles

- **`default`** — theory / linear-spiral. Ships with the template; the fallback for any course that
  names no profile.

Three further profiles the research flags as **structurally consequential** — **PBL/CBL**,
**CBE/mastery**, and **guided-inquiry/Socratic** — are planned as **later, independent increments**.
Each ships and validates on its own; none is required for a course to be generated, and none blocks
another.
