# agent-lab

A **portfolio of agent infrastructure work** — building, evaluating, and operating AI agents
with Claude Code and GitHub Copilot.

Three things this repo demonstrates:
- **Meta-tooling with an opinion:** a scaffolder + validator that scores Claude Code setups on effectiveness, context budget, and least-privilege — not just structure.
- **AI-assisted engineering under real constraints:** a purpose-built Claude Code workspace for a 24-hour hardware hackathon (FPGA + ESP32), designed around a tight token budget.
- **Evaluation as engineering:** a methodology + harness for measuring whether an agent setup actually works, not just whether it looks right.

---

## Layout

| Path | What it is |
|---|---|
| [`meta-env-setup/`](meta-env-setup/) | **Claude Code setup kit** — scaffolder, validator + effectiveness scorer, per-repo setups, eval harness. Self-contained: `cd meta-env-setup` to use it. |
| [`initial-sendbox/`](initial-sendbox/) | **GitHub Copilot Agent Mode setup** — custom agents, skills, hooks, instructions. The predecessor to the Claude Code work above. |
| [`agent-eval-kit/`](agent-eval-kit/) | **Planned:** end-to-end agent + task suite + LLM judge + CI gate. See [README](agent-eval-kit/README.md). |
| [`references/`](references/) | External repos as **git submodules** — upstream skills, templates, workshops. Read-only. See [`references/README.md`](references/README.md). |
| [`FUTURE_IDEAS.md`](FUTURE_IDEAS.md) | Backlog of things to build next (MCP server, cost tracking, prompt injection tests, Copilot vs Claude Code comparison). |

---

## Working with the submodules

Everything under `references/` is a pinned git submodule.

```bash
# Clone with all submodules
git clone --recurse-submodules https://github.com/arielybarak/agent-lab

# Already cloned without --recurse-submodules?
git submodule update --init --recursive

# Add a new reference
git submodule add <repo-url> references/<short-name>

# Update one reference to its latest upstream
git submodule update --remote references/<short-name>
```
