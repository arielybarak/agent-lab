# Hooks

This directory contains lightweight hook scripts that integrate with the agent pipeline.  
Each hook is a standalone Python 3 script with no external dependencies.

## Available Hooks

### `governance-audit`

Scans agent definition files (`.agent.md`) and governance policy YAML files for safety anti-patterns.  
Emits a JSON Lines audit report.

```bash
python hooks/governance-audit --path .github/agents --output audit.jsonl --fail-on critical
```

| Flag | Default | Description |
|------|---------|-------------|
| `--path` | `.github/agents` | Directory to scan |
| `--output` | `audit.jsonl` | Output JSON Lines report path |
| `--fail-on` | `critical` | Exit 1 when violations of this severity or above are found |

**Detected patterns:**
- Wildcard tool allowlist (`allowed_tools: ["*"]`)
- Hardcoded credentials
- Unrestricted shell execution
- Unlimited rate limits
- Disabled audit trails

---

### `session-auto-commit`

Stages all modified tracked files and creates a timestamped git commit.  
Call at the end of an agent session to ensure work is not lost.

```bash
python hooks/session-auto-commit --message "auto: end of session"
python hooks/session-auto-commit --dry-run   # preview what would be committed
```

---

### `session-logger`

Appends a structured JSON Lines entry to `session-logs/sessions.jsonl` for every agent event.

```bash
python hooks/session-logger --event start --agent my-agent
python hooks/session-logger --event end   --agent my-agent --outcome success
python hooks/session-logger --event error --agent my-agent --message "tool call failed"
```

Log entries include: timestamp, event type, agent name, outcome, git branch/commit, and PID.  
The `session-logs/` directory is gitignored — logs are local only.

---

## Integration with Agents

To register a hook with an agent, add a `hooks` section to the agent's `.agent.md` front-matter:

```yaml
---
name: 'My Agent'
tools: [...]
hooks:
  pre_session:  hooks/governance-audit
  post_session: hooks/session-auto-commit
  on_event:     hooks/session-logger
---
```

> **Note**: Hook execution is handled by the agent orchestrator. The hooks themselves are plain Python scripts and can also be run manually from the repository root.
