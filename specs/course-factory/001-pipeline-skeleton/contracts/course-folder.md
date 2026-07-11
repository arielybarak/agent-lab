# Contract — course folder & required delivery artifacts

**Owner:** spec 001 (FR-006/008/020). Defines what `courses/<name>/` contains at instantiation and
what MUST be present for the delivery gate. `deliver_check.py` enforces the delivery set (SC-008).

## At instantiation (FR-006/007/008)

`course-instantiate` copies the frozen `course-template/` into `courses/<name>/` and, **honoring the
selected archetype profile** and enabled modules, produces:

```text
courses/<name>/
├── .claude/            # copied verbatim from course-template/.claude/ (the frozen residue — NOT the factory's own .claude/)
├── COURSE_BRIEF.md     # the overlay authored by intake (FR-004) — profile + modules recorded here
├── BUILD_PROGRESS.md   # initialized at the START of the syllabus phase (FR-008)
├── SOURCES.md          # stub, populated by 002
├── FEEDBACK.md         # empty, written during the build (FR-026 / 003) and harvested by 004
└── DIFFS.md            # empty forward-diff ledger stub (FR-027)
```

Invariants:
- The source `course-template/` is **byte-for-byte unchanged** afterward (FR-007, SC-003).
- The copied template version is **stamped** into `BUILD_PROGRESS.md.template_version` (FR-006).
- The overlay reflects exactly one `archetype_profile` and the explicit `modules` selection (FR-005).
- If the template is **absent or unversioned**, instantiation **halts** and writes **no partial
  folder** (FR-001, edge case, SC-009).
- Course-name collisions are suffixed, never overwritten (spec Assumptions).

## At delivery (FR-020, SC-008)

The delivery gate requires the full per-course set present:

| Artifact | Produced by | Notes |
| :--- | :--- | :--- |
| `COURSE_BRIEF.md` | 001 intake | the overlay |
| `SOURCES.md` | 002 | grounding store (populated) |
| `BUILD_PROGRESS.md` | 001 | state (at `done`) |
| `DIFFS.md` | 001 | forward-diff ledger (may be empty) |
| `FEEDBACK.md` | 001 / 003 | critiques (may be empty) |
| `SYLLABUS.md` | 002 | the frozen approved syllabus — course content |
| lesson files | 003 | `.md`/`.ipynb` per 002's format decision — course content |
| `COURSE_REPORT.md` | 004 | graded scorecard; **presence** clears the gate, **any** verdict (FR-011/021) |
| `.claude/` | 001 copy | the frozen template residue |

`deliver_check.py` fails delivery if any required artifact is missing. A "needs work" verdict in
`COURSE_REPORT.md` is **delivered as-is**, never withheld and never blocking (FR-021).

> **Staging only.** `courses/` is staging; after delivery the author moves the course out of the repo
> manually. "Delivery" here = the pipeline reaching `done` with all artifacts present, not the
> physical move (spec Assumptions).
