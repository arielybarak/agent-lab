# Analysis-Phase Improvement Plan — meta-env-setup

**Date:** 2026-07-03 · **Status:** approved plan, NOT implemented
**Implementer:** a later agent (Opus) with no chat context — every item below is
implementable cold.
**Evidence base:** the post-hoc critique at
`/home/barak/book_generator_tom/.claude/setup-backlog.md` (read it in full first),
plus a prior gap-analysis pass that produced 7 proposed diffs to
`.claude/agents/setup-analyzer.md`. This plan supersedes that pass: it keeps its
detection gaps (generalized, consolidated into item 1) and adds pipeline/tool
changes the prior pass missed because it assumed every fix was analyzer prose.

All paths relative to `/home/barak/agents_sendbox/meta-env-setup/` unless absolute.

---

## Current state (what the analysis phase actually is today)

The "analysis phase" is not just `setup-analyzer.md`. It is:

1. `/new-claude-setup` (`.claude/commands/new-claude-setup.md`) step 1 delegates to
   the **setup-analyzer** agent (read-only; Read/Grep/Glob/Bash).
2. The analyzer's report is transcribed into **`templates/setup-spec.md`** →
   `claude-setups/<repo>/SETUP-SPEC.md`. The spec is the durable contract: the
   `block-author` writes against it and the `setup-critic` checks coverage against
   its §4 failure modes.
3. Brownfield: `/upgrade-claude-setup` step 3 runs the analyzer in *reconciliation
   mode* against an existing `.claude/` + a `setup-backlog.md`.
4. Downstream: scaffold (`tools/scaffold_claude_setup.py`) → author
   (`block-author`) → validate/score (`tools/validate_claude_setup.py`) → refine
   (`setup-critic` loop) → optional ablation ("prove") → package.

**Key structural facts the implementer must respect:**

- The analyzer's five determinants and the spec template's §1–§5 mirror each other
  one-to-one. **Any new determinant added to the analyzer MUST get a matching spec
  section, or its findings have nowhere to land** (the prior pass missed this — it
  only diffed the agent doc).
- The user is consulted at exactly two points today: thumbs-up on the block list
  (after the spec) and per-hook opt-in. The analyzer itself never asks anything.
- The "prove" step (step 8) is optional ablation. **Nothing in the pipeline ever
  executes an authored command.** `--score`/`--route` are static text heuristics.
- The analyzer reads only the target repo's files. Session history
  (`~/.claude/projects/<slug>/*.jsonl`) is invisible to it.

## What TOM proved goes wrong (evidence anchors)

Quotes from `book_generator_tom/.claude/setup-backlog.md`:

- **Broken blocks shipped:** "`/verify-generate --gpu` exists but calls the
  *anonymous* endpoint, whose quota is 0 → it 2-second-fails and tells you
  nothing"; "`/hf-logs` run returns the log but truncated to the startup banner…
  I fell back to manual curl **every single time**."
- **Session pain invisible:** "I diagnosed every one by hand-writing throwaway
  Python… **~15 times**, each rebuilt from scratch. None of it was captured";
  "~10 manual log pulls this session"; "~8 deploy → wait ~2 min → fail cycles."
- **Owner context missing:** F3 mock-backend "de-scoped (owner's call)";
  "don't reach for Storybook… for a solo build."
- **Stale blocks mislead:** "the two relevant skills (`tactile-stl-geometry`,
  `image-dxf-generation`) describe the **pre-migration** approach and are now
  actively wrong."
- **No feedback loop:** the backlog itself exists only because the owner
  hand-wrote a post-hoc critique; nothing shipped with the setup prompts it.
- **Repo signals were sitting in plain sight:** `[t]` timing prints at
  `src/dxf_3d.py:809-828`; the taper-segfault comment self-documented at
  `src/dxf_3d.py:415-419`; `sync_to_space.sh`; `web/src/lib/copy.js`
  `{hebrew, english}` parallel dicts; `web/IMPROVEMENTS.md` roadmap (~80% frontend);
  the un-runnable `tools/space_browser_test.mjs` (Chromium not installed).

---

## The plan — 8 items, priority order

Order rationale: item 1 is the foundation (everything downstream reads the
analyzer report + spec); items 2–3 are cheap doc/pipeline edits that close the
worst shipped-quality holes; items 4–5 are new code (bigger, independent); item 6
closes the long-term loop; item 7 is folder/doc housekeeping (`tools-pool/`
consolidation); item 8 adds greenfield/empty-workspace mode and rides with the
item-1 analyzer rewrite. Items 1, 3, 7, 8 are all doc edits and can share a PR;
2 is doc+pipeline; 4, 5 are separable code.

---

### 1. Pair-rewrite `setup-analyzer.md` + `templates/setup-spec.md` — new determinants

**What:** Expand the analyzer's five determinants to nine, and add matching spec
sections so the findings land in the contract. Edits to
`.claude/agents/setup-analyzer.md` and `templates/setup-spec.md` (and one-line
sync updates to the workflow summary in
`.claude/skills/claude-setup-scaffolder/SKILL.md` step 1 and
`.claude/commands/new-claude-setup.md` step 1).

**The nine determinants** (1–5 exist; sharpen 1 and 5; add 6–9):

1. *(expand existing #1)* **What the repo is + its domain inner loop** — beyond
   build/test/lint, find the function chain that turns input into the product
   artifact (mesh/image/PDF/dataset/binary/model). Detection tells to write into
   the agent doc: timing prints / profiler hooks (`time.time()`, `[t]`, `tqdm`);
   a stage emitting a parseable structured/binary file; an expensive or
   nondeterministic upstream stage (GPU/network/model) that can be stubbed to
   exercise the cheap downstream offline. If found → recommend an **offline bench**
   command. If that pipeline has stable invariants (dimensions, counts, schema)
   but no golden/snapshot test → also recommend a **checked-in fixture +
   regression check**. (TOM: `/stl-bench`, `/regress`.)
2. *(keep)* The one rule that overrides others.
3. *(keep)* Repetitive workflows → commands. Add: when a transcript-mining report
   exists (item 5), its repeated-command clusters are first-class input here.
4. *(expand existing #4)* Failure-prone spots — add **silent-drift / parity
   invariants**: two+ structures that must stay in lockstep (parallel locale
   dicts, vendored copies of a source tree, config mirrored across
   files/languages). They fail without an error → recommend a read-only parity
   check, not a skill. Detect by grepping for sibling key sets and duplicated
   paths. (TOM: `copy.js` hebrew/english, `hf_space/` vs `src/`, nikud maps.)
5. *(expand existing #5)* Existing setup — beyond "complement, don't duplicate,"
   check each existing block is still **true**: pull the concrete nouns it names
   (functions, flags, approaches) and grep the repo; zero hits = STALE → flag for
   REWRITE. Cross-check `git log` for migrations postdating the block. In
   brownfield mode, run `tools/validate_claude_setup.py <setup> --stale
   --repo <repo>` (item 4) and include its findings. A wrong block misleads worse
   than a missing one.
6. *(new)* **Feedback-loop economics** — for each way the repo is validated,
   estimate the cost of one iteration. Look for deploy/push scripts, cloud
   rebuilds, large model/asset loads per deploy, GPU-gated tests, CI-as-only-
   validator. Where validation runs through an expensive remote round-trip →
   recommend a **local pre-push gate** reproducing the checks offline. Rank all
   proposed blocks by (failure frequency × iteration cost), not frequency alone.
   (TOM: `/preflight` vs the ~8 × 2-min HF rebuild cycles.)
7. *(new)* **Direction of travel & product value** — read forward-looking docs
   (`ROADMAP*`, `TODO*`, `IMPROVEMENTS*`, open issues, recent git log themes) and
   the stated mission (README/CLAUDE.md). Recommend tooling for where the next
   bulk of work is going, and make a gate protecting the core product value
   (accessibility, correctness, safety…) non-negotiable in the pre-push gate.
   (TOM: `web/IMPROVEMENTS.md` ~80% frontend; a11y **is** the product; zero
   frontend tooling recommended.)
   **Decision (user-approved):** blocks identified for a *later* phase (not
   needed for current work) are still **authored now, in full**, by
   `block-author` — same quality bar as active blocks — but scaffolded directly
   into `tools-pool/<type>/<topic>/` instead of the active folder (see item 7
   below). Not a bare mention in the spec; a real, complete, pre-built block
   ready to `mv` in with zero authoring lag when the phase starts. Mark each in
   the spec's block list with its target: `active` or `tools-pool/<topic>`.
   **Exception — greenfield:** author-and-pool assumes real code exists to
   ground authoring and to `--stale`-check later. On an empty/greenfield
   workspace that grounding is absent, so **item 8 inverts this to
   defer-and-note.** Apply author-and-pool only when a codebase exists.
8. *(new)* **Environment executability** — for any block that must execute
   (bench, browser harness, gate), probe its runtime deps exist in *this* env
   (`which <bin>`, import check, lib check). A gate that can't run is worse than
   none — record missing deps as prerequisites in the spec, never assume.
   (TOM: `space_browser_test.mjs` dead because Chromium absent.)
9. *(new)* **Questions for the owner** — end the report with 3–5 questions only
   the owner can answer: where do you burn the most time; what's the next planned
   bulk of work; team size / who else uses this; what must never break; any
   tooling you've already rejected. These feed pipeline item 3. Never guess an
   answer that changes the block list. (TOM: F3 mock-backend was cut by owner's
   call; Storybook avoided because solo.)

**Spec template changes (`templates/setup-spec.md`):** add sections — §1 gains
"Domain inner loop" and "Iteration cost table" lines; new "§ Parity invariants";
new "§ Direction of travel / next bulk of work"; new "§ Environment prerequisites
(probed)"; new "§ Owner answers (from interview)"; §4 failure-mode table gains a
`cost-per-miss` column. Keep the template short — one line per new field, matching
the existing terse style.

**Also:** fold the prior pass's "How you work" additions: probe-before-recommend
(det. 8), balance retrospective vs prospective coverage (det. 7).

**Done when:** both files updated; the nine determinants and spec sections
correspond one-to-one; `python tools/validate_claude_setup.py .` still passes;
`--score .` shows no regression on the kit's own setup.

---

### 2. Smoke-test mandate — no command ships unexecuted

**Decision (user-approved):** mandatory with escape hatch.

**What:** every authored *command* gets executed once before packaging;
side-effectful / credentialed / quota-burning commands get a dry-run variant or
are explicitly flagged `UNTESTED` in the setup's README with the reason.

**Edits:**
- `.claude/commands/new-claude-setup.md` — insert a step between "Refine to
  target" (7) and "Prove (ablation)" (8): **"Smoke-test every command"** — run
  each command's core recipe once against the real repo (read-only ones as-is;
  mutating/credentialed ones via their dry-run path). A command whose recipe
  fails on first execution goes back to `block-author`. Record per-command
  result in the spec ("§ Smoke-test results": PASS / PASS-dry-run /
  UNTESTED+reason). Renumber later steps.
- `.claude/commands/upgrade-claude-setup.md` — same requirement inside step 4
  ("Work the backlog"): a FIX/ADD command's **done-check** (the backlog field
  "Done when") must be *executed*, not eyeballed.
- `.claude/agents/block-author.md` — add to its self-check: for commands, state
  the exact one-line invocation that proves it works, and run it if it is
  read-only; otherwise emit the dry-run to run at smoke-test time.
- `templates/setup-spec.md` — add "§ Smoke-test results" (item 1 already touches
  this file; do together).

**Evidence:** `/verify-generate --gpu` (anonymous quota=0 → useless) and
`/hf-logs` (head-only) both shipped broken; one execution each would have caught
both.

**Done when:** pipeline docs updated; a rerun of the pipeline on any repo
produces a spec with a filled smoke-test section.

---

### 3. Owner-interview step in `/new-claude-setup`

**Decision (user-approved):** yes, blocking (analyzer emits questions; pipeline
asks them before the spec is written).

**What:** in `.claude/commands/new-claude-setup.md`, split step 2 into:
- **2a. Interview** — take the analyzer's "Questions for the owner" (determinant
  9) and ask them via AskUserQuestion (batch, max 4 per call). Skip questions the
  analyzer could answer from files — the bar is "only the owner knows."
- **2b. Write the spec** — as today, now including "§ Owner answers"; the block
  list must be consistent with the answers (e.g. don't propose heavyweight visual
  testing to a solo dev who declined it).

Brownfield note in `/upgrade-claude-setup`: the backlog usually *is* the owner's
voice, so the interview is only for holes the backlog leaves open (ask at
reconciliation-table time, same mechanism).

**Evidence:** F3 "de-scoped (owner's call)"; Storybook cut for solo context —
both were guessable-wrong and answerable in 30 seconds.

**Done when:** command doc updated; interview happens before any scaffolding in a
fresh run.

---

### 4. New validator mode: `--stale --repo <path>`

**Decision (user-approved):** validator mode + a one-line analyzer hook (the
analyzer part is in item 1, det. 5).

**What:** add a Layer-1-style deterministic mode to
`tools/validate_claude_setup.py`:

- CLI: `--stale` requires `--repo <path-to-target-repo>` (the real repo the setup
  serves; needed because `claude-setups/<repo>/` working copies live outside the
  target).
- For each block (skills + commands + agents): extract **distinctive nouns** from
  its body + description — reuse `_distinctive()` / `_content_words()`; keep
  identifier-like tokens: `snake_case`, `CamelCase`, dotted paths, `*.py`/`*.js`
  filenames, quoted function names, config keys.
- **Also scan `tools-pool/**` blocks**, not just active ones, and label their
  findings `stale-suspect (pooled)` in the report. Pre-built pooled blocks
  (item 1 det. 7 / item 7) are authored ahead of need and can go stale before
  they're ever promoted — that's the same drift problem this mode exists to
  catch, just happening pre-emptively instead of post-migration.
- Grep each noun against the target repo (respecting `.gitignore` where cheap;
  skip `node_modules`, `.git`, `__pycache__`, `dist`, binary files).
- Report per block: `fresh` / `stale-suspect` with the list of dead nouns
  (mentioned in the block, zero hits in the repo). Heuristic threshold: flag when
  ≥ 2 identifier-like nouns are dead, or ≥ 50% of a block's identifier nouns are
  dead. Advisory only — never gates CI (same policy as `--score`).
- Output follows the existing `print_audit` style; `--json` supported.
- Tests in `tools/test_audit.py`: a fixture setup + fake repo where one skill
  cites a removed function (e.g. `skeletonize_image`) → flagged; a fresh skill →
  not flagged. Mirror the existing deterministic-scorer test style.
- Docs: `tools/README.md` + `evals/README.md` (add row to the layers table:
  staleness = "is each block still true against the code").

**Evidence:** `tactile-stl-geometry` still said boolean-union/taper after
`STROKE_TAPER_DEG = 0.0` landed (self-documented at `dxf_3d.py:415-419`);
`image-dxf-generation` still said skeletonization. Mechanical noun-grep catches
both with zero model calls, and stays useful *after* shipping (rerun post-
migration).

**Done when:** mode implemented + tests pass (`python tools/test_audit.py`);
running it on `claude-setups/book_generator_tom/ --repo
/home/barak/book_generator_tom` flags the two known-stale skills' old nouns if
run against the pre-rewrite versions (use git history or a fixture copy to
verify).

---

### 5. New tool: `tools/mine_transcripts.py` — session-pain miner

**Decision (user-approved):** yes, dedicated tool.

**What:** stdlib-only, read-only CLI that turns Claude Code session logs into
analyzer input.

- Input: `--repo <path>` → derive the project slug the way Claude Code does
  (path with `/` → `-`; e.g. `/home/barak/book_generator_tom` →
  `-home-barak-book-generator-tom`) → read
  `~/.claude/projects/<slug>/*.jsonl`. Also accept `--transcripts <dir>` override
  and `--since <days>` (default 45).
- Extract from each JSONL event stream (schema: newline-delimited JSON; tool
  calls appear as assistant messages with `tool_use` blocks — parse defensively,
  skip unparseable lines):
  - **Repeated Bash commands** — normalize (strip paths/args to a template),
    cluster, count. Emits: "`curl …/logs/run | python -c …` ran 11× → candidate
    command."
  - **Throwaway inline scripts** — `python -c`, heredocs, one-off `.py` files
    written to /tmp or scratch and executed. Cluster by token overlap. Emits:
    "STL byte-parser hand-written ~n× → candidate bench/tool."
  - **Deploy-and-wait loops** — command clusters matching push/sync/deploy
    scripts followed within the session by log-fetch/test commands; count cycles.
    Emits iteration-cost evidence for determinant 6.
  - **Error strings recurring across sessions** (same traceback head ≥ 3×).
- Output: a Markdown report (`--out` path, default stdout): top clusters with
  counts, one representative sample each, and a "candidate block" suggestion
  line per cluster. **No raw secrets:** redact tokens/bearer headers by regex.
- Wire-in: `.claude/agents/setup-analyzer.md` "How you work" gains: *"If
  transcripts exist for the target repo, run `python tools/mine_transcripts.py
  --repo <path>` first and treat its clusters as first-class evidence for
  determinants 3 (repetitive workflows) and 6 (iteration cost)."* (Add alongside
  item 1's edits.) `/new-claude-setup` step 1 mentions it as analyzer input.
- Tests: fixture JSONL in `tools/test_audit.py` style — synthetic transcript with
  a command repeated 5× and a secret to redact → assert cluster + redaction.

**Evidence:** the backlog's headline numbers — "~15 times", "~10 manual log
pulls", "~8 deploy cycles" — were all reconstructed by the owner from memory of
sessions. The repo alone can never show them; transcripts do. This converts the
post-hoc backlog's most valuable content into a pre-hoc automated input.

**Done when:** tool runs against real transcripts for `book_generator_tom`
(slug dir exists on this machine) and surfaces at least the curl-log-pull and
deploy-cycle clusters; tests pass; secret-redaction verified.

---

### 6. Ship a feedback loop into every generated setup — `/setup-retro`

**What:** stop relying on an owner spontaneously writing a critique. Every
generated setup gets a small `/setup-retro` command (new cookbook archetype +
scaffolder inclusion):

- Content: instructs the agent to author/update `.claude/setup-backlog.md` from
  `templates/setup-backlog.md` structure, grounded in the current session's pain
  + `git log` since the setup landed + (if available) `mine_transcripts.py`
  output; explicitly checks each existing skill's nouns against the code (poor
  man's `--stale`) and lists REWRITE candidates.
- Add archetype row to `cookbook/README.md` (Commands table): "Setup-retro —
  every setup; turns session pain into a machine-consumable backlog; the trap it
  removes: silent rot (TOM's Era-2)."
- `.claude/commands/new-claude-setup.md` step 9 (Package): include
  `/setup-retro` in every shipped setup by default; README of the generated
  setup tells the owner: run it after any big migration or painful session, then
  `/upgrade-claude-setup` consumes the result.
- Template body lives in `cookbook/templates/` as a copyable command file so
  `block-author` specializes it per repo (repo name, paths pre-filled).

**Evidence:** TOM's backlog — the single most valuable artifact in this whole
story — exists only because the owner volunteered it. Era-2 rot ("actively
wrong" skills) was detected months of sessions late. The upgrade pipeline
(`/upgrade-claude-setup`) already consumes backlogs; this closes the producer
side.

**Done when:** archetype + template exist; a fresh `/new-claude-setup` run
includes `/setup-retro` in the generated command list.

---

### 7. Unify the pool into one `tools-pool/` folder, and raise its visibility

**Decision (user-approved):** consolidate + make the mechanism a little more
prominent (not a big rewrite — a nudge).

**Current state (as-is, confirmed):** the pool is documented in exactly one place
— `README.md:130-143`, section "Skill pool — park skills to save budget" — and
only covers skills. In practice, generated setups already have **two separate
pool folders** side by side (seen in
`claude-setups/book_generator_tom/.claude/`): `skills-pool/` and
`commands-pool/`, each internally split by topic (`skills-pool/frontend/`,
`commands-pool/frontend/`). No mention in `tools/README.md`, the scaffolder
skill, or `templates/setup-spec.md`.

**What to change:**
- **Restructure:** replace the per-type pool folders (`skills-pool/`,
  `commands-pool/`, and any future `agents-pool/`) with **one**
  `.claude/tools-pool/` folder containing type subfolders:
  ```
  .claude/tools-pool/
  ├── skills/<topic>/<skill-name>/SKILL.md
  ├── commands/<topic>/<command-name>.md
  └── agents/<topic>/<agent-name>.md
  ```
  Park: `mv .claude/skills/<name> .claude/tools-pool/skills/<topic>/`.
  Reactivate: `mv .claude/tools-pool/skills/<topic>/<name> .claude/skills/`.
  One root folder to glance at instead of hunting `*-pool` siblings.
- **Update `tools/scaffold_claude_setup.py`** if it has any awareness of pool
  folders (check `import`/`init` — confirm whether it currently globs or ignores
  `*-pool/`; if it explicitly skips `skills-pool`/`commands-pool` by name, change
  that skip-list to the single `tools-pool/` prefix instead).
- **Migrate existing generated setups**: `claude-setups/book_generator_tom/`
  currently has `skills-pool/frontend/` and `commands-pool/frontend/` — fold both
  into `tools-pool/skills/frontend/` and `tools-pool/commands/frontend/` as part
  of this change (small, mechanical `mv`).
- **Raise visibility (a little, not a lot):**
  - `README.md` — rename the section "Skill pool" → "Tool pool", keep it short,
    update the folder diagram to `tools-pool/{skills,commands,agents}/`.
  - `.claude/skills/claude-setup-scaffolder/SKILL.md` — add one line to the
    "building blocks" table or the workflow section pointing at `tools-pool/` as
    where blocks go when a repo phase moves on (e.g. after Era-2 geometry work
    wraps, park `stl-bench`-adjacent skills instead of deleting them).
  - `templates/setup-spec.md` — §6 (decided block list) gets a **target**
    column per block: `active` | `tools-pool/<topic>`. Blocks marked
    `tools-pool` are still fully specified (rationale, archetype) — they are
    *authored*, not deferred (see determinant 7's decision above).
  - `.claude/commands/new-claude-setup.md` step 3 (Scaffold) — when a spec block
    targets `tools-pool/<topic>`, run `scaffold add <type> <name> --dir
    claude-setups/<repo>/.claude/tools-pool/<type>/<topic>` instead of the
    active path. Step 4 (Author) treats it identically — `block-author` doesn't
    write lower-quality content for a pooled block.
  - This is now a small **pipeline behavior change**, not documentation-only:
    scaffolding must support a `tools-pool/<type>/<topic>` destination, and the
    smoke-test mandate (item 2) still applies — a pooled block must prove it
    works *before* parking, not just before promotion, or it rots silently
    exactly like item 4's stale-skill problem, just pre-emptively.

**Evidence:** confirmed directly in the repo — `claude-setups/book_generator_tom/.claude/{skills-pool,commands-pool}/frontend/` exist as two parallel folders; the
mechanism is real and used, but under-documented (one README section, no
cross-reference from the scaffolder skill or the spec template) and split
per-type when the underlying idea (park a block, zero budget cost, promote by
topic) is the same for every block type.

**Done when:** `tools-pool/{skills,commands,agents}/` exists in the kit's own
`.claude/` (if applicable) and in `claude-setups/book_generator_tom/`; old
`*-pool/` folders removed; README section renamed and updated; scaffolder skill
+ spec template each carry one line pointing at it.

---

### 8. Greenfield / empty-workspace mode for the analysis phase

**Decision (user-approved):** add it; and on greenfield, **invert item 1 det. 7's
author-and-pool call → defer-and-note** (see below). "More questioning" is the
right instinct — the interview becomes the primary input, not a supplement.

**Why:** the whole plan reads signals *out of existing code*. On a repo that is
empty except a `README` / "about" / vision doc, nearly every signal goes dark —
inner loop (det. 1), parity (det. 4), staleness (det. 5 / item 4),
feedback-loop economics (det. 6), the transcript miner (item 5), and the
smoke-test mandate (item 2) all have **nothing to observe**. Only det. 7
(direction of travel) and det. 9 (owner interview) produce anything, and they
flip from supporting signals to **the entire evidence base**. The analyzer's
core discipline — *"cite real files/commands; an ungrounded item gets cut"*
(`setup-analyzer.md` "How you work"; spec template preamble) — then backfires:
nothing is citable, so a strict analyzer recommends almost nothing or
hallucinates. **Concrete hook:** `templates/setup-spec.md:12` already lists
`greenfield` as a maturity value, but no determinant or pipeline step acts on
it — the concept is named and ignored.

**What to add:**
- **Detect the mode cheaply** — in `setup-analyzer.md`, before running the nine
  determinants: count source files / LOC / git-history depth (e.g. Bash
  `git rev-list --count HEAD`, source-file count excluding docs/config). Below a
  threshold (suggest: < ~5 source files or < ~3 commits) → **greenfield mode**.
  Record the mode + the numbers in the report and in the spec's Maturity line.
- **Invert the evidence hierarchy for this mode** — the README/about/vision doc
  becomes the **spec seed**; det. 9's interview **expands** from 3–5 questions to
  a fuller intake, and runs *first* (before any file-signal pass, since there's
  little to pass over): intended stack & build/test tooling; the intended core
  workflow / "inner loop" the project is being built to do; what "done"/success
  looks like; where the author expects the hard/risky parts; what must never
  break; team size; anything already ruled out. Explicitly **relax** the
  "ungrounded item gets cut" rule here — recommendations are openly labeled
  *predictions from stated intent*, not observations.
- **Defer-and-note for speculative blocks (the inversion of det. 7's default):**
  author **only the universal, groundable blocks** now —
  - **CLAUDE.md** always (the one place the stated intent + the one overriding
    rule + the intended run-commands genuinely belong), and
  - optionally **one architecture / scaffolding skill** grounded in the *stated*
    intent (e.g. "logic in `src/`, notebooks orchestrate" if that's the plan).

  Everything else (benches, gates, domain skills, parity checks) is **recorded
  as a spec candidate with its trigger condition** — *not* pre-built into
  `tools-pool/`. Rationale: item 1 det. 7's author-and-pool was justified by
  having real code to ground authoring against and to `--stale`-check later; on
  an empty repo that grounding is absent, so pre-building only manufactures cruft
  that item 4's `--stale` will flag the instant code lands — and greenfield
  visions shift often. Cheaper to defer than to author-then-rewrite.
- **Set a re-analysis trigger** — because the *first real* analysis can only
  happen once code exists, greenfield mode's deliverable includes a scheduled
  catch-up: ship `/setup-retro` (item 6) as usual, plus a one-line note in the
  generated setup's README — *"this setup was built from intent, not code;
  re-run `/new-claude-setup` (or `/upgrade-claude-setup` once a backlog exists)
  when the repo crosses ~N source files / the first real feature lands."* The
  spec's candidate list (deferred blocks above) is what that re-run works from.

**Edits:**
- `.claude/agents/setup-analyzer.md` — add the greenfield detection + mode-switch
  block (expanded interview first; README-as-seed; relaxed grounding rule;
  defer-and-note default). Fits alongside the item-1 determinant rewrite.
- `.claude/commands/new-claude-setup.md` — step 1/2: when the analyzer reports
  greenfield, the interview (item 3) is mandatory and expanded; step 3 authors
  only the universal set; deferred candidates are written to the spec, not
  scaffolded.
- `templates/setup-spec.md` — the Maturity line (`:12`) drives a conditional:
  when `greenfield`, the block list's `target` column (from item 7) gains a
  third value `deferred (trigger: <condition>)`; add a short "§ Re-analysis
  trigger" line.

**Interaction with prior decisions:** this is the **one place** the author-and-
pool decision (last turn, item 1 det. 7) is deliberately reversed. Everywhere a
real codebase exists → author-and-pool. Empty workspace → defer-and-note. Make
the split explicit in det. 7's text so the implementer doesn't apply one rule
blindly.

**Done when:** analyzer detects greenfield on a fixture repo (README only) and
switches modes; a fresh `/new-claude-setup` on such a repo produces a spec with
an expanded interview section, a CLAUDE.md (+ maybe one intent-grounded skill)
authored, a deferred-candidate list with triggers, and a re-analysis trigger —
and scaffolds **no** speculative `tools-pool/` blocks.

---

## Explicitly out of scope / cut

- **Splitting the analyzer into multiple agents** (profiler + analyst): rejected —
  the new tools (items 4–5) give it deterministic inputs; a second agent adds
  latency and hand-off loss without new signal.
- **Auto-generating `tasks.json` eval suites during analysis**: deferred — the
  routing-tests + smoke-tests (item 2) cover the cheap 90%; behavioral task
  suites stay opt-in at the prove step.
- **Shipped drift-detection hook** (auto-run `--stale` in the target repo):
  rejected for now — hooks are opt-in per kit policy; `/setup-retro` (item 6)
  covers it with the owner in the loop.
- **Prior pass's assumption that all fixes are analyzer prose**: superseded —
  staleness → validator (item 4), repetition-detection → miner (item 5),
  execution-truth → pipeline (item 2), owner knowledge → interview (item 3).

## Suggested implementation order & PR slicing

1. **PR-1 (docs only):** items 1 + 2 + 3 — analyzer/spec pair-rewrite, smoke-test
   mandate, interview step. No code. Re-run `--score .` as regression check.
2. **PR-2 (code):** item 4 (`--stale`) with tests.
3. **PR-3 (code):** item 5 (`mine_transcripts.py`) with tests; then add its
   one-line wire-in to the analyzer (touches a PR-1 file — trivial rebase).
4. **PR-4 (content):** item 6 (cookbook archetype + packaging step).
5. **PR-5 (housekeeping):** item 7 (`tools-pool/` consolidation + doc bump) —
   independent of 1–6, can land anytime, but do it *after* PR-1 so the spec
   template edit lands once (both item 1 and item 7 touch
   `templates/setup-spec.md` §6 — sequence to avoid a conflicting diff).
6. **PR-6 (docs, part of the analyzer rewrite):** item 8 (greenfield mode) —
   naturally rides with PR-1 (same files: `setup-analyzer.md`,
   `new-claude-setup.md`, `setup-spec.md`). Land it *with* PR-1 or immediately
   after; it depends on item 7's spec `target` column (adds a third value
   `deferred`) and on det. 7's author-and-pool text (adds the greenfield
   exception), so sequence PR-1 → PR-5 → PR-6, or fold all three doc PRs into
   one.

Verification for the whole plan: rerun the brownfield pipeline mentally against
TOM — every backlog headline (`/stl-bench`, `/hf-logs` tail, `/preflight`, stale
skills, F1–F2 frontend gap, F3 de-scope) must now be caught by a named
determinant, tool, or pipeline step. If one isn't, the plan item covering it is
incomplete.
