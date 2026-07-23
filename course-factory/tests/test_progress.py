"""Tests for course-factory/tools/progress.py — the BUILD_PROGRESS.md state core.

Covers US2 (transitions, SC-006/007/010) and US3 (resume, lock, integrity — SC-004/005/009/012).
No agent in the loop (research R1): every scripted gate result is fed directly into the pure
transition function.
"""

from __future__ import annotations

import pytest

import progress


def fresh_state():
    return progress.init_state("intro-to-x", "1.0.0")


# --------------------------------------------------------------------------------------------
# State core: init / validate / read / write (T005)
# --------------------------------------------------------------------------------------------

def test_init_state_starts_at_syllabus():
    state = fresh_state()
    assert state["current_phase"] == "syllabus"
    assert state["phases"][0]["gate_status"] == "in-progress"
    assert all(p["gate_status"] == "pending" for p in state["phases"][1:])
    assert state["lock"] is None
    assert state["active_loop"] is None


def test_write_then_read_state_roundtrips(tmp_path):
    path = tmp_path / "BUILD_PROGRESS.md"
    state = fresh_state()
    progress.write_state(path, state)
    assert path.is_file()
    reread = progress.read_state(path)
    assert reread == state


def test_write_state_contains_exactly_one_json_block(tmp_path):
    path = tmp_path / "BUILD_PROGRESS.md"
    progress.write_state(path, fresh_state())
    text = path.read_text()
    assert text.count("```json") == 1


def test_read_state_missing_file_halts(tmp_path):
    with pytest.raises(progress.IntegrityError):
        progress.read_state(tmp_path / "BUILD_PROGRESS.md")


def test_read_state_corrupt_json_halts(tmp_path):
    path = tmp_path / "BUILD_PROGRESS.md"
    path.write_text("# broken\n\n```json\n{not valid json\n```\n")
    with pytest.raises(progress.IntegrityError):
        progress.read_state(path)


def test_read_state_no_json_block_halts(tmp_path):
    path = tmp_path / "BUILD_PROGRESS.md"
    path.write_text("# no state block here\n")
    with pytest.raises(progress.IntegrityError):
        progress.read_state(path)


def test_read_state_two_json_blocks_halts(tmp_path):
    path = tmp_path / "BUILD_PROGRESS.md"
    block = '```json\n{"a": 1}\n```\n'
    path.write_text(block + block)
    with pytest.raises(progress.IntegrityError):
        progress.read_state(path)


@pytest.mark.parametrize("corrupt", [
    lambda s: s.pop("lock") or s,                                    # missing required key
    lambda s: {**s, "current_phase": "not-a-phase"},                 # unknown phase
    lambda s: {**s, "phases": s["phases"][:-1]},                     # short phase list
])
def test_validate_state_rejects_malformed_shapes(corrupt):
    state = corrupt(fresh_state())
    with pytest.raises(progress.IntegrityError):
        progress.validate_state(state)


def test_validate_state_rejects_a_reopened_passed_phase():
    state = fresh_state()
    state = progress.transition(state, "pass")  # syllabus cleared, now at skeletons
    # Illegally mark a later phase "cleared" without going through it -> internally inconsistent.
    state["phases"][2]["gate_status"] = "cleared"
    with pytest.raises(progress.IntegrityError):
        progress.validate_state(state)


def test_validate_state_rejects_current_phase_without_prior_gate_pass():
    state = fresh_state()
    state["current_phase"] = "skeletons"  # jumped ahead without clearing syllabus
    with pytest.raises(progress.IntegrityError):
        progress.validate_state(state)


# --------------------------------------------------------------------------------------------
# Transition: forward-only, no skip, matched gate types (T014, SC-006/007/010)
# --------------------------------------------------------------------------------------------

def test_pass_clears_the_gate_and_advances():
    state = fresh_state()
    next_state = progress.transition(state, "pass")
    assert next_state["phases"][0]["gate_status"] == "cleared"
    assert next_state["phases"][0]["cleared_at"] is not None
    assert next_state["current_phase"] == "skeletons"
    assert next_state["phases"][1]["gate_status"] == "in-progress"


def test_pass_records_cleared_at_timestamp():
    state = progress.transition(fresh_state(), "pass", now="2026-07-11T10:00:00Z")
    assert state["phases"][0]["cleared_at"] == "2026-07-11T10:00:00Z"


def test_full_walk_advances_in_strict_order_to_done():
    state = fresh_state()
    order = []
    while state["current_phase"] != "done":
        order.append(state["current_phase"])
        state = progress.transition(state, "pass")
    assert order == progress.PHASES
    assert all(p["gate_status"] == "cleared" for p in state["phases"])


def test_every_phase_carries_its_matched_gate_type():
    state = fresh_state()
    for phase in state["phases"]:
        assert phase["gate_type"] == progress.GATE_TYPES[phase["name"]]


def test_transition_never_reopens_a_passed_phase():
    state = fresh_state()
    state = progress.transition(state, "pass")  # syllabus cleared
    syllabus_before = dict(state["phases"][0])
    state = progress.transition(state, "pass")  # skeletons cleared
    assert state["phases"][0] == syllabus_before  # untouched — no re-open (SC-010)


def test_transition_rejects_advance_past_done():
    state = fresh_state()
    for _ in progress.PHASES:
        state = progress.transition(state, "pass")
    assert state["current_phase"] == "done"
    with pytest.raises(progress.TransitionError):
        progress.transition(state, "pass")


def test_transition_rejects_unknown_gate_result():
    with pytest.raises(progress.TransitionError):
        progress.transition(fresh_state(), "sort-of-pass")


def test_needs_user_parks_with_no_field_changes():
    state = fresh_state()
    parked = progress.transition(state, "needs-user")
    assert parked == state  # nothing advanced; the orchestrator does the asking


def test_failed_raises_and_never_advances():
    state = fresh_state()
    with pytest.raises(progress.PhaseFailedError):
        progress.transition(state, "failed")


# --------------------------------------------------------------------------------------------
# Round-cap accounting (T018, FR-012) — loop -> loop -> pass, and the cap-hit accept-or-comment
# --------------------------------------------------------------------------------------------

def test_loop_increments_round_and_does_not_advance():
    state = fresh_state()
    state = progress.transition(state, "loop")
    assert state["active_loop"] == {"phase": "syllabus", "round": 1}
    assert state["current_phase"] == "syllabus"
    assert state["phases"][0]["gate_status"] == "in-progress"


def test_loop_then_loop_then_pass_clears_and_resets_active_loop():
    state = fresh_state()
    state = progress.transition(state, "loop")
    state = progress.transition(state, "loop")
    assert state["active_loop"]["round"] == 2
    state = progress.transition(state, "pass")
    assert state["active_loop"] is None
    assert state["current_phase"] == "skeletons"


def test_three_loops_hit_the_cap_then_a_fourth_loop_call_is_rejected():
    state = fresh_state()
    for _ in range(progress.ROUND_CAP):
        state = progress.transition(state, "loop")
    assert state["active_loop"]["round"] == progress.ROUND_CAP
    with pytest.raises(progress.TransitionError):
        progress.transition(state, "loop")  # must resolve via accept/extend first


def test_accept_round_cap_settles_the_refine_cycle_without_advancing_the_phase():
    state = fresh_state()
    for _ in range(progress.ROUND_CAP):
        state = progress.transition(state, "loop")
    state = progress.accept_round_cap(state)
    assert state["active_loop"] is None
    # Settling is not the same as the phase clearing — that's the caller's separate decision
    # (skeletons still needs the blocking scan, lessons still needs the other lessons; FR-012/024).
    assert state["phases"][0]["gate_status"] != "cleared"
    assert state["current_phase"] == "syllabus"


def test_accept_round_cap_without_a_pending_cap_raises():
    with pytest.raises(progress.TransitionError):
        progress.accept_round_cap(fresh_state())


def test_after_accept_round_cap_the_caller_can_still_explicitly_pass_the_phase():
    state = fresh_state()
    for _ in range(progress.ROUND_CAP):
        state = progress.transition(state, "loop")
    state = progress.accept_round_cap(state)
    state = progress.transition(state, "pass")  # the caller's own explicit clear
    assert state["phases"][0]["gate_status"] == "cleared"
    assert state["current_phase"] == "skeletons"


def test_extend_round_cap_grants_exactly_one_more_pass_then_settles_regardless_of_outcome():
    state = fresh_state()
    for _ in range(progress.ROUND_CAP):
        state = progress.transition(state, "loop")
    state = progress.extend_round_cap(state)
    assert state["active_loop"]["round"] == progress.ROUND_CAP + 1
    # The single extension's own outcome settles regardless (FR-012) — even another "loop" — but
    # still does not itself advance the phase.
    state = progress.transition(state, "loop")
    assert state["active_loop"] is None
    assert state["phases"][0]["gate_status"] != "cleared"
    assert state["current_phase"] == "syllabus"


def test_extend_round_cap_without_a_pending_cap_raises():
    with pytest.raises(progress.TransitionError):
        progress.extend_round_cap(fresh_state())


def test_clear_active_loop_settles_an_early_pass_without_advancing_the_phase():
    state = fresh_state()
    state = progress.transition(state, "loop")  # round 1, under the cap
    state = progress.clear_active_loop(state)
    assert state["active_loop"] is None
    assert state["current_phase"] == "syllabus"
    assert state["phases"][0]["gate_status"] != "cleared"


def test_clear_active_loop_is_a_noop_when_nothing_is_active():
    state = progress.clear_active_loop(fresh_state())
    assert state["active_loop"] is None


def test_loop_for_the_wrong_phase_is_rejected():
    state = fresh_state()
    state["active_loop"] = {"phase": "skeletons", "round": 1}
    with pytest.raises(progress.TransitionError):
        progress.transition(state, "loop")


def _capped_state_with_mismatched_loop_phase():
    """A state where active_loop is capped but (illegally) tagged for a different phase than
    current_phase — validate_state() would reject this on read, but the round-cap resolution
    helpers must not trust a hand-built dict either; they carry their own guard."""
    state = fresh_state()
    for _ in range(progress.ROUND_CAP):
        state = progress.transition(state, "loop")
    state["active_loop"]["phase"] = "skeletons"  # mismatched on purpose, bypassing transition()
    return state


def test_accept_round_cap_rejects_a_mismatched_loop_phase():
    with pytest.raises(progress.TransitionError):
        progress.accept_round_cap(_capped_state_with_mismatched_loop_phase())


def test_extend_round_cap_rejects_a_mismatched_loop_phase():
    with pytest.raises(progress.TransitionError):
        progress.extend_round_cap(_capped_state_with_mismatched_loop_phase())


def test_clear_active_loop_rejects_a_mismatched_loop_phase():
    state = fresh_state()
    state = progress.transition(state, "loop")
    state["active_loop"]["phase"] = "skeletons"
    with pytest.raises(progress.TransitionError):
        progress.clear_active_loop(state)


# --------------------------------------------------------------------------------------------
# Lesson status bookkeeping (used by resume + eventually 003)
# --------------------------------------------------------------------------------------------

def test_set_lesson_status_inserts_then_updates():
    state = fresh_state()
    state = progress.set_lesson_status(state, "L01", "in-progress")
    assert state["lessons"] == [{"id": "L01", "status": "in-progress"}]
    state = progress.set_lesson_status(state, "L01", "passed")
    assert state["lessons"] == [{"id": "L01", "status": "passed"}]


def test_set_lesson_status_rejects_unknown_status():
    with pytest.raises(progress.TransitionError):
        progress.set_lesson_status(fresh_state(), "L01", "kinda-done")


# --------------------------------------------------------------------------------------------
# Resume (T028, SC-004/005)
# --------------------------------------------------------------------------------------------

def test_resume_reads_current_phase_and_unfinished_lessons_from_disk_alone(tmp_path):
    state = fresh_state()
    state = progress.transition(state, "pass")  # syllabus cleared
    state = progress.transition(state, "pass")  # skeletons cleared -> lessons
    for lid, status in [("L01", "passed"), ("L02", "passed"), ("L03", "passed"),
                         ("L04", "not-started"), ("L05", "not-started"), ("L06", "not-started")]:
        state = progress.set_lesson_status(state, lid, status)
    progress.write_state(tmp_path / "BUILD_PROGRESS.md", state)

    resumed = progress.resume(tmp_path)
    assert resumed["current_phase"] == "lessons"
    done = [l["id"] for l in resumed["lessons"] if l["status"] == "passed"]
    todo = [l["id"] for l in resumed["lessons"] if l["status"] == "not-started"]
    assert done == ["L01", "L02", "L03"]
    assert todo == ["L04", "L05", "L06"]


def test_resume_needs_only_the_course_folder(tmp_path):
    progress.write_state(tmp_path / "BUILD_PROGRESS.md", fresh_state())
    # No other input than the folder itself:
    resumed = progress.resume(tmp_path)
    assert resumed["course_name"] == "intro-to-x"


def test_resume_detects_template_version_drift(tmp_path):
    progress.write_state(tmp_path / "BUILD_PROGRESS.md", fresh_state())
    with pytest.raises(progress.IntegrityError):
        progress.resume(tmp_path, expected_template_version="2.0.0")


def test_resume_missing_state_halts(tmp_path):
    with pytest.raises(progress.IntegrityError):
        progress.resume(tmp_path)


def test_resume_corrupt_state_halts(tmp_path):
    (tmp_path / "BUILD_PROGRESS.md").write_text("garbage, no json block")
    with pytest.raises(progress.IntegrityError):
        progress.resume(tmp_path)


# --------------------------------------------------------------------------------------------
# Lock (T029, FR-028, SC-012)
# --------------------------------------------------------------------------------------------

def test_acquire_lock_sets_holder_and_timestamps():
    state = progress.acquire_lock(fresh_state(), "cb-aaa", now="2026-07-11T10:00:00Z")
    assert state["lock"] == {
        "holder": "cb-aaa",
        "acquired_at": "2026-07-11T10:00:00Z",
        "last_progress_at": "2026-07-11T10:00:00Z",
    }


def test_second_holder_is_refused_while_the_first_is_live():
    state = progress.acquire_lock(fresh_state(), "cb-aaa", now="2026-07-11T10:00:00Z")
    with pytest.raises(progress.LockError):
        progress.acquire_lock(state, "cb-bbb", now="2026-07-11T10:01:00Z")  # 60s later, still live


def test_same_holder_may_reacquire():
    state = progress.acquire_lock(fresh_state(), "cb-aaa", now="2026-07-11T10:00:00Z")
    state = progress.acquire_lock(state, "cb-aaa", now="2026-07-11T10:01:00Z")
    assert state["lock"]["holder"] == "cb-aaa"


def test_stale_lock_is_reclaimable_by_a_new_holder():
    state = progress.acquire_lock(fresh_state(), "cb-aaa", now="2026-07-11T10:00:00Z")
    # 31 minutes later — past the default 30-minute stale window (LOCK_STALE_SECONDS).
    state = progress.acquire_lock(state, "cb-bbb", now="2026-07-11T10:31:00Z")
    assert state["lock"]["holder"] == "cb-bbb"


def test_a_lock_not_yet_stale_is_refused_even_past_the_liveness_window():
    state = progress.acquire_lock(fresh_state(), "cb-aaa", now="2026-07-11T10:00:00Z")
    # 6 minutes later — past LOCK_LIVENESS_SECONDS (5 min) but well under the stale window (30 min).
    with pytest.raises(progress.LockError):
        progress.acquire_lock(state, "cb-bbb", now="2026-07-11T10:06:00Z")


def test_refresh_lock_updates_last_progress_at():
    state = progress.acquire_lock(fresh_state(), "cb-aaa", now="2026-07-11T10:00:00Z")
    state = progress.refresh_lock(state, "cb-aaa", now="2026-07-11T10:05:00Z")
    assert state["lock"]["last_progress_at"] == "2026-07-11T10:05:00Z"
    assert state["lock"]["acquired_at"] == "2026-07-11T10:00:00Z"


def test_refresh_lock_by_a_non_holder_raises():
    state = progress.acquire_lock(fresh_state(), "cb-aaa")
    with pytest.raises(progress.LockError):
        progress.refresh_lock(state, "cb-bbb")


def test_release_lock_clears_it():
    state = progress.acquire_lock(fresh_state(), "cb-aaa")
    state = progress.release_lock(state)
    assert state["lock"] is None


def test_acquire_lock_after_release_never_conflicts():
    state = progress.acquire_lock(fresh_state(), "cb-aaa")
    state = progress.release_lock(state)
    state = progress.acquire_lock(state, "cb-bbb")  # a fresh invocation, immediately
    assert state["lock"]["holder"] == "cb-bbb"


# --------------------------------------------------------------------------------------------
# Lesson-set seeding (T037) — the skeleton handler publishes the planned set before working it
# --------------------------------------------------------------------------------------------

SYLLABUS_STUB = """# Syllabus (stub)

_Replaced by spec 002._

```json
{"lessons": [{"id": "L01", "title": "one"}, {"id": "L02", "title": "two"}]}
```
"""


def test_parse_syllabus_lessons_reads_the_ordered_id_list():
    assert progress.parse_syllabus_lessons(SYLLABUS_STUB) == ["L01", "L02"]


def test_parse_syllabus_lessons_halts_on_a_syllabus_with_no_lesson_set():
    with pytest.raises(progress.IntegrityError):
        progress.parse_syllabus_lessons("# Syllabus\n\nno machine block here\n")


def test_seed_lessons_adds_every_planned_lesson_as_not_started():
    state = progress.seed_lessons(fresh_state(), ["L01", "L02", "L03"])
    assert state["lessons"] == [
        {"id": "L01", "status": "not-started"},
        {"id": "L02", "status": "not-started"},
        {"id": "L03", "status": "not-started"},
    ]


def test_seed_lessons_never_resets_an_already_worked_lesson():
    """Re-seeding on resume must not undo completed work (SC-004) — seeding is idempotent."""
    state = progress.seed_lessons(fresh_state(), ["L01", "L02"])
    state = progress.set_lesson_status(state, "L01", "passed")
    state = progress.seed_lessons(state, ["L01", "L02", "L03"])
    by_id = {lesson["id"]: lesson["status"] for lesson in state["lessons"]}
    assert by_id == {"L01": "passed", "L02": "not-started", "L03": "not-started"}


# --------------------------------------------------------------------------------------------
# syllabus_subphase — 002's owned field, written and validated through this module (T039)
# --------------------------------------------------------------------------------------------

def test_set_syllabus_subphase_records_002s_checkpoint():
    state = progress.set_syllabus_subphase(fresh_state(), "research-done")
    assert state["syllabus_subphase"] == "research-done"


def test_set_syllabus_subphase_rejects_an_unknown_value():
    with pytest.raises(progress.TransitionError):
        progress.set_syllabus_subphase(fresh_state(), "half-done")


def test_set_syllabus_subphase_rejects_a_write_outside_the_syllabus_phase():
    state = progress.transition(fresh_state(), "pass")  # -> skeletons
    with pytest.raises(progress.TransitionError):
        progress.set_syllabus_subphase(state, "composed")


def test_validate_state_rejects_a_subphase_set_outside_the_syllabus_phase():
    state = progress.set_syllabus_subphase(fresh_state(), "composed")
    state["current_phase"] = "skeletons"
    state["phases"][0]["gate_status"] = "cleared"
    state["phases"][0]["cleared_at"] = "2026-07-11T10:00:00Z"
    state["phases"][1]["gate_status"] = "in-progress"
    with pytest.raises(progress.IntegrityError):
        progress.validate_state(state)


def test_validate_state_rejects_an_unknown_subphase_value():
    state = fresh_state()
    state["syllabus_subphase"] = "nonsense"
    with pytest.raises(progress.IntegrityError):
        progress.validate_state(state)


def test_leaving_the_syllabus_phase_clears_the_subphase():
    """Otherwise the very next write would fail validation (the field is null off-phase)."""
    state = progress.set_syllabus_subphase(fresh_state(), "presented")
    state = progress.transition(state, "pass")
    assert state["current_phase"] == "skeletons"
    assert state["syllabus_subphase"] is None


# --------------------------------------------------------------------------------------------
# CLI (argparse wiring itself — not just the underlying functions)
# --------------------------------------------------------------------------------------------

def test_cli_init_then_show_roundtrips(tmp_path):
    course_dir = tmp_path / "intro-to-x"
    course_dir.mkdir()
    assert progress.main(["init", str(course_dir), "intro-to-x", "1.0.0"]) == 0
    assert progress.main(["show", str(course_dir)]) == 0


def test_cli_transition_persists_to_disk(tmp_path, capsys):
    course_dir = tmp_path / "intro-to-x"
    course_dir.mkdir()
    progress.main(["init", str(course_dir), "intro-to-x", "1.0.0"])
    assert progress.main(["transition", str(course_dir), "pass"]) == 0
    state = progress.read_state(course_dir / "BUILD_PROGRESS.md")
    assert state["current_phase"] == "skeletons"


def test_cli_transition_on_missing_course_dir_fails_cleanly(tmp_path):
    assert progress.main(["transition", str(tmp_path / "no-such-course"), "pass"]) == 1


def test_cli_lock_acquire_then_refresh_then_release(tmp_path, capsys):
    course_dir = tmp_path / "intro-to-x"
    course_dir.mkdir()
    progress.main(["init", str(course_dir), "intro-to-x", "1.0.0"])

    assert progress.main(["lock-acquire", str(course_dir), "--holder", "cb-cli"]) == 0
    state = progress.read_state(course_dir / "BUILD_PROGRESS.md")
    assert state["lock"]["holder"] == "cb-cli"

    assert progress.main(["lock-refresh", str(course_dir), "--holder", "cb-cli"]) == 0
    assert progress.main(["lock-release", str(course_dir)]) == 0
    state = progress.read_state(course_dir / "BUILD_PROGRESS.md")
    assert state["lock"] is None


def test_cli_lock_refresh_by_a_non_holder_fails_cleanly(tmp_path):
    course_dir = tmp_path / "intro-to-x"
    course_dir.mkdir()
    progress.main(["init", str(course_dir), "intro-to-x", "1.0.0"])
    progress.main(["lock-acquire", str(course_dir), "--holder", "cb-aaa"])
    assert progress.main(["lock-refresh", str(course_dir), "--holder", "cb-bbb"]) == 1


def test_cli_seed_lessons_reads_a_real_syllabus_file(tmp_path):
    course_dir = tmp_path / "intro-to-x"
    course_dir.mkdir()
    progress.main(["init", str(course_dir), "intro-to-x", "1.0.0"])
    progress.main(["transition", str(course_dir), "pass"])  # -> skeletons (syllabus "frozen")

    syllabus_path = course_dir / "SYLLABUS.md"
    syllabus_path.write_text(
        '# Syllabus (stub)\n\n```json\n{"lessons": [{"id": "L01", "title": "one"}]}\n```\n'
    )
    assert progress.main(["seed-lessons", str(course_dir), str(syllabus_path)]) == 0
    state = progress.read_state(course_dir / "BUILD_PROGRESS.md")
    assert state["lessons"] == [{"id": "L01", "status": "not-started"}]


def test_cli_set_syllabus_subphase(tmp_path):
    course_dir = tmp_path / "intro-to-x"
    course_dir.mkdir()
    progress.main(["init", str(course_dir), "intro-to-x", "1.0.0"])
    assert progress.main(["set-syllabus-subphase", str(course_dir), "research-done"]) == 0
    state = progress.read_state(course_dir / "BUILD_PROGRESS.md")
    assert state["syllabus_subphase"] == "research-done"


def test_cli_resume_reports_template_version_drift(tmp_path):
    course_dir = tmp_path / "intro-to-x"
    course_dir.mkdir()
    progress.main(["init", str(course_dir), "intro-to-x", "1.0.0"])
    assert progress.main(["resume", str(course_dir), "--template-version", "9.9.9"]) == 1
