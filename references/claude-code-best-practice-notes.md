

Direct from Boris Cherny and team:
→ Always use plan mode, give Claude a way to verify
→ Ask Claude to interview you using AskUserQuestion tool
→ Use Git Worktrees for parallel development
→ /loop - schedule recurring tasks for up to 7 days
→ Code Review - fresh context windows catch bugs the original agent missed
→ Make phase-wise gated plans with tests for each phase
→ Use cross-model (Claude Code + Codex) to review your plan
→ CLAUDE[.]md should target under 200 lines per file
→ Use commands for workflows instead of sub-agents
→ Have feature-specific sub-agents with skills instead of general QA or backend engineer
→ Vanilla Claude Code is better than complex workflows for smaller tasks
→ Take screenshots and share with Claude when stuck
→ Use MCP to let Claude see Chrome console logs
→ Ask Claude to run terminal as background task for better debugging
→ Use cross-model for QA - e.g. Codex for plan and implementation review
→ Context rot kicks in around 300-400k tokens, don't let sessions drift past that
→ Rewind > correct, /rewind back to before the failed attempt instead of polluting context
→ /schedule - cloud-based recurring tasks that run even when your machine is off
→ Auto mode instead of dangerously-skip-permissions, a model-based classifier decides if each command is safe
→ Build a Gotchas section in every skill, add Claude's failure points over time

The community workflows included:
→ Superpowers (234K stars), brainstorming → git worktrees → subagent-driven development → TDD
→ Everything Claude Code (219K stars), /ecc:plan → /tdd → /code-review → /security-scan → merge
→ Matt Pocock Skills (138K stars), /grill-with-docs → /to-prd → /triage → /tdd → /handoff
→ Spec Kit (114K stars), specify → clarify → plan → tasks → implement → analyze
→ gstack (112K stars), office-hours → CEO/eng/design reviews → spec → qa → ship → canary
→ Cross-Model (Claude Code + Codex) Workflow
→ RPI (Research Plan Implement)
→ Ralph Wiggum Loop for autonomous tasks

The billion-dollar questions it addresses:
→ What exactly should you put inside CLAUDE[.]md, and what should you leave out?
→ When should you use command vs agent vs skill?
→ Why does Claude still ignore CLAUDE[.]md instructions, even when they say MUST in all caps?
→ Can we convert a codebase into specs and have AI regenerate the exact same code from those specs alone?
→ Should you rely on Claude Code's built-in plan mode, or build your own planning command?

The daily habits:
→ Update Claude Code daily
→ Start your day by reading the changelog
→ Follow r/ClaudeAI, r/ClaudeCode on Reddit
