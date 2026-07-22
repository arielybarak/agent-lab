"""Tests for the neutrality gate.

Run: python -m pytest course-factory/tools/test_neutrality_scan.py
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

import neutrality_scan as ns


def build_template(root: Path, *, core_text: str = "topic-neutral prose\n",
                   module_text: str = "topic-neutral prose\n") -> Path:
    """Write a minimal but structurally real template tree."""
    (root / ".claude/skills/lesson-arc").mkdir(parents=True)
    (root / ".claude/skills/diagrams").mkdir(parents=True)
    (root / "profiles/default").mkdir(parents=True)

    (root / ".claude/skills/lesson-arc/SKILL.md").write_text(core_text, encoding="utf-8")
    (root / ".claude/skills/diagrams/SKILL.md").write_text(module_text, encoding="utf-8")
    (root / "profiles/default/spine.md").write_text("linear-spiral\n", encoding="utf-8")
    (root / "neutrality-terms.txt").write_text("System Design\nHomeOS\n", encoding="utf-8")
    (root / "manifest.yaml").write_text(textwrap.dedent("""\
        version: "1.0.0"

        core:
          - .claude/skills/lesson-arc/SKILL.md

        profiles:
          default:
            default: true
            pieces:
              - profiles/default/spine.md

        modules:
          diagrams:
            pieces:
              - .claude/skills/diagrams/SKILL.md
            depends_on: []
        """), encoding="utf-8")
    return root


def test_clean_core_passes(tmp_path):
    root = build_template(tmp_path / "t")
    assert ns.main(["--template", str(root)]) == 0


def test_term_in_core_fails(tmp_path):
    root = build_template(tmp_path / "t", core_text="scale it like a System Design course\n")
    assert ns.main(["--template", str(root)]) == 1


def test_match_is_case_insensitive(tmp_path):
    root = build_template(tmp_path / "t", core_text="the homeos example\n")
    assert ns.main(["--template", str(root)]) == 1


def test_term_in_a_module_does_not_fail_the_gate(tmp_path):
    """Modules and profiles may carry subject-specific wording — only core must be clean."""
    root = build_template(tmp_path / "t", module_text="the HomeOS diagram\n")
    assert ns.main(["--template", str(root)]) == 0
    assert ns.main(["--template", str(root), "--all"]) == 0


def test_manifest_tiers_are_parsed(tmp_path):
    root = build_template(tmp_path / "t")
    tiers = ns.load_tiers(root / "manifest.yaml")
    assert tiers["core"] == [".claude/skills/lesson-arc/SKILL.md"]
    assert tiers["profile:default"] == ["profiles/default/spine.md"]
    assert tiers["module:diagrams"] == [".claude/skills/diagrams/SKILL.md"]


def test_missing_denylist_is_a_setup_error(tmp_path):
    root = build_template(tmp_path / "t")
    (root / "neutrality-terms.txt").unlink()
    assert ns.main(["--template", str(root)]) == 2


def test_manifest_path_that_does_not_exist_is_a_setup_error(tmp_path):
    root = build_template(tmp_path / "t")
    (root / ".claude/skills/lesson-arc/SKILL.md").unlink()
    assert ns.main(["--template", str(root)]) == 2


def test_real_template_core_is_neutral():
    """The shipped template must pass its own gate."""
    root = Path(__file__).resolve().parent.parent / "course-template"
    if not (root / "manifest.yaml").is_file():
        pytest.skip("course-template not present")
    assert ns.main(["--template", str(root)]) == 0
