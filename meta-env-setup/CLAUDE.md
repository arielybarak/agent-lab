# meta-env-setup

Claude Code kit for building and evaluating `.claude/` setups. Run all commands from this directory.

## Tools

- `tools/scaffold_claude_setup.py` — bootstrap a `.claude/` skeleton, add skills/commands/agents.
  `--pool <topic>` parks a block in `.claude/tools-pool/<kind>/<topic>/` (built now, zero routing
  budget until promoted with `mv`) — for a block that belongs to a later phase, not current work.
- `tools/mine_transcripts.py --repo <path>` — mines that repo's Claude Code session transcripts
  for repeated commands, throwaway inline scripts, and deploy→wait loops. Run it before analyzing
  a repo you've already worked in by hand — it surfaces pain the code alone can't show.
- `tools/validate_claude_setup.py` — structural gate + effectiveness modes (`--score`, `--stale
  --repo <path>` for blocks citing code that no longer exists, `--route`, `--ablate`)
- `evals/` — routing tests and task suites per repo

## When authoring skills

**Use the scaffold+score loop — do not skip it:**

```bash
# 1. Scaffold (generates valid frontmatter)
python tools/scaffold_claude_setup.py add skill <name> --dir <setup-dir> --desc "<what + when>"

# 2. Fill the body

# 3. Score — iterate description until high before finalizing body
python tools/validate_claude_setup.py <setup-dir> --score
```

The `skill-creator-lite` skill (`.claude/skills/skill-creator-lite/`) is the authoritative guide.
A hook fires automatically after every SKILL.md write to remind you to run `--score`.

Target: all sub-scores green, budget under ceiling. Description quality (trigger + specificity)
matters more than body length.

## Validate all setups

```bash
python tools/validate_claude_setup.py claude-setups/*/ . --score
```

## Brownfield — upgrade an existing repo setup from a backlog

Repo already has `.claude/` + a demands doc? Use `/upgrade-claude-setup` instead of `/new-claude-setup`:
1. Author a `setup-backlog.md` from `templates/setup-backlog.md` (or discover an existing `tooling-review.md`).
2. Run `/upgrade-claude-setup <repo-path>` — it imports, reconciles (incl. a `--stale` pass over
   existing blocks), authors, and refines to target.
