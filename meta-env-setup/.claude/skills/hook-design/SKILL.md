---
name: hook-design
description: >-
  Design and write an effective Claude Code hook — first decide it should even BE a
  hook (deterministic enforcement) vs. a CLAUDE.md rule or a command, then pick the
  right event (PreToolUse / PostToolUse / UserPromptSubmit / Stop / …), choose
  advisory (exit 0) vs. blocking (exit 2), parse the stdin event JSON, fail open on
  errors, wire it in settings.json, and test it with a sample event. USE WHEN adding
  or debugging a hook, guarding a path/branch, or enforcing a rule the model
  shouldn't have to remember.
---

# Hook Design

A hook is **deterministic automation** that fires on a Claude Code lifecycle event —
the one block type that runs *code*, not prompting. Its whole reason to exist is to
enforce something **reliably**, every time, without the model having to remember.

## When to Activate This Skill
- "Add a hook that …" / "guard against …" / "block edits to …"
- A rule keeps getting violated even though it's written down
- Deciding hook vs. CLAUDE.md vs. command

## Step 0 — should this even be a hook? (decide before writing)
Hooks are the wrong tool more often than people think. Use the cheapest thing that
works:

| If the need is… | Use | Not a hook because… |
|---|---|---|
| an always-true project rule | **CLAUDE.md** | the model already reads it every session |
| situational expertise | **a skill** | it should load only when relevant |
| a repeatable workflow you invoke | **a command** | you trigger it on purpose, not on an event |
| **must happen every time, deterministically** | **a hook** | only code can guarantee it (a guard, a nag, a log) |

If the model can be *trusted to follow* it from a written rule, don't spend a hook.
Reach for a hook when you need a guarantee: block a frozen path, refuse a secret
read, nag before an unfair benchmark, log every session.

## The loop
1. **Pick the event** and the **archetype**. Most guards are `PreToolUse`; reminders
   are `PostToolUse`; prompt-shaping is `UserPromptSubmit`. (Full event + exit-code
   tables and the archetype catalog: `reference.md` in this folder.)
2. **Start from a bundled template, critically** (don't write from scratch — both
   live in `templates/`, so they travel with this skill):
   - blocking guard → copy `templates/guard-hook.py` (exit 2, fail-open).
   - advisory nag → copy `templates/advisory-hook.py` (exit 0 + stdout).
   Both parse a *tool* event — **adapt the stdin read to your event** (a
   `UserPromptSubmit` hook reads `prompt`, not `tool_input`; see `reference.md` §3).
   *(In the kit, `scaffold … add hook` also generates a skeleton.)*
3. **Write it** to the three safety laws below.
4. **Test it** with a sample event before trusting it:
   ```bash
   echo '{"tool_input":{"file_path":"project-A/x"}}' | python .claude/hooks/<name>.py; echo "exit=$?"
   ```
   Confirm the exit code (2 to block, 0 to allow/advise) and the message.
5. **Wire it.** Add it to `settings.json` (exact shape in `reference.md` §5). *(In
   the kit, `validate_claude_setup.py <setup>` then checks the wiring points at a real
   script and flags orphans.)*

## The three safety laws (non-negotiable)
1. **Fail open.** Any parse error or unexpected shape → `return 0`. A hook must never
   wedge the session on its *own* bug. (Blocking on the bug you meant to catch is
   fine; blocking on a typo is not.)
2. **Be fast.** `PreToolUse` runs *synchronously before the tool* — it sits in the
   critical path. No network, no heavy work. Milliseconds.
3. **Advisory by default; blocking is opt-in.** Prefer exit 0 + a stdout note. Reserve
   exit 2 (and JSON `deny`) for genuine guards, and make the message tell Claude how
   to proceed, not just "no".

## Gotchas
- **The scaffold skeleton assumes a tool event.** `PostToolUse` also has
  `tool_response`; `UserPromptSubmit` has `prompt`, not `tool_input`. Match the parse
  to the event or the hook silently no-ops.
- **Exit 2 means different things per event** (blocks the call vs. just feeds Claude
  vs. blocks the prompt). Know which — `reference.md` has the table.
- **stdout is not always silent.** For `UserPromptSubmit`/`SessionStart`, exit-0
  stdout is *injected into context*; elsewhere it's shown in the transcript. Don't
  print noise.
- A hook is only as trustworthy as its test. An untested hook is a liability, not a guard.

## Deeper reference
Event taxonomy, exit-code semantics, stdin shapes per event, the advanced **JSON
output** control, settings wiring, the **archetype catalog**, and a critique of
common mistakes: read `reference.md` in this folder (loads on demand — costs no
routing budget). Two ready-to-adapt templates sit in `templates/`. Everything this
skill needs is bundled here — copy the folder and it works standalone.
