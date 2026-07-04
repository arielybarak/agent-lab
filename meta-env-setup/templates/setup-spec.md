# Setup Spec — <repo>

> A short PRD for the setup, produced by the analysis step **before** scaffolding.
> It makes authoring far better (the `block-author` writes against it) and gives the
> `setup-critic` a coverage checklist. Save the filled copy to
> `claude-setups/<repo>/SETUP-SPEC.md`. Cite real files/commands throughout — every
> claim should be grounded in the repo (in **greenfield mode** the claims are openly
> *predictions from stated intent* instead — say so).

## 0. Mode & maturity
- **Mode:** code-bearing / **greenfield** (empty except README/about) — with the
  numbers that decided it: `<N source files>`, `<N commits>`.
- **Maturity:** greenfield / active / frozen submission / teaching.
- **Owner answers (from the interview):** the analyzer's determinant-9 questions and
  what the owner said — where time is burned, what's coming next, team size, what must
  never break, tooling already rejected. The block list below must be consistent with these.

## 1. What the repo is — and its domain inner loop
- **Domain / purpose:** …
- **Language(s) & stack:** …
- **How it's run** (cite the real files): build `…` · test `…` · lint `…`
  (from `pyproject.toml` / `package.json` / `Makefile` / CI).
- **Domain inner loop:** the function chain that turns input → the product artifact
  (mesh / image / PDF / dataset / binary / model) — cite the module/functions. Note
  any timing prints, the parseable artifact it emits, and the expensive/nondeterministic
  upstream stage that could be **stubbed** for an offline bench.

## 2. The one rule that overrides others
> The project-specific principle a newcomer would violate. Goes at the TOP of CLAUDE.md.

… *(e.g. "recall-first — optimize F2, never trade recall for accuracy"; "project-A is
frozen"; "no logic in notebooks")*

## 3. Repetitive workflows  → candidate commands
| Workflow done over and over (cite transcript cluster if any) | Command |
|---|---|
| … | `/…` |

## 4. Failure modes (where people get it wrong) → skills / agents / hooks
| Failure mode (cite where it bites) | Block that prevents it | Type | Cost per miss |
|---|---|---|---|
| … | … | skill / agent / hook | how expensive one miss is (see §6) |

## 4b. Silent-drift / parity invariants
> Two+ structures that must stay in lockstep and fail with no error (parallel locale
> dicts, vendored copies, config mirrored across files). Each → a read-only parity check.

- … (cite the sibling structures) → `/…`

## 5. Feedback-loop economics
> The cost of one validation iteration, per path. Where the cheapest "did it work?"
> runs through an expensive remote round-trip (deploy, cloud rebuild, GPU), a local
> pre-push gate is the highest-leverage block.

- **Slowest/most expensive loop:** … (cite deploy/push script, rebuild time, model load)
- **Pre-push gate proposed?** yes/no → `/…` (what offline checks it bundles)

## 6. Direction of travel & product value
- **Next bulk of work** (cite `IMPROVEMENTS.md` / `ROADMAP` / issues / recent git log): …
- **Core product value that must never break** (→ a non-negotiable gate): …

## 7. Environment prerequisites (probed)
> For every block that must execute, the runtime dep and whether it's present here.

| Block | Needs | Present in this env? | If missing |
|---|---|---|---|
| … | `chromium` / GPU / lib | `which …` result | prerequisite to install / flag UNTESTED |

## 8. Existing setup → complement, don't duplicate (+ freshness)
- Present already: `.claude/` ? `AGENTS.md` ? `.github/agents` ? `skills/` ?
- **Stale?** blocks whose cited nouns no longer grep in the code (`--stale --repo`) → REWRITE.
- **Do NOT add** … (already covered by …).

## 9. The decided block list (with one-line rationale + target each)
Pick from the [cookbook](../cookbook/README.md) archetypes; justify each block in one
line — if you can't, cut it. **Target** = `active` · `tools-pool/<topic>` (fully-built,
parked for a later phase) · `deferred (trigger: <condition>)` (greenfield — noted, not built).

- **CLAUDE.md** — outline: overriding rule → what it is → layout → commands → conventions → gotchas.  · target: active
- **Skills** (2–4): `name` — why it earns its place (archetype: …).  · target: …
- **Commands**: `/name` — the paragraph it replaces.  · target: …
- **Agents**: `name` — scope + least-privilege `tools:` (archetype: …).  · target: …
- **Hooks**: `name` — what it guards; advisory or blocking.  · target: …

## 10. Smoke-test results
> Every command is executed once before packaging (item: smoke-test mandate). Record
> the outcome; a command that fails on first run goes back to the author.

| Command | Result | Note |
|---|---|---|
| `/…` | PASS / PASS-dry-run / UNTESTED | why (e.g. needs GPU quota → dry-run) |

## 11. Re-analysis trigger (greenfield / evolving repos)
> When should this setup be re-analyzed? The first real analysis of a greenfield repo
> can only happen once code exists; evolving repos drift after big migrations.

- Re-run `/new-claude-setup` (or `/upgrade-claude-setup` once a backlog exists) when: …
  *(e.g. "> ~N source files land", "the first real feature ships", "after the engine migration")*

## 12. Effectiveness targets (the exit condition for /refine-setup)
- `validate` clean · composite **≥ 85** · 0 `[CUT?]` · routing **100%**
- Every failure mode in §4 maps to a block in §9; every parity invariant in §4b has a check.
- Every command in §10 is PASS or explicitly UNTESTED with a reason.
- (Optional) `--ablate --execute`: no block flagged `CUT`.
