# Plan: Test Agent Pipeline with Mini ML Project

## Goal

Validate the full Copilot agent pipeline end-to-end by building a small, self-contained PyTorch classification model. This smoke-test confirms that each agent hands off correctly to the next and that the TDD cycle produces working, clean code.

---

## Project: Mini Iris Classifier

A minimal PyTorch neural network that classifies the Iris dataset. Small enough to iterate quickly; complex enough to exercise the full pipeline.

**Acceptance criteria:**
- Dataset loaded via `torch.utils.data.DataLoader`
- Model trained for at least 10 epochs and reaches > 90% validation accuracy
- All code passes `ruff` linting
- At least one `pytest` unit test per module

---

## Agent Pipeline

> **Pre-flight check:** All agents listed below must be present in `.github/agents/` before starting. Agents marked ⬇️ must be downloaded from [awesome-copilot](https://github.com/github/awesome-copilot/tree/main/agents) if not present.

| Step | Agent file | Role |
|------|-----------|------|
| 1 | `research/task-researcher.agent.md` | Research PyTorch Iris classifier patterns |
| 2 | `planning/plan.agent.md` | Produce a step-by-step implementation plan |
| 3 | `coding/tdd-red.agent.md` | Write failing pytest tests first |
| 4 | `coding/tdd-green.agent.md` ⬇️ | Write minimal code to make tests pass |
| 5 | `coding/tdd-refactor.agent.md` ⬇️ | Improve quality, add type hints, docstrings |
| 6 | `coding/debug.agent.md` | Fix any remaining failures |
| 7 | `coding/janitor.agent.md` | Final cleanup and linting pass |

Optional / supporting agents:
- `coding/swe-subagent.agent.md` ⬇️ — drop-in SWE agent for ad-hoc fixes
- `coding/se-security-reviewer.agent.md` ⬇️ — security review before final commit
- `mentoring/sensei.agent.md` — Socratic walkthrough after the project is done

---

## Known Issues (surfaces before execution)

### 1. Missing agents  ⚠️
`tdd-green`, `tdd-refactor`, and `swe-subagent` are **not** in `.github/agents/` but are required by this plan. Download them from awesome-copilot before starting:

```bash
# From repo root
curl -s -o .github/agents/coding/tdd-green.agent.md \
  https://raw.githubusercontent.com/github/awesome-copilot/main/agents/tdd-green.agent.md

curl -s -o .github/agents/coding/tdd-refactor.agent.md \
  https://raw.githubusercontent.com/github/awesome-copilot/main/agents/tdd-refactor.agent.md

curl -s -o .github/agents/coding/swe-subagent.agent.md \
  https://raw.githubusercontent.com/github/awesome-copilot/main/agents/swe-subagent.agent.md
```

### 2. Overly aggressive autonomy  ⚠️
Several agents in the pipeline (e.g., `implementer`, `tdd-green`) are configured to proceed autonomously after forming a plan. In a learning/research context this is risky — the agent may make architectural decisions, install packages, or modify tests without a human checkpoint.

**Suggestions (no code change required now):**
- Add an explicit `"Confirm your plan with the user before proceeding"` instruction to each agent's Execution Guidelines.
- Consider using the `confirm` tool or a manual approval gate between `tdd-red` → `tdd-green` and `tdd-green` → `tdd-refactor`.
- Alternatively, run agents one at a time in VS Code Agent Mode with `auto-approve` disabled.
- For multi-step pipelines, review the [GitHub Copilot Agent governance hooks](../../hooks/README.md) already in this repo.

---

## Execution Checklist

- [ ] All agents present in `.github/agents/` (see table above)
- [ ] `src/` directory created for mini ML project
- [ ] Step 1 — task-researcher: gather Iris classifier references
- [ ] Step 2 — plan: produce implementation plan
- [ ] Step 3 — tdd-red: write failing tests
- [ ] Step 4 — tdd-green: write minimal passing implementation
- [ ] Step 5 — tdd-refactor: improve quality (type hints, docstrings, linting)
- [ ] Step 6 — debug: resolve any remaining test failures
- [ ] Step 7 — janitor: final cleanup
- [ ] Validation: `pytest` passes and `ruff check src/` is clean
