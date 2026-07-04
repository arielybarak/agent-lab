# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`agents_sendbox` is a **collection hub**, not an application. It gathers AI-agent tooling
(skills, plugins, project templates, workshops) to study and remix, with the long-term goal
of assembling one "perfect" agent setup for new projects. Three kinds of content live here:

- **`references/`** — external repos pulled in as **git submodules** (other people's work:
  `caveman`, `mattpocock-skills`, `ideal-project-scaffolder`, `sdd-workshop`). Treat these as
  read-only upstreams — do **not** edit files inside them; changes belong upstream. See
  `references/README.md` for what each one is and what's worth borrowing.
- **`initial-sendbox/`** — a first-party project: a GitHub Copilot Agent Mode setup
  (custom agents, skills, hooks, instructions) plus a small Python package used to exercise it.
- **`meta-env-setup/`** — first-party **Claude Code** tooling gathered into one self-contained,
  shareable kit: a scaffolder + validator/auditor, the method skills, ready-to-install `.claude`
  setups for *other* repos, and an effectiveness-eval harness. See "First-party Claude Code
  tooling" below.

Because the references are submodules, after cloning run
`git submodule update --init --recursive` (or clone with `--recurse-submodules`). Update one
upstream with `git submodule update --remote references/<name>`.

## Where the working code is: `initial-sendbox/`

The agent system is config-as-files, designed for GitHub Copilot (CCA / Agent Mode), not a
runtime you launch:

- **`.github/agents/<role>/*.agent.md`** — agent personas grouped by role: `research/`,
  `planning/`, `coding/`, `mentoring/`. Each is a Markdown file with required YAML front-matter
  (`name`, `description`). The intended workflow chains them:
  `task-researcher → plan → tdd-red → implementer → (debug) → (janitor)`; mentoring agents never
  edit code. For quick work, use `software-engineer-agent-v1` directly.
- **`.github/instructions/*.instructions.md`** — coding standards auto-applied by file glob
  (e.g. `*.py` → PEP 8 + PyTorch conventions; `*.cpp/*.h` → Google C++ / IntelliSense rules).
  Most are kept close to verbatim from [github/awesome-copilot](https://github.com/github/awesome-copilot)
  for easy updates — preserve that when touching them.
- **`skills/`** — reusable instruction snippets, loaded on demand. Single-file skills are `.md`;
  richer ones are a folder containing `SKILL.md`.
- **`hooks/`** — lifecycle automation: `session-logger/`, `session-auto-commit/`, and
  `governance-audit/` (audits `.agent.md` files against governance rules).
- **`test-project/`** — `fall-detection-mini`, a tiny PyTorch audio-classifier package. Its sole
  purpose is to give the agent pipeline a real, end-to-end target to operate on.
- **`AGENTS.md`** / **`CONTEXT.md`** — read both before agent work in this folder; `CONTEXT.md`
  states the learning intent, `AGENTS.md` is what Copilot's Coding Agent reads on an assigned issue.

## First-party Claude Code tooling — `meta-env-setup/`

Where `initial-sendbox/` targets **GitHub Copilot**, this layer targets **Claude Code**. It is a
**self-contained, shareable kit** for *building and evaluating* `.claude/` setups, gathered under
one folder. **Run its commands from inside `meta-env-setup/`** (`cd meta-env-setup`) — every path
below is relative to that folder. See `meta-env-setup/README.md` for the overview.

- **`tools/`** — stdlib-only `scaffold_claude_setup.py` (bootstraps a `.claude/` skeleton, adds
  skills/commands/agents, `--pool <topic>` parks a block in `tools-pool/` at zero routing-budget
  cost), `mine_transcripts.py` (mines a repo's Claude Code session transcripts for repeated
  commands / throwaway scripts / deploy-wait loops — evidence the code alone can't show), and
  `validate_claude_setup.py` (CI-style structure check + four advisory **effectiveness** modes —
  `--score` static audit, `--stale --repo` flags blocks citing identifiers no longer in the code,
  `--route` routing tests, `--ablate` ablation; only the default gate fails CI). See `tools/README.md`.
- **`evals/`** — methodology + per-repo eval data (task suites, routing tests) for the effectiveness
  modes; tracked because `claude-setups/` is gitignored. See `evals/README.md`.
- **`.claude/skills/`** — the kit's method skills (they auto-activate when you work inside the
  kit): `claude-setup-scaffolder` (the whole pipeline), a kit-native measured `skill-creator-lite`
  (author one skill, sharpened against `--score`), and `hook-design` (design an effective hook).
  The repo-root `skills/skill-creator` is the heavier official Anthropic skill-creator
  (behavioral eval — runs real Claude with/without the skill), kept as a reference upstream.
- **`.claude/`** — the kit's *own* Claude Code setup: the `/new-claude-setup` and
  `/audit-claude-setup` commands plus the read-only `setup-analyzer` agent. Because it now lives
  here, those commands auto-load only when you work from inside `meta-env-setup/`. (Its
  `settings.json` ships with empty permissions on purpose — add your own.)
- **`claude-setups/<repo>/`** — complete `.claude` setups authored here for *other* repos
  (currently `DL-Project`, `project-VLSI`, `Integrated_HWSW`, and `System_Design_SelfLearn`),
  each with a dry-run-by-default `install.sh`. Never written into the real repos automatically;
  gitignored. See `claude-setups/README.md`.

Validate + score every setup (and the kit's own), from inside `meta-env-setup/`:
```bash
cd meta-env-setup
python tools/validate_claude_setup.py claude-setups/*/ .            # structural gate
python tools/validate_claude_setup.py claude-setups/*/ . --score    # + effectiveness/minimality score
```

## Common commands

Python lint/format (CI pins **ruff 0.4.4**), run from `initial-sendbox/`:
```bash
ruff check src/ hooks/
ruff format src/ hooks/ --check
```

The `test-project` package (run from `initial-sendbox/test-project/`):
```bash
pip install -e ".[dev]"          # or: uv pip install -e ".[dev]"  — installs torch + pytest
pytest                            # all tests (testpaths = tests/)
pytest tests/test_model.py        # one file
pytest tests/test_model.py::test_name   # one test
```

Validate agent files / governance (mirrors the CI checks), from `initial-sendbox/`:
```bash
# every .agent.md must have YAML front-matter with name + description
python hooks/governance-audit --path .github/agents --output /tmp/audit.jsonl --fail-on critical
actionlint                        # lints the workflow YAML
```

## Conventions to follow (from copilot-instructions.md & AGENTS.md)

These are explicit project rules, not generic advice:

- The author is learning **industry-standard** practices — write code as a professional would,
  and **briefly explain the *why*** behind conventions and design decisions.
- **C++** → Google C++ Style Guide; **Python** → Google Python Style Guide. Prefer simplicity
  over clever one-liners or heavy abstractions.
- Consult relevant `skills/` files before generating code (e.g. `pytorch-best-practices.md` for ML).
- **Do not create new test frameworks** that don't already exist, and **do not add dependencies**
  without explaining the trade-off. Prefer **pytest** (Python) and **Google Test / gtest** (C++).

## Gotcha: dormant workflows

`initial-sendbox/.github/workflows/` (`ci.yml`, `agent-validation.yml`) reference paths relative
to a repo root (`src/`, `hooks/`, `.github/agents`). Since they now live in a **subfolder**, GitHub
Actions will not auto-run them from this hub's root — they're effectively documentation/reference
for the commands above unless invoked manually. Adjust paths (or relocate the workflows) if you
want them to actually run in CI.
