#!/usr/bin/env python3
"""Frozen-region guard — Claude Code PreToolUse hook.

Blocks edits to a protected path (a frozen module, a vendored dir, a submitted
assignment). Advisory archetypes are the same shape but `return 0` with a stdout
note instead of `return 2`.

Claude Code feeds the tool event as JSON on stdin. Contract:
  * exit 0  -> allow (anything printed to stdout is shown as an advisory note)
  * exit 2  -> BLOCK (stderr message is fed back to Claude so it can adjust)

Wire it in .claude/settings.json:
  "hooks": {
    "PreToolUse": [
      {"matcher": "Edit|Write|MultiEdit",
       "hooks": [{"type": "command",
                  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py\""}]}
    ]
  }

Golden rule: never break a workflow on the hook's own bug — fail OPEN (exit 0) on
any parse error or unexpected shape.
"""

import json
import sys

# TODO: the path prefixes this hook protects (relative to the repo root).
PROTECTED_PREFIXES = (
    "project-A/",     # e.g. a frozen/submitted module
    "vendor/",
)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0  # fail OPEN — a malformed event must never wedge the session

    tool_input = event.get("tool_input", {}) or {}
    path = tool_input.get("file_path") or ""
    if not isinstance(path, str):
        return 0

    # Normalize a leading ./ and compare against the protected prefixes.
    rel = path.lstrip("./")
    if any(rel.startswith(p) for p in PROTECTED_PREFIXES):
        sys.stderr.write(
            f"[guard] '{path}' is in a frozen/protected region "
            f"({', '.join(PROTECTED_PREFIXES)}). Edit a copy or get explicit sign-off "
            f"before changing it.\n"
        )
        return 2  # BLOCK

    return 0  # allow


if __name__ == "__main__":
    sys.exit(main())
