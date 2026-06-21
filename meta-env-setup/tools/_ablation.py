#!/usr/bin/env python3
"""Layer 3 — ablation harness for Claude Code setups (the gold-standard proof).

Runs a small task suite under several *conditions* — the FULL setup, the setup
with one block removed (leave-one-out), and NO setup at all — then compares
pass-rates. A block whose removal does NOT lower any task's pass-rate is dead
weight (``CUT``); a block whose removal hurts earns its place (``KEEP``). This is
the only layer that can *prove* "minimal yet maximal".

It is slow and costs compute (it launches ``claude -p`` many times), so it is
opt-in: the default is a free ``dry-run`` preview of the run matrix; pass
``--execute`` to actually run. Stdlib only; imported by
``validate_claude_setup.py`` for the ``--ablate`` mode.

Task suite format (``evals/<repo>/tasks.json``)::

    {"tasks": [
      {"id": "recall-first",
       "prompt": "Let's switch our metric from F2 to plain accuracy ...",
       "expect_skill": "ml-experiment-tracking",          # informational
       "assertions": [
         {"type": "output_contains_any", "values": ["recall", "F2"]},
         {"type": "output_excludes", "value": "sounds great"}
       ]}
    ]}

Assertion types: ``output_contains`` / ``output_contains_any`` / ``output_excludes``
(checked against the agent's final text) and ``file_exists`` / ``file_contains``
(checked in the sandbox working dir). A run passes a task iff ALL its assertions hold.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

RUN_TIMEOUT = 240          # seconds per agent invocation
KEEP_DROP = 0.34           # a block "earns its place" if removing it drops a task >= this


# --------------------------------------------------------------------------- #
# Setup discovery
# --------------------------------------------------------------------------- #
def _setup_paths(root: Path) -> tuple[Path, Path | None]:
    claude = root / ".claude" if (root / ".claude").is_dir() else root
    claude_md = None
    for name in ("CLAUDE.md", "CLAUDE-additions.md", "CLAUDE.local.md"):
        if (root / name).is_file():
            claude_md = root / name
            break
    return claude, claude_md


def _enumerate_blocks(claude: Path) -> list[tuple[str, str, Path]]:
    """Yield (kind, name, path-to-remove) for every removable block."""
    out: list[tuple[str, str, Path]] = []
    sd = claude / "skills"
    if sd.is_dir():
        for d in sorted(p for p in sd.iterdir() if p.is_dir()):
            out.append(("skill", d.name, d))
    for kind, sub in (("command", "commands"), ("agent", "agents")):
        dd = claude / sub
        if dd.is_dir():
            for f in sorted(dd.glob("*.md")):
                out.append((kind, f.stem, f))
    return out


def _load_tasks(root: Path, explicit: str | None) -> tuple[list[dict] | None, Path]:
    path = Path(explicit) if explicit else Path("evals") / root.name / "tasks.json"
    if not path.is_file():
        return None, path
    spec = json.loads(path.read_text(encoding="utf-8"))
    tasks = [t for t in spec.get("tasks", []) if isinstance(t, dict) and t.get("prompt")]
    return tasks, path


# --------------------------------------------------------------------------- #
# Sandbox + agent invocation
# --------------------------------------------------------------------------- #
def _build_sandbox(claude: Path, claude_md: Path | None, remove: Path | None,
                   include_setup: bool) -> Path:
    """A throwaway working dir containing the (possibly ablated) setup."""
    tmp = Path(tempfile.mkdtemp(prefix="ablate-"))
    if include_setup:
        shutil.copytree(claude, tmp / ".claude")
        if claude_md is not None:
            shutil.copy2(claude_md, tmp / "CLAUDE.md")
        if remove is not None:
            target = tmp / ".claude" / remove.relative_to(claude)
            if target.is_dir():
                shutil.rmtree(target)
            elif target.is_file():
                target.unlink()
    return tmp


def _run_claude(prompt: str, workdir: Path) -> str:
    """Run one headless agent turn; return its final text (or an error marker)."""
    extra = os.environ.get("ABLATION_CLAUDE_ARGS", "").split()
    cmd = ["claude", "-p", prompt, "--output-format", "json", *extra]
    try:
        proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True,
                              timeout=RUN_TIMEOUT)
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        return f"__ABLATION_ERROR__ {exc}"
    raw = proc.stdout.strip()
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return str(data.get("result") or data.get("text") or raw)
    except json.JSONDecodeError:
        pass
    return raw or proc.stderr


# --------------------------------------------------------------------------- #
# Assertions
# --------------------------------------------------------------------------- #
def _check(assertion: dict, output: str, workdir: Path) -> bool:
    kind = assertion.get("type")
    low = output.lower()
    if kind == "output_contains":
        return assertion.get("value", "").lower() in low
    if kind == "output_contains_any":
        return any(str(v).lower() in low for v in assertion.get("values", []))
    if kind == "output_excludes":
        return assertion.get("value", "").lower() not in low
    if kind == "file_exists":
        return (workdir / assertion.get("path", "")).exists()
    if kind == "file_contains":
        f = workdir / assertion.get("path", "")
        return f.is_file() and assertion.get("value", "").lower() in \
            f.read_text(encoding="utf-8", errors="ignore").lower()
    return False  # unknown assertion type fails closed


def _task_passes(task: dict, output: str, workdir: Path) -> bool:
    asserts = task.get("assertions", [])
    return bool(asserts) and all(_check(a, output, workdir) for a in asserts)


def _pass_rate(task: dict, claude: Path, claude_md: Path | None, remove: Path | None,
               include_setup: bool, repeats: int) -> float:
    passes = 0
    for _ in range(repeats):
        sandbox = _build_sandbox(claude, claude_md, remove, include_setup)
        try:
            out = _run_claude(task["prompt"], sandbox)
            if out.startswith("__ABLATION_ERROR__"):
                raise RuntimeError(out.replace("__ABLATION_ERROR__", "claude run failed:"))
            passes += _task_passes(task, out, sandbox)
        finally:
            shutil.rmtree(sandbox, ignore_errors=True)
    return passes / repeats


# --------------------------------------------------------------------------- #
# Orchestration  (split out so the verdict logic is unit-testable without
# launching a single agent — see tools/test_audit.py, which mocks _run_claude.)
# --------------------------------------------------------------------------- #
def _mean(d: dict[str, float]) -> float:
    return sum(d.values()) / len(d) if d else 0.0


def _conditions(blocks: list[tuple[str, str, Path]]) -> list[tuple[str, Path | None, bool]]:
    conds: list[tuple[str, Path | None, bool]] = [("full", None, True), ("no-setup", None, False)]
    conds += [(f"{kind}:{name}", path, True) for kind, name, path in blocks]
    return conds


def _execute(conditions, tasks, claude, claude_md, repeats) -> dict[str, dict[str, float]]:
    return {
        label: {task["id"]: _pass_rate(task, claude, claude_md, remove, include, repeats)
                for task in tasks}
        for label, remove, include in conditions
    }


def _verdict(results, blocks, root, tasks, repeats) -> tuple[list[str], list[str]]:
    full = results.get("full", {})
    cut: list[str] = []
    lines = [f"[ABLATE] {root}  ({len(tasks)} tasks x {repeats} repeats)",
             f"  {'full':<28} mean pass-rate {_mean(full):.2f}",
             f"  {'no-setup':<28} mean pass-rate {_mean(results.get('no-setup', {})):.2f}  (baseline)"]
    for kind, name, _ in blocks:
        label = f"{kind}:{name}"
        cond = results.get(label, {})
        max_drop = max((full[t] - cond.get(t, 0.0)) for t in full) if full else 0.0
        verdict = "KEEP" if max_drop >= KEEP_DROP else "CUT "
        if verdict.strip() == "CUT":
            cut.append(label)
        lines.append(f"  - {label:<26} mean {_mean(cond):.2f}  {verdict} (worst task drop {max_drop:+.2f})")
    lines.append(f"  VERDICT: {len(cut)} of {len(blocks)} blocks removable without measurable loss"
                 + (": " + ", ".join(cut) if cut else ""))
    return lines, cut


def run_ablation(root: Path, tasks_path: str | None, repeats: int,
                 dry_run: bool = True, as_json: bool = False) -> int:
    claude, claude_md = _setup_paths(root)
    if not claude.is_dir():
        print(f"[ABLATE] {root}: no .claude/ directory found")
        return 1
    tasks, tpath = _load_tasks(root, tasks_path)
    if tasks is None:
        print(f"[ABLATE] {root}: no task suite found (looked for {tpath})")
        return 1

    blocks = _enumerate_blocks(claude)
    conditions = _conditions(blocks)
    n_runs = len(conditions) * len(tasks) * repeats

    # ---- dry-run / unavailable: preview the matrix, launch nothing ----
    have_claude = shutil.which("claude") is not None
    if dry_run or not have_claude:
        why = "dry-run" if dry_run else "claude CLI not found — preview only"
        print(f"[ABLATE {why}] {root}")
        print(f"  task suite: {tpath}")
        print(f"  tasks: {len(tasks)} | repeats: {repeats} | "
              f"conditions: {len(conditions)} (1 full + 1 no-setup + {len(blocks)} leave-one-out)")
        print(f"  would launch {n_runs} agent runs (claude -p)"
              + ("" if have_claude else "  [claude not on PATH]"))
        print("  pass --execute to run; tune cost with --repeats N")
        for label, _, _ in conditions:
            print(f"    - {label}")
        return 0

    # ---- real execution ----
    print(f"[ABLATE] {root}: launching {n_runs} agent runs "
          f"({len(conditions)} conditions x {len(tasks)} tasks x {repeats} repeats)…")
    results = _execute(conditions, tasks, claude, claude_md, repeats)
    lines, cut = _verdict(results, blocks, root, tasks, repeats)
    print("\n".join(lines))
    if as_json:
        print(json.dumps({"root": str(root), "repeats": repeats,
                          "results": results, "cut": cut}, indent=2))
    return 0
