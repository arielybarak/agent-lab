#!/usr/bin/env python3
"""Validate a Claude Code setup (``.claude/``) — CI-friendly, stdlib only.

Mirrors the spirit of ``initial-sendbox/hooks/governance-audit`` (which audits
Copilot ``.agent.md`` files) but targets Claude Code's layout:

  * ``skills/*/SKILL.md`` -> front-matter with non-empty ``name`` + ``description``;
                             ``name`` matches the folder and is kebab-case.
  * ``commands/*.md``     -> front-matter present; ``description`` recommended.
  * ``agents/*.md``       -> front-matter with non-empty ``name`` + ``description``.
  * ``settings.json``     -> valid JSON; every hook ``command`` that points at a
                             ``.claude/hooks/<script>`` resolves to a real file
                             (broken wiring is an ERROR); hook scripts present but
                             never referenced are flagged as orphans (warning).
  * ``description``        -> warns if a TODO placeholder, too terse (< 40 chars),
                             or too long (> 1024 chars — it costs routing budget).

Exit code is non-zero when any ERROR-level issue is found, so it can gate CI.
A tiny hand-rolled front-matter parser is used on purpose: no PyYAML dependency,
and the ``key: value`` subset is all these files use.

Usage::

    python tools/validate_claude_setup.py claude-setups/DL-Project
    python tools/validate_claude_setup.py claude-setups/*          # many at once
    python tools/validate_claude_setup.py claude-setups/DL-Project --json --strict
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MAX_DESCRIPTION = 1024
MIN_DESCRIPTION = 40
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HOOK_REF = re.compile(r"\.claude/hooks/([A-Za-z0-9_./-]+\.py)")


@dataclass
class Issue:
    severity: str  # "error" | "warning"
    path: str
    message: str


@dataclass
class Report:
    root: str
    issues: list[Issue] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=lambda: {"skills": 0, "commands": 0, "agents": 0, "hooks": 0})
    skipped: bool = False

    def error(self, path: Path, msg: str) -> None:
        self.issues.append(Issue("error", str(path), msg))

    def warn(self, path: Path, msg: str) -> None:
        self.issues.append(Issue("warning", str(path), msg))

    @property
    def n_errors(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def n_warnings(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def files_checked(self) -> int:
        return sum(self.counts.values())


def parse_front_matter(text: str) -> dict[str, str] | None:
    """Return ``key: value`` front-matter as a dict, or None if absent.

    Handles a leading ``---`` fence, simple ``key: value`` pairs (values may be
    quoted or use ``>-`` / ``|`` block scalars, flattened to one string), and a
    closing ``---``.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None

    data: dict[str, str] = {}
    key: str | None = None
    block = False
    for raw in lines[1:end]:
        if block:
            if raw.startswith((" ", "\t")) and key is not None:
                data[key] = (data[key] + " " + raw.strip()).strip()
                continue
            block = False
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            continue
        k, _, v = raw.partition(":")
        key = k.strip()
        v = v.strip()
        if v in (">-", ">", "|", "|-"):
            data[key] = ""
            block = True
        else:
            data[key] = v.strip().strip('"').strip("'")
    return data


def _is_todo(value: str) -> bool:
    return value.strip().upper().startswith("TODO")


def _check_description(report: Report, path: Path, desc: str) -> None:
    if _is_todo(desc):
        report.warn(path, "`description` is still a TODO placeholder")
    elif len(desc) < MIN_DESCRIPTION:
        report.warn(path, f"`description` is only {len(desc)} chars — too terse to route well")
    elif len(desc) > MAX_DESCRIPTION:
        report.warn(path, f"`description` is {len(desc)} chars (> {MAX_DESCRIPTION})")


def _check_named(report: Report, path: Path, fm: dict[str, str] | None, expect_name: str | None) -> None:
    """Shared check for files that must have name + description (skills, agents)."""
    if fm is None:
        report.error(path, "missing YAML front-matter (--- ... ---)")
        return
    name = fm.get("name", "").strip()
    desc = fm.get("description", "").strip()
    if not name:
        report.error(path, "front-matter missing non-empty `name`")
    else:
        if expect_name and name != expect_name:
            report.warn(path, f"`name` ({name!r}) does not match its file/folder ({expect_name!r})")
        if not KEBAB.match(name):
            report.warn(path, f"`name` ({name!r}) is not kebab-case")
    if not desc:
        report.error(path, "front-matter missing non-empty `description`")
    else:
        _check_description(report, path, desc)


def _validate_settings(report: Report, claude: Path) -> None:
    """JSON validity + hook wiring (referenced scripts exist; flag orphans)."""
    settings = claude / "settings.json"
    referenced: set[str] = set()
    if settings.is_file():
        try:
            data = json.loads(settings.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(settings, f"invalid JSON: {exc}")
            data = {}
        for event_hooks in (data.get("hooks") or {}).values():
            for entry in event_hooks or []:
                for hook in entry.get("hooks", []) or []:
                    cmd = hook.get("command", "") or ""
                    for rel in HOOK_REF.findall(cmd):
                        referenced.add(Path(rel).name)
                        if not (claude / "hooks" / Path(rel).name).is_file():
                            report.error(settings, f"hook command references missing script: {rel}")
    # Orphan hook scripts: present on disk but never wired into settings.json.
    hooks_dir = claude / "hooks"
    if hooks_dir.is_dir():
        for script in sorted(hooks_dir.glob("*.py")):
            report.counts["hooks"] += 1
            if script.name not in referenced:
                report.warn(script, "hook script is not referenced by settings.json (orphan)")


def validate(root: Path) -> Report:
    report = Report(root=str(root))
    if root.is_file():
        report.skipped = True  # e.g. a glob that also matched README.md — ignore, don't fail
        return report
    claude = root / ".claude" if (root / ".claude").is_dir() else root
    if not claude.is_dir():
        report.error(root, "no .claude/ directory found")
        return report

    skills_dir = claude / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                report.error(skill_dir, "skill folder has no SKILL.md")
                continue
            report.counts["skills"] += 1
            _check_named(report, skill_md, parse_front_matter(skill_md.read_text(encoding="utf-8")), skill_dir.name)

    commands_dir = claude / "commands"
    if commands_dir.is_dir():
        for cmd in sorted(commands_dir.glob("*.md")):
            report.counts["commands"] += 1
            fm = parse_front_matter(cmd.read_text(encoding="utf-8"))
            if fm is None:
                report.warn(cmd, "no front-matter; a `description:` line is recommended")
            elif not fm.get("description", "").strip():
                report.warn(cmd, "front-matter missing `description`")
            else:
                _check_description(report, cmd, fm["description"].strip())

    agents_dir = claude / "agents"
    if agents_dir.is_dir():
        for agent in sorted(agents_dir.glob("*.md")):
            report.counts["agents"] += 1
            _check_named(report, agent, parse_front_matter(agent.read_text(encoding="utf-8")), agent.stem)

    _validate_settings(report, claude)
    return report


def print_human(report: Report) -> None:
    if report.skipped:
        print(f"SKIP  {report.root}: not a directory")
        return
    for issue in report.issues:
        tag = "ERROR  " if issue.severity == "error" else "warning"
        print(f"  [{tag}] {issue.path}: {issue.message}")
    c = report.counts
    status = "FAIL" if report.n_errors else "OK"
    print(
        f"{status}  {report.root}: "
        f"{c['skills']} skills, {c['commands']} commands, {c['agents']} agents, {c['hooks']} hooks; "
        f"{report.n_errors} error(s), {report.n_warnings} warning(s)."
    )


# ===========================================================================
# Layer 1 — effectiveness audit (``--score``). ADVISORY: never gates CI.
#
# "Valid" only means well-formed. These heuristics estimate whether a setup is
# *effective* (helps the agent) and *minimal* (no dead-weight blocks burning the
# always-loaded routing budget). They flag SUSPECTS cheaply and deterministically;
# only ablation (``--ablate``) can *prove* a block earns its place.
# ===========================================================================

# Words too common to signal what a block is *about* (English + setup-generic).
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "when", "then", "else", "of",
    "to", "in", "on", "for", "with", "without", "by", "at", "from", "into",
    "as", "is", "are", "be", "this", "that", "these", "those", "it", "its",
    "you", "your", "we", "our", "they", "use", "uses", "used", "using", "add",
    "added", "new", "run", "running", "runs", "file", "files", "code", "repo",
    "repository", "project", "setup", "claude", "skill", "command", "agent",
    "hook", "should", "must", "can", "will", "via", "per", "each", "any", "all",
    "not", "no", "do", "does", "done", "how", "what", "which", "one", "two",
    "see", "also", "etc", "like", "such", "more", "most", "less", "than", "so",
    "its", "their", "them", "here", "there", "out", "up", "down", "over",
    "rule", "rules", "common", "available", "guidance", "companion", "prefer",
    "follow", "follows", "way", "lives", "live", "things", "thing", "where",
    "don", "doesn", "isn", "won", "let", "gets", "get", "got", "makes", "make",
    "skills", "commands", "agents", "subagents", "hooks", "tools", "setups",
}

# Cues that a description says *when* to fire (not merely what it is).
TRIGGER_CUES = (
    "use when", "when ", "whenever", "after ", "before ", "if you", "anytime",
    "any time", "asks", "request", "starting", "writing", "choosing", "before",
)

# Soft ceiling for the always-loaded surface (tokens). Above it the routing
# budget is getting heavy — a nudge, not an error.
BUDGET_CEILING_TOKENS = 2500
REDUNDANCY_THRESHOLD = 0.40   # desc-vs-desc Jaccard above this => overlap suspect
BRIEF_ECHO_MIN = 2            # shared distinctive tokens with CLAUDE.md => echo suspect
GROUNDED_MIN = 0.05           # desc-vs-repo-vocab overlap below this => generic suspect

# Composite weights (documented + tunable). Sum to 1.0.
# Coverage is deliberately NOT scored: static coverage detection returned a flat
# ~0.66 for every setup (no discriminating power), so it only added noise to the
# number. It survives as an advisory [HINT] line instead. Ablation is the real
# coverage test.
WEIGHTS = {
    "trigger": 0.35,
    "specificity": 0.25,
    "redundancy": 0.25,
    "budget": 0.10,
    "leastpriv": 0.05,
}

WORD_RE = re.compile(r"[a-z0-9][a-z0-9+.#_-]*")


def _tokens(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def _content_words(text: str) -> list[str]:
    return [t for t in _tokens(text) if t not in STOPWORDS and len(t) > 2]


def _word_set(text: str) -> set[str]:
    return set(_content_words(text))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _estimate_tokens(text: str) -> int:
    """~4 chars/token — the usual rough English heuristic; no tokenizer dep."""
    return max(1, round(len(text) / 4))


def _distinctive(token: str) -> bool:
    """A figure specific enough that sharing it signals copy-paste, not topic.

    Decimals (``0.9552``, ``99.2``, ``5.6``) and integers with >=3 digits
    (``241``). Deliberately NOT alpha identifiers (kebab cross-references like
    ``notebook-to-src`` are *good*) and NOT list markers (``1.``, ``2.``) or
    short common numbers (``16``, ``3``, ``96``).
    """
    return bool(re.fullmatch(r"\d+\.\d+", token) or re.fullmatch(r"\d{3,}", token))


def _strip_front_matter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        try:
            end = lines.index("---", 1)
            return "\n".join(lines[end + 1:])
        except ValueError:
            return text
    return text


def _trigger_score(desc: str) -> float:
    """0/0.5/1.0 — does the description carry both *what* and *when*?"""
    low = desc.lower()
    has_when = any(c in low for c in TRIGGER_CUES) or bool(re.search(r"\.\w{1,5}\b", low))
    has_what = len(_word_set(desc)) >= 4
    return (0.5 if has_when else 0.0) + (0.5 if has_what else 0.0)


@dataclass
class Block:
    kind: str           # "skill" | "command" | "agent"
    name: str
    description: str
    body: str = ""
    tools: str | None = None
    path: str = ""


def _read_claude_md(root: Path) -> str:
    for fname in ("CLAUDE.md", "CLAUDE-additions.md", "CLAUDE.local.md"):
        f = root / fname
        if f.is_file():
            return f.read_text(encoding="utf-8")
    return ""


def _collect_blocks(claude: Path) -> list[Block]:
    blocks: list[Block] = []
    sd = claude / "skills"
    if sd.is_dir():
        for d in sorted(p for p in sd.iterdir() if p.is_dir()):
            md = d / "SKILL.md"
            if not md.is_file():
                continue
            text = md.read_text(encoding="utf-8")
            fm = parse_front_matter(text) or {}
            blocks.append(Block("skill", fm.get("name", d.name) or d.name,
                                fm.get("description", ""), _strip_front_matter(text),
                                None, str(md)))
    cd = claude / "commands"
    if cd.is_dir():
        for f in sorted(cd.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            fm = parse_front_matter(text) or {}
            blocks.append(Block("command", f.stem, fm.get("description", ""),
                                _strip_front_matter(text), None, str(f)))
    ad = claude / "agents"
    if ad.is_dir():
        for f in sorted(ad.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            fm = parse_front_matter(text) or {}
            blocks.append(Block("agent", fm.get("name", f.stem) or f.stem,
                                fm.get("description", ""), _strip_front_matter(text),
                                fm.get("tools"), str(f)))
    return blocks


@dataclass
class Audit:
    root: str
    skipped: bool = False
    error: str = ""
    budget_tokens: int = 0
    budget_breakdown: dict = field(default_factory=dict)
    subscores: dict = field(default_factory=dict)
    score: int = 0
    cut: list = field(default_factory=list)       # [path, why]
    sharpen: list = field(default_factory=list)   # [path, why]
    gaps: list = field(default_factory=list)       # [why]


def audit(root: Path) -> Audit:
    a = Audit(root=str(root))
    if root.is_file():
        a.skipped = True
        return a
    base = root
    claude = root / ".claude" if (root / ".claude").is_dir() else root
    if not claude.is_dir():
        a.error = "no .claude/ directory found"
        return a
    # CLAUDE.md may sit beside .claude/ (claude-setups/<repo>/CLAUDE.md) or inside it.
    claude_md = _read_claude_md(base) or _read_claude_md(claude) or _read_claude_md(claude.parent)
    repo_vocab = _word_set(claude_md)
    blocks = _collect_blocks(claude)

    # 1) Context budget — the always-loaded surface (CLAUDE.md + every description).
    md_tok = _estimate_tokens(claude_md)
    desc_tok = sum(_estimate_tokens(b.description) for b in blocks)
    a.budget_tokens = md_tok + desc_tok
    a.budget_breakdown = {"claude_md": md_tok, "descriptions": desc_tok, "n_blocks": len(blocks)}

    # 2) Trigger quality — per description.
    trigger_scores = []
    for b in blocks:
        ts = _trigger_score(b.description)
        trigger_scores.append(ts)
        if ts < 1.0 and b.kind != "command":  # commands route by name, less critical
            why = "description lacks a clear *when* (trigger phrase)" if ts >= 0.5 else \
                  "description is too thin to route (missing what *and* when)"
            a.sharpen.append([b.path, why])

    # 3) Redundancy — desc-vs-desc overlap (hard), and echoing CLAUDE.md
    #    specifics (soft). Kept as separate penalties: duplicate descriptions are
    #    a real "cut one" problem; echoing a figure is just "trim the copy".
    n_dup = n_echo = 0
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            jac = _jaccard(_word_set(blocks[i].description), _word_set(blocks[j].description))
            if jac >= REDUNDANCY_THRESHOLD:
                n_dup += 1
                a.cut.append([blocks[j].path,
                              f"description overlaps '{blocks[i].name}' (Jaccard {jac:.2f}) — merge or sharpen"])
    if repo_vocab:
        md_distinct = {t for t in _tokens(claude_md) if _distinctive(t)}
        for b in blocks:
            shared = sorted({t for t in _tokens(b.body) if _distinctive(t)} & md_distinct)
            if len(shared) >= BRIEF_ECHO_MIN:
                n_echo += 1
                ex = ", ".join(shared[:3])
                a.sharpen.append([b.path,
                                  f"echoes CLAUDE.md specifics ({ex}) — keep the pointer, cut the copy"])

    # 4) Specificity — is each block grounded in this repo's vocabulary?
    grounded = 0
    for b in blocks:
        overlap = _jaccard(_word_set(b.description), repo_vocab) if repo_vocab else 0.0
        frac = (len(_word_set(b.description) & repo_vocab) / max(1, len(_word_set(b.description)))) if repo_vocab else 1.0
        if not repo_vocab or frac >= GROUNDED_MIN:
            grounded += 1
        else:
            a.cut.append([b.path, "description shares almost no vocabulary with CLAUDE.md — generic filler?"])
        _ = overlap

    # 5) Coverage — recurring brief terms absent from the routing surface
    #    (block names + descriptions). A hint, not a verdict: static coverage is
    #    noisy; ablation (--ablate) is the real coverage test.
    if repo_vocab and blocks:
        surface = set().union(*[_word_set(b.name.replace("-", " ") + " " + b.description) for b in blocks])
        freq: dict[str, int] = {}
        for t in _content_words(claude_md):
            freq[t] = freq.get(t, 0) + 1
        meaningful = [(t, c) for t, c in freq.items() if re.fullmatch(r"[a-z]{4,}", t) and c >= 2]
        top = [t for t, _ in sorted(meaningful, key=lambda kv: -kv[1])[:20]]
        uncovered = [t for t in top if t not in surface][:5]
        if uncovered:
            a.gaps.append("recurring brief terms not in any block name/description: " + ", ".join(uncovered))

    # 6) Least-privilege — agents that inherit all tools.
    agents = [b for b in blocks if b.kind == "agent"]
    narrowed = 0
    for b in agents:
        if b.tools and b.tools.strip():
            narrowed += 1
        else:
            a.sharpen.append([b.path, "agent has no `tools:` — inherits ALL tools; narrow for least-privilege"])

    # ---- sub-scores in [0,1] ----
    n = max(1, len(blocks))
    s = a.subscores
    s["trigger"] = round(sum(trigger_scores) / n, 3) if blocks else 1.0
    s["specificity"] = round(grounded / n, 3) if blocks else 1.0
    s["redundancy"] = round(max(0.0, 1.0 - 0.25 * n_dup - 0.06 * n_echo), 3)
    over = max(0, a.budget_tokens - BUDGET_CEILING_TOKENS)
    s["budget"] = round(max(0.0, 1.0 - over / BUDGET_CEILING_TOKENS), 3)
    s["leastpriv"] = round(narrowed / len(agents), 3) if agents else 1.0

    a.score = round(100 * sum(WEIGHTS[k] * s[k] for k in WEIGHTS))
    return a


def _audit_to_dict(a: Audit) -> dict:
    return {
        "root": a.root, "skipped": a.skipped, "error": a.error,
        "score": a.score, "budget_tokens": a.budget_tokens,
        "budget_breakdown": a.budget_breakdown, "subscores": a.subscores,
        "cut": a.cut, "sharpen": a.sharpen, "gaps": a.gaps,
    }


def print_audit(a: Audit) -> None:
    if a.skipped:
        print(f"SKIP  {a.root}: not a directory")
        return
    if a.error:
        print(f"[SCORE] {a.root}: {a.error}")
        return
    bb = a.budget_breakdown
    print(f"[SCORE] {a.root}: composite {a.score}/100")
    print(f"  budget: {a.budget_tokens} tok always-loaded "
          f"(CLAUDE.md {bb.get('claude_md', 0)} + {bb.get('n_blocks', 0)} descriptions {bb.get('descriptions', 0)})"
          + ("  [over ceiling]" if a.budget_tokens > BUDGET_CEILING_TOKENS else ""))
    print("  sub-scores: " + ", ".join(f"{k} {a.subscores[k]:.2f}" for k in WEIGHTS))
    for label, items in (("CUT?", a.cut), ("SHARPEN", a.sharpen)):
        for path, why in items:
            print(f"  [{label}] {path}: {why}")
    for why in a.gaps:
        print(f"  [HINT] {why}  (advisory; not scored)")


# ===========================================================================
# Layer 2 — routing tests (``--route``). Does each description actually fire on
# the right prompts (and stay quiet on the wrong ones)? Default is a stdlib
# nearest-description classifier (deterministic, no model call).
# ===========================================================================

def _stem(token: str) -> str:
    """Crude suffix stripper so 'exporting' ~ 'export'. Routing-only (kept out of
    the Layer-1 word sets so it can't perturb the tuned audit numbers)."""
    for suf in ("ing", "ed", "es", "s"):
        if token.endswith(suf) and len(token) - len(suf) >= 3:
            return token[: -len(suf)]
    return token


def _stemmed_set(text: str) -> set[str]:
    return {_stem(t) for t in _content_words(text)}


def _predict_skill(prompt: str, skills: list[Block]) -> str | None:
    pw = _stemmed_set(prompt)
    best, best_score = None, 0.0
    for sk in skills:
        score = _jaccard(pw, _stemmed_set(sk.name.replace("-", " ") + " " + sk.description))
        if score > best_score:
            best, best_score = sk.name, score
    return best if best_score > 0 else None


def _find_routing_tests(root: Path, explicit: str | None) -> Path | None:
    if explicit:
        return Path(explicit)
    for cand in (Path("evals") / root.name / "routing-tests.json",
                 root / "routing-tests.json",
                 root / "eval" / "routing-tests.json"):
        if cand.is_file():
            return cand
    return None


def route(root: Path, tests_path: str | None) -> tuple[int, int, list[str]]:
    """Return (passed, total, lines)."""
    claude = root / ".claude" if (root / ".claude").is_dir() else root
    skills = [b for b in _collect_blocks(claude) if b.kind == "skill"]
    tests_file = _find_routing_tests(root, tests_path)
    lines: list[str] = []
    if tests_file is None or not tests_file.is_file():
        lines.append(f"[ROUTE] {root}: no routing-tests.json found (looked in evals/{root.name}/)")
        return 0, 0, lines
    spec = json.loads(tests_file.read_text(encoding="utf-8"))
    passed = total = 0
    lines.append(f"[ROUTE] {root}  (tests: {tests_file})")
    for skill_name, cases in spec.items():
        if skill_name.startswith("_") or not isinstance(cases, dict):
            continue  # allow "_comment" and other metadata keys
        for prompt in cases.get("should_fire", []):
            total += 1
            pred = _predict_skill(prompt, skills)
            ok = pred == skill_name
            passed += ok
            lines.append(f"  {'PASS' if ok else 'FAIL'}  fire   {skill_name!r} <- {prompt!r}"
                         + ("" if ok else f"  (routed to {pred!r})"))
        for prompt in cases.get("should_not_fire", []):
            total += 1
            pred = _predict_skill(prompt, skills)
            ok = pred != skill_name
            passed += ok
            lines.append(f"  {'PASS' if ok else 'FAIL'}  quiet  {skill_name!r} <- {prompt!r}"
                         + ("" if ok else "  (wrongly routed here)"))
    lines.append(f"  -> {passed}/{total} routing assertions passed")
    return passed, total, lines


# ===========================================================================
# Layer 1b — staleness (``--stale --repo <path>``). ADVISORY: never gates CI.
#
# A block that describes code which no longer exists misleads worse than a
# missing block (the TOM Era-2 problem: skills still naming boolean-union / taper
# / skeletonization after the engine migration removed them). This is a purely
# MECHANICAL check — it extracts the distinctive *identifiers* a block cites
# (snake_case, CONSTANT_CASE, CamelCase, filenames) and greps them against the
# target repo. Zero hits => "dead noun". Enough dead nouns => stale-suspect.
# (Prose-concept drift like the word "skeletonization" is the analyzer's job, not
# this scan's.) Pooled blocks (tools-pool/) are scanned too: a pre-built parked
# block can rot before it's ever promoted.
# ===========================================================================

STALE_SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", "dist", "build", ".venv", "venv",
    ".next", ".cache", "outputs", "vendor", "target", ".mypy_cache", ".pytest_cache",
}
STALE_MAX_FILE_BYTES = 2_000_000

_IDENT_PATTERNS = (
    re.compile(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+"),                 # CONSTANT_CASE
    re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+"),                 # snake_case
    re.compile(r"[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+"),            # CamelCase
    re.compile(r"[\w-]+\.(?:py|js|jsx|ts|tsx|mjs|cpp|hpp|h|cc|sv|svh|go|rs|rb|java|yaml|yml)\b"),  # filenames
)


def _identifier_nouns(text: str) -> set[str]:
    """Distinctive code identifiers a block cites — the things that can go stale.

    Deliberately narrow: only tokens that unambiguously name a code artifact
    (multi-part identifiers, filenames), so a hit is real and false positives are
    rare. Plain English words are ignored — they'd grep-hit anything.
    """
    out: set[str] = set()
    for pat in _IDENT_PATTERNS:
        out.update(pat.findall(text))
    return out


def _repo_token_index(repo: Path) -> set[str]:
    """Every identifier present anywhere in the repo's text files (+ file basenames)."""
    tokens: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in STALE_SKIP_DIRS]
        for fn in filenames:
            tokens.add(fn)  # a filename cited verbatim counts as present
            f = Path(dirpath) / fn
            try:
                if f.stat().st_size > STALE_MAX_FILE_BYTES:
                    continue
                raw = f.read_bytes()
            except OSError:
                continue
            if b"\x00" in raw[:4096]:
                continue  # binary
            tokens |= _identifier_nouns(raw.decode("utf-8", "ignore"))
    return tokens


def _is_stale(nouns: set[str], repo_tokens: set[str]) -> tuple[bool, list[str]]:
    """(stale?, sorted dead nouns). Flag when >=2 dead, or >=50% dead of >=2 total."""
    dead = sorted(n for n in nouns if n not in repo_tokens)
    flag = len(dead) >= 2 or (len(nouns) >= 2 and len(dead) / len(nouns) >= 0.5)
    return flag, dead


@dataclass
class StaleFinding:
    path: str
    kind: str
    pooled: bool
    n_nouns: int
    dead: list[str]
    verdict: str  # "fresh" | "stale-suspect"


def _collect_pool_blocks(claude: Path) -> list[Block]:
    """Blocks parked under tools-pool/ (invisible to Claude Code, but can still rot)."""
    blocks: list[Block] = []
    pool = claude / "tools-pool"
    if not pool.is_dir():
        return blocks
    for md in sorted(pool.glob("skills/*/*/SKILL.md")):
        text = md.read_text(encoding="utf-8")
        fm = parse_front_matter(text) or {}
        blocks.append(Block("skill", fm.get("name", md.parent.name) or md.parent.name,
                            fm.get("description", ""), _strip_front_matter(text), None, str(md)))
    for f in sorted(pool.glob("commands/*/*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_front_matter(text) or {}
        blocks.append(Block("command", f.stem, fm.get("description", ""),
                            _strip_front_matter(text), None, str(f)))
    for f in sorted(pool.glob("agents/*/*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_front_matter(text) or {}
        blocks.append(Block("agent", fm.get("name", f.stem) or f.stem, fm.get("description", ""),
                            _strip_front_matter(text), fm.get("tools"), str(f)))
    return blocks


def stale(root: Path, repo_path: str) -> tuple[list[StaleFinding], str]:
    """Scan every block (active + pooled) for identifiers absent from the target repo."""
    claude = root / ".claude" if (root / ".claude").is_dir() else root
    repo = Path(repo_path)
    if not repo.is_dir():
        return [], f"repo path not found: {repo_path}"
    repo_tokens = _repo_token_index(repo)
    active = _collect_blocks(claude)
    pooled = _collect_pool_blocks(claude)
    findings: list[StaleFinding] = []
    for blocks, is_pooled in ((active, False), (pooled, True)):
        for b in blocks:
            nouns = _identifier_nouns(b.description + "\n" + b.body)
            flag, dead = _is_stale(nouns, repo_tokens)
            findings.append(StaleFinding(b.path, b.kind, is_pooled, len(nouns), dead,
                                         "stale-suspect" if flag else "fresh"))
    return findings, ""


def print_stale(root: Path, findings: list[StaleFinding], err: str) -> None:
    if err:
        print(f"[STALE] {root}: {err}")
        return
    suspects = [f for f in findings if f.verdict == "stale-suspect"]
    print(f"[STALE] {root}: {len(suspects)}/{len(findings)} block(s) stale-suspect")
    for f in findings:
        if f.verdict != "stale-suspect":
            continue
        tag = "stale-suspect (pooled)" if f.pooled else "stale-suspect"
        ex = ", ".join(f.dead[:4]) + ("…" if len(f.dead) > 4 else "")
        print(f"  [{tag}] {f.path}: {len(f.dead)}/{f.n_nouns} cited identifiers not found in repo ({ex})")
    print("  (advisory; identifier-grep only — the analyzer judges prose-concept drift)")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate, score, route-test, stale-check, or ablate Claude Code (.claude/) setups.")
    p.add_argument("roots", nargs="+", help="setup root(s) (folder containing .claude/, or a .claude/ itself)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--strict", action="store_true", help="validate: treat warnings as failures")
    p.add_argument("--score", action="store_true", help="Layer 1: static effectiveness audit (advisory)")
    p.add_argument("--min-score", type=int, default=None, help="--score: exit 1 if composite < N")
    p.add_argument("--route", action="store_true", help="Layer 2: routing tests (evals/<repo>/routing-tests.json)")
    p.add_argument("--route-tests", help="explicit path to a routing-tests.json")
    p.add_argument("--stale", action="store_true", help="Layer 1b: flag blocks citing identifiers absent from --repo (advisory)")
    p.add_argument("--repo", help="--stale: path to the real target repo the setup serves")
    p.add_argument("--ablate", action="store_true", help="Layer 3: ablation — defaults to a free dry-run preview (see tools/_ablation.py)")
    p.add_argument("--execute", action="store_true", help="--ablate: actually launch the agent runs (costs compute)")
    p.add_argument("--tasks", help="--ablate: explicit path to a tasks.json")
    p.add_argument("--repeats", type=int, default=3, help="--ablate: runs per (condition, task) to fight noise")
    args = p.parse_args(argv)

    # Layer 3 — ablation (delegated to the heavy, agent-running module).
    if args.ablate:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import _ablation  # noqa: E402  (local module, only needed for this mode)
        return _ablation.run_ablation(Path(args.roots[0]), args.tasks, args.repeats,
                                      dry_run=not args.execute, as_json=args.json)

    # Layer 1b — staleness (block identifiers vs. the real repo). Advisory; exit 0.
    if args.stale:
        if not args.repo:
            print("--stale requires --repo <path-to-target-repo>", file=sys.stderr)
            return 2
        results = [(r, *stale(Path(r), args.repo)) for r in args.roots]
        if args.json:
            print(json.dumps([
                {"root": str(r), "error": err,
                 "findings": [vars(f) for f in findings]}
                for r, findings, err in results], indent=2))
        else:
            for i, (r, findings, err) in enumerate(results):
                if i:
                    print()
                print_stale(Path(r), findings, err)
        return 0

    # Layer 2 — routing tests.
    if args.route:
        results = [route(Path(r), args.route_tests) for r in args.roots]
        if args.json:
            print(json.dumps([{"root": str(r), "passed": pa, "total": to}
                              for (pa, to, _), r in zip(results, args.roots)], indent=2))
        else:
            for i, (_, _, lines) in enumerate(results):
                if i:
                    print()
                print("\n".join(lines))
        return 1 if any(pa < to for pa, to, _ in results) else 0

    # Layer 1 — effectiveness audit.
    if args.score:
        audits = [audit(Path(r)) for r in args.roots]
        if args.json:
            print(json.dumps([_audit_to_dict(a) for a in audits], indent=2))
        else:
            for i, a in enumerate(audits):
                if i:
                    print()
                print_audit(a)
        if args.min_score is not None:
            return 1 if any((not a.skipped and not a.error and a.score < args.min_score) for a in audits) else 0
        return 0

    # Default — structural validity gate (unchanged; the only mode that gates CI).
    reports = [validate(Path(r)) for r in args.roots]
    if args.json:
        print(json.dumps(
            [
                {
                    "root": r.root,
                    "skipped": r.skipped,
                    "counts": r.counts,
                    "errors": r.n_errors,
                    "warnings": r.n_warnings,
                    "issues": [vars(i) for i in r.issues],
                }
                for r in reports
            ],
            indent=2,
        ))
    else:
        for i, r in enumerate(reports):
            if i:
                print()
            print_human(r)

    failed = any(r.n_errors or (args.strict and r.n_warnings) for r in reports)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
