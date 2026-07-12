# Contract: Version Stamp (`VERSION`) + Drift Check

**Producer**: spec 000. **Consumers**: spec 001 (records the stamp at copy time, drift-checks on
resume — 001 FR-001/007), spec 004 (the rubric shares this identity — 004 FR-005). This is the
anchor for "the template is a frozen, versioned snapshot" (FR-016/017, Principle V).

## Location & format

`course-factory/course-template/VERSION` — a single line, `MAJOR.MINOR.PATCH` (semver, D3).

```
1.0.0
```

## Bump semantics

| Change to the template | Bump | Why |
| :--- | :--- | :--- |
| Full re-distillation (re-run FR-002 filter over the whole reference `.claude/`) | **MAJOR** | New snapshot of the whole asset. |
| Rubric-only re-stamp adopted from a `comparison/` proposal (Edge Cases, 004 FR-018/019) | **MINOR** or **PATCH** | Narrow: does NOT re-run the full critical-thinking filter; provenance points to the `comparison/` proposal, not the reference course. |
| No content change | none | Stamp is stable; the template is byte-frozen between distillations (US2 AC-4). |

## One identity, not two

The `VERSION` value **is** the rubric asset's version identity (FR-016 ↔ 004 FR-005). The factory
maintains **one** counter across the template and its rubric — never two independent version numbers.
A rubric revision bumps this same file.

## Drift check (the seam 001 tests)

1. At copy time, 001 records the current `VERSION` into the course (e.g. in `BUILD_PROGRESS.md` /
   the stamped overlay).
2. On resume, 001 compares the recorded stamp against the template's current `VERSION`.
3. **Mismatch MUST be detectable 100% of the time** (SC-006) — a recorded `1.0.0` against a template
   now at `1.1.0` (or `2.0.0`) flags drift, prompting a manual re-sync (re-copy + reapply overlay).

## Simulation for this spec's own acceptance

Per US2 Independent Test: record a stamp, bump `VERSION`, confirm the comparison flags the mismatch.
No running pipeline needed — a string compare of recorded-vs-current is the whole check.

## Out of scope

The re-sync *mechanism* (pulling template improvements into already-built courses) is a later manual
step owned by 001's Assumptions, not this spec.
