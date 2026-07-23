#!/usr/bin/env python3
"""deliver_check.py — the required-artifact-presence check at delivery (001 FR-020, SC-008).

Schema: specs/course-factory/001-pipeline-skeleton/contracts/course-folder.md. Delivery clears on
`COURSE_REPORT.md` **presence**, any verdict (FR-011/021) — this check only verifies the full
artifact set exists, it never grades content.

Lesson-file location: `002`/`003` own the final `.md`/`.ipynb` format decision (spec Assumptions);
001 ships stub phase handlers and picks `lessons/<id>.md` or `.ipynb` as the placeholder
convention its stub writes to. Real handlers may relocate this — this check only needs the
convention to exist somewhere consistent, and reads it from `BUILD_PROGRESS.md`'s `lessons[]`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import progress  # noqa: E402

REQUIRED_FILES = [
    "COURSE_BRIEF.md",
    "SOURCES.md",
    "BUILD_PROGRESS.md",
    "DIFFS.md",
    "FEEDBACK.md",
    "SYLLABUS.md",
    "COURSE_REPORT.md",
]

# Canonical set lives in progress.py (settle_lesson() records only these) — import it rather than
# re-declaring, so the "what counts as a finished lesson" rule can never drift between the two tools.
TERMINAL_LESSON_STATUSES = progress.TERMINAL_LESSON_STATUSES


def missing_artifacts(course_dir: Path, state: dict[str, Any]) -> list[str]:
    """Return every required artifact that is absent — empty means delivery may clear (SC-008)."""
    missing = [name for name in REQUIRED_FILES if not (course_dir / name).is_file()]
    claude_dir = course_dir / ".claude"
    if not claude_dir.is_dir() or not any(claude_dir.rglob("*")):
        missing.append(".claude/ (missing or empty — the frozen template residue, FR-020)")

    lessons = state.get("lessons") or []
    if not lessons:
        missing.append("lessons[] (no lessons recorded in BUILD_PROGRESS.md)")
    for lesson in lessons:
        if lesson["status"] not in TERMINAL_LESSON_STATUSES:
            missing.append(f"lessons/{lesson['id']} (status: {lesson['status']}, not terminal)")
            continue
        lid = lesson["id"]
        if not any((course_dir / "lessons" / f"{lid}{ext}").is_file() for ext in (".md", ".ipynb")):
            missing.append(f"lessons/{lid}.md|.ipynb")

    return missing


def check_delivery(course_dir: Path, state: dict[str, Any]) -> bool:
    return not missing_artifacts(course_dir, state)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("course_dir", type=Path)
    args = parser.parse_args(argv)

    try:
        state = progress.read_state(args.course_dir / "BUILD_PROGRESS.md")
    except progress.IntegrityError as exc:
        print(f"deliver_check: {exc}", file=sys.stderr)
        return 2

    missing = missing_artifacts(args.course_dir, state)
    if missing:
        print("MISSING:")
        for item in missing:
            print(f"  - {item}")
        return 1

    print("PASS: all required delivery artifacts present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
