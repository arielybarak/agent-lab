# course-factory/tools/ — the deterministic layer

Stdlib-only Python (repo convention: no third-party deps, pytest for tests). These are the
**correctness-critical mechanical operations** spec 001 ships as scripts rather than agent
discipline, so the spec's hard-zero Success Criteria (SC-003/004/006/008/009/010/012) are true by
construction and `pytest`-assertable with no agent in the loop (`specs/course-factory/
001-pipeline-skeleton/research.md` R1). The judgment work — the intake interview, brief authoring,
orchestration narrative — lives in `course-factory/.claude/` and calls these.

## `progress.py` — the `BUILD_PROGRESS.md` state core

**Guarantees:** legal-transition-only phase advancement (no skip, no re-open, matched
`gate_type`), a pure round-cap accounting for the capped skeleton/lesson refine loop, a minimal
lock (refuses a live holder, allows a stale reclaim), and an integrity halt on any missing/corrupt/
inconsistent state or a `template_version` drift. Schema: `specs/course-factory/
001-pipeline-skeleton/contracts/build-progress-schema.md`.

**Called by:** `/course-instantiate` (init), `/course-build` (everything else), `/course-status`
(read-only `show`/`resume`).

```bash
python3 tools/progress.py init <course_dir> <name> <template_version>
python3 tools/progress.py show <course_dir>
python3 tools/progress.py resume <course_dir> [--template-version X]
python3 tools/progress.py transition <course_dir> {pass|needs-user|loop|failed}
python3 tools/progress.py accept-round-cap <course_dir>       # settle a capped refine cycle as-is
python3 tools/progress.py extend-round-cap <course_dir>       # grant exactly one more pass
python3 tools/progress.py clear-active-loop <course_dir>       # settle an early (under-cap) pass
python3 tools/progress.py set-lesson-status <course_dir> <lesson_id> {not-started|in-progress|passed|accepted-at-cap}
python3 tools/progress.py seed-lessons <course_dir> <syllabus_path>   # populate lessons[] from a frozen SYLLABUS.md
python3 tools/progress.py set-syllabus-subphase <course_dir> {research-in-progress|research-done|composed|presented}
python3 tools/progress.py lock-acquire <course_dir> [--holder TOKEN]
python3 tools/progress.py lock-refresh <course_dir> --holder TOKEN   # NOT lock-acquire — see below
python3 tools/progress.py lock-release <course_dir>
```

**Design notes worth knowing before touching this file:**

- **A refine cycle settling is never a phase clearing.** `loop`/`clear-active-loop`/
  `accept-round-cap`/`extend-round-cap` only ever touch `active_loop` — none of them advance
  `current_phase`. Only an explicit `transition ... pass` does. This is what lets `skeletons` (one
  round-cap cycle, then a *separate* blocking scan, FR-024) and `lessons` (**several** round-cap
  cycles, one per lesson, before the phase itself is done) share the same mechanism without either
  auto-advancing early — see `.claude/skills/phase-stubs/SKILL.md` for the full per-phase sequencing
  the orchestrator follows.
- **The lock uses one enforced threshold, not two.** FR-028 names both a short "liveness window"
  and a "generous" stale timeout. At MVP only `LOCK_STALE_SECONDS` (30 min) actually gates
  refuse-vs-reclaim; `LOCK_LIVENESS_SECONDS` (5 min) documents the *expected* refresh cadence of a
  live session but isn't a second hard gate. There's no specified behavior for the gap between the
  two windows in the spec, so refusing until the stale timeout (rather than adding a third,
  undefined state) is the simpler, safer default — revisit only if real runs show it's wrong.
- **`lock-refresh` ≠ `lock-acquire`.** The driver's per-invocation holder token must call
  `lock-refresh` after every persisted unit, not re-run `lock-acquire` — the latter resets
  `acquired_at` on every call (it's meant for a *new* invocation claiming the lock), which would
  erase the audit trail of when this invocation actually started holding the build.
- **`BUILD_PROGRESS.md` is Markdown wrapping exactly one fenced ` ```json ` block** (research R3);
  the prose around it is regenerated on every write and is never authoritative.
- **`lessons[]` is seeded from the frozen `SYLLABUS.md`, not hand-listed.** `parse_syllabus_lessons()`
  reads the syllabus's own fenced json block (`{"lessons": [{"id": ..., "title": ...}, ...]}`) and
  `seed_lessons()` idempotently populates `lessons[]` from it — this is the link between "the
  syllabus gate cleared" and "the skeleton/lesson phases know what to work," and it's what a real
  build must call (the driver, right after the syllabus `pass`) instead of inventing lesson ids.
- **`syllabus_subphase` is validated against its own fixed enum**, not left open for 002 to invent
  later — `contracts/build-progress-schema.md` already names the four values; `set_syllabus_subphase()`
  is 002's only sanctioned way to write it, and it's cleared back to null the moment the syllabus
  phase itself clears (so it never lingers stale into a later phase).

## `instantiate.py` — copy-never-mutate + overlay + version stamp

**Guarantees:** halts (writing nothing) on an absent/unversioned/inconsistent template, or on a
`COURSE_BRIEF.md` missing any required field or an explicit per-module enabled/disabled entry —
never fabricates a default (FR-003). On success, the source template is byte-for-byte unchanged
(builds in a staging dir, renames into place only on full success) and the new `courses/<name>/`
carries exactly core + the selected profile's pieces + enabled modules' pieces, `COURSE_BRIEF.md`,
`BUILD_PROGRESS.md` (at syllabus start), and the `SOURCES.md`/`FEEDBACK.md`/`DIFFS.md` stubs.

**Called by:** `/course-instantiate`.

```bash
python3 tools/instantiate.py --spec <COURSE_SPEC.md> --template <template dir> \
    --brief <COURSE_BRIEF.md> --courses-dir <staging dir>
```

**Design notes:**

- **`manifest.yaml` is parsed with a small stdlib indentation parser** (`parse_manifest`), not
  PyYAML — matches the repo's stdlib-only convention and mirrors spec 000's own
  `neutrality_scan.py::load_tiers`. The manifest's shape is fixed by `specs/course-factory/
  000-course-template/contracts/template-manifest.md`; if that shape ever grows real YAML features
  (anchors, flow mappings, multi-line scalars), this parser needs to grow with it or be replaced.
- **`COURSE_BRIEF.md`'s on-disk shape is a design decision made here, not in the published data
  model:** human prose + exactly one fenced ` ```json ` block, the same convention
  `BUILD_PROGRESS.md` uses (research R3) — chosen so this stdlib-only tool never needs a second
  ad hoc parser. See the field list in `instantiate.py`'s module docstring.
- **`archetype_profile`/`modules` must already be resolved and explicit** by the time
  `COURSE_BRIEF.md` is written — FR-005's default-fallback is intake's job (`intake-interviewer`
  recommends, `/course-intake` confirms with the author); this tool only validates presence and
  validity against the manifest, it never invents a value.

## `diffs.py` — the append-only `DIFFS.md` ledger

**Guarantees:** only appends; never rewrites or reorders an existing entry (FR-027). Schema:
`specs/course-factory/001-pipeline-skeleton/contracts/diffs-ledger.md`.

**Called by:** `/course-build`, whenever a forward diff is applied under FR-023.

```bash
python3 tools/diffs.py <course_dir>/DIFFS.md --target <phase/artifact> \
    --what-changed "<delta>" --why "<reason>" --applied-at-phase <current_phase>
```

## `deliver_check.py` — the required-artifact-presence check

**Guarantees:** delivery's required set (`contracts/course-folder.md`) is fully present, including
one file per non-terminal-excluded lesson under `lessons/<id>.{md,ipynb}`. Never grades content —
`COURSE_REPORT.md`'s **presence**, any verdict, is what the pipeline gate itself cares about
(FR-011/021); this script is a sanity check the orchestrator runs after `deliver` clears, not the
gate itself.

**Called by:** `/course-build`, after the `deliver` phase's `transition ... pass`.

```bash
python3 tools/deliver_check.py <course_dir>
```

**Design note:** the lesson-file location (`lessons/<id>.md`/`.ipynb`) is 001's own placeholder
convention for its stub handlers — the real `.md` vs `.ipynb` decision belongs to spec 002
(written into `COURSE_BRIEF.md.lesson_format`); if 002/003 pick a different layout, update
`REQUIRED_FILES`/the lesson-file check here to match.

## `neutrality_scan.py` — spec 000's core-neutrality gate

Owned by spec 000 (`course-template/`'s distillation), not 001 — kept here because it operates on
the same `course-template/` tree 001's tools read. See its own module docstring; briefly: scans
every path `manifest.yaml` marks `core` against `neutrality-terms.txt` and fails if the mandatory
core carries subject-specific wording (000 FR-020/SC-002). `python3 tools/neutrality_scan.py`.

## Running the tests

```bash
python3 -m pytest course-factory/tests/ -q
```
