# agents_sendbox

A **collection hub** for AI-agent tooling — skills, plugins, project templates, and
workshops gathered from across the community (and from my own past setups). The goal:
study what works, borrow the best ideas, and eventually assemble *the* perfect agent
setup for new projects.

This repo is not an app you run. It's a curated library you read, compare, and remix.

---

## Layout

| Path | What it is |
|---|---|
| [`references/`](references/) | External materials pulled in as **git submodules** — other people's skills, plugins, templates, and workshops. See [`references/README.md`](references/README.md) for the full catalog. |
| [`initial-sendbox/`](initial-sendbox/) | **My own first setup** — a GitHub Copilot Agent Mode sandbox (custom agents, skills, hooks, instructions). The starting point this hub will improve on. |
| `SaFE-pitch_prep.pptx` | Unrelated pitch deck (kept here for convenience). |

---

## Working with the submodules

Everything under `references/` is a pinned git submodule, so this repo records the
exact commit of each source without copying its history.

**Clone this repo with all materials:**
```bash
git clone --recurse-submodules https://github.com/arielybarak/agents_sendbox
# already cloned without --recurse-submodules?
git submodule update --init --recursive
```

**Add a new reference:**
```bash
git submodule add <repo-url> references/<short-name>
```
Then add a row to [`references/README.md`](references/README.md).

**Update one reference to its latest upstream:**
```bash
git submodule update --remote references/<short-name>
```

**Remove a reference:**
```bash
git submodule deinit -f references/<short-name>
git rm -f references/<short-name>
```

---

## Roadmap

1. **Gather** — collect agent setups, skills, and templates into `references/` *(in progress)*.
2. **Study** — compare approaches; note what's worth borrowing in the references catalog.
3. **Build** — assemble a curated "perfect setup" in its own tracked folder (not a submodule),
   freely remixing ideas from the references.
