# AGENTS.md — Copilot Coding Agent (CCA) Guide

This file is read by GitHub Copilot's Coding Agent (CCA) when it is assigned a GitHub Issue. It explains the repository layout, the available agent pipeline, and the conventions Copilot must follow when working here.

---

## Repository Purpose

This is a personal research and coding environment for **C++ and Python (PyTorch/ML) projects**. It is built around GitHub Copilot Agent Mode and is meant to be reused as a launchpad for future projects.

Key technologies used in projects spawned from this environment:
- **C++** (Google C++ Style Guide, CMake, vcpkg)
- **Python** (Google Python Style Guide, PEP 8, PyTorch)

---

## Directory Layout

```
.github/
  agents/           ← Custom Copilot agent definitions (one .agent.md per persona)
    coding/         ← Agents that write, fix, test, and clean code
    mentoring/      ← Agents that guide learning (never write code directly)
    planning/       ← Agents that produce plans, not code
    research/       ← Agents that research before coding
  instructions/     ← Auto-applied coding standards for specific file types
  prompts/          ← Prompt files for common workflows
  copilot-instructions.md  ← Global instructions applied to every Copilot session
skills/             ← Reusable instruction snippets (load on demand)
src/                ← Practice / example source code
```

---

## Global Coding Rules (always apply)

1. **Industry standards** — write code the way a professional engineer at a real company would write it. Follow established conventions and explain the *why* behind them.
2. **Simplicity over cleverness** — prefer clear, readable code over clever one-liners.
3. **C++ style** → [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
4. **Python style** → [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
5. **Consult `skills/`** for domain-specific directives (e.g., `pytorch-best-practices.md`, `cpp-style-guidelines.md`).

---

## Agent Pipeline (recommended order for new features)

```
1. task-researcher  ──►  2. plan  ──►  3. tdd-red  ──►  4. implementer
                                                              │
                                                    (if bugs) ▼
                                                         5. debug
                                                              │
                                                  (when stable) ▼
                                                         6. janitor
```

For quick fixes or exploratory work: use **Software Engineer Agent** directly.

---

## Instruction Files (auto-applied by file type)

| File pattern | Instruction file | What it enforces |
|---|---|---|
| `**/*.cpp, **/*.h, **/*.hpp` | `cpp.instructions.md` | C++ IntelliSense tool usage, symbol lookup rules |
| `**/*.cmake, **/CMakeLists.txt, **/*.cpp` | `cmake-vcpkg.instructions.md` | CMake/vcpkg manifest mode, cross-platform build |
| `**/*.py` | `python.instructions.md` | PEP 8, type hints, docstrings |
| `**/*.py` | `pytorch.instructions.md` | PyTorch training conventions, DataLoader, device placement, reproducibility |
| `**` | `code-review.instructions.md` | Code review priority levels and checklist |

---

## Skills Available

Load these when the task calls for it:

| Skill file                           | When to load                          |
|--------------------------------------|--- -----------------------------------|
| `skills/add-educational-comments.md` | Any code generation that should teach |
| `skills/cpp-style-guidelines.md`     | C++ code generation or review         |
| `skills/python-style-guidelines.md`  | Python code generation or review      |
| `skills/pytorch-best-practices.md`   | PyTorch / deep learning code          |

---

## CCA Workflow Notes

- **Always read `CONTEXT.md`** before starting — it lists the learning topics and intent of this repository.
- **Always read `skills/` files** relevant to the language you are working in before generating code.
- **Do not create test frameworks** that don't already exist in the project.
- **Do not introduce new dependencies** without explaining the trade-off.
- **Prefer `pytest`** for Python test files; **prefer `Google Test (gtest)`** for C++ test files.
- When the task involves ML code, follow the patterns in `skills/pytorch-best-practices.md`.
