---
name: skill-creator-lite
description: >-
  Author a new Claude Code skill (.claude/skills/<name>/SKILL.md) that actually
  triggers and pulls its weight — write a trigger-rich what+when description,
  encode the non-obvious thing people get wrong (not generic best practice), then
  measure it with tools/validate_claude_setup.py --score and sharpen until it
  scores well. USE WHEN creating, updating, or improving a skill, writing a skill
  description, or deciding what belongs in a skill vs. CLAUDE.md.
---

# Skill Creator Lite (kit-native, measured)

A skill is on-demand expertise Claude loads **only when relevant**. Its whole job
is to (1) get **picked at the right moment** and (2) say the thing a newcomer to
*this* repo would get wrong. This skill makes that a measured loop, not a guess —
it ends at `--score`, not at "looks good."

## When to Activate This Skill
- "Create / add / write a skill for X"
- "Improve / sharpen this skill (or its description)"
- "Should this be a skill, a command, or just CLAUDE.md?"

## Step 0 — capture intent (don't skip to scaffolding)
A skill comes out generic when you skip this. Before scaffolding, pin down:
1. **What** should it let Claude do? (one specific capability, not a theme)
2. **When** should it fire? (the literal phrasings/contexts → these become the `USE WHEN`)
3. **What does it touch?** (tools, files, commands it depends on)
4. **What's the non-obvious thing people get wrong *here*?** — the most important
   answer. If there's no repo-specific failure mode, it may not deserve a skill
   (it's generic best practice, and `--score` specificity will say so).

If the conversation already shows the workflow (the user said "turn this into a
skill"), mine the answers from history first and just confirm the gaps.

## The loop (scaffold → fill → score → sharpen)

```bash
# 1. Scaffold the skeleton (valid frontmatter from the start)
python tools/scaffold_claude_setup.py add skill <name> --dir <setup> --desc "<what + when>"

# 2. Fill in the body (see structure below)

# 3. MEASURE — this is the step the old framework lacked
python tools/validate_claude_setup.py <setup> --score

# 4. Sharpen until the description scores well, then (optionally) prove it routes:
python tools/validate_claude_setup.py <setup> --route   # if you add evals/<repo>/routing-tests.json
```
Read the `[SCORE]` output: aim for high **trigger** (has *what* + *when*), high
**specificity** (uses this repo's vocabulary, not generic words), and no
**redundancy** flags (don't restate CLAUDE.md). Iterate on the description first —
it's the highest-leverage text in the whole skill.

**When `--score` is low, read the symptom and fix it directly:**

| Symptom | Fix |
|---|---|
| low **trigger** | add an explicit `USE WHEN …`; name the real phrasings/contexts |
| low **specificity** | too generic — lead with distinctive domain nouns from CLAUDE.md, cut filler words |
| **redundancy** flag | you copied figures/rules CLAUDE.md already states — replace the copy with a pointer |
| over **budget** | trim this description (and other blocks' too) — every description is always-loaded |

## Write the description first (Claude routes on it)
State **what it does** AND **when to fire it**. Pack in the real trigger phrases.

- ✅ `Canonical audio/DSP conventions for this project — 16 kHz mono 3 s clips, log-Mel
  spectrograms, librosa params. USE WHEN writing or reviewing preprocessing, feature
  extraction, or anything that produces spectrograms.`
- ❌ `A skill for audio tasks.` (no *when*, no distinctive nouns → won't route, scores low)

Rules of thumb: lead with distinctive domain nouns; add an explicit `USE WHEN …`
clause; a strong negative trigger ("NEVER use X for this") is fine; 40–1024 chars.
**Lean assertive** — Claude tends to *under*-fire skills, so spell the trigger
situations out plainly rather than hinting at them (see `reference.md` §1).

## Body structure (keep it sharp)
```markdown
## When to Activate This Skill   — the trigger phrases, restated
## <Core conventions / workflow>  — imperative, verb-first ("Quantize…", "Split by room…")
## Gotchas                        — the non-obvious thing people get wrong HERE
```
**Simple skill** = `SKILL.md` only. **Complex skill** = a folder with `SKILL.md`
plus supporting files in `scripts/` (executable), `references/` (load-on-demand
docs), or `assets/` (output templates), referenced on demand. Keep the body under
~500 lines and push depth into a `reference.md` (progressive disclosure — see
`reference.md` §2 for the resource buckets and budgets).

## The quality bar (what "good" means here)
- Encodes **the thing people get wrong in this repo**, not generic best practice
  (generic filler is exactly what `--score` specificity flags).
- **Don't restate CLAUDE.md** — point to it. Copied figures/rules trip the
  redundancy check; keep the pointer, cut the copy.
- One sharp skill beats three vague ones — every description costs routing budget.
- Imperative instructions; concrete examples; references resolve.

## Supplementary resources (load on demand)
For the full **description gallery** (real good/bad examples), the **anti-pattern
list**, the simple-vs-complex decision, and the **quality checklist**, read
`reference.md` in this folder. It's intentionally detailed — it loads only when
you're actually authoring a skill, so it costs no routing budget. (This split is
itself the "complex skill" pattern this skill teaches.)

## Gotchas
- **This is Claude Code, not a "PAI/Kai" setup** — skills live in
  `.claude/skills/<name>/SKILL.md`; there is **no** `KAI.md` / `${PAI_DIR}` /
  "available_skills" registry to update. Claude discovers a skill from its
  `description` alone, so that text *is* the product.
- A skill the validator can't score well is a skill Claude probably won't trigger.
  Treat a low **trigger** sub-score as a real defect, not a nitpick.
- If a "skill" is really a repeatable command you keep invoking, make it a slash
  **command**; if it's an always-true project rule, it belongs in **CLAUDE.md**.
  Pairs with the `claude-setup-scaffolder` skill (when each block earns its place).
- **`--score` is static** — it predicts whether a skill *routes*; it doesn't run
  Claude, so it can't confirm the skill actually triggers or improves output in
  practice. Treat a good score as a strong signal, not proof — sanity-check the new
  skill on a real prompt or two before trusting it.
