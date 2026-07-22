# Contract — `FEEDBACK.md` → `insights/` harvest

**Owner:** spec 004 (FR-014–017) owns **producing/maintaining** `insights/`. **Read side** (not this
contract): intake (001 FR-025), syllabus compose (002 FR-016), drafting (003). **Homes:**
`course-factory/.claude/commands/{insight-capture,harvest-feedback}.md` (factory-level) +
`course-factory/insights/` (the digest) + `course-factory/tools/harvest.py` (append mechanics).

## The digest — `insights/`

- **Form:** a small set of **topic-organized** `.md` files (one per recurring theme —
  anti-fabrication, running-example design, estimation method, kata design, mirroring the categories
  `DESIGN.md` names). Each entry is **dated** and **sourced** to the course it was harvested from.
- **Directory-shaped, not one monolith** — so each harvest is a small diff and append-only is natural.
- **Starts empty** — no corpus seeded from the reference course (Principle XII). An **empty digest is
  valid input** everywhere it is read.
- Readers (001/002/003) load the whole directory as **one digest**.

## Two user-invoked paths (FR-015) — and ONLY these

1. **`/insight-capture`** — a user-triggered **per-insight capture**: log a single insight to
   `insights/<theme>.md` on demand, independent of any bulk harvest.
2. **`/harvest-feedback <course>`** — a `setup-retro`-style **bulk harvest**: distill a course's
   `FEEDBACK.md` critiques (agent judgment — distilled, not verbatim) and append them via
   `harvest.py`.

**No third path.** There is **no automatic or scheduled trigger** (FR-016, SC-007): nothing in 001's
orchestration, no phase transition, no course-completion event invokes the harvest. "User-invoked
only" is guaranteed by **construction** — the harvest has no non-user caller (R6).

## Append mechanics (`harvest.py`) — the mechanical guarantees

| Rule | Behavior |
| :--- | :--- |
| **Append-only** | Never overwrite an existing course's insights; new files or append-only sections keyed by `source_course` + `date`. **0 clobbered** (SC-007). |
| **Empty = no-op** | An empty `FEEDBACK.md` harvests as a **no-op, not an error** (FR-017, SC-007). |
| **Represented** | Every critique in a non-empty `FEEDBACK.md` is **represented** in `insights/` (distilled, not necessarily verbatim) — **0 silently dropped** (SC-007). |
| **Dedupe-safe** | Re-harvesting the same course does not duplicate already-captured insights. |

## What this contract does NOT do

- It does **not** write `FEEDBACK.md` — that is the build-time critique write side (001 gate-event
  comments FR-026; 003 evaluator critiques FR-020). 004 **reads** `FEEDBACK.md` and harvests up.
- It does **not** merge with `COURSE_REPORT.md` (distinct purpose — `course-report.md` contract).

## SC mapping

SC-007 (every critique represented; append-only; 0 clobbered; 0 errors on empty; 0 automatic triggers).
