#!/usr/bin/env python3
"""Neutrality gate for course-template's mandatory core.

The mandatory core must carry no subject-specific wording (spec 000 FR-020 / SC-002). This scans
exactly the paths `manifest.yaml` marks as `core` against the maintained denylist in
`neutrality-terms.txt`, and exits non-zero on any hit.

Scope is deliberate: modules and profiles MAY carry subject-specific terms — only the core must be
clean. Pass --all to scan every tier anyway (advisory; never changes the exit code contract for
core).

The denylist is a maintained artifact that ships with the template, so a re-distillation re-runs
the same gate. It is a plain term-per-line file with no comment syntax, which keeps it usable
verbatim with `grep -f` (the documented manual fallback in the feature's quickstart.md).

Usage:
    python tools/neutrality_scan.py [--template DIR] [--all]

Exit codes:
    0  no hits in core
    1  at least one hit in core
    2  the template or one of its required files is missing/malformed
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "course-template"


class TemplateError(Exception):
    """The template tree is missing a required file or is malformed."""


def load_terms(path: Path) -> list[str]:
    """Read the denylist: one term per line, blanks ignored, no comment syntax."""
    if not path.is_file():
        raise TemplateError(f"denylist not found: {path}")
    terms = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    terms = [t for t in terms if t]
    if not terms:
        raise TemplateError(f"denylist is empty: {path}")
    return terms


def load_tiers(manifest: Path) -> dict[str, list[str]]:
    """Extract `tier -> [path]` from manifest.yaml.

    Deliberately a small line parser rather than a YAML dependency: the repo is stdlib-only, and
    the manifest's shape is fixed by contracts/template-manifest.md. It reads the top-level
    `core:` list and every `pieces:` list, tagging each with the tier it was found under.
    """
    if not manifest.is_file():
        raise TemplateError(f"manifest not found: {manifest}")

    tiers: dict[str, list[str]] = {"core": []}
    section = None      # "core" | "profiles" | "modules"
    current = None      # the tier label paths are currently being collected into
    in_pieces = False

    for raw in manifest.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1]
            current = "core" if section == "core" else None
            in_pieces = False
            continue

        if stripped.startswith("- "):
            value = stripped[2:].strip().strip('"').strip("'")
            if current and (section == "core" or in_pieces):
                tiers.setdefault(current, []).append(value)
            continue

        if section in ("profiles", "modules") and indent == 2 and stripped.endswith(":"):
            name = stripped[:-1]
            kind = "profile" if section == "profiles" else "module"
            current = f"{kind}:{name}"
            tiers.setdefault(current, [])
            in_pieces = False
            continue

        in_pieces = stripped == "pieces:"

    if not tiers["core"]:
        raise TemplateError(f"manifest declares no core pieces: {manifest}")
    return tiers


def scan(root: Path, paths: list[str], terms: list[str]) -> list[tuple[str, int, str, str]]:
    """Return (path, line_no, term, line_text) for every case-insensitive term hit."""
    patterns = [(t, re.compile(re.escape(t), re.IGNORECASE)) for t in terms]
    hits: list[tuple[str, int, str, str]] = []
    for rel in paths:
        target = root / rel
        if not target.is_file():
            raise TemplateError(f"manifest lists a path that does not exist: {rel}")
        for line_no, text in enumerate(target.read_text(encoding="utf-8").splitlines(), start=1):
            for term, pattern in patterns:
                if pattern.search(text):
                    hits.append((rel, line_no, term, text.strip()))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE,
                        help="template root (default: ../course-template)")
    parser.add_argument("--all", action="store_true",
                        help="also scan profiles and modules (advisory — they may carry terms)")
    args = parser.parse_args(argv)

    root: Path = args.template
    try:
        terms = load_terms(root / "neutrality-terms.txt")
        tiers = load_tiers(root / "manifest.yaml")
        core_hits = scan(root, tiers["core"], terms)
        other_hits = {}
        if args.all:
            for tier, paths in tiers.items():
                if tier != "core":
                    other_hits[tier] = scan(root, paths, terms)
    except TemplateError as exc:
        print(f"neutrality-scan: {exc}", file=sys.stderr)
        return 2

    print(f"scanned {len(tiers['core'])} core file(s) against {len(terms)} term(s)")
    for rel, line_no, term, text in core_hits:
        print(f"CORE HIT  {rel}:{line_no}: {term!r} in {text}")

    if args.all:
        for tier, hits in sorted(other_hits.items()):
            for rel, line_no, term, text in hits:
                print(f"(advisory) {tier}  {rel}:{line_no}: {term!r} in {text}")

    if core_hits:
        print(f"\nFAIL: {len(core_hits)} subject-specific term(s) in the mandatory core")
        return 1
    print("\nPASS: 0 subject-specific terms in the mandatory core")
    return 0


if __name__ == "__main__":
    sys.exit(main())
