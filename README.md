# Agents Playground

A personal sandbox for practicing **GitHub Copilot Agent Mode** and AI-assisted development workflows, used alongside the [GeekAcademy 2026](https://geekacademy.co.il) program.

---

## What Is This Repo?

This repository is a curated collection of:

| Folder | Purpose |
|---|---|
| `.github/agents/` | Custom Copilot agents — each one configures a different AI persona |
| `skills/` | Reusable instruction snippets that agents can load on demand |
| `src/` | Practice code to experiment on |

You don't "run" this repo — you open it in VS Code and use it as a launchpad for AI-powered workflows.

---

## How Copilot Agents Work (Quick Concept)

Think of a **Copilot agent** as a specialist you can hire for a specific job. Each agent is defined by:

1. **A system prompt** — tells the AI how to behave (e.g., "you are a strict TDD enforcer")
2. **A tool list** — controls what actions it can take (read files, run terminal, search web, etc.)

When you switch to an agent in the Chat view, every message you send is automatically framed by that agent's context. You get a focused, role-specific assistant without having to re-explain your rules every time.

---

## Setup

### 1. Open the repo in VS Code
```bash
git clone https://github.com/arielybarak/agents_playground
cd agents_playground
code .
```

### 2. Open the Chat view
Press `Ctrl+Alt+I` to open the Copilot Chat panel.

### 3. Pick an agent
Click the agent dropdown (shows "Agent / Ask / Plan" by default) and select any agent from the list below.

> **Why can't I see all agents?**  
> VS Code only scans `.github/agents/` root by default. This repo's `.vscode/settings.json` already adds the subdirectories — just reload the window once (`Ctrl+Shift+P` → "Developer: Reload Window").

---

## Agent Catalog

Agents are organized into four categories. Use the pipeline diagram below to decide which one to start with.

### Research
> Use these **before you write a single line of code**, to understand the problem deeply.

| Agent | When to use |
|---|---|
| **Task Researcher** | Deep-dive into your own codebase or external sources to produce a structured research document before planning. Best for "I need to understand X before I touch it." |
| **Scientific Paper Research** | Search biomedical/scientific literature. Powered by the BGPT MCP server. Best for evidence-based feature validation or health-tech projects. |

---

### Planning
> Use these **after research, before coding**. No code changes are made — only plans.

| Agent | When to use |
|---|---|
| **Plan** | Creates a detailed, step-by-step implementation plan from your requirements. Reads your codebase first, asks clarifying questions, then outputs a concrete plan. Hand the plan to an implementer agent when done. |

---

### Coding
> Use these **to actually write, fix, or improve code**.

| Agent | When to use |
|---|---|
| **TDD Red** | Write failing tests *first*, before any implementation exists. Follows a GitHub Issue to extract requirements and turns them into a `test_X fails as expected` report. Start here for new features. |
| **Implementer** | Takes an approved plan and implements it strictly. Enforces TDD (no code without a failing test first). The most structured coding agent — best when you have a clear plan. |
| **Software Engineer Agent** | General-purpose, autonomous coding. No strict plan required. Best for exploratory work, refactors, or when you don't want to run the full pipeline. |
| **Polyglot Test Generator** | Orchestrates comprehensive test generation via a Research-Plan-Implement pipeline. Works with any language — ideal for C++ (gtest) and Python (pytest). Use when you need to add or improve test coverage for an existing codebase. |
| **Security Reviewer** | Reviews code for security vulnerabilities: OWASP Top 10, Zero Trust, and LLM/ML-specific threats. Creates a prioritized code-review report. Run after implementation, before merge. |
| **Debug** | Diagnoses and fixes bugs systematically. Reproduces → Root cause → Fix → Verify. Use when something is broken and you want a methodical investigation. |
| **Janitor** | Cleans up tech debt: removes dead code, unused imports, over-engineering, outdated comments. Run this after a feature is stable. |

---

### Mentoring
> These agents **never edit code** — they only challenge your thinking.

| Agent | When to use |
|---|---|
| **Mentor** | Guides you to the right answer through Socratic questioning and hints. Best when you're stuck and want to learn, not just get an answer. |
| **Sensei** | Socratic mentor for junior developers, using the PEAR Loop (Plan → Explore → Analyze → Rewrite). Never gives direct answers. Uses progressive clue levels so you reach the solution yourself. Sourced from [Awesome Copilot](https://github.com/github/awesome-copilot). |
| **Critical Thinking** | Repeatedly asks "Why?" until it reaches the root of your assumption. Best when you feel confident but want a second opinion before committing to an approach. |

---

## The Development Pipeline

For well-defined features, chain agents in this order:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FULL FEATURE PIPELINE                           │
│                                                                         │
│  1. task-researcher  ──►  2. plan  ──►  3. tdd-red                     │
│                                              │                          │
│                                              ▼                          │
│                                       4. implementer                    │
│                                              │                          │
│                                    (if bugs) ▼                          │
│                                         5. debug                        │
│                                              │                          │
│                                  (when stable) ▼                        │
│                                         6. janitor                      │
│                                              │                          │
│                              (before merge) ▼                           │
│                                   7. security-reviewer                  │
│                                                                         │
│   sensei / mentor / critical-thinking  ◄──  available at any stage      │
└─────────────────────────────────────────────────────────────────────────┘
```

For quick, exploratory work: skip straight to **Software Engineer Agent**.

For test coverage: use **Polyglot Test Generator** on any existing codebase.

---

## Skills

Skills are reusable instruction snippets stored in `skills/`. An agent can reference a skill to load specific behavior on demand — for example, loading `add-educational-comments.md` to get detailed inline explanations in generated code.

| Skill file | What it does |
|---|---|
| `add-educational-comments.md` | Adds university-level explanatory comments to generated code |
| `cpp-style-guidelines.md` | Enforces Google C++ Style Guide |
| `python-style-guidelines.md` | Enforces Google Python Style Guide |
| `pytorch-best-practices.md` | PyTorch-specific patterns and conventions |

> **Planned:** Agents will be wired up to auto-load relevant skills based on the task type.

---

## Instructions

Instructions live in `.github/instructions/` and are automatically applied by VS Code based on file patterns — you don't need to load them manually.

| Instruction file | Applies to | What it enforces |
|---|---|---|
| `cpp.instructions.md` | `**/*.cpp, **/*.h, **/*.hpp` | Use C++ IntelliSense tools (GetSymbolInfo, GetSymbolReferences, CallHierarchy) over manual grep |
| `cmake-vcpkg.instructions.md` | `**/*.cmake, **/CMakeLists.txt` | vcpkg manifest mode, CMakePresets, cross-platform (MSVC/Clang/GCC) |
| `python.instructions.md` | `**/*.py` | PEP 8, type hints, PEP 257 docstrings, edge-case handling |
| `langchain-python.instructions.md` | `**/*.py` | LangChain Runnable interface, RAG patterns, vector stores, LLM best practices |
| `code-review.instructions.md` | `**` | Prioritized code-review checklist (Critical → Important → Suggestion) |

> All instruction files were sourced from [github/awesome-copilot](https://github.com/github/awesome-copilot) and are kept verbatim for easy future updates.

---

## Tips

- **Start broad, then focus.** Use `Software Engineer Agent` to explore. Once you know the scope, switch to the full pipeline.
- **The mentoring agents are for learning, not speed.** Use `Sensei`, `Mentor`, or `Critical Thinking` when you want to grow, not just get code.
- **Security review before every merge.** Use `Security Reviewer` to catch OWASP / Zero Trust issues before pushing to main.
- **CCA (Copilot Coding Agent)** — When assigning a GitHub Issue to Copilot, it reads `AGENTS.md` first. Keep that file up to date with your conventions.
- **Agents ignore unknown tools gracefully.** If a tool isn't available (e.g., `runTests` without a test framework), it's silently skipped.
- **Reload the window after editing agent files.** VS Code caches agent definitions on startup.
- **Check `.vscode/settings.json`** if you add a new agent subfolder — you'll need to register it under `chat.agentFilesLocations`.
- **Instructions are applied automatically** for matching file types — no need to mention them in the chat.

---

## References

- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
- [VS Code Custom Agents Docs](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code Agent Tools Reference](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- [Copilot Coding Agent (CCA) Docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [GeekAcademy 2026](https://geekacademy.co.il)
