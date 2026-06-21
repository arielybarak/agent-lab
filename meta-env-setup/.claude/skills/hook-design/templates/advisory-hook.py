#!/usr/bin/env python3
"""Advisory nag — Claude Code PreToolUse hook (copy-and-adapt).

The NON-blocking archetype: it never stops anything, it just prints a reminder to
the transcript when a risky pattern shows up. Shown here on a Bash command (so you
also see the `command` stdin shape, not just `file_path`). For the BLOCKING variant,
see guard-hook.py.

Contract: exit 0 always (this hook only advises). Stdout is shown in the transcript.

Wire it in .claude/settings.json:
  "hooks": {
    "PreToolUse": [
      {"matcher": "Bash",
       "hooks": [{"type": "command",
                  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/advise.py\""}]}
    ]
  }

Golden rule: fail OPEN and never raise — an advisory hook that errors is worse than
no hook, because it adds noise without value.
"""

import json
import sys

# TODO: (substring, advice) pairs. Tune to the thing people forget in THIS repo.
NAGS = (
    ("pytest", "Run the full suite, not just one test, before claiming green."),
    ("benchmark", "Drop the page cache and use repeated runs for a fair benchmark."),
)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0  # fail OPEN

    # PreToolUse on Bash carries the command string (not file_path).
    command = (event.get("tool_input", {}) or {}).get("command", "")
    if isinstance(command, str):
        low = command.lower()
        for needle, advice in NAGS:
            if needle in low:
                print(f"[advise] {advice}")
                break  # one nudge is enough; don't spam

    return 0  # always allow — this hook only advises


if __name__ == "__main__":
    sys.exit(main())
