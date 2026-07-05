# agent-lab

**A hub for AI-agent tooling — setups I build, evaluate, and study.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

`agent-lab` gathers the agent infrastructure I build and the upstreams I learn from,
with one goal: assemble a rigorous, reusable setup for new projects. It's a
**collection, not a single app** — each part below has its own README.

---

## Flagship — `meta-env-setup/`

A small, dependency-free Python toolkit that **scaffolds** a Claude Code `.claude/`
setup (skills, slash-commands, agents) and then **grades** it — effectiveness,
context budget, and least-privilege — instead of just checking that it parses.
Grading its *own* setup scores **93/100**.

→ Quickstart, scoring rubric, and per-repo setups:
**[`meta-env-setup/README.md`](meta-env-setup/README.md)**

---

## Layout

| Path | What it is |
|---|---|
| [`meta-env-setup/`](meta-env-setup/) | **Flagship.** The Claude Code setup kit above — scaffold + grade + eval. Self-contained; has its own README. |
| [`skills/`](skills/) | Reusable Claude skills — `skill-creator` (the official Anthropic skill, vendored) and a lighter first-party `skill-creator-lite`. |
| [`docs/roadmap/`](docs/roadmap/) | Design docs for the next builds — see [Roadmap](#roadmap). |
| [`references/`](references/) | External repos as **git submodules** — upstream skills, templates, workshops. Read-only. See [`references/README.md`](references/README.md). |
| [`scripts/`](scripts/) | Small utilities (e.g. a Claude Code status-line renderer). |
| `initial-sendbox/` | An earlier **GitHub Copilot Agent Mode** experiment — predecessor to the Claude Code work. Kept for reference. |

---

## Roadmap

Ideas live in [`FUTURE_IDEAS.md`](FUTURE_IDEAS.md); once one has a real thesis it
graduates to a spec in [`docs/roadmap/`](docs/roadmap/):

- **[Agent Eval Kit](docs/roadmap/agent-eval-kit.md)** — a runnable agent + curated
  task suite + calibrated LLM-as-judge + a CI gate that fails on quality regressions.
  Takes grading from *static config* to *runtime behavior*.
- **[Cross-Format Converter](docs/roadmap/cross-format-converter.md)** — translate a
  setup between Claude Code and Google Antigravity and report *translation fidelity*
  (what converts clean, what's lossy, what's dropped).

---

## Working with the submodules

Everything under `references/` is a pinned git submodule.

```bash
# Cloned without --recurse-submodules? Pull them in:
git submodule update --init --recursive

# Update one reference to its latest upstream:
git submodule update --remote references/<short-name>
```
