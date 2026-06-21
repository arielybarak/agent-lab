# Setup Spec — <repo>

> A short PRD for the setup, produced by the analysis step **before** scaffolding.
> It makes authoring far better (the `block-author` writes against it) and gives the
> `setup-critic` a coverage checklist. Save the filled copy to
> `claude-setups/<repo>/SETUP-SPEC.md`. Cite real files/commands throughout — every
> claim should be grounded in the repo.

## 1. What the repo is
- **Domain / purpose:** …
- **Language(s) & stack:** …
- **Maturity:** (greenfield / active / frozen submission / teaching) …
- **How it's run** (cite the real files): build `…` · test `…` · lint `…`
  (from `pyproject.toml` / `package.json` / `Makefile` / CI).

## 2. The one rule that overrides others
> The project-specific principle a newcomer would violate. Goes at the TOP of CLAUDE.md.

… *(e.g. "recall-first — optimize F2, never trade recall for accuracy"; "project-A is
frozen"; "no logic in notebooks")*

## 3. Repetitive workflows  → candidate commands
| Workflow done over and over | Command |
|---|---|
| … | `/…` |

## 4. Failure modes (where people get it wrong) → skills / agents / hooks
| Failure mode (cite where it bites) | Block that prevents it | Type |
|---|---|---|
| … | … | skill / agent / hook |

## 5. Existing setup → complement, don't duplicate
- Present already: `.claude/` ? `AGENTS.md` ? `.github/agents` ? `skills/` ?
- **Do NOT add** … (already covered by …).

## 6. The decided block list (with one-line rationale each)
Pick from the [cookbook](../cookbook/README.md) archetypes; justify each block in one
line — if you can't, cut it.

- **CLAUDE.md** — outline: overriding rule → what it is → layout → commands → conventions → gotchas.
- **Skills** (2–4): `name` — why it earns its place (archetype: …).
- **Commands**: `/name` — the paragraph it replaces.
- **Agents**: `name` — scope + least-privilege `tools:` (archetype: …).
- **Hooks**: `name` — what it guards; advisory or blocking.

## 7. Effectiveness targets (the exit condition for /refine-setup)
- `validate` clean · composite **≥ 85** · 0 `[CUT?]` · routing **100%**
- Every failure mode in §4 maps to a block in §6.
- (Optional) `--ablate --execute`: no block flagged `CUT`.
