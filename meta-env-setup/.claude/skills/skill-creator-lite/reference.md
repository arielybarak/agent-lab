# skill-creator-lite — deep-dive reference

On-demand companion to `SKILL.md`. Load this when authoring a non-trivial skill or
when a description won't score well and you need the gallery + checklist. Nothing
here is always-loaded, so it can be as detailed as it's useful.

---

## 1. The description is the product

Claude never sees a skill's body until it has already decided to load it — and it
decides **from the description alone**. So the description does two jobs at once:
*advertise what's inside* and *fire at the right moment*. Everything else is
secondary.

### Anatomy of a description that scores well
1. **Lead with distinctive domain nouns** — the specific things this skill is about
   (`ESP32-S3`, `log-Mel spectrograms`, `Design Compiler`), not generic words
   (`tasks`, `helper`, `code`). This drives the **specificity** sub-score.
2. **Add an explicit `USE WHEN …` clause** — the literal situations/phrasings that
   should trigger it. This drives the **trigger** sub-score.
3. **A negative trigger is allowed and powerful** — "NEVER use X for this" steers
   Claude away from a wrong tool.
4. **40–1024 characters.** Below 40 is too thin to route; above ~1024 wastes
   always-loaded budget.

### Gallery (real, `--score`-passing skills from this kit)
**Good — `audio-dsp-pipeline` (DL-Project):**
> Canonical audio/DSP conventions for this project — 16 kHz mono 3 s clips, log-Mel
> spectrograms, librosa params, SNR-controlled fall+water mixing, and the SAFE /
> FSD50K / WaterLeakage corpus. USE WHEN writing or reviewing preprocessing, feature
> extraction, augmentation, or anything that produces or consumes spectrograms.

✅ distinctive nouns (16 kHz, log-Mel, librosa, FSD50K) · ✅ explicit USE WHEN · ✅ a
clear boundary (what it covers).

**Good — `tinyml-deployment` (DL-Project):**
> ESP32-S3 edge-deployment constraints and the quantize/prune/export path … USE WHEN
> exporting a model, estimating whether it fits on-device, quantizing/pruning.

✅ names the hardware + the exact workflow it owns.

**Bad — what `--score` will dock:**
> A skill for audio tasks.

❌ no *when* (trigger 0.5 or 0.0) · ❌ no distinctive nouns (specificity tanks) · ❌
so generic it competes with every other skill (bad routing).

> Conventions and best practices for working with data in the project, including
> many useful tips you should always follow when doing data things.

❌ long but still vague — length ≠ specificity. Padding doesn't help; distinctive
nouns do.

### How triggering actually works (and why to lean assertive)
Two realities shape how you word the description:

- **Claude *under*-fires skills.** The common failure is not triggering when it
  should — not over-triggering. So state the trigger situations assertively: spell
  out the phrasings/contexts that should load it, and it's fine to add an explicit
  "use this whenever …". A description that's a little pushy beats a tasteful one
  that never fires. (This is what the **trigger** sub-score is nudging toward.)
- **Trivial tasks won't trigger *any* skill.** Claude only consults a skill for work
  it can't already do in one step — "read this file" won't load a skill no matter
  how perfect the description. Reserve skills for substantive, multi-step expertise,
  and don't over-tune wording for one-liners that will never route anyway.

---

## 2. Simple vs. complex — pick the smaller one that fits

| Choose **simple** (`SKILL.md` only) when… | Choose **complex** (folder + supporting files) when… |
|---|---|
| one focused capability | a multi-phase methodology |
| the quick-ref fits in the body | you have a gallery / checklist / templates to load on demand |
| no deep reference needed | the deep dive would bloat the always-relevant body |

For complex skills, **keep the deep material in a separate file** (like this one)
and point to it from `SKILL.md`. That's progressive disclosure: the body stays
scannable; the depth loads only when needed. (This skill is itself the example.)

### The three resource buckets
A complex skill's supporting files come in three kinds — name the right one:

| Bucket | Holds | Loaded |
|---|---|---|
| `scripts/` | executable code for deterministic/repetitive work | run on demand; never read into context |
| `references/` | docs/specs the model reads when it needs them (like this file) | read on demand |
| `assets/` | files used *in the output* — templates, icons, fonts | copied/used, not reasoned over |

**Bundle a repeated helper.** If every run of the skill ends up writing the same
throwaway script (a `build_chart.py`, a `convert.py`), ship it once in `scripts/`
and point the body at it — write it once instead of regenerating it each invocation.

### Budgets (concrete)
- **Metadata** (name + description) ≈ 100 words — *always* loaded, so every word
  costs routing budget in every session.
- **SKILL.md body** — keep under ~500 lines. Approaching that is the signal to split
  the depth out into a `reference.md`.
- **Reference files** — fine to run long, but add a short table of contents to any
  file over ~300 lines so the model can jump to the part it needs.

---

## 3. Writing the body

**Imperative, verb-first instructions** — the body is a procedure, not prose.
- ✅ "Quantize to int8, then check the tensor arena against PSRAM."
- ✅ "Split by source recording, never randomly."
- ❌ "You should probably consider splitting the data carefully."

**Be specific and actionable** — name the exact command, file, threshold.
- ✅ "Run `pytest tests/unit/models -q`."
- ❌ "Run the tests."

**Reference, don't duplicate** — the single most common bloat source.
- ✅ "Recall-first; see the rule in CLAUDE.md."
- ❌ [pasting the F2 = 0.9552 figures CLAUDE.md already states] → trips the
  redundancy check. Keep the pointer, cut the copy.

**Structure to aim for:**
```markdown
## When to Activate This Skill   — restate the trigger phrases
## <Core conventions / workflow>  — the imperative steps
## Gotchas                        — the non-obvious thing people get wrong HERE
## Supplementary resources        — point to deeper files (only if complex)
```

---

## 4. Skill vs. command vs. CLAUDE.md

Authoring a skill starts with checking it should even *be* one:

| It's a… | …when | Put it in |
|---|---|---|
| **skill** | situational expertise loaded on relevance | `.claude/skills/<n>/SKILL.md` |
| **command** | a repeatable workflow you keep invoking by name | `.claude/commands/<n>.md` |
| **CLAUDE.md rule** | an always-true project rule | repo `CLAUDE.md` |

If it's really one of the other two, stop and make that instead. (Pairs with the
`claude-setup-scaffolder` skill, which decides when each block earns its place.)

---

## 5. Anti-patterns (framework-agnostic)

1. **Vague description** — "a skill for development." No nouns, no triggers.
2. **Duplicating CLAUDE.md** — restating the brief instead of pointing to it.
3. **Missing `USE WHEN`** — Claude can't tell when to fire it.
4. **Non-imperative body** — "you should…" / "we will…" instead of "do X."
5. **Over-structuring a simple skill** — a deep-dive file for a 20-line skill.
6. **Under-structuring a complex skill** — a 400-line body that should split.
7. **Broken references** — pointing at files/paths that don't exist.
8. **No concrete examples** — only abstract instructions.
9. **Generic best practice** — advice true of every repo, specific to none. This is
   exactly what the **specificity** sub-score flags.
10. **Stopping at "looks good"** — never running `--score`. A skill the validator
    can't score well is a skill Claude probably won't trigger.

---

## 6. Quality checklist

**Before writing**
- [ ] Confirmed it's a *skill* (not a command or a CLAUDE.md rule) — §4
- [ ] No existing skill already covers this (don't duplicate — complement)
- [ ] Decided simple vs. complex — §2

**Description**
- [ ] States *what* + *when*, with real `USE WHEN` phrasings
- [ ] Leads with distinctive domain nouns; 40–1024 chars

**Body**
- [ ] Imperative, specific, actionable
- [ ] Encodes the non-obvious thing people get wrong *here*
- [ ] References CLAUDE.md rather than restating it
- [ ] Examples included; all file references resolve

**The measured loop (don't skip)**
```bash
python tools/validate_claude_setup.py <setup> --score
```
- [ ] **trigger** high (has what + when)
- [ ] **specificity** high (repo vocabulary, not generic)
- [ ] no **redundancy** flag (not echoing CLAUDE.md)
- [ ] (optional) add `evals/<repo>/routing-tests.json` and pass `--route`

Iterate on the **description first** — it's the highest-leverage text you'll write.

---

## 7. Worked example — read a real one

The fastest way to internalize all of the above is to read a skill that already
passes. Open `claude-setups/DL-Project/.claude/skills/audio-dsp-pipeline/SKILL.md`
and run:
```bash
python tools/validate_claude_setup.py claude-setups/DL-Project --score
```
Note how its description front-loads the nouns and the `USE WHEN`, how the body is
imperative, and how it *points to* CLAUDE.md's recall-first rule rather than copying
it. Then write yours to clear the same bar.
