"""Tests for course-factory/tools/instantiate.py.

Covers US1 (SC-001/002/003/009): brief-completeness backstop, overlay-for-selected-profile +
enabled modules + version stamp + stubs, copy-never-mutate, and the absent/unversioned-template halt.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

import instantiate as inst
import progress

FIXTURE_TEMPLATE = Path(__file__).resolve().parent / "fixtures" / "template-min"
FIXTURE_SPEC = Path(__file__).resolve().parent / "fixtures" / "specs" / "well-formed.md"


def well_formed_brief(*, profile: str = "default", modules: dict | None = None) -> str:
    fields = {
        "topic_scope": {"topic": "Widget Systems", "in_scope": ["assembly"], "out_of_scope": ["materials"]},
        "audience": {"description": "a hobbyist", "prior_knowledge": "basic hand tools"},
        "running_example": "MiniLine",
        "source_pointers": ["fixture placeholder"],
        "archetype_profile": profile,
        "modules": modules if modules is not None else {"sample-module": False},
        "lesson_format": None,
    }
    return "# Course Brief\n\n```json\n" + json.dumps(fields, indent=2) + "\n```\n"


def _tree_checksum(root: Path) -> dict[str, str]:
    checksums = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            checksums[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return checksums


# --------------------------------------------------------------------------------------------
# Brief completeness backstop (T006, SC-001/002) — halts, no fabrication, no partial folder
# --------------------------------------------------------------------------------------------

@pytest.mark.parametrize("mutate,missing", [
    (lambda f: f.pop("running_example"), "running_example"),
    (lambda f: f.__setitem__("running_example", ""), "running_example"),
    (lambda f: f.pop("archetype_profile"), "archetype_profile"),
    (lambda f: f.pop("modules"), "modules"),
    (lambda f: f.__setitem__("modules", {}), "modules"),  # missing sample-module entry
    (lambda f: f.pop("source_pointers"), "source_pointers"),
    (lambda f: f.__setitem__("source_pointers", []), "source_pointers"),
    (lambda f: f.__setitem__("audience", {"description": "x"}), "prior_knowledge"),
    (lambda f: f.__setitem__("topic_scope", {"topic": "x"}), "in_scope"),
])
def test_instantiate_halts_on_a_brief_missing_a_required_field(tmp_path, mutate, missing):
    fields = json.loads(well_formed_brief().split("```json\n", 1)[1].rsplit("\n```", 1)[0])
    mutate(fields)
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text("# Course Brief\n\n```json\n" + json.dumps(fields) + "\n```\n")
    courses_dir = tmp_path / "courses"

    with pytest.raises(inst.BriefError, match=missing):
        inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)

    assert not courses_dir.exists() or list(courses_dir.iterdir()) == []


def test_instantiate_halts_on_an_unknown_module_name(tmp_path):
    """A typo'd module name (e.g. 'diagram' for 'diagrams') must halt, not silently enable
    nothing — accepting it would look like success while doing nothing (FR-005)."""
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief(modules={"sample-module": False, "smaple-module": True}))
    courses_dir = tmp_path / "courses"

    with pytest.raises(inst.BriefError, match="smaple-module"):
        inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)
    assert not courses_dir.exists() or list(courses_dir.iterdir()) == []


def test_instantiate_halts_on_malformed_brief_json(tmp_path):
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text("# Course Brief\n\n```json\n{not valid\n```\n")
    courses_dir = tmp_path / "courses"

    with pytest.raises(inst.BriefError):
        inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)
    assert not courses_dir.exists() or list(courses_dir.iterdir()) == []


# --------------------------------------------------------------------------------------------
# Overlay + copy + version stamp + stubs (T006, SC-002)
# --------------------------------------------------------------------------------------------

def test_instantiate_produces_a_correct_overlaid_course_folder(tmp_path):
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief(modules={"sample-module": True}))
    courses_dir = tmp_path / "courses"

    course_dir = inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)

    assert course_dir.parent == courses_dir
    assert course_dir.name  # a slug was derived

    # Core + selected profile + enabled module all present:
    assert (course_dir / ".claude/skills/core-skill/SKILL.md").is_file()
    assert (course_dir / "profiles/default/spine.md").is_file()
    assert (course_dir / ".claude/skills/sample-module/SKILL.md").is_file()

    # The per-course artifacts:
    assert (course_dir / "COURSE_BRIEF.md").is_file()
    assert "MiniLine" in (course_dir / "COURSE_BRIEF.md").read_text()
    for stub in ("SOURCES.md", "FEEDBACK.md", "DIFFS.md"):
        assert (course_dir / stub).is_file()

    # BUILD_PROGRESS.md initialized at syllabus start, version stamped:
    state = progress.read_state(course_dir / "BUILD_PROGRESS.md")
    assert state["current_phase"] == "syllabus"
    assert state["template_version"] == "1.0.0"


def test_instantiate_excludes_a_disabled_module(tmp_path):
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief(modules={"sample-module": False}))
    courses_dir = tmp_path / "courses"

    course_dir = inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)

    assert not (course_dir / ".claude/skills/sample-module/SKILL.md").exists()
    assert (course_dir / ".claude/skills/core-skill/SKILL.md").is_file()  # core always present


def test_instantiate_derives_the_course_name_from_the_spec_title(tmp_path):
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief())
    courses_dir = tmp_path / "courses"

    course_dir = inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)
    assert course_dir.name == "intro-to-widget-systems"


def test_instantiate_without_a_spec_derives_the_name_from_the_brief_topic(tmp_path):
    """--spec is optional (only used for the title) — the brief's topic_scope.topic is the
    fallback, since instantiate() must work standalone against just a brief."""
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief())
    courses_dir = tmp_path / "courses"

    course_dir = inst.instantiate(spec=None, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)
    assert course_dir.name == "widget-systems"  # from topic_scope.topic, not a spec title


def test_instantiate_halts_when_neither_spec_nor_brief_topic_can_name_the_course(tmp_path):
    fields = json.loads(well_formed_brief().split("```json\n", 1)[1].rsplit("\n```", 1)[0])
    fields["topic_scope"]["topic"] = ""
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text("# Course Brief\n\n```json\n" + json.dumps(fields) + "\n```\n")

    # An empty topic is itself already a caught brief defect (topic_scope.topic is required) —
    # this asserts intake's completeness check fires before name-derivation is even reached.
    with pytest.raises(inst.BriefError):
        inst.instantiate(spec=None, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=tmp_path / "courses")


# --------------------------------------------------------------------------------------------
# Copy-never-mutate (T006, SC-003)
# --------------------------------------------------------------------------------------------

def test_source_template_is_byte_for_byte_unchanged_after_instantiation(tmp_path):
    before = _tree_checksum(FIXTURE_TEMPLATE)

    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief(modules={"sample-module": True}))
    inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=tmp_path / "courses")

    after = _tree_checksum(FIXTURE_TEMPLATE)
    assert after == before


# --------------------------------------------------------------------------------------------
# Absent / unversioned template halts, writes no partial folder (T007, FR-001, SC-009)
# --------------------------------------------------------------------------------------------

def test_absent_template_halts(tmp_path):
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief())
    courses_dir = tmp_path / "courses"

    with pytest.raises(inst.TemplateError):
        inst.instantiate(spec=FIXTURE_SPEC, template=tmp_path / "no-such-template", brief=brief_path, courses_dir=courses_dir)
    assert not courses_dir.exists() or list(courses_dir.iterdir()) == []


def test_missing_version_file_halts(tmp_path):
    broken = tmp_path / "template"
    shutil.copytree(FIXTURE_TEMPLATE, broken)
    (broken / "VERSION").unlink()

    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief())
    courses_dir = tmp_path / "courses"

    with pytest.raises(inst.TemplateError):
        inst.instantiate(spec=FIXTURE_SPEC, template=broken, brief=brief_path, courses_dir=courses_dir)
    assert not courses_dir.exists() or list(courses_dir.iterdir()) == []


def test_manifest_version_mismatch_halts(tmp_path):
    broken = tmp_path / "template"
    shutil.copytree(FIXTURE_TEMPLATE, broken)
    (broken / "VERSION").write_text("9.9.9\n")

    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief())
    courses_dir = tmp_path / "courses"

    with pytest.raises(inst.TemplateError):
        inst.instantiate(spec=FIXTURE_SPEC, template=broken, brief=brief_path, courses_dir=courses_dir)
    assert not courses_dir.exists() or list(courses_dir.iterdir()) == []


def test_no_partial_folder_survives_a_mid_copy_failure(tmp_path):
    broken = tmp_path / "template"
    shutil.copytree(FIXTURE_TEMPLATE, broken)
    # manifest promises a module piece that doesn't exist on disk -> must fail mid-copy, cleanly.
    # Appended as a sibling *under* the existing `modules:` key, not a second top-level `modules:`
    # section — the parser (like real YAML) lets a duplicate top-level key silently overwrite the
    # first, which would drop `sample-module` entirely and mask what this test means to exercise.
    manifest_path = broken / "manifest.yaml"
    appended_module = (
        "  broken-module:\n"
        "    pieces:\n"
        "      - .claude/skills/does-not-exist/SKILL.md\n"
        "    depends_on: []\n"
    )
    manifest_path.write_text(manifest_path.read_text() + appended_module)

    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief(modules={"sample-module": False, "broken-module": True}))
    courses_dir = tmp_path / "courses"

    with pytest.raises(inst.TemplateError):
        inst.instantiate(spec=FIXTURE_SPEC, template=broken, brief=brief_path, courses_dir=courses_dir)
    assert not courses_dir.exists() or list(courses_dir.iterdir()) == []


# --------------------------------------------------------------------------------------------
# Course-name collisions are suffixed, never overwritten (spec Assumptions)
# --------------------------------------------------------------------------------------------

def test_course_name_collision_is_suffixed_not_overwritten(tmp_path):
    courses_dir = tmp_path / "courses"
    courses_dir.mkdir()
    (courses_dir / "intro-to-widget-systems").mkdir()
    (courses_dir / "intro-to-widget-systems" / "sentinel.txt").write_text("do not touch")

    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief())

    course_dir = inst.instantiate(spec=FIXTURE_SPEC, template=FIXTURE_TEMPLATE, brief=brief_path, courses_dir=courses_dir)

    assert course_dir.name == "intro-to-widget-systems-2"
    # The pre-existing folder is untouched:
    assert (courses_dir / "intro-to-widget-systems" / "sentinel.txt").read_text() == "do not touch"


# --------------------------------------------------------------------------------------------
# Manifest parsing itself
# --------------------------------------------------------------------------------------------

def test_parse_manifest_matches_the_fixture_shape():
    manifest = inst.parse_manifest((FIXTURE_TEMPLATE / "manifest.yaml").read_text())
    assert manifest["version"] == "1.0.0"
    assert manifest["core"] == [".claude/skills/core-skill/SKILL.md"]
    assert manifest["profiles"]["default"]["default"] is True
    assert manifest["profiles"]["default"]["pieces"] == ["profiles/default/spine.md"]
    assert manifest["modules"]["sample-module"]["depends_on"] == []


# --------------------------------------------------------------------------------------------
# CLI (argparse wiring itself — not just instantiate())
# --------------------------------------------------------------------------------------------

def test_cli_instantiates_and_prints_the_course_dir(tmp_path, capsys):
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text(well_formed_brief())
    courses_dir = tmp_path / "courses"

    exit_code = inst.main([
        "--spec", str(FIXTURE_SPEC),
        "--template", str(FIXTURE_TEMPLATE),
        "--brief", str(brief_path),
        "--courses-dir", str(courses_dir),
    ])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "instantiated:" in out
    assert (courses_dir / "intro-to-widget-systems").is_dir()


def test_cli_reports_a_halt_on_stderr_and_returns_nonzero(tmp_path, capsys):
    brief_path = tmp_path / "COURSE_BRIEF.md"
    brief_path.write_text("# Course Brief\n\n```json\n{not valid\n```\n")

    exit_code = inst.main([
        "--template", str(FIXTURE_TEMPLATE),
        "--brief", str(brief_path),
        "--courses-dir", str(tmp_path / "courses"),
    ])
    assert exit_code == 1
    assert "halted" in capsys.readouterr().err
