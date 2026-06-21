# Agent Eval Kit — Future Project

## Goal

Build a self-contained portfolio piece that proves: **"I can build agents and prove they work."**

The full artifact:
1. **A small real agent** — built with the Anthropic SDK (Python), does something concrete (e.g. code reviewer, research assistant). Includes tool use, error handling, retries, cost + latency tracking, and tracing (Langfuse or OpenTelemetry).
2. **A task suite** — ~20–50 hand-curated input/expected-output pairs covering the agent's scope, including edge cases.
3. **An LLM-as-judge** — an LLM that auto-grades the agent's outputs. Calibrated: agreement measured against human labels (Cohen's κ), known biases documented.
4. **A CI gate** — the task suite runs on every commit and fails if quality drops below threshold. Show a real red→green eval diff in a PR.
5. **A "what broke and why" writeup** — honest failure-mode analysis. This is the senior signal.

## Why this matters for recruiters

- Evals are the skill the industry is desperate for and most candidates fake.
- Combining "I built the agent" + "I measured it rigorously" + "I caught a regression" is a complete engineering story, not a demo.
- Builds directly on existing work in `meta-env-setup/` (scoring rubric, validator, effectiveness modes).

## Connections to existing repo work

- `meta-env-setup/tools/validate_claude_setup.py` — existing scoring logic; the eval kit extends this idea to *runtime* agent behavior
- `meta-env-setup/evals/` — existing eval methodology; look here for patterns to reuse
- `meta-env-setup/.claude/skills/claude-setup-scaffolder` — the meta-pattern this kit should follow

## When to build

After the current `meta-env-setup/` work reaches a stable state. This is the *next* major portfolio spike.

## Open design questions (decide when starting)

- What does the agent actually *do*? (Something real and demonstrable; not a toy)
- LLM judge: same model or a separate evaluator model?
- CI: GitHub Actions or local only?
- Tracing: Langfuse (hosted) vs. self-hosted OTel collector?
