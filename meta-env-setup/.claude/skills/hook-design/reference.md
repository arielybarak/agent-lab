# hook-design — deep-dive reference

On-demand companion to `SKILL.md`. The event/exit-code/JSON detail that the kit's
scaffold skeleton and cookbook templates assume but don't explain. Loads only when
you're actually building a hook.

> **Accuracy note (be critical about sources — including this one):** the
> **exit-code + stdin** mechanism below is stable and is what the kit's templates
> use — trust it. The **JSON-output** schema (§4) is more powerful but its exact
> field names have shifted across Claude Code versions — treat §4 as the shape, and
> verify field names against the current Claude Code hooks docs before relying on them.

---

## 1. Events — pick the one that fires when you need it

| Event | Fires… | Uses `matcher`? | Key stdin fields | Typical hook |
|---|---|---|---|---|
| **PreToolUse** | before a tool runs | yes (tool name) | `tool_name`, `tool_input` | guard / block (frozen path, secret) |
| **PostToolUse** | after a tool succeeds | yes | `tool_name`, `tool_input`, `tool_response` | lint/format check, reminder |
| **UserPromptSubmit** | when the user sends a prompt | no | `prompt` | inject context, block disallowed prompts |
| **Stop** | when Claude is about to finish | no | `stop_hook_active` | force a check before stopping |
| **SubagentStop** | when a subagent finishes | no | `stop_hook_active` | gate subagent output |
| **SessionStart** | session begins / resumes | no | `source` | load context into the session |
| **PreCompact** | before context compaction | no | — | preserve/log state |
| **Notification** | Claude emits a notification | no | `message` | desktop/Slack ping |

Plus session-end and others in newer versions — check the docs for the full current
list. Every payload also carries `session_id`, `cwd`, `transcript_path`,
`hook_event_name`.

## 2. Exit codes — the reliable control surface

| Exit | Meaning | What happens |
|---|---|---|
| **0** | success | stdout shown in the transcript. **Exception:** for `UserPromptSubmit` and `SessionStart`, exit-0 stdout is **injected into Claude's context**. |
| **2** | blocking error | stderr is routed per event (see below) |
| other | non-blocking error | stderr shown to the **user**; the flow continues |

**What exit 2 blocks, per event** (this is the part people get wrong):
- `PreToolUse` → **the tool call is blocked**; stderr is fed to Claude so it can adjust.
- `PostToolUse` → the tool already ran; stderr is fed to **Claude** (e.g. "you left a lint error — fix it").
- `UserPromptSubmit` → **the prompt is blocked** and not processed; stderr goes to the user.
- `Stop` / `SubagentStop` → **stopping is blocked**; Claude keeps going.
- `SessionStart` / `Notification` / `PreCompact` → nothing to block; exit 2 is effectively a non-blocking error.

## 3. stdin shapes (the minimum you parse)
```jsonc
// PreToolUse
{ "hook_event_name": "PreToolUse", "tool_name": "Edit",
  "tool_input": { "file_path": "src/x.py", "old_string": "…" } }
// PostToolUse — adds the result
{ "tool_name": "Bash", "tool_input": {…}, "tool_response": { "stdout": "…", "exit_code": 0 } }
// UserPromptSubmit — no tool_input!
{ "hook_event_name": "UserPromptSubmit", "prompt": "deploy to prod" }
```
**The #1 bug:** reading `tool_input.file_path` on a `UserPromptSubmit` hook → it's
always empty, the hook silently no-ops. Match the parse to the event.

## 4. JSON output — advanced, expressive control (verify field names)
Instead of exit codes, a hook may `print` a JSON object on stdout (and exit 0) to
control flow with a reason. The **shape**:
```jsonc
{ "continue": false,            // stop further processing
  "stopReason": "…",            // shown when continue=false
  "suppressOutput": true,       // hide this hook's stdout from the transcript
  // PreToolUse permission decision:
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",          // allow | deny | ask
    "permissionDecisionReason": "frozen path" },
  // UserPromptSubmit / SessionStart context injection:
  "hookSpecificOutput": { "additionalContext": "…" } }
```
Prefer **exit codes** for simple allow/block/advise (stable, obvious). Reach for JSON
only when you need a *reason* attached to a decision or to *inject context* — and
confirm the current field names first.

## 5. Wire it in settings.json
```jsonc
"hooks": {
  "PreToolUse": [
    { "matcher": "Edit|Write|MultiEdit",          // tool-name regex; "*" or "" = all
      "hooks": [ { "type": "command",
                   "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py\"" } ] }
  ]
}
```
- **Matcher** applies to tool events; alternation `A|B|C` and `*` work. Non-tool
  events (`UserPromptSubmit`, `Stop`, `SessionStart`) don't filter by matcher.
- Use **`$CLAUDE_PROJECT_DIR`** — never a machine-specific absolute path.
- The kit's validator checks the command points at a real script and flags orphans.

## 6. Test before you trust
```bash
# does it block what it should?
echo '{"tool_input":{"file_path":"project-A/top.sv"}}' | python .claude/hooks/guard.py; echo "exit=$?"  # want 2
# does it pass everything else?
echo '{"tool_input":{"file_path":"src/ok.py"}}'        | python .claude/hooks/guard.py; echo "exit=$?"  # want 0
# does it fail OPEN on garbage?
echo 'not json'                                        | python .claude/hooks/guard.py; echo "exit=$?"  # want 0
# (meta-env kit only) check the settings.json wiring points at a real script + flag orphans:
python tools/validate_claude_setup.py <setup>
```

## 7. Archetypes & bundled templates (self-contained)
This skill ships two ready-to-adapt templates in **`templates/`** — copy the whole
`hook-design/` folder and they come with it, no kit required.

| Archetype | Event · matcher | Behavior | Start from |
|---|---|---|---|
| **Frozen-region guard** | PreToolUse · `Edit\|Write\|MultiEdit` | **BLOCK** (exit 2) edits to a protected path | `templates/guard-hook.py` |
| **Quality/fairness nag** | PreToolUse · `Bash` | advise (exit 0 + stdout) before a risky command | `templates/advisory-hook.py` |
| **Wrong-place guard** | PreToolUse · `Edit\|Write` | advise when code lands in the wrong file | adapt `advisory-hook.py` (match `file_path`) |
| **Consistency reminder** | PostToolUse · `Edit` | nudge after editing a file type | adapt `advisory-hook.py` (read `tool_response`) |
| **Secret guard** | PreToolUse + settings `deny` | block reads/writes of secret files | `guard-hook.py` + `deny: Read(./.env)` |

**Adapt, critically:** both templates parse a *tool* event. For `UserPromptSubmit`
read `prompt`; for `PostToolUse` you also get `tool_response` (§3). Swap the
`PROTECTED_PREFIXES` / `NAGS` constants for your repo, then test (§6).

*(In the full meta-env kit, `cookbook/README.md` lists more archetypes and
`scaffold … add hook` generates a skeleton — handy, but not needed: the two bundled
templates already cover the blocking and advisory shapes.)*

## 8. Common mistakes (the critique)
1. **`tool_input` on a non-tool event** → silent no-op (§3).
2. **No fail-open** → one bad payload wedges the session (§safety law 1).
3. **Heavy/networked PreToolUse** → every tool call now waits on it.
4. **Blanket `matcher: "*"`** that fires on everything and slows the session.
5. **exit 2 on an advisory hook** → breaks a flow that only needed a nudge.
6. **Untested** → you find out it never fired (or always fired) in production.
7. **Absolute paths** instead of `$CLAUDE_PROJECT_DIR` → breaks on another machine.
8. **Expecting stdout to steer Claude** on an event where exit-0 stdout is transcript-only (§2).
