#!/usr/bin/env python3
"""Scaffold a Claude Code setup (``.claude/``) for any repository.

Meta-tooling for the ``agents_sendbox`` hub. Bootstrapping a Claude Code
configuration — skills, slash commands, subagents, hooks, settings — is a
repetitive, boilerplate-heavy task, so this turns it into one-liners instead of
hand-copying templates every time a new repo needs an AI setup.

Stdlib only: runs anywhere with ``python3`` and stays trivially auditable (the
hub's "simplicity over cleverness" rule, see CLAUDE.md).

Examples
--------
Create the skeleton and seed a CLAUDE.md::

    python tools/scaffold_claude_setup.py init claude-setups/my-repo --with-claude-md

Add building blocks (``--dir`` is the folder that holds ``.claude/``; default ``.``).
``--desc`` fills the description so the validator passes without a TODO warning::

    python tools/scaffold_claude_setup.py add skill   perf-profiling --dir claude-setups/my-repo \\
        --desc "perf + FlameGraph workflow; USE WHEN profiling or reading a flamegraph"
    python tools/scaffold_claude_setup.py add command profile     --dir claude-setups/my-repo
    python tools/scaffold_claude_setup.py add agent   perf-analyst --dir claude-setups/my-repo
    python tools/scaffold_claude_setup.py add hook    bench-guard  --dir claude-setups/my-repo

Inspect what a setup contains::

    python tools/scaffold_claude_setup.py list --dir claude-setups/my-repo

Generated files are minimal but *valid*: skills/agents carry the required
``name`` + ``description`` front-matter, so ``validate_claude_setup.py`` passes on
a fresh scaffold. Fill in the body, then re-validate.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# --- Templates ---------------------------------------------------------------

_SKILL_TODO = (
    "TODO one to three sentences: what this skill does AND when to use it "
    "(include trigger phrases). Claude reads ONLY this line to decide whether to "
    "load the skill, so make it specific."
)
_AGENT_TODO = (
    "TODO when the orchestrator should delegate to this subagent. Be specific — "
    "routing is decided from this line. Add 'Use PROACTIVELY for ...' if it should "
    "auto-trigger."
)

SKILL_TEMPLATE = """\
---
name: {name}
description: >-
  {desc}
---

# {title}

## When to use
- TODO trigger condition
- TODO user phrasing that should activate this skill

## Workflow
1. TODO step
2. TODO step

## Conventions / gotchas
- TODO the non-obvious rule a newcomer would get wrong
"""

COMMAND_TEMPLATE = """\
---
description: {desc}
argument-hint: "[optional-args]"
---

TODO: the prompt body that runs when the user types /{name}.

Reference arguments with `$ARGUMENTS` (everything after the command) or the
positional forms `$1`, `$2`, ... You can also embed shell output with
`!`+backtick-command and file contents with `@path/to/file`.
"""

AGENT_TEMPLATE = """\
---
name: {name}
description: >-
  {desc}
# `tools` is optional. Omit it to inherit all tools; narrow it for least-privilege.
tools: Read, Grep, Glob
---

You are TODO — a focused subagent.

## Scope
- You DO: TODO
- You do NOT: TODO (e.g. never edit code; report findings only)

## Method
1. TODO how you work
2. TODO what you return to the caller
"""

HOOK_TEMPLATE = '''\
#!/usr/bin/env python3
"""{title} — Claude Code hook (advisory, non-blocking by default).

Claude Code feeds the tool event as JSON on stdin. Exit 0 to allow; print to
stdout for an advisory note shown in the transcript; for a PreToolUse hook, exit
2 with a message on stderr to BLOCK the action (the message is fed back to Claude).

Wire it in .claude/settings.json, e.g.:

    "hooks": {{
      "PreToolUse": [
        {{
          "matcher": "Edit|Write",
          "hooks": [
            {{ "type": "command",
              "command": "python3 \\"$CLAUDE_PROJECT_DIR/.claude/hooks/{name}.py\\"" }}
          ]
        }}
      ]
    }}

Keep it conservative — never break a workflow on the hook's own bug.
"""

import json
import sys


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0  # never break the workflow on a parse error
    tool_input = event.get("tool_input", {{}}) or {{}}
    path = tool_input.get("file_path") or ""
    # TODO: decide when to advise. Example:
    # if isinstance(path, str) and path.endswith(".py"):
    #     print("[{name}] advisory message")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

SETTINGS_TEMPLATE = """\
{
  "permissions": {
    "allow": [],
    "deny": [],
    "additionalDirectories": []
  }
}
"""

CLAUDE_MD_TEMPLATE = """\
# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is
TODO one paragraph: the project's purpose and current state.

## The one rule that overrides others
TODO the project-specific principle a newcomer would violate.

## Layout
TODO the directories that matter and what lives in each.

## Common commands
```bash
# TODO build / test / lint entry points
```

## Conventions to follow
- TODO project-specific rules (style guide, do's and don'ts).

## Gotchas
- TODO the things that surprise newcomers.
"""

# `add` element kind -> subdir under .claude/
ELEMENTS = {"skill": "skills", "command": "commands", "agent": "agents", "hook": "hooks"}
SUBDIRS = ("skills", "commands", "agents", "hooks")


def _write(path: Path, content: str, force: bool, executable: bool = False) -> bool:
    """Write ``content`` to ``path``; skip if it exists unless ``force``."""
    if path.exists() and not force:
        print(f"  skip (exists): {path}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)
    print(f"  wrote: {path}")
    return True


def _title(name: str) -> str:
    """`perf-profiling` -> `Perf Profiling` for a human-readable heading."""
    return name.replace("-", " ").replace("_", " ").title()


def cmd_init(args: argparse.Namespace) -> int:
    """Create the ``.claude/`` skeleton (+ optional CLAUDE.md) at the target."""
    root = Path(args.target)
    claude = root / ".claude"
    print(f"Scaffolding Claude Code setup at: {root}")
    for sub in SUBDIRS:
        (claude / sub).mkdir(parents=True, exist_ok=True)
        _write(claude / sub / ".gitkeep", "", args.force)
    _write(claude / "settings.json", SETTINGS_TEMPLATE, args.force)
    if args.with_claude_md:
        _write(root / "CLAUDE.md", CLAUDE_MD_TEMPLATE, args.force)
    me = Path(__file__).name
    print(
        "\nDone. Next:\n"
        f"  - add a skill:   python {me} add skill <name> --dir {root} --desc '...'\n"
        f"  - add a command: python {me} add command <name> --dir {root}\n"
        f"  - add an agent:  python {me} add agent <name> --dir {root} --desc '...'\n"
        f"  - add a hook:    python {me} add hook <name> --dir {root}\n"
        f"  - validate:      python {Path(__file__).parent / 'validate_claude_setup.py'} {root}"
    )
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    """Add a single skill / command / agent / hook under an existing setup root."""
    root = Path(args.dir)
    base = root / ".claude" / ELEMENTS[args.kind]
    name = args.name
    print(f"Adding {args.kind}: {name}")

    if args.kind == "skill":
        target = base / name / "SKILL.md"
        content = SKILL_TEMPLATE.format(name=name, title=_title(name), desc=args.desc or _SKILL_TODO)
        wrote = _write(target, content, args.force)
    elif args.kind == "command":
        target = base / f"{name}.md"
        desc = args.desc or f"TODO short text shown in the slash-command menu for /{name}."
        content = COMMAND_TEMPLATE.format(name=name, desc=desc)
        wrote = _write(target, content, args.force)
    elif args.kind == "agent":
        target = base / f"{name}.md"
        content = AGENT_TEMPLATE.format(name=name, desc=args.desc or _AGENT_TODO)
        wrote = _write(target, content, args.force)
    else:  # hook
        target = base / f"{name}.py"
        content = HOOK_TEMPLATE.format(name=name, title=_title(name))
        wrote = _write(target, content, args.force, executable=True)
        if wrote:
            print(
                f"  note: wire it into {root}/.claude/settings.json under \"hooks\" "
                "(the file header shows the snippet)."
            )

    if not wrote:
        print("  (use --force to overwrite)")
        return 1
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List the building blocks present in a setup."""
    root = Path(args.dir)
    claude = root / ".claude" if (root / ".claude").is_dir() else root
    if not claude.is_dir():
        print(f"no .claude/ found at {root}", file=sys.stderr)
        return 1
    print(f"Setup: {root}")
    skills = sorted(p.parent.name for p in claude.glob("skills/*/SKILL.md"))
    commands = sorted(p.stem for p in claude.glob("commands/*.md"))
    agents = sorted(p.stem for p in claude.glob("agents/*.md"))
    hooks = sorted(p.name for p in claude.glob("hooks/*.py"))
    for label, items in (("skills", skills), ("commands", commands), ("agents", agents), ("hooks", hooks)):
        print(f"  {label:9} ({len(items)}): {', '.join(items) if items else '-'}")
    print(f"  settings: {'present' if (claude / 'settings.json').is_file() else 'MISSING'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Scaffold a Claude Code (.claude/) setup for a repository.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create the .claude/ skeleton")
    p_init.add_argument("target", help="setup root (the folder that will contain .claude/)")
    p_init.add_argument("--with-claude-md", action="store_true", help="also seed a CLAUDE.md stub")
    p_init.add_argument("--force", action="store_true", help="overwrite existing files")
    p_init.set_defaults(func=cmd_init)

    p_add = sub.add_parser("add", help="add a skill / command / agent / hook")
    p_add.add_argument("kind", choices=sorted(ELEMENTS), help="element type")
    p_add.add_argument("name", help="element name (kebab-case)")
    p_add.add_argument("--dir", default=".", help="setup root containing .claude/ (default: .)")
    p_add.add_argument("--desc", default="", help="fill the description (skills/commands/agents)")
    p_add.add_argument("--force", action="store_true", help="overwrite if it exists")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list the blocks in a setup")
    p_list.add_argument("--dir", default=".", help="setup root containing .claude/ (default: .)")
    p_list.set_defaults(func=cmd_list)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
