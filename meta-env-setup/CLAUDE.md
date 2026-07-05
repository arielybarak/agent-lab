# meta-env-setup

Claude Code kit for building and evaluating `.claude/` setups. Run all commands from this directory.
Full narrative + evidence: `README.md`. This file is the operational quick-reference.

## Layout

- `tools/` — the machinery, detailed in "Tools" below (+ `_ablation.py`, `test_audit.py`;
  see `tools/README.md` for flags).
- `.claude/` — the kit's own setup (auto-loads when working in this folder): commands
  `/new-claude-setup` (greenfield), `/upgrade-claude-setup` (brownfield), `/refine-setup`,
  `/audit-claude-setup`; agents `setup-analyzer` (nine-determinant inspection + reconcile),
  `block-author` (fill), `setup-critic` (judge + prescribe); skills `claude-setup-scaffolder`
  (the whole pipeline), `skill-creator-lite` (author one skill, scored), `hook-design`.
- `cookbook/` — proven block archetypes (skills/commands/agents/hooks) with copy-paste
  templates. **Check here before writing a block from scratch** — start from an archetype,
  not a blank file.
- `templates/` — `setup-spec.md` (the PRD the analysis step fills) and `setup-backlog.md`
  (the brownfield-upgrade backlog shape).
- `evals/` — routing tests + task suites per repo (effectiveness-mode input).
- `plans/` — writeups of methodology changes to the kit itself (e.g. analyzer improvements).
- `claude-setups/<repo>/` — generated `.claude/` setups for other repos, each with a dry-run
  `install.sh`. Gitignored — never written into the real target repo except via
  `install.sh --apply`.

## Tools

- `tools/scaffold_claude_setup.py` — bootstrap a `.claude/` skeleton, add skills/commands/agents.
  `--pool <topic>` parks a block in `.claude/tools-pool/<kind>/<topic>/` (built now, zero routing
  budget until promoted with `mv`) — for a block that belongs to a later phase, not current work.
- `tools/mine_transcripts.py --repo <path>` — mines that repo's Claude Code session transcripts
  for repeated commands, throwaway inline scripts, and deploy→wait loops. Run it before analyzing
  a repo you've already worked in by hand — it surfaces pain the code alone can't show.
- `tools/validate_claude_setup.py` — structural gate + effectiveness modes (`--score`, `--stale
  --repo <path>` for blocks citing code that no longer exists, `--route`, `--ablate`)

## When authoring skills

**Use the scaffold+score loop — do not skip it:**

```bash
# 1. Scaffold (generates valid frontmatter)
python tools/scaffold_claude_setup.py add skill <name> --dir <setup-dir> --desc "<what + when>"

# 2. Fill the body — start from a cookbook/ archetype if one fits

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
1. Author a `setup-backlog.md` from `templates/setup-backlog.md`, or discover an existing
   `tooling-review.md` in the target repo — or, if the target repo already has this kit's
   `/setup-retro` command installed, run that first to generate one from the painful session.
2. Run `/upgrade-claude-setup <repo-path>` — it imports, reconciles (incl. a `--stale` pass over
   existing blocks), authors, and refines to target.
