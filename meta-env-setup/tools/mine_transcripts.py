#!/usr/bin/env python3
"""Mine Claude Code session transcripts for candidate setup blocks — stdlib only.

Repo files show *what the code is*; they do **not** show *what the human kept doing
by hand*. A command hand-rolled 15 times, a deploy→wait→fail loop repeated 8 times —
these are the strongest possible signals for a slash command or an offline bench, and
no static scan of the repo can see them. This tool reads the local Claude Code
transcripts for a repo (``~/.claude/projects/<slug>/*.jsonl``) and surfaces:

  * **Repeated commands**      -> candidate slash commands.
  * **Throwaway inline scripts** (``python -c`` / heredocs) -> candidate tools/benches.
  * **Deploy -> wait loops**   -> iteration-cost evidence (analyzer determinant 6).
  * **Recurring errors**       -> candidate gotcha skills.

Read-only. Secrets (bearer tokens, ``hf_``/``sk-``/``ghp_`` keys, …) are redacted from
every printed sample. Output is a Markdown report the ``setup-analyzer`` consumes as
first-class evidence for determinants 3 (repetitive workflows) and 6 (iteration cost).

Usage::

    python tools/mine_transcripts.py --repo /path/to/repo
    python tools/mine_transcripts.py --repo /path/to/repo --since 30 --out report.md
    python tools/mine_transcripts.py --transcripts ~/.claude/projects/<slug>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- Secret redaction (applied to every printed sample) ----------------------
_SECRET_PATTERNS = (
    re.compile(r"(?i)(authorization:\s*bearer\s+)\S+"),
    re.compile(r"\bhf_[A-Za-z0-9]{8,}"),
    re.compile(r"\bsk-[A-Za-z0-9]{12,}"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}"),
    re.compile(r"\bgh[oprsu]_[A-Za-z0-9]{20,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(token|password|passwd|secret|api[_-]?key)\b(\s*[=:]\s*)\S+"),
)


def _redact(text: str) -> str:
    if not text:
        return text
    out = text
    out = _SECRET_PATTERNS[0].sub(r"\1<REDACTED>", out)
    out = _SECRET_PATTERNS[7].sub(r"\1\2<REDACTED>", out)
    for pat in _SECRET_PATTERNS[1:7]:
        out = pat.sub("<REDACTED>", out)
    return out


# --- Project-path -> transcripts-dir slug ------------------------------------
def slug_for(repo: Path) -> str:
    """Claude Code maps a project path to ``~/.claude/projects/<slug>/`` by turning
    every non-alphanumeric char into ``-`` (``/home/a/book_gen`` -> ``-home-a-book-gen``)."""
    return re.sub(r"[^a-zA-Z0-9]", "-", str(repo.resolve()))


def transcripts_dir_for(repo: Path) -> Path:
    return Path.home() / ".claude" / "projects" / slug_for(repo)


# --- Command normalization (for clustering) ----------------------------------
def normalize_cmd(cmd: str) -> str:
    """Collapse a command to a template so variants cluster: strip quoted strings,
    paths, ids and numbers, keeping the structural skeleton."""
    c = cmd.strip()
    c = re.sub(r'"[^"]*"', "<str>", c)
    c = re.sub(r"'[^']*'", "<str>", c)
    c = re.sub(r"https?://\S+", "<url>", c)
    c = re.sub(r"/[\w./~-]+", "<path>", c)
    c = re.sub(r"\b[0-9a-f]{8,}\b", "<id>", c)
    c = re.sub(r"\b\d+\b", "<n>", c)
    c = re.sub(r"\s+", " ", c)
    return c[:80]


def is_throwaway(cmd: str) -> bool:
    """An inline one-off script the human wrote instead of a reusable tool."""
    return bool(re.search(r"\bpython[0-9]?\s+-c\b", cmd)) or "<<" in cmd or \
        bool(re.search(r">\s*/tmp/\S+\.py", cmd))


_DEPLOY_RE = re.compile(r"\b(sync_to_space|git\s+push|deploy|sync[._-]|npm\s+run\s+deploy|vercel|docker\s+push)\b", re.I)
_WAIT_RE = re.compile(r"\b(logs?/run|logs?/build|hf-logs|space-probe|ping_assets|\.hf\.space|/gradio_api/|curl.*logs)\b", re.I)
_ERR_RE = re.compile(r"(Traceback \(most recent call last\)|^\w*(Error|Exception):|RUNTIME_ERROR|segmentation fault|exit -?139|returncode=-?11)", re.M)


def _err_signature(text: str) -> str | None:
    """A short, clusterable head of an error, or None."""
    m = _ERR_RE.search(text or "")
    if not m:
        return None
    # take the matched line, trimmed
    line = text[m.start():].splitlines()[0].strip()
    return normalize_cmd(line)[:70]


# --- Extraction --------------------------------------------------------------
def _within(ts: str | None, cutoff: datetime | None) -> bool:
    if cutoff is None or not ts:
        return True
    try:
        when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return True
    return when >= cutoff


def _iter_events(transcripts: Path):
    for jf in sorted(transcripts.glob("*.jsonl")):
        try:
            with jf.open(encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
        except OSError:
            continue


def _tool_result_text(block: dict) -> str:
    content = block.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def mine(transcripts: Path, since_days: int | None) -> dict:
    """Return clustered signals from a repo's transcripts (read-only)."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=since_days)) if since_days else None
    bash: Counter[str] = Counter()
    bash_sample: dict[str, str] = {}
    throwaway: Counter[str] = Counter()
    throwaway_sample: dict[str, str] = {}
    errors: Counter[str] = Counter()
    n_deploy = n_wait = n_events = 0
    n_files = len(list(transcripts.glob("*.jsonl"))) if transcripts.is_dir() else 0

    for o in _iter_events(transcripts) if transcripts.is_dir() else []:
        n_events += 1
        ts = o.get("timestamp")
        if not _within(ts, cutoff):
            continue
        msg = o.get("message")
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            if btype == "tool_use" and block.get("name") == "Bash":
                cmd = (block.get("input") or {}).get("command", "") or ""
                if not cmd.strip():
                    continue
                key = normalize_cmd(cmd)
                bash[key] += 1
                bash_sample.setdefault(key, cmd)
                if _DEPLOY_RE.search(cmd):
                    n_deploy += 1
                if _WAIT_RE.search(cmd):
                    n_wait += 1
                if is_throwaway(cmd):
                    throwaway[key] += 1
                    throwaway_sample.setdefault(key, cmd)
            elif btype == "tool_result":
                sig = _err_signature(_tool_result_text(block))
                if sig:
                    errors[sig] += 1

    return {
        "n_files": n_files, "n_events": n_events,
        "bash": bash, "bash_sample": bash_sample,
        "throwaway": throwaway, "throwaway_sample": throwaway_sample,
        "errors": errors, "n_deploy": n_deploy, "n_wait": n_wait,
    }


# --- Report ------------------------------------------------------------------
def render_markdown(repo: Path, transcripts: Path, r: dict, min_repeats: int) -> str:
    L = [f"# Transcript mining — {repo}",
         f"> {r['n_files']} session file(s), {r['n_events']} events, from `{transcripts}`.",
         "> Read-only; secrets redacted. Analyzer input for determinants 3 (workflows) & 6 (iteration cost).",
         ""]
    if r["n_files"] == 0:
        L.append("_No transcripts found for this repo — nothing to mine (greenfield or fresh clone)._")
        return "\n".join(L)

    L.append(f"## Repeated commands (>= {min_repeats}x) -> candidate /commands")
    rep = [(k, c) for k, c in r["bash"].most_common() if c >= min_repeats]
    if rep:
        for k, c in rep[:15]:
            L.append(f"- **{c}x** `{k}`")
            L.append(f"  - e.g. `{_redact(r['bash_sample'][k])[:160]}`")
    else:
        L.append("- _none above threshold._")

    L.append("")
    L.append("## Throwaway inline scripts -> candidate tools / offline bench")
    tw = [(k, c) for k, c in r["throwaway"].most_common()]
    if tw:
        total_tw = sum(c for _, c in tw)
        L.append(f"- {total_tw} inline `python -c`/heredoc runs across {len(tw)} shape(s) — "
                 "each is a harness the human rebuilt instead of a reusable tool.")
        for k, c in tw[:8]:
            L.append(f"  - **{c}x** e.g. `{_redact(r['throwaway_sample'][k])[:160]}`")
    else:
        L.append("- _none detected._")

    L.append("")
    L.append("## Deploy -> wait loops -> iteration-cost evidence (determinant 6)")
    if r["n_deploy"] or r["n_wait"]:
        L.append(f"- **{r['n_deploy']}** deploy/sync/push invocations and **{r['n_wait']}** "
                 "log-fetch/probe calls — each deploy is a slow remote round-trip. A local "
                 "pre-push gate would convert these into sub-second offline checks.")
    else:
        L.append("- _no deploy/wait pattern detected._")

    L.append("")
    L.append("## Recurring errors -> candidate gotcha skills")
    errs = [(k, c) for k, c in r["errors"].most_common() if c >= min_repeats]
    if errs:
        for k, c in errs[:8]:
            L.append(f"- **{c}x** `{_redact(k)}`")
    else:
        L.append("- _none above threshold._")

    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Mine Claude Code transcripts for candidate setup blocks (read-only).")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--repo", help="path to the target repo (its transcripts dir is derived)")
    g.add_argument("--transcripts", help="explicit ~/.claude/projects/<slug> dir")
    p.add_argument("--since", type=int, default=45, help="only events in the last N days (0 = all; default 45)")
    p.add_argument("--min-repeats", type=int, default=3, help="cluster threshold for 'repeated' (default 3)")
    p.add_argument("--out", help="write the Markdown report here (default: stdout)")
    args = p.parse_args(argv)

    if args.repo:
        repo = Path(args.repo)
        transcripts = transcripts_dir_for(repo)
    else:
        transcripts = Path(args.transcripts)
        repo = transcripts

    # Fail soft on a missing dir: an empty report, not a crash (greenfield repos
    # and fresh clones simply have no transcripts to mine).
    report = render_markdown(repo, transcripts, mine(transcripts, args.since or None), args.min_repeats)

    if args.out:
        Path(args.out).write_text(report + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
