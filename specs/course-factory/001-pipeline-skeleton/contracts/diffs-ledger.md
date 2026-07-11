# Contract — `DIFFS.md` forward-diff ledger

**Owner:** spec 001 (FR-023/027). **Consumers:** 002, 003, 004 — every downstream reader of a gated
artifact MUST read the frozen artifact **together with** its `DIFFS.md` entries, never the frozen
artifact alone once a diff exists against it.

## Purpose

Gated phases are immutable once passed (FR-023). When the author later requests a change that belongs
to an already-gated earlier artifact, the change is **not** applied by re-opening that phase; it is
applied as an explicit forward diff at the *current* phase and **logged here**. `DIFFS.md` is the
canonical record of every post-freeze change — the audit trail that keeps the pipeline forward-only
(SC-010).

## File shape

- Created as an **empty stub** at instantiation (FR-008).
- **Append-only**, chronological. `diffs.py` only appends; existing entries are **never** edited or
  reordered (FR-027).
- One entry per applied forward diff.

### Entry schema

```markdown
## [YYYY-MM-DDThh:mm:ssZ] <target phase or artifact>
- **What changed:** <the concrete change>
- **Why:** <the reason / what gap it fills>
- **Applied at phase:** <current_phase when the diff was applied>
```

| Field | Meaning |
| :--- | :--- |
| timestamp | ISO-8601 UTC; entries are in applied order. |
| target phase/artifact | The gated artifact the change logically belongs to (e.g. `syllabus` / `SYLLABUS.md`). |
| what changed | The concrete delta. |
| why | The reason / the gap it fills. |
| applied at phase | The `current_phase` at which the diff was actually applied (always ≥ the target phase — forward-only). |

## Read rule for consumers

When a consumer (002/003/004) loads a gated artifact, it MUST also load `DIFFS.md` and apply/read any
entries whose target is that artifact. "Frozen artifact + its `DIFFS.md` entries" is the single
canonical view — reading the frozen artifact alone once a diff exists against it is a contract
violation.
