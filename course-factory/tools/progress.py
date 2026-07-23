#!/usr/bin/env python3
"""BUILD_PROGRESS.md state core — the pipeline's sole source of truth (001 FR-015/016/017/018).

Schema: specs/course-factory/001-pipeline-skeleton/contracts/build-progress-schema.md. This module
owns the fenced ```json block inside BUILD_PROGRESS.md; the surrounding Markdown prose is advisory
and regenerated from the block on every write (research R3) — never hand-edit the JSON, always go
through this module.

Three guarantees live here, each backed by a pure function so pytest can assert them with no agent
in the loop (research R1):
  - `transition()` — legal-move-only phase advancement (no skip, no re-open, matched gate types).
  - the lock functions — a live holder blocks entry; a stale one is reclaimable (FR-028).
  - `resume()` / `validate_state()` — integrity halts on missing/corrupt/inconsistent state or a
    template_version drift, rather than guessing (FR-022).

Stdlib only (repo convention) — the state block is JSON specifically because `json` is stdlib and
unambiguous (research R3); no third-party YAML/JSON-schema dependency.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

PHASES = ["syllabus", "skeletons", "lessons", "deliver"]
GATE_TYPES = {
    "syllabus": "user-approval",
    "skeletons": "agent-then-user",
    "lessons": "rubric",
    "deliver": "report-generated",
}
GATE_STATUSES = {"pending", "in-progress", "cleared"}
LESSON_STATUSES = {"not-started", "in-progress", "passed", "accepted-at-cap"}
GATE_RESULTS = {"pass", "needs-user", "loop", "failed"}

# 002's checkpointable sub-phases (002 FR-018) — already fixed by this contract
# (contracts/build-progress-schema.md's `syllabus_subphase` row), not 002's to invent later, so
# it's validated here like any other enum field.
SYLLABUS_SUBPHASES = {"research-in-progress", "research-done", "composed", "presented"}

# The automated skeleton/lesson refine loop is capped at 3 rounds (FR-012); on a 4th "loop" the
# orchestrator must park for the author's accept-or-comment decision instead of reinvoking.
ROUND_CAP = 3

# Lock windows (FR-028, data-model rule 8) — configurable constants, not per-course variability.
# A hold younger than LOCK_STALE_SECONDS is treated as live and refuses a second entrant; only past
# that generous timeout may a new invocation reclaim it. LOCK_LIVENESS_SECONDS documents the normal
# refresh cadence (a live session persists roughly every unit of progress) but is not itself a
# second enforcement gate at MVP — see tools/README.md for the reasoning.
LOCK_LIVENESS_SECONDS = 300
LOCK_STALE_SECONDS = 1800

_JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)
_REQUIRED_KEYS = {
    "schema_version", "course_name", "template_version", "current_phase", "phases",
    "syllabus_subphase", "lessons", "active_loop", "lock", "diffs_ref",
}


class IntegrityError(Exception):
    """BUILD_PROGRESS.md is missing, corrupt, or internally inconsistent (FR-022, SC-009)."""


class TransitionError(Exception):
    """An illegal state transition was attempted (no gate pass, phase skip, re-open, bad input)."""


class PhaseFailedError(TransitionError):
    """A phase handler reported 'failed' — halt and surface (FR-022); no advance."""


class LockError(Exception):
    """The build is held by another live session (FR-028, SC-012)."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def mint_holder_token() -> str:
    """A short per-invocation lock token (contracts/build-progress-schema.md § lock.holder) —
    a Claude Code session has no stable tool-visible id, so a fresh one is minted each run."""
    return f"cb-{uuid.uuid4().hex[:16]}"


# --------------------------------------------------------------------------------------------
# State construction & validation
# --------------------------------------------------------------------------------------------

def init_state(course_name: str, template_version: str) -> dict[str, Any]:
    """The initial state at instantiation: positioned at the start of the syllabus phase (FR-008)."""
    return {
        "schema_version": SCHEMA_VERSION,
        "course_name": course_name,
        "template_version": template_version,
        "current_phase": PHASES[0],
        "phases": [
            {
                "name": name,
                "gate_type": GATE_TYPES[name],
                "gate_status": "in-progress" if name == PHASES[0] else "pending",
                "cleared_at": None,
            }
            for name in PHASES
        ],
        "syllabus_subphase": None,
        "lessons": [],
        "active_loop": None,
        "lock": None,
        "diffs_ref": "DIFFS.md",
    }


def validate_state(state: Any) -> None:
    """Raise IntegrityError on any shape or consistency violation (FR-022). Never repairs silently."""
    if not isinstance(state, dict):
        raise IntegrityError("state block is not a JSON object")

    missing = _REQUIRED_KEYS - state.keys()
    if missing:
        raise IntegrityError(f"state missing required field(s): {sorted(missing)}")

    phase_enum = PHASES + ["done"]
    if state["current_phase"] not in phase_enum:
        raise IntegrityError(f"unknown current_phase: {state['current_phase']!r}")

    phases = state["phases"]
    if not isinstance(phases, list) or [p.get("name") for p in phases] != PHASES:
        raise IntegrityError(f"phases[] must list {PHASES} in order")

    for p in phases:
        if p.get("gate_type") != GATE_TYPES.get(p.get("name")):
            raise IntegrityError(
                f"phase {p.get('name')!r} has gate_type {p.get('gate_type')!r}, "
                f"expected {GATE_TYPES.get(p.get('name'))!r}"
            )
        if p.get("gate_status") not in GATE_STATUSES:
            raise IntegrityError(f"phase {p.get('name')!r} has invalid gate_status {p.get('gate_status')!r}")

    idx_current = phase_enum.index(state["current_phase"])
    for i, p in enumerate(phases):
        is_cleared = p["gate_status"] == "cleared"
        should_be_cleared = i < idx_current
        if should_be_cleared and not is_cleared:
            raise IntegrityError(
                f"current_phase is {state['current_phase']!r} but phase {p['name']!r} "
                "before it is not cleared"
            )
        if is_cleared and not should_be_cleared:
            raise IntegrityError(
                f"phase {p['name']!r} is cleared but is not before current_phase "
                f"{state['current_phase']!r} — a passed phase must never be re-opened (SC-010)"
            )

    subphase = state["syllabus_subphase"]
    if subphase is not None and subphase not in SYLLABUS_SUBPHASES:
        raise IntegrityError(f"unknown syllabus_subphase: {subphase!r}")
    if subphase is not None and state["current_phase"] != "syllabus":
        raise IntegrityError(
            f"syllabus_subphase is {subphase!r} but current_phase is {state['current_phase']!r} — "
            "it must be null once the syllabus phase is left"
        )

    for lesson in state["lessons"]:
        if "id" not in lesson or lesson.get("status") not in LESSON_STATUSES:
            raise IntegrityError(f"malformed lessons[] entry: {lesson!r}")

    loop = state["active_loop"]
    if loop is not None:
        if loop.get("phase") not in PHASES or not isinstance(loop.get("round"), int) or loop["round"] < 0:
            raise IntegrityError(f"malformed active_loop: {loop!r}")
        if loop["phase"] != state["current_phase"]:
            raise IntegrityError(
                f"active_loop is for phase {loop['phase']!r} but current_phase is "
                f"{state['current_phase']!r} — a refine loop must belong to the current phase"
            )

    lock = state["lock"]
    if lock is not None:
        if not {"holder", "acquired_at", "last_progress_at"} <= lock.keys():
            raise IntegrityError(f"malformed lock: {lock!r}")


# --------------------------------------------------------------------------------------------
# Read / write BUILD_PROGRESS.md
# --------------------------------------------------------------------------------------------

def render_markdown(state: dict[str, Any]) -> str:
    """Regenerate the human-facing prose from the state block (R3) — always derived, never hand-edited."""
    marker = {"cleared": "x", "in-progress": "~", "pending": " "}
    lines = [
        f"# Build Progress — {state['course_name']}",
        "",
        "_Auto-generated by `course-factory/tools/progress.py` — do not hand-edit the JSON block "
        "below; it is regenerated on every write._",
        "",
        f"**Current phase:** `{state['current_phase']}`",
        f"**Template version:** `{state['template_version']}`",
        "",
        "## Phases",
        "",
    ]
    for p in state["phases"]:
        cleared = f" (cleared {p['cleared_at']})" if p["cleared_at"] else ""
        lines.append(f"- [{marker[p['gate_status']]}] **{p['name']}** — {p['gate_type']}{cleared}")

    if state["lessons"]:
        lines += ["", "## Lessons", ""]
        for lesson in state["lessons"]:
            lines.append(f"- `{lesson['id']}`: {lesson['status']}")

    if state["active_loop"]:
        lines += ["", f"**Active refine loop:** {state['active_loop']['phase']} — "
                       f"round {state['active_loop']['round']}/{ROUND_CAP}"]

    if state["lock"]:
        lines += ["", f"**Locked by:** `{state['lock']['holder']}` "
                       f"(last progress {state['lock']['last_progress_at']})"]

    lines += ["", "```json", json.dumps(state, indent=2, sort_keys=False), "```", ""]
    return "\n".join(lines)


def read_state(path: Path) -> dict[str, Any]:
    """Parse the single fenced json block. Raises IntegrityError on anything but a clean read."""
    if not path.is_file():
        raise IntegrityError(f"BUILD_PROGRESS.md not found: {path}")

    text = path.read_text(encoding="utf-8")
    matches = _JSON_BLOCK_RE.findall(text)
    if len(matches) == 0:
        raise IntegrityError(f"no fenced ```json block found in {path}")
    if len(matches) > 1:
        raise IntegrityError(f"expected exactly one fenced ```json block in {path}, found {len(matches)}")

    try:
        state = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise IntegrityError(f"corrupt json block in {path}: {exc}") from exc

    validate_state(state)
    return state


def write_state(path: Path, state: dict[str, Any]) -> None:
    """Validate then persist — the only sanctioned way to update BUILD_PROGRESS.md (FR-016)."""
    validate_state(state)
    path.write_text(render_markdown(state), encoding="utf-8")


# --------------------------------------------------------------------------------------------
# Transition function — the legal-move-only state machine (FR-009/010, SC-006/007/010)
# --------------------------------------------------------------------------------------------

def transition(state: dict[str, Any], gate_result: str, *, now: str | None = None) -> dict[str, Any]:
    """(state, gate_result) -> next state. Operates only on `current_phase`'s own entry, so a
    phase skip is structurally impossible (SC-006) and a passed phase is never re-touched (SC-010).

    gate_result:
      - "pass"       clear the current phase's gate, advance current_phase (or reach "done"). The
                     caller decides when a phase is truly done — for `skeletons` that's after the
                     blocking user scan (FR-024), for `lessons` that's after every lesson reaches a
                     terminal status (FR-015) — never merely because one refine cycle settled.
      - "needs-user" park: no field changes — the orchestrator's job is to stop and ask (FR-011).
      - "loop"       one more capped refine round (FR-012); at the cap, further "loop" calls raise
                     until the caller resolves the park via accept_round_cap()/extend_round_cap().
                     Resolving a round-cap park only clears `active_loop` — it never advances
                     `current_phase` on its own (see accept_round_cap()).
      - "failed"     raise PhaseFailedError — halt and surface (FR-022); never advance.
    """
    if gate_result not in GATE_RESULTS:
        raise TransitionError(f"unknown gate result: {gate_result!r}")
    if state["current_phase"] == "done":
        raise TransitionError("cannot transition: the build is already done")

    state = copy.deepcopy(state)
    now = now or _now_iso()
    phase_name = state["current_phase"]
    idx = PHASES.index(phase_name)
    phase = state["phases"][idx]

    if gate_result == "failed":
        raise PhaseFailedError(f"phase {phase_name!r} reported 'failed' — halt and surface (FR-022)")

    if gate_result == "needs-user":
        return state

    if gate_result == "loop":
        loop = state["active_loop"] or {"phase": phase_name, "round": 0}
        if loop["phase"] != phase_name:
            raise TransitionError(
                f"active_loop is for phase {loop['phase']!r}, not the current phase {phase_name!r}"
            )
        if loop["round"] > ROUND_CAP:
            # The single accept-or-comment extension (extend_round_cap) was already granted —
            # whatever the handler returns now settles the refine cycle regardless of outcome
            # (FR-012). Settling clears active_loop only; it does not itself clear the phase (the
            # caller may still have a blocking scan or other lessons pending).
            state["active_loop"] = None
            return state
        elif loop["round"] == ROUND_CAP:
            raise TransitionError(
                f"phase {phase_name!r} is already parked at the round cap ({ROUND_CAP}) — resolve "
                "via accept_round_cap() or extend_round_cap() before transitioning again"
            )
        else:
            loop["round"] += 1
            state["active_loop"] = loop
            return state

    # gate_result == "pass"
    phase["gate_status"] = "cleared"
    phase["cleared_at"] = now
    state["active_loop"] = None
    if phase_name == "syllabus":
        state["syllabus_subphase"] = None  # 002's field is only meaningful while in-phase
    next_idx = idx + 1
    if next_idx < len(PHASES):
        state["current_phase"] = PHASES[next_idx]
        state["phases"][next_idx]["gate_status"] = "in-progress"
    else:
        state["current_phase"] = "done"
    return state


def accept_round_cap(state: dict[str, Any]) -> dict[str, Any]:
    """The author's 'accept as-is' decision at a round-cap park — settles the refine cycle
    (clears `active_loop`) but does **not** itself clear the phase (FR-012). Whether the phase may
    now clear is the caller's call: `skeletons` still needs the blocking user scan (FR-024) after
    its agent-review round-cap settles; `lessons` still needs every other lesson terminal. Once
    the caller's own condition is met, it calls `transition(state, "pass")` explicitly."""
    loop = state.get("active_loop")
    if not loop or loop["round"] != ROUND_CAP:
        raise TransitionError("no round-cap park is pending an accept-or-comment decision")
    if loop["phase"] != state["current_phase"]:
        raise TransitionError(
            f"active_loop is for phase {loop['phase']!r}, not the current phase "
            f"{state['current_phase']!r}"
        )
    state = copy.deepcopy(state)
    state["active_loop"] = None
    return state


def clear_active_loop(state: dict[str, Any]) -> dict[str, Any]:
    """Clear `active_loop` when a refine cycle concludes **early**, under the cap — e.g. a
    lesson's rubric passes on round 1 or 2, or the skeleton batch's agent-review passes before
    round 3. Unlike accept_round_cap(), this doesn't require the cap to have been reached; it's
    the ordinary "it passed, move on to the next unit" case. Never advances the phase — call
    transition(state, "pass") separately once the phase's own condition is actually met."""
    state = copy.deepcopy(state)
    loop = state["active_loop"]
    if loop is not None and loop["phase"] != state["current_phase"]:
        raise TransitionError(
            f"active_loop is for phase {loop['phase']!r}, not the current phase "
            f"{state['current_phase']!r}"
        )
    state["active_loop"] = None
    return state


def extend_round_cap(state: dict[str, Any]) -> dict[str, Any]:
    """The author's 'comment' decision at a round-cap park — grants exactly one more refine pass;
    its outcome settles the refine cycle regardless (FR-012's single extension, enforced by
    transition()'s `round > ROUND_CAP` branch) but likewise never clears the phase on its own."""
    loop = state.get("active_loop")
    if not loop or loop["round"] != ROUND_CAP:
        raise TransitionError("no round-cap park is pending an accept-or-comment decision")
    if loop["phase"] != state["current_phase"]:
        raise TransitionError(
            f"active_loop is for phase {loop['phase']!r}, not the current phase "
            f"{state['current_phase']!r}"
        )
    state = copy.deepcopy(state)
    state["active_loop"]["round"] = ROUND_CAP + 1
    return state


def set_lesson_status(
    state: dict[str, Any], lesson_id: str, status: str, *, now: str | None = None
) -> dict[str, Any]:
    """Upsert one lesson's status in lessons[] (003's write, FR-015) without touching current_phase
    — the lessons phase itself only clears once the driver calls transition(state, "pass") after
    every lesson reaches a terminal status."""
    if status not in LESSON_STATUSES:
        raise TransitionError(f"unknown lesson status: {status!r}")
    state = copy.deepcopy(state)
    for lesson in state["lessons"]:
        if lesson["id"] == lesson_id:
            lesson["status"] = status
            return state
    state["lessons"].append({"id": lesson_id, "status": status})
    return state


# --------------------------------------------------------------------------------------------
# Syllabus lesson-set seeding — the link between the frozen SYLLABUS.md and lessons[]
# --------------------------------------------------------------------------------------------

def parse_syllabus_lessons(syllabus_text: str) -> list[str]:
    """Read the ordered lesson-id list out of a frozen SYLLABUS.md — the same "prose + one fenced
    json block" convention as BUILD_PROGRESS.md/COURSE_BRIEF.md (research R3), here holding
    `{"lessons": [{"id": ..., "title": ...}, ...]}`. This is what lets the driver seed `lessons[]`
    (seed_lessons()) and the skeleton handler know how many skeletons to draft — one per planned
    lesson (003's skeleton-handler.md). Raises IntegrityError rather than guessing at a missing or
    malformed lesson set (FR-022)."""
    matches = _JSON_BLOCK_RE.findall(syllabus_text)
    if len(matches) != 1:
        raise IntegrityError(f"SYLLABUS.md must contain exactly one fenced json block, found {len(matches)}")
    try:
        data = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise IntegrityError(f"corrupt json block in SYLLABUS.md: {exc}") from exc
    lessons = data.get("lessons")
    if not isinstance(lessons, list) or not lessons:
        raise IntegrityError("SYLLABUS.md's json block has no non-empty 'lessons' list")
    return [lesson["id"] for lesson in lessons]


def seed_lessons(state: dict[str, Any], lesson_ids: list[str]) -> dict[str, Any]:
    """Idempotently ensure `lessons[]` carries an entry for every planned lesson, defaulting a
    new one to `not-started`. Never resets an already-present lesson's status — re-seeding on
    resume (e.g. after a forward diff adds a lesson) must not undo completed work (SC-004)."""
    state = copy.deepcopy(state)
    existing_ids = {lesson["id"] for lesson in state["lessons"]}
    for lesson_id in lesson_ids:
        if lesson_id not in existing_ids:
            state["lessons"].append({"id": lesson_id, "status": "not-started"})
    return state


# --------------------------------------------------------------------------------------------
# syllabus_subphase — 002's field, written and validated through this module
# --------------------------------------------------------------------------------------------

def set_syllabus_subphase(state: dict[str, Any], subphase: str) -> dict[str, Any]:
    """002's checkpoint write (its FR-018) — never hand-edited, always through here
    (build-progress-schema rule 1). Only valid while `current_phase == "syllabus"`; `transition()`
    clears this field back to null on leaving the phase, so it never lingers stale (see its `pass`
    branch)."""
    if subphase not in SYLLABUS_SUBPHASES:
        raise TransitionError(f"unknown syllabus_subphase: {subphase!r}")
    if state["current_phase"] != "syllabus":
        raise TransitionError(
            f"syllabus_subphase can only be written while current_phase == 'syllabus', "
            f"not {state['current_phase']!r}"
        )
    state = copy.deepcopy(state)
    state["syllabus_subphase"] = subphase
    return state


# --------------------------------------------------------------------------------------------
# Lock (FR-028, SC-012)
# --------------------------------------------------------------------------------------------

def acquire_lock(
    state: dict[str, Any],
    holder: str,
    *,
    now: str | None = None,
    stale_seconds: int = LOCK_STALE_SECONDS,
) -> dict[str, Any]:
    """Refuse entry if another holder's lock is not yet stale (SC-012); reclaim a stale one,
    recording the reclaim by simply overwriting it with the new holder (the reclaim IS the new
    lock row — no separate log needed, the prior holder is gone from the state either way)."""
    state = copy.deepcopy(state)
    now_dt = _parse_iso(now) if now else datetime.now(timezone.utc)
    lock = state["lock"]
    if lock and lock["holder"] != holder:
        age = (now_dt - _parse_iso(lock["last_progress_at"])).total_seconds()
        if age < stale_seconds:
            raise LockError(
                f"course is locked by {lock['holder']!r} ({age:.0f}s since last progress, "
                f"stale after {stale_seconds}s)"
            )
    now_str = now or _now_iso()
    state["lock"] = {"holder": holder, "acquired_at": now_str, "last_progress_at": now_str}
    return state


def refresh_lock(state: dict[str, Any], holder: str, *, now: str | None = None) -> dict[str, Any]:
    """Refresh last_progress_at on each persisted unit (FR-016) so the lock stays live."""
    state = copy.deepcopy(state)
    lock = state["lock"]
    if not lock or lock["holder"] != holder:
        raise LockError("cannot refresh: this invocation does not hold the lock")
    lock["last_progress_at"] = now or _now_iso()
    return state


def release_lock(state: dict[str, Any]) -> dict[str, Any]:
    """Clear the lock on park or clean exit (data-model rule 8)."""
    state = copy.deepcopy(state)
    state["lock"] = None
    return state


# --------------------------------------------------------------------------------------------
# Resume (FR-017/018, SC-004/005/009)
# --------------------------------------------------------------------------------------------

def resume(course_dir: Path, *, expected_template_version: str | None = None) -> dict[str, Any]:
    """Read BUILD_PROGRESS.md and return the state to continue from — the course folder alone is
    enough (SC-005). Raises IntegrityError on missing/corrupt/inconsistent state or version drift;
    never guesses (FR-022, SC-009)."""
    state = read_state(Path(course_dir) / "BUILD_PROGRESS.md")
    if expected_template_version is not None and state["template_version"] != expected_template_version:
        raise IntegrityError(
            f"template_version drift: course was stamped {state['template_version']!r}, "
            f"current template is {expected_template_version!r}"
        )
    return state


# --------------------------------------------------------------------------------------------
# CLI — a thin, scriptable surface for the .claude/ driver commands to shell out to
# --------------------------------------------------------------------------------------------

def _load(course_dir: Path) -> Path:
    return Path(course_dir) / "BUILD_PROGRESS.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BUILD_PROGRESS.md state core")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="initialize BUILD_PROGRESS.md at syllabus start")
    p_init.add_argument("course_dir", type=Path)
    p_init.add_argument("course_name")
    p_init.add_argument("template_version")

    p_show = sub.add_parser("show", help="print the current state block")
    p_show.add_argument("course_dir", type=Path)

    p_resume = sub.add_parser("resume", help="resume: read state, drift-check template_version")
    p_resume.add_argument("course_dir", type=Path)
    p_resume.add_argument("--template-version", default=None)

    p_trans = sub.add_parser("transition", help="apply a gate result to the current phase")
    p_trans.add_argument("course_dir", type=Path)
    p_trans.add_argument("gate_result", choices=sorted(GATE_RESULTS))

    p_acc = sub.add_parser("accept-round-cap", help="author accepts the capped artifact as-is")
    p_acc.add_argument("course_dir", type=Path)

    p_ext = sub.add_parser("extend-round-cap", help="author grants exactly one more refine pass")
    p_ext.add_argument("course_dir", type=Path)

    p_clear = sub.add_parser("clear-active-loop", help="settle a refine cycle that passed early (under the cap)")
    p_clear.add_argument("course_dir", type=Path)

    p_lesson = sub.add_parser("set-lesson-status", help="upsert one lesson's status")
    p_lesson.add_argument("course_dir", type=Path)
    p_lesson.add_argument("lesson_id")
    p_lesson.add_argument("status", choices=sorted(LESSON_STATUSES))

    p_seed = sub.add_parser("seed-lessons", help="seed lessons[] from a frozen SYLLABUS.md's lesson list")
    p_seed.add_argument("course_dir", type=Path)
    p_seed.add_argument("syllabus_path", type=Path)

    p_subphase = sub.add_parser("set-syllabus-subphase", help="002's checkpoint write")
    p_subphase.add_argument("course_dir", type=Path)
    p_subphase.add_argument("subphase", choices=sorted(SYLLABUS_SUBPHASES))

    p_lock_acq = sub.add_parser("lock-acquire", help="acquire the build lock for this invocation")
    p_lock_acq.add_argument("course_dir", type=Path)
    p_lock_acq.add_argument("--holder", default=None, help="defaults to a freshly minted token")

    p_lock_ref = sub.add_parser("lock-refresh", help="refresh last_progress_at for this invocation's holder")
    p_lock_ref.add_argument("course_dir", type=Path)
    p_lock_ref.add_argument("--holder", required=True, help="the token this invocation acquired the lock with")

    p_lock_rel = sub.add_parser("lock-release", help="release the build lock")
    p_lock_rel.add_argument("course_dir", type=Path)

    args = parser.parse_args(argv)
    path = _load(args.course_dir)

    try:
        if args.cmd == "init":
            state = init_state(args.course_name, args.template_version)
            write_state(path, state)
        elif args.cmd == "show":
            state = read_state(path)
            print(json.dumps(state, indent=2))
            return 0
        elif args.cmd == "resume":
            state = resume(args.course_dir, expected_template_version=args.template_version)
            print(json.dumps(state, indent=2))
            return 0
        elif args.cmd == "transition":
            state = read_state(path)
            state = transition(state, args.gate_result)
            write_state(path, state)
        elif args.cmd == "accept-round-cap":
            state = read_state(path)
            state = accept_round_cap(state)
            write_state(path, state)
        elif args.cmd == "extend-round-cap":
            state = read_state(path)
            state = extend_round_cap(state)
            write_state(path, state)
        elif args.cmd == "clear-active-loop":
            state = read_state(path)
            state = clear_active_loop(state)
            write_state(path, state)
        elif args.cmd == "set-lesson-status":
            state = read_state(path)
            state = set_lesson_status(state, args.lesson_id, args.status)
            write_state(path, state)
        elif args.cmd == "seed-lessons":
            state = read_state(path)
            syllabus_text = args.syllabus_path.read_text(encoding="utf-8")
            lesson_ids = parse_syllabus_lessons(syllabus_text)
            state = seed_lessons(state, lesson_ids)
            write_state(path, state)
        elif args.cmd == "set-syllabus-subphase":
            state = read_state(path)
            state = set_syllabus_subphase(state, args.subphase)
            write_state(path, state)
        elif args.cmd == "lock-acquire":
            state = read_state(path)
            holder = args.holder or mint_holder_token()
            state = acquire_lock(state, holder)
            write_state(path, state)
            print(holder)
            return 0
        elif args.cmd == "lock-refresh":
            state = read_state(path)
            state = refresh_lock(state, args.holder)
            write_state(path, state)
        elif args.cmd == "lock-release":
            state = read_state(path)
            state = release_lock(state)
            write_state(path, state)
    except (IntegrityError, TransitionError, LockError) as exc:
        print(f"progress: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(state, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
