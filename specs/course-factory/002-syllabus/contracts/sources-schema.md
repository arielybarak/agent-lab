# Contract — `SOURCES.md` entry schema

**Owner:** spec 002 (populates the stub 001 creates). **Consumers:** 003 (lesson claims cite `[Sn]`
into it), 004 (traceability check at grading). **Enforced by:** `sources_lint.py` (SC-001). This is the
per-course grounding store; it is the anti-fabrication foundation for the **whole course** (FR-004), not
just the syllabus.

## File shape

Human-readable Markdown. One entry per kept source, each opening with its stable `[Sn]` key. Prose
around entries is advisory; the linter keys on the entry structure below.

```markdown
### [S1] — <short title>
- **type**: repo | course | syllabus | post
- **citation**: <URL for heavy sources> | <inline citation for a post/comment/tip>
- **reliability**: <prose weighing reliability over popularity — required, non-empty>
- **topics**: <comma-separated topics this source covers>   ← feeds convergence
- **flags**: (indirect) | (secondary) | (supporting) | unresolvable   ← optional
```

## Field rules (what `sources_lint.py` checks)

| Field | Rule | SC |
| :--- | :--- | :--- |
| `[Sn]` key | Present, unique, sequential, **append-stable** — never reused for a different source (FR-004, Assumptions). | SC-001 |
| `reliability` | Present and **non-empty**; a bare star count / popularity figure alone **fails** — stars are a green flag, not proof (FR-002). | SC-001 |
| `citation` | Present: a link for heavy sources, an inline citation for posts/comments/tips (FR-003). **No DOI is required** for repo/course/post types (R5 boundary — mentor-research's Crossref/ERIC identity-verify is for academic citations; here it is stars-as-green-flag + inspection). | — |
| `type` | One of the four; drives which citation form is expected. | — |
| `topics` | Present; the convergence signal (new sources stop adding topics, FR-005). | — |
| `flags` | Optional; `unresolvable` marks a dead link **found during this phase** — flagged once, **not** re-checked (edge case; 004's traceability catches a later death). | — |

## Dedupe rule (from `mentor-research`)

**Dedupe by work, not by URL.** Two links to the same work (publisher page + author PDF; repo + its
release page) are **one** `[Sn]` key. `sources_lint.py` flags an obvious duplicate-work (same title,
two entries) as a warning; the composer collapses it.

## Namespace

`[Sn]` is the **per-course** namespace. It must not collide with `[Pn]` (the cross-course `pedagogy/`
catalog), which is deliberately a separate namespace (mentor-research §2). A syllabus/lesson citing both
side by side keeps them distinct.
