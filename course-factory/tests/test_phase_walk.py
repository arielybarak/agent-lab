"""US2 end-to-end: drive the phase walk with scripted stub gate results, no agent in the loop
(research R1). Feeds pass / loop→loop→pass / cap-hit needs-user / failed directly into
progress.transition(), and asserts the full delivery artifact set at `done` (SC-007/008).
"""

from __future__ import annotations

import shutil

import pytest

import deliver_check
import progress


def fresh_state():
    return progress.init_state("intro-to-x", "1.0.0")


def write_stub_artifacts(course_dir, state):
    """What 001's stub phase handlers would have written by the time the walk reaches `done`.
    Sources the required-file list from deliver_check.REQUIRED_FILES itself (not a second,
    hand-copied list here) so this fixture can never silently drift from what the tool enforces."""
    course_dir.mkdir(parents=True, exist_ok=True)
    claude_dir = course_dir / ".claude"
    claude_dir.mkdir(exist_ok=True)
    (claude_dir / "commands").mkdir(exist_ok=True)
    (claude_dir / "commands" / "course-report.md").write_text("# /course-report (stub)\n", encoding="utf-8")
    for name in deliver_check.REQUIRED_FILES:
        if name == "BUILD_PROGRESS.md":
            continue  # written separately below, via progress.write_state
        (course_dir / name).write_text(f"# {name} (stub)\n", encoding="utf-8")
    lessons_dir = course_dir / "lessons"
    lessons_dir.mkdir(exist_ok=True)
    for lesson in state["lessons"]:
        (lessons_dir / f"{lesson['id']}.md").write_text(f"# {lesson['id']} (stub)\n", encoding="utf-8")
    progress.write_state(course_dir / "BUILD_PROGRESS.md", state)


def test_ordered_walk_reaches_done_with_matched_gate_types():
    state = fresh_state()
    visited = []
    while state["current_phase"] != "done":
        phase = state["current_phase"]
        assert state["phases"][progress.PHASES.index(phase)]["gate_type"] == progress.GATE_TYPES[phase]
        visited.append(phase)
        state = progress.transition(state, "pass")
    assert visited == progress.PHASES  # strict order, no skip (SC-006/007)
    assert all(p["gate_status"] == "cleared" for p in state["phases"])


def test_walk_never_advances_without_a_recorded_gate_pass():
    state = fresh_state()
    state = progress.transition(state, "needs-user")  # parked, not cleared
    assert state["current_phase"] == "syllabus"
    assert state["phases"][0]["gate_status"] != "cleared"


def test_loop_then_loop_then_pass_during_skeletons():
    state = fresh_state()
    state = progress.transition(state, "pass")  # syllabus -> skeletons
    assert state["current_phase"] == "skeletons"

    state = progress.transition(state, "loop")
    state = progress.transition(state, "loop")
    assert state["active_loop"] == {"phase": "skeletons", "round": 2}
    assert state["current_phase"] == "skeletons"  # still working the batch

    state = progress.transition(state, "pass")
    assert state["current_phase"] == "lessons"
    assert state["phases"][1]["gate_status"] == "cleared"
    assert state["active_loop"] is None


def test_cap_hit_parks_for_accept_or_comment_then_accept_settles_the_cycle():
    state = fresh_state()
    state = progress.transition(state, "pass")  # -> skeletons
    for _ in range(progress.ROUND_CAP):
        state = progress.transition(state, "loop")
    assert state["active_loop"]["round"] == progress.ROUND_CAP  # capped, parked
    assert state["current_phase"] == "skeletons"  # not advanced without the decision

    state = progress.accept_round_cap(state)
    assert state["active_loop"] is None
    # Settling the agent-review round cap is not the same as clearing the phase — skeletons still
    # needs the blocking user scan (FR-024) before /course-build calls transition(..., "pass").
    assert state["current_phase"] == "skeletons"
    assert state["phases"][1]["gate_status"] != "cleared"

    # Only the orchestrator's own explicit pass (after the blocking scan approves) clears it:
    state = progress.transition(state, "pass")
    assert state["current_phase"] == "lessons"
    assert state["phases"][1]["gate_status"] == "cleared"


def test_lessons_phase_runs_each_lesson_through_its_own_round_cap_cycle():
    """The lessons phase clears only once every lesson is terminal — a single lesson's refine
    cycle (loop/cap/settle) never advances current_phase on its own (FR-012/015)."""
    state = fresh_state()
    state = progress.transition(state, "pass")  # syllabus -> skeletons
    state = progress.transition(state, "pass")  # skeletons -> lessons
    assert state["current_phase"] == "lessons"

    # Lesson L01: rubric passes early, under the cap.
    state = progress.transition(state, "loop")
    state = progress.clear_active_loop(state)
    state = progress.set_lesson_status(state, "L01", "passed")
    assert state["current_phase"] == "lessons"  # still working the phase

    # Lesson L02: hits the round cap, author accepts as-is.
    for _ in range(progress.ROUND_CAP):
        state = progress.transition(state, "loop")
    state = progress.accept_round_cap(state)
    state = progress.set_lesson_status(state, "L02", "accepted-at-cap")
    assert state["active_loop"] is None
    assert state["current_phase"] == "lessons"  # L01/L02 done, but the phase isn't yet

    # Only once every lesson is terminal does the driver clear the phase itself:
    state = progress.transition(state, "pass")
    assert state["current_phase"] == "deliver"
    assert state["phases"][2]["gate_status"] == "cleared"


def test_failed_halts_the_walk_and_never_advances():
    state = fresh_state()
    state = progress.transition(state, "pass")  # -> skeletons
    with pytest.raises(progress.PhaseFailedError):
        progress.transition(state, "failed")
    # Nothing in the caller's `state` variable changed — the exception is raised before mutation
    # is returned, and `transition` never writes state itself (the driver decides what to persist).
    assert state["current_phase"] == "skeletons"
    assert state["phases"][1]["gate_status"] == "in-progress"


def test_full_delivery_artifact_set_present_at_done(tmp_path):
    state = fresh_state()
    state = progress.transition(state, "pass")  # syllabus
    state = progress.transition(state, "pass")  # skeletons
    for lid in ("L01", "L02", "L03"):
        state = progress.set_lesson_status(state, lid, "passed")
    state = progress.transition(state, "pass")  # lessons -> deliver
    state = progress.transition(state, "pass")  # deliver -> done
    assert state["current_phase"] == "done"

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)

    missing = deliver_check.missing_artifacts(course_dir, state)
    assert missing == []
    assert deliver_check.check_delivery(course_dir, state) is True


def test_delivery_check_fails_when_an_artifact_is_missing(tmp_path):
    state = fresh_state()
    for _ in progress.PHASES:
        state = progress.transition(state, "pass")
    state = progress.set_lesson_status(state, "L01", "passed")

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)
    (course_dir / "COURSE_REPORT.md").unlink()

    assert deliver_check.check_delivery(course_dir, state) is False
    assert "COURSE_REPORT.md" in deliver_check.missing_artifacts(course_dir, state)


def test_delivery_check_fails_when_a_lesson_file_is_missing(tmp_path):
    state = fresh_state()
    for _ in progress.PHASES:
        state = progress.transition(state, "pass")
    state = progress.set_lesson_status(state, "L01", "passed")

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)
    (course_dir / "lessons" / "L01.md").unlink()

    missing = deliver_check.missing_artifacts(course_dir, state)
    assert any("L01" in item for item in missing)


def test_delivery_gate_clears_on_report_presence_regardless_of_verdict(tmp_path):
    """FR-011/021: COURSE_REPORT.md's presence clears delivery, any verdict."""
    state = fresh_state()
    for _ in progress.PHASES:
        state = progress.transition(state, "pass")
    state = progress.set_lesson_status(state, "L01", "passed")

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)
    (course_dir / "COURSE_REPORT.md").write_text("# Course Report\n\nVerdict: needs-work\n")

    assert deliver_check.check_delivery(course_dir, state) is True


def test_walk_reaches_delivery_with_lessons_seeded_from_the_syllabus(tmp_path):
    """T037 regression: the live spine populates lessons[] by SEEDING it from the frozen syllabus
    (progress.seed_lessons), not by a test hand-listing ids. Before this path existed, lessons[]
    stayed empty through the whole walk and deliver_check reported "no lessons recorded" — SC-008
    could never clear in a real run. Here nothing hand-writes the id list: it flows from the
    syllabus artifact, exactly as /course-build does after the syllabus gate clears."""
    syllabus_text = (
        "# Syllabus (stub)\n\n_Replaced by spec 002._\n\n"
        '```json\n'
        '{"lessons": [{"id": "L01", "title": "one"}, '
        '{"id": "L02", "title": "two"}, {"id": "L03", "title": "three"}]}\n'
        '```\n'
    )

    state = fresh_state()
    # Syllabus approved -> the driver seeds lessons[] from the now-frozen SYLLABUS.md, then advances.
    lesson_ids = progress.parse_syllabus_lessons(syllabus_text)
    state = progress.seed_lessons(state, lesson_ids)
    state = progress.transition(state, "pass")  # syllabus -> skeletons
    state = progress.transition(state, "pass")  # skeletons -> lessons
    assert state["current_phase"] == "lessons"
    # The set the lessons phase iterates came from the syllabus, not from the test.
    assert [lesson["id"] for lesson in state["lessons"]] == ["L01", "L02", "L03"]
    assert all(lesson["status"] == "not-started" for lesson in state["lessons"])

    # Work exactly the seeded, not-yet-terminal lessons — never a hand-authored id list.
    for lesson in list(state["lessons"]):
        state = progress.set_lesson_status(state, lesson["id"], "passed")
    state = progress.transition(state, "pass")  # lessons -> deliver
    state = progress.transition(state, "pass")  # deliver -> done
    assert state["current_phase"] == "done"

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)
    assert deliver_check.missing_artifacts(course_dir, state) == []
    assert deliver_check.check_delivery(course_dir, state) is True


def test_delivery_check_fails_when_claude_dir_is_empty(tmp_path):
    """An empty .claude/ (vs. missing) must also fail — a degenerate directory isn't the frozen
    template residue FR-020 requires."""
    state = fresh_state()
    for _ in progress.PHASES:
        state = progress.transition(state, "pass")
    state = progress.set_lesson_status(state, "L01", "passed")

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)
    shutil.rmtree(course_dir / ".claude")
    (course_dir / ".claude").mkdir()  # exists, but empty

    missing = deliver_check.missing_artifacts(course_dir, state)
    assert any(".claude" in item for item in missing)
    assert deliver_check.check_delivery(course_dir, state) is False


def test_deliver_check_cli_reports_missing_artifacts(tmp_path, capsys):
    state = fresh_state()
    for _ in progress.PHASES:
        state = progress.transition(state, "pass")
    state = progress.set_lesson_status(state, "L01", "passed")

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)
    (course_dir / "COURSE_REPORT.md").unlink()

    exit_code = deliver_check.main([str(course_dir)])
    assert exit_code == 1
    assert "MISSING" in capsys.readouterr().out


def test_deliver_check_cli_passes_on_a_complete_course(tmp_path, capsys):
    state = fresh_state()
    for _ in progress.PHASES:
        state = progress.transition(state, "pass")
    state = progress.set_lesson_status(state, "L01", "passed")

    course_dir = tmp_path / "intro-to-x"
    write_stub_artifacts(course_dir, state)

    assert deliver_check.main([str(course_dir)]) == 0
    assert "PASS" in capsys.readouterr().out
