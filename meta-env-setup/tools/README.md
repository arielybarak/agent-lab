# tools/ — Claude-setup meta-tooling

Bootstrapping a Claude Code (`.claude/`) configuration for a repo is a repetitive,
boilerplate-heavy task. These two stdlib-only scripts turn it into one-liners, so
the hub can spin up and quality-gate per-repo setups quickly and consistently.

No third-party dependencies — they run anywhere with `python3` and stay trivially
auditable (matching the hub's "simplicity over cleverness" rule in `CLAUDE.md`).

## `scaffold_claude_setup.py` — create the skeleton
```bash
# Create .claude/{skills,commands,agents,hooks} + settings.json (+ optional CLAUDE.md)
python tools/scaffold_claude_setup.py init claude-setups/<repo> --with-claude-md

# Add building blocks (--dir = folder holding .claude/; --desc fills the description)
python tools/scaffold_claude_setup.py add skill   <name> --dir claude-setups/<repo> --desc "..."
python tools/scaffold_claude_setup.py add command <name> --dir claude-setups/<repo>
python tools/scaffold_claude_setup.py add agent   <name> --dir claude-setups/<repo> --desc "..."
python tools/scaffold_claude_setup.py add hook    <name> --dir claude-setups/<repo>   # then wire in settings.json

# Inspect what a setup contains
python tools/scaffold_claude_setup.py list --dir claude-setups/<repo>
```
Generated files are minimal but **valid** — skills and agents already carry the
required `name` + `description` front-matter, so the validator passes on a fresh
scaffold. Fill in the body, then re-validate. Use `--force` to overwrite.

## `validate_claude_setup.py` — gate the result (CI-friendly)
```bash
python tools/validate_claude_setup.py claude-setups/<repo>
python tools/validate_claude_setup.py claude-setups/*/ .                # all setups + hub at once
python tools/validate_claude_setup.py claude-setups/<repo> --json      # machine-readable
python tools/validate_claude_setup.py claude-setups/<repo> --strict    # warnings fail too
```
Checks: skills/agents have non-empty `name` + `description`; `name` matches the
folder and is kebab-case; commands have a `description`; descriptions aren't TODO
placeholders, too terse, or over-long; **`settings.json` is valid JSON and every
hook it wires points at a real script** (and hook scripts nothing references are
flagged as orphans). Accepts **multiple roots** at once. **Exit code is non-zero
on any error**, so it can gate CI. It mirrors the spirit of
`initial-sendbox/hooks/governance-audit` (which audits Copilot `.agent.md` files)
but targets Claude Code's layout.

## Beyond validity: is the setup *effective* and *minimal*?
`validate` proves a setup is **well-formed**; it says nothing about whether each
block pulls its weight. Three further modes (same tool) measure that — a 3-layer
evaluation from cheap static guesses to behavioral proof. **Only the default mode
gates CI**; the rest are advisory / their own test suites.
```bash
# Layer 1 — static effectiveness audit: context budget, redundancy, trigger
# quality, specificity, agent least-privilege -> a 0-100 score + cut/sharpen hints.
python tools/validate_claude_setup.py claude-setups/<repo> --score
python tools/validate_claude_setup.py claude-setups/<repo> --score --min-score 80   # optional gate

# Layer 2 — routing tests: do descriptions fire on the right prompts (evals/<repo>/routing-tests.json)?
python tools/validate_claude_setup.py claude-setups/<repo> --route

# Layer 3 — ablation: remove a block, re-run real tasks, see what degrades.
python tools/validate_claude_setup.py claude-setups/<repo> --ablate            # free dry-run preview
python tools/validate_claude_setup.py claude-setups/<repo> --ablate --execute  # launches `claude -p`
```
The eval data (task suites, routing tests) and the full methodology live in
[`../evals/`](../evals/). Layer 3's heavy, agent-running logic is isolated in
`_ablation.py`. The deterministic scorers + the ablation verdict logic are unit-tested:
```bash
python tools/test_audit.py
```

## How they fit the workflow
These are step 3, step 5, and step 7 of the `claude-setup-scaffolder` skill
(`.claude/skills/claude-setup-scaffolder/`): analyze → decide → **scaffold** → fill →
**validate** → package → **evaluate**. The per-repo outputs land in `claude-setups/<repo>/`.

## Quick self-check
```bash
python tools/validate_claude_setup.py claude-setups/*/ .   # every setup + the hub's own
```
