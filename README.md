# agent-lab

**A hub for AI-agent tooling — setups I build, evaluate, and study.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

`agent-lab` gathers the agent infrastructure I build and the upstreams I learn from,
with one goal: assemble a rigorous, reusable setup for new projects. It's a
**collection, not a single app** — each part below has its own README. It's also a running
set of **experiments in AI-assisted engineering**: increasingly the *method* is part of the
work, not just the tools — see [Spec-Driven Development](#method--spec-driven-development-sdd).

---

## Flagship — `meta-env-setup/`

An **end-to-end kit for building, measuring, and evolving Claude Code environments**. Instead of relying on human guesswork to decide what tools an AI agent needs, `meta-env-setup` treats configuration as engineering: it analyzes codebases, mines empirical usage, and uses multi-layered evaluation to prove a setup is effective and minimal.

### Key Capabilities

- **Empirical Analysis & Transcript Mining:** Rather than prescribing generic toolkits, an autonomous `setup-analyzer` inspects repo architecture and mines historical session transcripts (`tools/mine_transcripts.py`) to uncover real developer pain points (repeated commands, throwaway scripts, and deploy-wait loops).
- **Automated Scaffolding & Upgrading:** Features one-command greenfield bootstrapping (`/new-claude-setup`) and brownfield reconciliation (`/upgrade-claude-setup`) to systematically add, fix, rewrite, or cut configuration blocks.
- **Multi-Layered Evaluation:** Replaces subjective "vibes" with verifiable metrics:
  - **Static Scoring (`--score`):** A reproducible 0–100 composite audit evaluating trigger quality, specificity, redundancy, context budget, and least-privilege (scoring **93/100** on its own setup).
  - **Staleness Detection (`--stale`):** Automatically flags instructions or blocks referencing renamed, moved, or deleted code.
  - **Routing Verification (`--route`):** Tests descriptions against prompt suites to ensure skills trigger only when intended.
  - **Ablation Testing (`--ablate`):** Removes individual blocks and re-runs tasks to prove whether a tool is genuinely essential or dead weight.
- **Budget-Aware Tool Pool:** Allows parking fully engineered skills or commands in a dormant `tools-pool/` at zero routing-budget cost until their project phase begins.
- **Production-Ready Bundles:** Ships method skills (`skill-creator-lite`, `hook-design`), interactive retro tools (`/setup-retro`), and dry-run installable configurations for external projects (`claude-setups/<repo>/`).

`stdlib only` · `zero third-party deps` · `24 tests passing`

→ **Explore the pipeline, scoring rubric, and ready-to-install setups:** **[`meta-env-setup/README.md`](meta-env-setup/README.md)**

---

## Method — Spec-Driven Development (SDD)

Everything new here is built **spec-first**, with an AI-assisted [Spec-Driven Development](https://github.com/github/spec-kit)
workflow rather than prompting a model straight into code. Each feature moves through explicit,
reviewable artifacts — **spec → clarify → plan → tasks → analyze** — governed by a per-project
**constitution** of non-negotiable principles, so the AI's work stays grounded, auditable, and
resumable across sessions.

`course-factory` is the current worked example: its four subject-specs
([`specs/course-factory/`](specs/course-factory/)) were each authored and clarified this way,
against a ratified [constitution](.specify/memory/course-factory/constitution.md). **SDD is the
default for every project from here on** — the methodology itself, and these experiments running
real AI agents through it, are as much what this repo is showing as the tools they produce.

---

## Layout

| Path | What it is |
|---|---|
| [`meta-env-setup/`](meta-env-setup/) | **Flagship.** The Claude Code setup kit above — scaffold + grade + eval. Self-contained; has its own README. |
| [`course-factory/`](course-factory/) | **In design (spec-first).** A topic-agnostic course generator — feed it a course spec, it researches, drafts, and quality-gates a full course (generalizing the method behind `System_Design_SelfLearn`). Its build is decomposed into **four SDD subject-specs** ([`specs/course-factory/`](specs/course-factory/)), all clarified; design doc + specs, see its README. |
| [`specs/`](specs/) + [`.specify/`](.specify/) | **Spec-Driven Development.** Per-feature specs (spec → plan → tasks) plus the spec-kit engine and per-project **constitution** that drive them. See [Method](#method--spec-driven-development-sdd). |
| [`skills/`](skills/) | Reusable Claude skills — `skill-creator` (the official Anthropic skill, vendored) and a lighter first-party `skill-creator-lite`. |
| [`docs/roadmap/`](docs/roadmap/) | Design docs for the next builds — see [Roadmap](#roadmap). |
| [`references/`](references/) | External repos as **git submodules** — upstream skills, templates, workshops. Read-only. See [`references/README.md`](references/README.md). |
| [`scripts/`](scripts/) | Small utilities (e.g. a Claude Code status-line renderer). |
| `initial-sendbox/` | An earlier **GitHub Copilot Agent Mode** experiment — predecessor to the Claude Code work. Kept for reference. |

---

## Roadmap

Ideas live in [`docs/FUTURE_IDEAS.md`](docs/FUTURE_IDEAS.md); once one has a real thesis it
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
