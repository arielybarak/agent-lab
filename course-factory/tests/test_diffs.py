"""Tests for course-factory/tools/diffs.py — the append-only DIFFS.md forward-diff ledger
(FR-023/027, SC-010)."""

from __future__ import annotations

import diffs


def test_append_diff_creates_file_with_header(tmp_path):
    path = tmp_path / "DIFFS.md"
    diffs.append_diff(
        path, target="syllabus", what_changed="added a unit on X", why="gap found in skeletons",
        applied_at_phase="skeletons", now="2026-07-11T10:00:00Z",
    )
    text = path.read_text()
    assert text.startswith("# Forward-Diff Ledger")
    assert "## [2026-07-11T10:00:00Z] syllabus" in text
    assert "- **What changed:** added a unit on X" in text
    assert "- **Why:** gap found in skeletons" in text
    assert "- **Applied at phase:** skeletons" in text


def test_append_diff_is_append_only_never_touches_prior_entries(tmp_path):
    path = tmp_path / "DIFFS.md"
    diffs.append_diff(path, target="syllabus", what_changed="first change", why="reason one",
                       applied_at_phase="skeletons", now="2026-07-11T10:00:00Z")
    before = path.read_text()

    diffs.append_diff(path, target="skeletons", what_changed="second change", why="reason two",
                       applied_at_phase="lessons", now="2026-07-11T11:00:00Z")
    after = path.read_text()

    assert after.startswith(before)  # the first entry is untouched, the second is appended after
    assert after.count("## [") == 2


def test_read_diffs_returns_entries_in_applied_order(tmp_path):
    path = tmp_path / "DIFFS.md"
    diffs.append_diff(path, target="syllabus", what_changed="a", why="ra",
                       applied_at_phase="skeletons", now="2026-07-11T10:00:00Z")
    diffs.append_diff(path, target="skeletons", what_changed="b", why="rb",
                       applied_at_phase="lessons", now="2026-07-11T11:00:00Z")

    entries = diffs.read_diffs(path)
    assert [e["target"] for e in entries] == ["syllabus", "skeletons"]
    assert [e["timestamp"] for e in entries] == ["2026-07-11T10:00:00Z", "2026-07-11T11:00:00Z"]
    assert entries[0]["what_changed"] == "a"
    assert entries[1]["applied_at_phase"] == "lessons"


def test_read_diffs_on_nonexistent_file_returns_empty_list(tmp_path):
    assert diffs.read_diffs(tmp_path / "DIFFS.md") == []


def test_applied_at_phase_is_recorded_and_never_reopens_the_target_phase(tmp_path):
    """A forward diff targets an earlier gated phase but is applied at the current one —
    current_phase itself never moves backward (SC-010); this ledger is the audit trail for that."""
    path = tmp_path / "DIFFS.md"
    diffs.append_diff(path, target="syllabus", what_changed="revised unit ordering",
                       why="lesson-phase drafting revealed a gap", applied_at_phase="lessons",
                       now="2026-07-11T12:00:00Z")
    entry = diffs.read_diffs(path)[0]
    assert entry["target"] == "syllabus"
    assert entry["applied_at_phase"] == "lessons"


def test_cli_appends_an_entry(tmp_path, capsys):
    path = tmp_path / "DIFFS.md"
    exit_code = diffs.main([
        str(path), "--target", "syllabus", "--what-changed", "added a unit",
        "--why", "gap found later", "--applied-at-phase", "lessons",
    ])
    assert exit_code == 0
    assert "appended forward diff" in capsys.readouterr().out
    assert len(diffs.read_diffs(path)) == 1
