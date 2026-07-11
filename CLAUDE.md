# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repo map

Collection hub, not one app. Method is spec-first (see SDD below). Parts, each with its own README:

- `meta-env-setup/` — the live project. Kit for building/grading/evaluating **Claude Code** `.claude/` setups.
- `course-factory/` — topic-agnostic course generator. **In design, not wired up** — pipeline doesn't run yet; source of truth is `course-factory/DESIGN.md`.
- `specs/` + `.specify/` + root `.claude/skills/speckit-*` — the shared spec-kit (SDD) environment driving the above.
- `agent-eval-kit/`, `docs/roadmap/` — design docs only, **not built**.
- `references/` — 8 pinned git submodules (other people's work). Read-only: do not edit; changes go upstream. See `references/README.md`. After clone: `git submodule update --init --recursive`; bump one: `git submodule update --remote references/<name>`.
- `initial-sendbox/` — **archived** GitHub Copilot experiment. Past, not used; don't take commands or conventions from it.
- `docs/temp.md` — unrelated scratch notes, ignore.

## Spec-Driven Development

The repo root **is** the spec-kit environment (git root = `agent-lab`). Products (e.g. `course-factory/`) are subdirs kept product-only (DESIGN.md, code, templates); their specs + governance live in the root machinery:

- `.specify/` — engine: `scripts/bash/{create-new-feature,setup-plan,setup-tasks,common,check-prerequisites}.sh`, `templates/`, `memory/`.
- Root `.claude/skills/speckit-*` — workflow skills. A feature moves spec → clarify → plan → tasks → analyze, each in its own file. Invoke as slash commands (`/speckit-specify`, etc.).
- Specs namespaced `specs/<project>/<NNN>-<feature>/` → `spec.md`, `plan.md`, `tasks.md`, `checklists/`. Read `specs/<project>/README.md` first — it's the index; pick one spec and work it without re-deriving the decomposition.

Footguns (cause errors if unknown):

- Constitution real path is `.specify/memory/<project>/constitution.md`. `.specify/memory/constitution.md` is a relative symlink to the active project's copy = the active-project selector. Edit the real path, **not the symlink** — `/speckit-constitution` (or any Write to the symlink path) can replace the symlink with a regular file. Recreate: `ln -s <project>/constitution.md .specify/memory/constitution.md`.
- New specs do not auto-nest — `create-new-feature.sh` defaults to flat `specs/<NNN>-name`. To keep the namespace, set `SPECIFY_FEATURE_DIRECTORY=specs/<project>/<NNN>-name` before `/speckit-specify` (auto-persists to `feature.json`). Derive `<project>` from feature.json's current `feature_directory`; compute `<NNN>` by scanning `specs/<project>/`.
- `.specify/feature.json` = active-feature pointer; kept uncommitted.

## meta-env-setup/

Run everything from inside it (`cd meta-env-setup`) — its `.claude/` commands/agents auto-load only from there, and all paths below are relative to it. Stdlib only, zero deps. See `meta-env-setup/README.md`, `tools/README.md`.

- `tools/`: `scaffold_claude_setup.py` (bootstraps a `.claude/` skeleton; `--pool <topic>` parks a block in `tools-pool/` at zero routing-budget cost), `mine_transcripts.py` (mines session transcripts for repeated commands / throwaway scripts / deploy-wait loops), `validate_claude_setup.py` (structure gate + advisory modes `--score`, `--stale --repo`, `--route`, `--ablate` — only the default gate fails CI).
- Commands: `/new-claude-setup` (greenfield end-to-end loop), `/upgrade-claude-setup` (brownfield: import live `.claude/`, reconcile blocks ADD/FIX/REWRITE/KEEP/CUT), `/refine-setup` (measure → critique → rewrite → re-measure), `/audit-claude-setup` (structure + frontmatter + weight check).
- Agents (read-only): `setup-analyzer`, `block-author`, `setup-critic`. Skills: `claude-setup-scaffolder`, `skill-creator-lite`, `hook-design`.
- `claude-setups/<repo>/` — setups authored for other repos, dry-run-by-default `install.sh`; gitignored, never auto-written into real repos. `evals/` — task suites / routing tests (tracked because `claude-setups/` isn't).

```bash
cd meta-env-setup
python tools/test_audit.py                                         # 24/24 tests
python tools/validate_claude_setup.py claude-setups/*/ .            # structural gate
python tools/validate_claude_setup.py claude-setups/*/ . --score    # + effectiveness/minimality score
```

## Conventions

- Author is learning industry-standard practice — write code as a professional would, and briefly explain the *why* behind conventions/design decisions.
- Prefer simplicity over clever one-liners or heavy abstractions.
- Don't add dependencies without stating the trade-off; don't invent new test frameworks. Prefer pytest.
