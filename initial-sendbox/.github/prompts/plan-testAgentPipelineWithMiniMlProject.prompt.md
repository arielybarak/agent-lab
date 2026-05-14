# Plan: Test Agent Pipeline with Mini ML Project

**TL;DR:** Build a tiny audio-based fall detection classifier inside `agents_playground/test-project/` — just 4-5 Python files — by walking through the agent pipeline step by step. The project is deliberately small so you can observe each agent's behavior and evaluate whether they add value or add noise.

> **Pre-flight fixes applied:** Before executing this plan, three critical agent issues were resolved:
> 1. `tdd-red` C# bias → replaced with polyglot "Test Framework Patterns" (Python/JS/Java/C#/Go auto-detect)
> 2. `implementer` phantom handoffs → created missing `Analyst`, `Planner`, and `Code Reviewer` agents
> 3. `software-engineer-agent` aggressive autonomy → replaced with confidence-based autonomy model

## Steps

### 1. Create project scaffold
Create `test-project/` with a minimal structure:
- `test-project/README.md`
- `test-project/src/dataset.py` (synthetic audio dataset)
- `test-project/src/model.py` (small 1D CNN)
- `test-project/src/train.py` (training loop)
- `test-project/src/evaluate.py` (metrics)
- `test-project/tests/` (pytest)

### 2. Invoke `task-researcher` agent
Ask it to research: "What's a minimal approach to audio-based fall detection using 1D CNNs on mel-spectrograms?" It should produce research notes in `.copilot-tracking/research/`. This tests whether its research-only constraint holds and whether the output is useful or bloated.

### 3. Invoke `plan` agent
Feed it the researcher output and ask it to create an implementation plan for the 4-file project. Evaluate whether it actually reads the codebase structure and skills files before planning, or just generates generic advice.

### 4. Invoke `tdd-red` agent
Ask it to write failing tests for `dataset.py` and `model.py`. The agent now auto-detects the project language and should use pytest. Verify it picks up the Python project correctly and does not fall back to C# patterns.

### 5. Invoke `implementer` agent
Give it the plan and failing tests. Ask it to implement `dataset.py`, `model.py`, `train.py`, `evaluate.py`. Evaluate whether it follows the PyTorch instructions (tensor shape comments, explicit device placement, DataLoader usage, seed setting). Also verify: do the handoffs to `Analyst`, `Planner`, and `Code Reviewer` resolve correctly now that those agents exist?

### 6. Invoke `janitor` agent
Run it on the completed project to see if it cleans up anything meaningful or just adds noise on a tiny codebase.

### 7. Invoke `mentor` agent
Ask it to review the final code and challenge assumptions (e.g., "Is a 1D CNN the right choice? What about class imbalance?"). Evaluate whether it actually probes or just agrees.

## Agent Issues Tracker

### Resolved (pre-flight)

| Issue | Agent | Fix Applied |
|-------|-------|-------------|
| ~~C#-focused TDD agent~~ | `tdd-red` | Replaced "C# Test Patterns" section with polyglot "Test Framework Patterns" — auto-detects language via existing tests and project config. Covers Python, JS/TS, Java, C#, Go. |
| ~~Phantom handoff targets~~ | `implementer` | Created three missing agents: `research/analyst.agent.md`, `planning/planner.agent.md`, `coding/code-reviewer.agent.md`. |
| ~~Overly aggressive autonomy~~ | `software-engineer-agent` | Replaced "ZERO-CONFIRMATION POLICY" with "Confidence-Based Autonomy" — acts freely when 100% certain, must ask when ambiguous. |

### Remaining (out of scope for now)

| Issue | Agent | Severity | Detail |
|-------|-------|----------|--------|
| **External MCP dependency** | `scientific-paper-research` | Low | Requires the BGPT MCP server (`https://bgpt.pro/mcp/sse`). Won't work locally without configuration. Not blocking for this test, but worth noting. |
| **C++ references in global instructions** | `copilot-instructions.md` | Low | Still mentions C++ and Google C++ Style Guide. If this is copied to a Python-only project, the agent wastes context on irrelevant rules. |
| **Missing `.copilot-tracking/` in .gitignore** | `task-researcher` | Low | The researcher writes to `.copilot-tracking/research/` but this directory is not in `.gitignore`. Research artifacts will get committed unless handled. |

## Verification
- After each agent invocation, review its output for: relevance, adherence to its own constraints, and whether it consumed the skills/instructions files
- Run `pytest test-project/tests/` to verify the TDD + implementation cycle produced working code
- Run `python test-project/src/train.py` to verify the training loop runs on synthetic data
- Compare the researcher's output quality vs. time spent — is it worth the overhead for a small project?

## Decisions
- **Synthetic data only**: Generate fake mel-spectrogram tensors to keep the project self-contained (no downloads, no external datasets)
- **Minimal scope**: 4 source files + tests. No logging framework, no experiment tracking, no notebooks
- **Sequential agent invocation**: Follow the pipeline order from `AGENTS.md` (`researcher → plan → tdd-red → implementer → janitor`) to test the intended workflow
