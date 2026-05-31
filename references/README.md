# References — materials catalog

External agent tooling gathered for study, pulled in as **git submodules** (pinned to a
commit, not copied). Each entry below: what it is, how it's used, and what's worth
borrowing for the eventual "perfect setup".

> Update a single one: `git submodule update --remote references/<name>`
> Add a new one: `git submodule add <url> references/<name>` — then add a row here.

## At a glance

| Folder | Type | One-liner | Upstream |
|---|---|---|---|
| [`caveman`](caveman/) | Skill / plugin | Makes agent output terse to cut ~75% of output tokens | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) |
| [`mattpocock-skills`](mattpocock-skills/) | Skills pack | Small, composable "skills for real engineers" | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [`ideal-project-scaffolder`](ideal-project-scaffolder/) | Project template | Copier meta-template for AI-ready project workspaces | [yitzhak-shaked/ideal-project-scaffolder](https://github.com/yitzhak-shaked/ideal-project-scaffolder) |
| [`sdd-workshop`](sdd-workshop/) | Workshop | Hands-on spec-driven development with the Kiro IDE | [094459/sdd-workshop](https://github.com/094459/sdd-workshop) |

---

## caveman
**Type:** Claude Code skill/plugin (also works with Codex, Gemini, Cursor, Windsurf, Cline, Copilot, 30+)
**Upstream:** https://github.com/JuliusBrussee/caveman

Makes the agent "talk like caveman" — strips filler from responses to cut roughly **75%
of output tokens** while keeping full technical accuracy. Ships as a skill/plugin with
its own `commands/`, `agents/`, `skills/`, `plugins/`, plus `benchmarks/` and `evals/`.

- **Borrow for:** token/cost reduction; a working example of a packaged multi-tool plugin
  with benchmarks and evals to back up its claims.
- **Look at:** `README.md`, `INSTALL.md`, `skills/`, `evals/`, `benchmarks/`.

## mattpocock-skills
**Type:** Agent skills pack (install via skills.sh)
**Upstream:** https://github.com/mattpocock/skills

Matt Pocock's everyday engineering skills — deliberately **small, adaptable, and
composable**, designed to stay out of your way (an explicit alternative to heavier
process frameworks like GSD / BMAD / Spec-Kit). Install with
`npx skills@latest add mattpocock/skills`, then run `/setup-matt-pocock-skills`.

- **Borrow for:** skill design philosophy (small + composable), issue-tracker/triage
  workflow integration, the `/setup-*` onboarding pattern.
- **Look at:** `skills/`, `CLAUDE.md`, `docs/`.

## ideal-project-scaffolder
**Type:** Copier-based project meta-template — *my own earlier "ideal setup" attempt*
**Upstream:** https://github.com/yitzhak-shaked/ideal-project-scaffolder

One questionnaire generates a tailored project scaffold: per-language manifests, an agent
instruction file in the convention your chosen agent expects, preconfigured MCP servers,
per-domain instruction files, and a DDD source/test layout. Run with
`uvx copier copy --trust gh:yitzhak-shaked/ideal-project-scaffolder .`.

- **Borrow for:** the whole "generate a fresh AI-ready project" angle — this is the most
  direct prior art for the perfect-setup goal. MCP wiring, `just mcp` diagnostics,
  per-agent instruction conventions.
- **Look at:** `copier.yml`, `template/`, `_hooks/`, `docs/`, `TEMPLATE_MAINTENANCE.md`.

## sdd-workshop
**Type:** Hands-on workshop (Kiro IDE)
**Upstream:** https://github.com/094459/sdd-workshop

A self-paced or facilitator-led workshop on **spec-driven development**: requirements
(EARS), design, steering files, then implementation tasks — across greenfield and
brownfield labs. Built around the Kiro IDE.

- **Borrow for:** the spec → design → tasks workflow; EARS requirement phrasing; the
  idea of "steering files" as persistent context.
- **Look at:** `workshop/01-intro.md` onward, `updates/`.

---

## Adding the next batch
Drop URLs anytime. Convention: one submodule per repo under `references/<short-name>`,
plus a section here covering **what it is / how it's used / what to borrow**.
