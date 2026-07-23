#!/usr/bin/env python3
"""Instantiation — copy the frozen course-template into a new course folder (001 FR-001/006/007/008).

Two halves, in order:
  1. Validate the frozen template (VERSION + manifest.yaml) and the already-authored
     COURSE_BRIEF.md for completeness — halt on either defect, writing no partial folder.
  2. Copy-never-mutate: copy exactly the manifest's core + selected-profile + enabled-module
     paths into `courses/<slug>/`, stamp the template version, initialize BUILD_PROGRESS.md at
     syllabus start (via progress.py), and create the SOURCES.md/FEEDBACK.md/DIFFS.md stubs.

`COURSE_BRIEF.md`'s on-disk shape: intake (the agent-driven `.claude/` command, not this tool)
authors a Markdown file containing exactly one fenced ```json block with the structured fields
below — the same "human prose + one machine block" convention BUILD_PROGRESS.md uses (research
R3), reused here so this stdlib-only tool never needs a YAML/frontmatter parser for a second format:

    {
      "topic_scope": {"topic": "...", "in_scope": [...], "out_of_scope": [...]},
      "audience": {"description": "...", "prior_knowledge": "..."},
      "running_example": "...",
      "source_pointers": ["...", ...],
      "archetype_profile": "default",
      "modules": {"<module-name>": true/false, ...},
      "lesson_format": null
    }

`archetype_profile` and `modules` MUST already be resolved and explicit by the time intake writes
the brief (FR-005's default-fallback is intake's job); this tool validates presence and validity
against the template's manifest, it never invents a value (Principle II / FR-003).

The manifest (`manifest.yaml`) is parsed with a small stdlib indentation parser, not PyYAML — the
repo convention is stdlib-only, and the manifest's shape is fixed by
specs/course-factory/000-course-template/contracts/template-manifest.md. See `parse_manifest()`.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import progress  # noqa: E402  (local import after sys.path setup)

_JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)
_SLUG_RE = re.compile(r"[^a-z0-9]+")


class TemplateError(Exception):
    """The frozen template is absent, unversioned, or malformed (FR-001, SC-009)."""


class BriefError(Exception):
    """COURSE_BRIEF.md is missing a required field — a blocking condition, never fabricated
    (FR-003, SC-001/002)."""


class CourseNameCollisionError(Exception):
    """The resolved course name was claimed by another process between collision-check and
    rename — narrows (does not eliminate) a TOCTOU window; safe to retry (spec Assumptions:
    collisions are suffixed, never overwritten)."""


# --------------------------------------------------------------------------------------------
# Manifest parsing — a small stdlib indentation parser, not a YAML dependency (see module docstring)
# --------------------------------------------------------------------------------------------

def _parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return None
    if raw == "[]":
        return []
    if raw.lower() in ("true", "false"):
        return raw.lower() == "true"
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    return raw


def parse_manifest(text: str) -> dict[str, Any]:
    """Parse manifest.yaml's fixed, small schema (version / core / profiles / modules) — 2-space
    indentation, no anchors, no flow mappings, no multi-line scalars (contracts/template-manifest.md)."""
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        stripped = raw.split("#", 1)[0].rstrip()
        if stripped.strip():
            indent = len(stripped) - len(stripped.lstrip(" "))
            lines.append((indent, stripped.strip()))

    pos = 0

    def parse_block(indent: int) -> Any:
        nonlocal pos
        if pos < len(lines) and lines[pos][0] == indent and lines[pos][1].startswith("- "):
            result: list[Any] = []
            while pos < len(lines) and lines[pos][0] == indent and lines[pos][1].startswith("- "):
                result.append(_parse_scalar(lines[pos][1][2:]))
                pos += 1
            return result

        result: dict[str, Any] = {}
        while pos < len(lines) and lines[pos][0] == indent:
            content = lines[pos][1]
            if ":" not in content:
                raise TemplateError(f"malformed manifest line: {content!r}")
            key, _, rest = content.partition(":")
            key, rest = key.strip(), rest.strip()
            pos += 1
            if rest:
                result[key] = _parse_scalar(rest)
            elif pos < len(lines) and lines[pos][0] > indent:
                result[key] = parse_block(lines[pos][0])
            else:
                result[key] = None
        return result

    return parse_block(0)


def read_template(template_dir: Path) -> tuple[str, dict[str, Any]]:
    """Validate the frozen template exists and is versioned. Returns (version, manifest)."""
    version_path = template_dir / "VERSION"
    manifest_path = template_dir / "manifest.yaml"
    if not version_path.is_file():
        raise TemplateError(f"template has no VERSION file: {template_dir}")
    if not manifest_path.is_file():
        raise TemplateError(f"template has no manifest.yaml: {template_dir}")

    version = version_path.read_text(encoding="utf-8").strip()
    if not version:
        raise TemplateError(f"template VERSION is empty: {version_path}")

    manifest = parse_manifest(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != version:
        raise TemplateError(
            f"manifest version {manifest.get('version')!r} != VERSION file {version!r} — "
            "unversioned/inconsistent template (FR-001)"
        )

    profiles = manifest.get("profiles") or {}
    defaults = [name for name, p in profiles.items() if p.get("default")]
    if len(defaults) != 1:
        raise TemplateError(f"template must have exactly one default:true profile, found {defaults}")

    return version, manifest


# --------------------------------------------------------------------------------------------
# Brief validation — the mechanical anti-fabrication backstop (FR-003, SC-001/002)
# --------------------------------------------------------------------------------------------

def parse_brief(text: str) -> dict[str, Any]:
    matches = _JSON_BLOCK_RE.findall(text)
    if len(matches) != 1:
        raise BriefError(f"COURSE_BRIEF.md must contain exactly one fenced json block, found {len(matches)}")
    try:
        return json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise BriefError(f"corrupt json block in COURSE_BRIEF.md: {exc}") from exc


def validate_brief(brief: dict[str, Any], manifest: dict[str, Any]) -> None:
    """Halt on any missing required field — never fabricate a default (FR-003, SC-001/002)."""

    def require(condition: bool, message: str) -> None:
        if not condition:
            raise BriefError(message)

    topic_scope = brief.get("topic_scope") or {}
    require(bool(topic_scope.get("topic")), "COURSE_BRIEF.md is missing topic_scope.topic")
    require("in_scope" in topic_scope, "COURSE_BRIEF.md is missing topic_scope.in_scope")
    require("out_of_scope" in topic_scope, "COURSE_BRIEF.md is missing topic_scope.out_of_scope")

    audience = brief.get("audience") or {}
    require(bool(audience.get("description")), "COURSE_BRIEF.md is missing audience.description")
    require(bool(audience.get("prior_knowledge")), "COURSE_BRIEF.md is missing audience.prior_knowledge")

    require(bool(brief.get("running_example")), "COURSE_BRIEF.md is missing the required running_example")
    require(bool(brief.get("source_pointers")), "COURSE_BRIEF.md is missing source_pointers")

    profile = brief.get("archetype_profile")
    require(bool(profile), "COURSE_BRIEF.md is missing archetype_profile")
    require(
        profile in (manifest.get("profiles") or {}),
        f"COURSE_BRIEF.md names archetype_profile {profile!r}, not one of the template's profiles",
    )

    modules = brief.get("modules")
    require(isinstance(modules, dict), "COURSE_BRIEF.md is missing an explicit modules selection")
    template_modules = set((manifest.get("modules") or {}).keys())
    missing_modules = template_modules - modules.keys()
    require(
        not missing_modules,
        f"COURSE_BRIEF.md's modules selection omits: {sorted(missing_modules)} — every template "
        "module needs an explicit enabled/disabled entry (FR-005)",
    )
    unknown_modules = modules.keys() - template_modules
    require(
        not unknown_modules,
        f"COURSE_BRIEF.md's modules selection names {sorted(unknown_modules)}, which the template "
        "doesn't offer — a typo'd module name would otherwise silently enable nothing (FR-005)",
    )


# --------------------------------------------------------------------------------------------
# Course naming (spec Assumptions: slug of the title, collisions suffixed never overwritten)
# --------------------------------------------------------------------------------------------

def slugify(text: str) -> str:
    slug = _SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return slug or "course"


def derive_course_title(spec_path: Path | None, brief: dict[str, Any]) -> str:
    if spec_path and spec_path.is_file():
        for line in spec_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                # templates/COURSE_SPEC.template.md's H1 is "Course Spec: <title>" — take the part
                # after the label, since the label itself isn't part of the course's name.
                if ":" in title:
                    title = title.split(":", 1)[1].strip()
                return title
    topic = (brief.get("topic_scope") or {}).get("topic")
    if topic:
        return topic
    raise BriefError("cannot derive a course name: no spec title and no topic_scope.topic")


def resolve_course_name(title: str, courses_dir: Path) -> str:
    base = slugify(title)
    candidate = base
    n = 2
    while (courses_dir / candidate).exists():
        candidate = f"{base}-{n}"
        n += 1
    return candidate


# --------------------------------------------------------------------------------------------
# Copy set — core + selected profile's pieces + enabled modules' pieces (FR-006)
# --------------------------------------------------------------------------------------------

def collect_copy_paths(manifest: dict[str, Any], profile: str, modules: dict[str, bool]) -> list[str]:
    paths = list(manifest.get("core") or [])
    profile_def = (manifest.get("profiles") or {}).get(profile) or {}
    paths += list(profile_def.get("pieces") or [])
    for name, enabled in modules.items():
        if enabled:
            module_def = (manifest.get("modules") or {}).get(name) or {}
            paths += list(module_def.get("pieces") or [])
    return paths


STUB_ARTIFACTS = {
    "SOURCES.md": "# Sources\n\n_Populated during the syllabus phase (spec 002)._\n",
    "FEEDBACK.md": "# Feedback\n\n_Gate-event author feedback accumulates here during the build "
                   "(FR-026) and is harvested into `insights/` on request (spec 004)._\n",
    "DIFFS.md": "# Forward-Diff Ledger\n\n_Append-only (FR-027) — a change to an already-gated "
                "artifact is logged here, never applied by re-opening the phase._\n",
}


def instantiate(*, spec: Path | None, template: Path, brief: Path, courses_dir: Path) -> Path:
    """Run the full instantiation. Raises TemplateError/BriefError and writes nothing on any
    halt — the folder is assembled in a staging dir and only moved into place on full success."""
    version, manifest = read_template(template)

    brief_text = brief.read_text(encoding="utf-8")
    brief_fields = parse_brief(brief_text)
    validate_brief(brief_fields, manifest)

    title = derive_course_title(spec, brief_fields)
    courses_dir.mkdir(parents=True, exist_ok=True)
    course_name = resolve_course_name(title, courses_dir)

    copy_paths = collect_copy_paths(manifest, brief_fields["archetype_profile"], brief_fields["modules"])

    staging = Path(tempfile.mkdtemp(prefix=".instantiate-", dir=courses_dir))
    try:
        for rel in copy_paths:
            src = template / rel
            if not src.is_file():
                raise TemplateError(f"manifest lists a path that does not exist: {rel}")
            dst = staging / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)

        (staging / "COURSE_BRIEF.md").write_text(brief_text, encoding="utf-8")
        for name, content in STUB_ARTIFACTS.items():
            (staging / name).write_text(content, encoding="utf-8")

        state = progress.init_state(course_name, version)
        progress.write_state(staging / "BUILD_PROGRESS.md", state)

        final = courses_dir / course_name
        if final.exists():
            # Narrows, rather than eliminates, the TOCTOU window opened by resolve_course_name()'s
            # earlier existence check — another process claimed this name while this one was
            # copying. Never overwrite (spec Assumptions); the caller may retry.
            raise CourseNameCollisionError(f"{final} was created by another process during instantiation")
        staging.rename(final)
        return final
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise


# --------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", type=Path, default=None, help="COURSE_SPEC.md (for the title/slug)")
    parser.add_argument("--template", type=Path, required=True, help="frozen course-template/ root")
    parser.add_argument("--brief", type=Path, required=True, help="the intake-authored COURSE_BRIEF.md")
    parser.add_argument("--courses-dir", type=Path, required=True, help="staging dir for courses/<name>/")
    args = parser.parse_args(argv)

    try:
        course_dir = instantiate(
            spec=args.spec, template=args.template, brief=args.brief, courses_dir=args.courses_dir
        )
    except (TemplateError, BriefError, CourseNameCollisionError, progress.IntegrityError) as exc:
        print(f"instantiate: halted — {exc}", file=sys.stderr)
        return 1

    print(f"instantiated: {course_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
