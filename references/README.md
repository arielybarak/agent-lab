# references — upstreams I study

External work pulled in as **git submodules** (pinned, read-only) plus a few loose notes and
docs. These are other people's setups I read, compare, and borrow from — **don't edit files inside
a submodule**; changes belong upstream. This file is the catalog: what each one is and what's worth
taking.

---

## Submodules

| Path | Source | What it is / worth borrowing |
|---|---|---|
| [`caveman/`](caveman/) | `JuliusBrussee/caveman` | The **caveman** skill — ultra-compressed responses (drops filler, keeps technical substance). Borrow: a tight, persistence-aware skill prompt. |
| [`mattpocock-skills/`](mattpocock-skills/) | `mattpocock/skills` | Matt Pocock's Claude **skills** collection. Borrow: skill-authoring patterns and trigger phrasing. |
| [`ideal-project-scaffolder/`](ideal-project-scaffolder/) | `yitzhak-shaked/ideal-project-scaffolder` | A **project scaffolder** setup. Borrow: how it structures a greenfield project + its scaffolding prompts. |
| [`claude-code-best-practice/`](claude-code-best-practice/) | `shanraisshan/claude-code-best-practice` | A **Claude Code best-practices** collection. Borrow: concrete workflow tips (see notes file below). |
| [`sdd/`](sdd/) | `094459/sdd` | **Spec-driven development** — core material. |
| [`sdd-workshop/`](sdd-workshop/) | `094459/sdd-workshop` | **Spec-driven development** — workshop form of the above. |
| [`spec-driven-development-workshop/`](spec-driven-development-workshop/) | `094459/spec-driven-development-workshop` | Another **SDD workshop** variant from the same author. |

> The three `094459/*` repos (`sdd`, `sdd-workshop`, `spec-driven-development-workshop`) overlap —
> keep them together and pick the freshest when borrowing.

## Loose docs (first-party, not submodules)

| File | What it is |
|---|---|
| [`claude-code-best-practice-notes.md`](claude-code-best-practice-notes.md) | My distilled notes from the `claude-code-best-practice` upstream (Boris Cherny / team tips). |
| [`enterprise-agent-platform-structure.md`](enterprise-agent-platform-structure.md) | A reference folder-structure spec for a hypothetical `enterprise-agent-platform/` (agents / tools / orchestration / governance / evals layout). Study material, not this repo's structure. |

---

## Working with the submodules

Everything under `references/` (except the loose docs above) is a pinned git submodule — this repo
records the exact commit of each source without copying its history.

**Clone with all materials:**
```bash
git clone --recurse-submodules https://github.com/arielybarak/agent-lab
# already cloned without --recurse-submodules?
git submodule update --init --recursive
```

**Add a new reference:**
```bash
git submodule add <repo-url> references/<short-name>
```
Then add a row to the catalog above.

**Update one reference to its latest upstream:**
```bash
git submodule update --remote references/<short-name>
```

**Remove a reference:**
```bash
git submodule deinit -f references/<short-name>
git rm -f references/<short-name>
```
