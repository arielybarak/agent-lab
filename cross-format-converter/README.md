# Cross-Format Converter — Future Project

Translate an agent setup between **Claude Code** (`.claude/`) and **Google
Antigravity** (`.agents/` + `GEMINI.md` / `AGENTS.md`) — and **report how much
survives the trip**.

> Status: **design doc only** (no code yet). This README *is* the design.

## Goal

A converter that takes a `.claude/` setup and emits the equivalent Antigravity
setup (and, later, the reverse), plus a **translation report** that says exactly
what converted cleanly, what was approximated, and what had to be dropped.

The portfolio signal: this repo already spans two agent ecosystems — GitHub Copilot
(`initial-sendbox/`) and Claude Code (`meta-env-setup/`). A Claude↔Antigravity
converter proves **format-level fluency across the agent-tooling landscape**, not
just inside one vendor. The on-brand twist is the same one that defines
`meta-env-setup/`: **don't just produce output — measure it.** Here the measurement
is *translation fidelity*.

## The two formats side by side

**Antigravity's config surface** (verified June 2026 — see [Sources](#sources)):

| Antigravity construct | Path | Notes |
|---|---|---|
| Global rules | `~/.gemini/GEMINI.md` | always-on, all workspaces |
| Workspace rules | `.agents/rules/*.md` (legacy `.agent/rules`) | markdown, 12k chars each, `@filename` includes |
| **Cross-tool rules** | `AGENTS.md` (workspace root) | **read by Antigravity *and* Claude Code**; applied after `GEMINI.md` |
| Skills | `.agents/skills/<name>/SKILL.md` (+assets); global `~/.gemini/config/skills/` | directory package, description-triggered, progressive disclosure |
| Workflows (= slash commands) | `.agents/workflows/<name>.md`, invoked `/name` | step list, 12k chars |
| Subagents | plugin `agents/<name>.md`; `/agents` panel | async / background oriented |
| Hooks | `hooks.json` (global + workspace) | before/after tool exec, before/after model call, stop conditions |
| Settings / MCP | `~/.gemini/antigravity-cli/settings.json`, `mcp_config.json` | |

**The mapping** — Claude Code `.claude/` → Antigravity, each with a fidelity rating:

| Claude Code block | Antigravity equivalent | Fidelity | What's lossy |
|---|---|---|---|
| `CLAUDE.md` (project) | `AGENTS.md` (shared standard) — *not* `GEMINI.md` | **Clean** | none — `AGENTS.md` is read by both tools |
| `~/.claude/CLAUDE.md` (global) | `~/.gemini/GEMINI.md` | **Clean** | global scope only |
| `.claude/skills/<n>/SKILL.md` (+reference/scripts/assets) | `.agents/skills/<n>/SKILL.md` (+assets) | **Clean** | normalize frontmatter field names; `scripts/` execution differs |
| `.claude/commands/<n>.md` (`$ARGUMENTS`, `!`shell, `@file`) | `.agents/workflows/<n>.md` (`/name`) | Lossy | arg/shell-embed syntax differs; 12k char cap |
| `.claude/agents/<n>.md` (name/description/**`tools`** allowlist) | plugin `agents/<n>.md` / subagent | Lossy | least-privilege `tools:` model differs; Antigravity subagents are async |
| `settings.json` hooks (PreToolUse/PostToolUse, exit-2 block) | `hooks.json` (before/after tool/model, stop) | Lossy | event taxonomy + block-vs-advisory exit semantics differ |
| `settings.json` permissions/model | `settings.json` (antigravity-cli) | **No clean equivalent** | different schema; document, don't auto-translate |
| MCP servers | `mcp_config.json` | **Clean** | near-direct |

## The non-obvious insight: lean on `AGENTS.md`

The naive design translates `CLAUDE.md` ↔ `GEMINI.md`. **Don't.** `AGENTS.md` is a
*shared* standard that **both** Antigravity and Claude Code already read. So the
highest-fidelity bridge for project rules is to emit/consume `AGENTS.md` — one file,
zero translation, read natively by both sides. The vendor-specific files
(`CLAUDE.md`, `GEMINI.md`) then hold only the genuinely vendor-specific overrides.

This also reframes the whole tool: for the **rules** layer, the best converter does
*less*, not more.

## Fidelity & the "translation report"

The deliverable is not just converted files — it's a report, in the spirit of
`meta-env-setup/tools/validate_claude_setup.py`:

- **Clean** — converted with no semantic loss (rules, skills, MCP).
- **Lossy** — converted but approximated; the report names exactly what changed
  (e.g. "command `$ARGUMENTS` → workflow step prose"; "hook `exit 2` block →
  advisory only").
- **Dropped** — no target equivalent (e.g. per-tool permission allowlists); listed so
  the user re-adds them by hand.

A setup that converts 100% clean is rare and that's the point: the report makes the
*incompatibilities between ecosystems* legible. That's the interesting artifact.

## Direction & scope (first build)

- **One way first:** `.claude/` → Antigravity (richer → simpler is the easier
  direction; the reverse is an open question below).
- **Single repo**, single setup at a time.
- **Start with the clean mappings** — rules (via `AGENTS.md`), skills, MCP. These are
  ~1:1 and give a working tool fast.
- **Then the lossy ones** — commands→workflows, agents→subagents.
- **Defer** hooks and permissions (most lossy; document-only at first).

## Connections to existing repo work

- `meta-env-setup/tools/validate_claude_setup.py` — the *fidelity report* reuses its
  parse-and-grade shape (stdlib-only, deterministic, emits a structured verdict).
- `meta-env-setup/tools/scaffold_claude_setup.py` — already knows the `.claude/` block
  taxonomy; the converter reads the same structure.
- `claude-setups/<repo>/` — ready-made real `.claude/` setups to use as conversion
  fixtures / test inputs.
- The **Copilot vs. Claude Code comparison** idea in `FUTURE_IDEAS.md` is the prose
  sibling of this tool; findings here feed that writeup (and vice versa).

## Open design questions (decide when starting)

- **`SKILL.md` frontmatter deltas** — exact field-name differences between Claude
  Code and Antigravity skills (both use `name` + `description`; confirm the rest).
- **All-in on `AGENTS.md`?** — emit rules *only* as `AGENTS.md`, or also write a
  vendor file for overrides?
- **Round-trip** — is Antigravity → Claude Code feasible, or is the loss one-way
  (simpler → richer requires invented detail)?
- **Plugin packaging** — Antigravity bundles `skills/` + `agents/` + `hooks.json` +
  `rules/` into a `plugin.json` package; convert into a plugin, or loose files?

## Sources

- Antigravity docs — Rules & Workflows, Skills (`antigravity.google/docs`)
- Google Codelabs — *Authoring Google Antigravity Skills*
- `addyosmani/agent-skills` — `docs/antigravity-setup.md`
