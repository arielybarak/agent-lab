# Future Ideas & Work Items

Things to build, add, or develop in this repo. Rough priority order within each section.

---

## Agent infrastructure

### Agent Eval Kit (`agent-eval-kit/`)
Folder already exists with a detailed README. The full artifact:
- A small real agent built with the Anthropic SDK (Python)
- A task suite of ~20–50 input/expected-output pairs with checkable outcomes
- An LLM-as-judge that auto-grades outputs, calibrated against human labels
- A CI gate (GitHub Actions) that fails if quality drops between commits
- A "what broke and why" writeup

**Why:** Proves you can build agents *and* measure them rigorously. The combination is rare.

### Bridge static `--score` with empirical triggering eval
Combine the two skill-authoring approaches now in the repo into a two-layer pipeline:
- **Cheap pre-filter:** `meta-env-setup/tools/validate_claude_setup.py --score` — static, deterministic, CI-able, repo-aware. Runs on every commit.
- **Behavioral confirm:** the official skill-creator's empirical triggering loop (`skills/skill-creator/scripts/run_loop.py`) — runs real Claude on queries (3× repeats, train/test split) to verify the skill *actually* triggers and improves output.

The bridge: use static scoring as the fast gate, behavioral eval as the ground-truth verification. Static pre-filter → behavioral confirm. This combination (cheap CI proxy + expensive empirical check) doesn't exist in either tool today and is genuinely novel — and portfolio-worthy.

**Why:** Yours answers "is this skill well-written for this repo?" statically; theirs answers "does it actually change what Claude does?" empirically. Neither alone is complete; the bridge is.

### Cross-Format Converter — Claude Code ↔ Antigravity (`cross-format-converter/`)
Folder already exists with a detailed design doc. Translate a `.claude/` setup to/from
**Google Antigravity** (`.agents/` + `GEMINI.md`/`AGENTS.md`), and emit a **translation
report** rating each block clean / lossy / dropped. Skills and rules map nearly 1:1; the
key insight is that `AGENTS.md` is a *shared* standard both tools read, so the best
converter does *less* on the rules layer. Reuses the parse-and-grade shape of
`meta-env-setup/tools/validate_claude_setup.py`.

**Why:** Proves format-level fluency across the whole agent-tooling landscape, not just
one vendor — and the fidelity report makes cross-ecosystem incompatibilities legible. The
prose sibling of the Copilot-vs-Claude comparison below.

### MCP Server
Build a custom MCP (Model Context Protocol) server — a small process that exposes tools Claude
Code can invoke. Natural candidate: a "score this skill file" tool that wraps
`meta-env-setup/tools/validate_claude_setup.py --score`, callable directly from within Claude Code.

**Why:** Shows you understand Claude Code at the protocol level, not just the user/config level.
Most candidates configure Claude; few can extend it.

### Prompt Injection Test Suite
A suite of adversarial inputs designed to make an agent do something it shouldn't: write to
forbidden paths, leak context, call tools outside its permission scope. Document what's defended
and what isn't. Builds directly on the existing least-privilege work in `meta-env-setup/`.

**Why:** Security-aware agent work is rare in portfolios. Combined with the existing
least-privilege scoring, it makes a complete security story.

### Cost Tracking in the Eval Kit
When building the eval kit, extend beyond token budgets to actual $ cost per task run.
A small dashboard showing cost per task, and the effect of prompt changes on cost efficiency.

**Why:** Production-thinking signal. Shows you care about real-world deployability, not just quality.

---

## Documentation / writing

### Copilot vs. Claude Code Comparison
A structured comparison of `initial-sendbox/` (GitHub Copilot Agent Mode) and
`meta-env-setup/` (Claude Code) — routing quality, context budget, least-privilege,
eval capability, skill/hook system. A practitioner perspective that almost no one else has,
because almost no one has built both setups seriously.

**Why:** Zero code required. Very quotable in interviews. Unique angle.

---

## Other directions (orthogonal to the above)

The ideas above mostly *build another way to measure a setup*. These push different ways —
validating the method itself, shipping it, and stress-testing it.

### Meta-eval: validate the scorer against real outcomes
Take a handful of setups spanning low-to-high `--score`, run a fixed task suite on each with
real Claude, and measure whether higher scores actually correlate with better task success.
Report the correlation — including where it breaks down.

**Why:** The whole repo rests on "higher score → better setup." *Proving* that (or honestly
finding its limits) is the most credible, most senior move available — it turns an opinion into
evidence and second-guesses your own tool. No other setup-scorer does this.

### Ship the validator as a GitHub Action + pre-commit hook
Wrap `validate_claude_setup.py` so anyone adopts it in one line —
`uses: arielybarak/claude-setup-validator@v1` in CI, or a `pre-commit` hook that blocks a
commit on a broken setup. Versioned, documented, with a sample workflow.

**Why:** "I built a tool" is weaker than "others run my tool in one line." Shows packaging,
versioning, and DevEx maturity — the gap between a script and a product.

### Cross-model behavior delta
Run the *same* setup under Opus / Sonnet / Haiku and measure how routing and outputs differ.
Emit a short "model-portability report": what stays stable, what changes when you swap models.

**Why:** Real teams switch models for cost and latency. Whether a setup behaves the same across
models is deployment-critical and almost never measured.

### Routing-stability (flakiness) harness
Run the routing tests K times and report a *stability* score — how often the right skill fires,
not just whether it can once. Surface the flaky blocks.

**Why:** A setup that routes correctly 6 times in 10 is broken in a way a single-shot test hides.
Measuring variance, not just correctness, is a genuinely deeper eval.

### Score-over-time drift tracking
Record each commit's composite score to a small history file, show the trend, and flag
regressions. Setups rot as the code moves under them — catch the decay.

**Why:** One-shot scoring is a demo; tracking drift across a repo's life is an ops signal.
Pairs naturally with the `--stale` mode already in the kit.

### Generalize the rubric beyond code repos
Point the scorer at non-code agent setups — a writing assistant, a research agent, a
data-analysis helper — and check whether the five sub-scores still hold. Document what breaks.

**Why:** Tests whether the method is a general theory of "good agent setup" or just fits code.
Either answer is worth writing up, and it sharpens the rubric.

---

## Course-factory

Product ideas for the course generator (`course-factory/`). Each ties to a spec or an optional
template module — noted inline so they're actionable when picked up. None are in the four current
specs; they're deliberate later extensions.

### More lesson/exercise formats — HTML & presentations, mixed per-artifact
Today the lesson-format decision is `.md` by default / `.ipynb` when code-heavy (owned by spec 002,
written into `COURSE_BRIEF.md`). Extend it to **HTML** — including slide-deck / **presentation**
style lessons — and make the choice **per-artifact** rather than one format per course: e.g. lessons
as HTML slides while coding exercises live in `.ipynb` or source files, or any other combination.
Needs a format field per lesson/exercise in the syllabus + brief, and an optional renderer module
(like *diagrams*) in `course-template/`.

**Why:** Different material teaches best in different forms — presentations suit conceptual arcs,
notebooks suit code, HTML enables interactivity. Forcing one container per course leaves teaching
value on the table.

### Inline multiple-choice comprehension checks
Short, quick MCQs embedded **during** a lesson (not just the end-of-lesson exercise) to give and
verify understanding as the learner goes — cheap formative checkpoints. Fits as an **opt-in template
module** (alongside katas / diagrams / Socratic) that spec 003's lesson authoring emits when enabled,
and the rubric (004) could check that checkpoints exist and map to the lesson's objectives. Pairs
naturally with the fake-student learnability signal.

**Why:** Active-recall checkpoints catch confusion early and reinforce as they go, at low authoring
cost — a lighter complement to full exercises, and a second signal on whether a lesson lands.

### Research teaching methods → a technique library the templates compose from
Do a dedicated research pass on **pedagogy / instructional design** so the factory composes courses
from proven teaching methods rather than ad-hoc structure. Store a **library of techniques + worked
examples keyed by material/course type** (concept-heavy, code-heavy, math, history, …) that
`course-template/` modules and the mentor-composition in specs 002/003 draw on at generation time.
Lives as a knowledge asset next to `insights/`; could feed rubric add-ons (004) for method-fit.

**Why:** Turns "mentor judgment" into a grounded, reusable catalog of what actually teaches well, so
every generated course inherits proven methods and the best templates get better over time — the
compounding idea (`insights/`) applied to pedagogy itself.

### Borrow spec-kit's artifact discipline for the course build
course-factory is itself authored *with* spec-kit (spec → clarify → plan → tasks → analyze, each a
separate status-stamped document checked against a constitution). Apply that same rigor to how it
**builds a course** at runtime:
- Emit each phase's output as a **separate, versioned, status-stamped artifact** (like a spec's
  `Status:` field), not just rows in `BUILD_PROGRESS.md`.
- A **clarify-style pass** — ≤N targeted questions whose answers are encoded back into
  `COURSE_BRIEF.md` (formalize what intake does informally today).
- **Per-phase quality checklists as gate artifacts** (a syllabus checklist, a lesson checklist),
  mirroring spec-kit's `checklists/requirements.md` — the gate becomes a checkable file, not only an
  agent judgment.
- An **analyze-style cross-artifact consistency check** (brief ↔ syllabus ↔ skeletons ↔ lessons) that
  catches drift the per-phase gates miss — the sibling of 004's course-level grading.
- A per-course **decisions / seam log** (like `specs/README.md`'s *Resolved decisions*) so a resumed
  build honors settled calls. Ties to specs **001** (phase artifacts + resume) and **004** (analyze ≈
  course-level consistency), with the pedagogy constitution ↔ rubric as the governing-doc analog.

**Why:** The same discipline that keeps *building the factory* coherent across sessions — small
reviewable artifacts, targeted clarify, cross-artifact analyze — is exactly what a long, multi-session
*course* build needs. We're already living proof the method works; point it at the output too.

---

## Notes
- Ideas here are *not* prioritized against each other — pick based on what's most interesting
  and what the portfolio needs at the time.
- When starting one of these, move it to its own folder/README rather than expanding this file.
