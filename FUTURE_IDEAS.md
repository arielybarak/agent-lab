# Future Ideas & Work Items

Things to build, add, or develop in this repo. Rough priority order within each section.

---

## Agent infrastructure

### Agent Eval Kit (`agent-eval-kit/`)
Folder already exists with a detailed README. The full artifact:
- A small real agent built with the Anthropic SDK (Python)
- A task suite of ~20–50 input/expected-output pairs with checkable outcomes
- An LLM-as-judge that auto-grades outputs, calibrated against human labels
- A CI gate (GitHub Actions) that fails if quality drops between commits
- A "what broke and why" writeup

**Why:** Proves you can build agents *and* measure them rigorously. The combination is rare.

### Bridge static `--score` with empirical triggering eval
Combine the two skill-authoring approaches now in the repo into a two-layer pipeline:
- **Cheap pre-filter:** `meta-env-setup/tools/validate_claude_setup.py --score` — static, deterministic, CI-able, repo-aware. Runs on every commit.
- **Behavioral confirm:** the official skill-creator's empirical triggering loop (`skills/skill-creator/scripts/run_loop.py`) — runs real Claude on queries (3× repeats, train/test split) to verify the skill *actually* triggers and improves output.

The bridge: use static scoring as the fast gate, behavioral eval as the ground-truth verification. Static pre-filter → behavioral confirm. This combination (cheap CI proxy + expensive empirical check) doesn't exist in either tool today and is genuinely novel — and portfolio-worthy.

**Why:** Yours answers "is this skill well-written for this repo?" statically; theirs answers "does it actually change what Claude does?" empirically. Neither alone is complete; the bridge is.

### MCP Server
Build a custom MCP (Model Context Protocol) server — a small process that exposes tools Claude
Code can invoke. Natural candidate: a "score this skill file" tool that wraps
`meta-env-setup/tools/validate_claude_setup.py --score`, callable directly from within Claude Code.

**Why:** Shows you understand Claude Code at the protocol level, not just the user/config level.
Most candidates configure Claude; few can extend it.

### Prompt Injection Test Suite
A suite of adversarial inputs designed to make an agent do something it shouldn't: write to
forbidden paths, leak context, call tools outside its permission scope. Document what's defended
and what isn't. Builds directly on the existing least-privilege work in `meta-env-setup/`.

**Why:** Security-aware agent work is rare in portfolios. Combined with the existing
least-privilege scoring, it makes a complete security story.

### Cost Tracking in the Eval Kit
When building the eval kit, extend beyond token budgets to actual $ cost per task run.
A small dashboard showing cost per task, and the effect of prompt changes on cost efficiency.

**Why:** Production-thinking signal. Shows you care about real-world deployability, not just quality.

---

## Documentation / writing

### Copilot vs. Claude Code Comparison
A structured comparison of `initial-sendbox/` (GitHub Copilot Agent Mode) and
`meta-env-setup/` (Claude Code) — routing quality, context budget, least-privilege,
eval capability, skill/hook system. A practitioner perspective that almost no one else has,
because almost no one has built both setups seriously.

**Why:** Zero code required. Very quotable in interviews. Unique angle.

---

## Notes
- Ideas here are *not* prioritized against each other — pick based on what's most interesting
  and what the portfolio needs at the time.
- When starting one of these, move it to its own folder/README rather than expanding this file.
