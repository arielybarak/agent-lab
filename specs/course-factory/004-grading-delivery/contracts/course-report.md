# Contract — `COURSE_REPORT.md` + the `/course-report` command

**Owner:** spec 004 (FR-011/012/013) owns the report's **generation + contents**. **Home:**
`course-factory/course-template/.claude/commands/course-report.md` — a **mandatory-core** frozen
template command (constitution IX), inherited by every course. **Coordinates with:** 001's
`course-folder.md` (001 invokes `/course-report` at the delivery terminal state and owns the folder
contract; 004 owns what the report *says*).

## Output file

`courses/<name>/COURSE_REPORT.md` — the delivered **quality report** to the user, generated from the
course-evaluator's `Scorecard`.

## Required contents (SC-005)

| Section | Source | Rule |
| :--- | :--- | :--- |
| **Rubric scores** | `Scorecard.per_dimension` | per-dimension scores (core + requested add-ons) |
| **Verdict** | `Scorecard.verdict` | `pass` \| `needs-work` — stated plainly |
| **Wins** | `Scorecard.wins` | what the course does well |
| **Cleanups** | `Scorecard.cleanups` | ranked improvements (weights inform ranking) |
| **Traceability** | `Scorecard.traceability` | any unresolvable `[Sn]` findings (may be empty) |
| **Rubric version** | `Scorecard.rubric_version` | the template `VERSION` that graded the course (FR-005/013) — makes the grade reproducible/re-syncable |

## Delivery-gate semantics (the crucial rule)

- The delivery gate is the report's **generation**, **not** a passing verdict (constitution VI
  Delivery row; 001 FR-011/021). A **`needs-work`** report is **delivered as-is** — never withheld,
  never blocked (FR-011).
- A `needs-work` verdict's gaps feed the `/improve-course` backlog / a forward diff (FR-010), they do
  **not** gate delivery and do **not** re-open a passed phase (SC-006).
- 001 treats the **presence** of `COURSE_REPORT.md`, not its verdict, as satisfying the delivery gate
  (001's `course-folder.md`).

## Distinct from `FEEDBACK.md` (FR-012)

| | `COURSE_REPORT.md` | `FEEDBACK.md` |
| :--- | :--- | :--- |
| Audience | the **user** | the **factory** |
| Purpose | reports the course's **graded quality** | feeds improvement back (→ harvested to `insights/`) |
| Written by | `/course-report` (this contract) | build-time critiques (001/003 write side) + 004's harvest read side |

The two MUST NOT be merged (SC-005).

## SC mapping

SC-005 (100% of delivered courses carry a `COURSE_REPORT.md` with scores + verdict + rubric version,
distinct from `FEEDBACK.md`).
