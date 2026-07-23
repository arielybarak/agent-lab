#!/usr/bin/env python3
"""DIFFS.md — the append-only forward-diff ledger (001 FR-023/027).

Gated phases are immutable once passed. A later change to an already-gated artifact is applied as
an explicit forward diff at the current phase and logged here — never by re-opening the phase.
Schema: specs/course-factory/001-pipeline-skeleton/contracts/diffs-ledger.md. This module only
appends; it never edits or reorders existing entries.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_HEADER = "# Forward-Diff Ledger\n\n_Append-only (FR-027) — never edited retroactively._\n"
_ENTRY_RE = re.compile(
    r"^## \[(?P<timestamp>[^\]]+)\] (?P<target>.+)\n"
    r"- \*\*What changed:\*\* (?P<what_changed>.*)\n"
    r"- \*\*Why:\*\* (?P<why>.*)\n"
    r"- \*\*Applied at phase:\*\* (?P<applied_at_phase>.*)\n?",
    re.MULTILINE,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_diff(
    path: Path,
    *,
    target: str,
    what_changed: str,
    why: str,
    applied_at_phase: str,
    now: str | None = None,
) -> None:
    """Append one forward-diff entry. Creates the file (with header) if it doesn't exist yet.
    Never reads existing entries back into memory to rewrite them — pure append."""
    now = now or _now_iso()
    entry = (
        f"\n## [{now}] {target}\n"
        f"- **What changed:** {what_changed}\n"
        f"- **Why:** {why}\n"
        f"- **Applied at phase:** {applied_at_phase}\n"
    )
    if not path.is_file():
        path.write_text(_HEADER, encoding="utf-8")
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)


def read_diffs(path: Path) -> list[dict[str, str]]:
    """Parse existing entries in applied order — for tests/consumers, never for rewriting."""
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    return [m.groupdict() for m in _ENTRY_RE.finditer(text)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append one entry to a course's DIFFS.md")
    parser.add_argument("diffs_path", type=Path)
    parser.add_argument("--target", required=True)
    parser.add_argument("--what-changed", required=True)
    parser.add_argument("--why", required=True)
    parser.add_argument("--applied-at-phase", required=True)
    args = parser.parse_args(argv)

    append_diff(
        args.diffs_path,
        target=args.target,
        what_changed=args.what_changed,
        why=args.why,
        applied_at_phase=args.applied_at_phase,
    )
    print(f"appended forward diff to {args.diffs_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
