# initial-sendbox

My **first AI-agent setup** — a sandbox built around **GitHub Copilot Agent Mode** for
practicing AI-assisted development, alongside the [GeekAcademy 2026](https://geekacademy.co.il)
program. It now lives as one folder inside the [`agent-lab`](../README.md) hub: the
baseline that the eventual "perfect setup" will improve on.

You don't "run" this — you open it in VS Code and use it as a launchpad for AI-powered
workflows. The `test-project/` subfolder is a small Python package used to exercise the
agents end-to-end.

---

## Layout

```
.github/
  agents/           ← Custom Copilot agent definitions (.agent.md), grouped by role
    coding/         ← write, fix, test, clean code
    mentoring/      ← guide learning (never edit code)
    planning/       ← produce plans, not code
    research/       ← research before coding
  instructions/     ← auto-applied coding standards, matched by file pattern
  prompts/          ← reusable prompt files for common workflows
  workflows/        ← GitHub Actions (CI + agent validation)
  copilot-instructions.md  ← global instructions applied to every Copilot session
skills/             ← reusable instruction snippets (loaded on demand)
hooks/              ← lifecycle automation (logging, auto-commit, governance audit)
src/                ← practice / scratch source code
test-project/       ← a small Python package used to test the agent pipeline
AGENTS.md           ← guide read by Copilot's Coding Agent (CCA) on assigned issues
CONTEXT.md          ← repo purpose & course-topic context for Copilot
```

---

## Agent catalog

Agents are defined in `.github/agents/` and grouped by role. Chain them for well-defined
features; jump straight to a coding agent for quick exploration.

### Research — understand before writing code
| Agent | When to use |
|---|---|
| **task-researcher** | Deep-dive your codebase or external sources into a structured research doc before planning. |
| **analyst** | General analysis of a problem space or codebase. |
| **scientific-paper-research** | Search biomedical/scientific literature (BGPT MCP server). Best for evidence-based or health-tech work. |

### Planning — no code changes, only plans
| Agent | When to use |
|---|---|
| **plan** | Detailed, step-by-step implementation plan from requirements; reads the codebase, asks clarifying questions. |
| **planner** | Lighter-weight planning pass. |
| **prd** | Produce a product-requirements document before scoping work. |

### Coding — write, fix, improve
| Agent | When to use |
|---|---|
| **tdd-red** | Write failing tests *first* from a GitHub Issue's requirements. Start here for new features. |
| **implementer** | Implements an approved plan strictly; enforces TDD (no code without a failing test). |
| **software-engineer-agent-v1** | General-purpose autonomous coding; no strict plan needed. Best for exploration/refactors. |
| **polyglot-test-generator** | Research→Plan→Implement pipeline for comprehensive tests (C++ gtest, Python pytest, …). |
| **debug** | Methodical bug fixing: reproduce → root cause → fix → verify. |
| **janitor** | Clean up tech debt: dead code, unused imports, over-engineering, stale comments. |
| **code-reviewer** | Prioritized review pass (Critical → Important → Suggestion). |

### Mentoring — never edit code, only challenge your thinking
| Agent | When to use |
|---|---|
| **mentor** | Socratic questioning and hints when you're stuck and want to learn. |
| **sensei** | Socratic mentor for juniors using the PEAR Loop (Plan → Explore → Analyze → Rewrite). |
| **critical-thinking** | Repeatedly asks "Why?" to surface hidden assumptions before you commit. |

**Suggested pipeline:** task-researcher → plan → tdd-red → implementer → (debug) → (janitor),
with mentoring agents available at any stage. For quick work, skip to software-engineer-agent-v1.

---

## Skills

Reusable instruction snippets in `skills/`, loaded on demand. Single-file skills are `.md`;
richer ones are a folder with a `SKILL.md`.

| Skill | What it does |
|---|---|
| `add-educational-comments.md` | University-level explanatory comments in generated code |
| `cpp-style-guidelines.md` | Enforces the Google C++ Style Guide |
| `python-style-guidelines.md` | Enforces the Google Python Style Guide |
| `pytorch-best-practices.md` | PyTorch-specific patterns and conventions |
| `agent-governance/` | Governance rules for agent behavior |
| `agentic-eval/` | Evaluating agent outputs |
| `prd/` | Producing a product-requirements document |

---

## Instructions

Files in `.github/instructions/` are applied automatically by VS Code based on file
patterns — no need to mention them in chat.

| Instruction file | Enforces |
|---|---|
| `cpp.instructions.md` | C++ IntelliSense tooling over manual grep |
| `cmake-vcpkg.instructions.md` | vcpkg manifest mode, CMakePresets, cross-platform builds |
| `python.instructions.md` | PEP 8, type hints, PEP 257 docstrings, edge cases |
| `pytorch.instructions.md` | PyTorch training conventions (DataLoader, device, reproducibility) |
| `code-review.instructions.md` | Prioritized code-review checklist |
| `agent-safety.instructions.md` | Safety guardrails for agent actions |
| `context-engineering.instructions.md` | How to assemble and manage context |
| `memory-bank.instructions.md` | Persistent memory conventions |
| `github-actions-ci-cd-best-practices.instructions.md` | CI/CD workflow best practices |

> Most instruction files were sourced from [github/awesome-copilot](https://github.com/github/awesome-copilot) and kept close to verbatim for easy updates.

---

## Hooks

Lifecycle automation in `hooks/` (see `hooks/README.md` for details):

| Hook | Purpose |
|---|---|
| `session-logger/` | Log agent sessions |
| `session-auto-commit/` | Auto-commit work during a session |
| `governance-audit/` | Audit agent actions against governance rules |

---

## Setup

```bash
# from the agent-lab hub root
code initial-sendbox
```
1. Open the Copilot Chat panel (`Ctrl+Alt+I`).
2. Pick an agent from the dropdown. If some don't appear, reload the window
   (`Ctrl+Shift+P` → "Developer: Reload Window") — `.vscode/settings.json` registers the
   agent subfolders under `chat.agentFilesLocations`.

---

## Tips

- **Start broad, then focus.** Explore with `software-engineer-agent-v1`, then switch to the full pipeline.
- **Mentoring agents are for learning, not speed.** Use them when you want to grow.
- **CCA reads `AGENTS.md` first** when you assign a GitHub Issue to Copilot — keep it current.
- **Reload the window after editing agent files** — VS Code caches them on startup.
- **Register new agent subfolders** in `.vscode/settings.json`.
- **Instructions apply automatically** for matching file types — no need to mention them.

---

## References

- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
- [VS Code Custom Agents Docs](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Copilot Coding Agent (CCA) Docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) · [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [GeekAcademy 2026](https://geekacademy.co.il)
