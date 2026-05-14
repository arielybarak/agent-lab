---
name: agent-governance
description: |
  Patterns and techniques for adding governance, safety, and trust controls to AI agent systems. Use this skill when:
  - Building AI agents that call external tools (APIs, databases, file systems)
  - Implementing policy-based access controls for agent tool usage
  - Adding semantic intent classification to detect dangerous prompts
  - Creating trust scoring systems for multi-agent workflows
  - Building audit trails for agent actions and decisions
  - Enforcing rate limits, content filters, or tool restrictions on agents
  - Working with any agent framework (PydanticAI, CrewAI, OpenAI Agents, LangChain, AutoGen)
---

# Agent Governance Patterns

Patterns for adding safety, trust, and policy enforcement to AI agent systems.

## Overview

Governance patterns ensure AI agents operate within defined boundaries — controlling which tools they can call, what content they can process, how much they can do, and maintaining accountability through audit trails.

```
User Request → Intent Classification → Policy Check → Tool Execution → Audit Log
                     ↓                      ↓               ↓
              Threat Detection         Allow/Deny      Trust Update
```

## When to Use

- **Agents with tool access**: Any agent that calls external tools (APIs, databases, shell commands)
- **Multi-agent systems**: Agents delegating to other agents need trust boundaries
- **Production deployments**: Compliance, audit, and safety requirements
- **Sensitive operations**: Financial transactions, data access, infrastructure management

---

## Pattern 1: Governance Policy

Define what an agent is allowed to do as a composable, serializable policy object.

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import re

class PolicyAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"  # flag for human review

@dataclass
class GovernancePolicy:
    """Declarative policy controlling agent behavior."""
    name: str
    allowed_tools: list[str] = field(default_factory=list)       # allowlist
    blocked_tools: list[str] = field(default_factory=list)       # blocklist
    blocked_patterns: list[str] = field(default_factory=list)    # content filters
    max_calls_per_request: int = 100                             # rate limit
    require_human_approval: list[str] = field(default_factory=list)  # tools needing approval

    def check_tool(self, tool_name: str) -> PolicyAction:
        """Check if a tool is allowed by this policy."""
        if tool_name in self.blocked_tools:
            return PolicyAction.DENY
        if tool_name in self.require_human_approval:
            return PolicyAction.REVIEW
        if self.allowed_tools and tool_name not in self.allowed_tools:
            return PolicyAction.DENY
        return PolicyAction.ALLOW

    def check_content(self, content: str) -> Optional[str]:
        """Check content against blocked patterns. Returns matched pattern or None."""
        for pattern in self.blocked_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return pattern
        return None
```

### Policy Composition

Combine multiple policies (e.g., org-wide + team + agent-specific):

```python
def compose_policies(*policies: GovernancePolicy) -> GovernancePolicy:
    """Merge policies with most-restrictive-wins semantics."""
    combined = GovernancePolicy(name="composed")

    for policy in policies:
        combined.blocked_tools.extend(policy.blocked_tools)
        combined.blocked_patterns.extend(policy.blocked_patterns)
        combined.require_human_approval.extend(policy.require_human_approval)
        combined.max_calls_per_request = min(
            combined.max_calls_per_request,
            policy.max_calls_per_request
        )
        if policy.allowed_tools:
            if combined.allowed_tools:
                combined.allowed_tools = [
                    t for t in combined.allowed_tools if t in policy.allowed_tools
                ]
            else:
                combined.allowed_tools = list(policy.allowed_tools)

    return combined
```

### Policy as YAML

Store policies as configuration, not code:

```yaml
# governance-policy.yaml
name: production-agent
allowed_tools:
  - search_documents
  - query_database
  - send_email
blocked_tools:
  - shell_exec
  - delete_record
blocked_patterns:
  - "(?i)(api[_-]?key|secret|password)\\s*[:=]"
  - "(?i)(drop|truncate|delete from)\\s+\\w+"
max_calls_per_request: 25
require_human_approval:
  - send_email
```

---

## Pattern 2: Semantic Intent Classification

Detect dangerous intent in prompts before they reach the agent.

```python
THREAT_SIGNALS = [
    (r"(?i)send\s+(all|every|entire)\s+\w+\s+to\s+", "data_exfiltration", 0.8),
    (r"(?i)(sudo|as\s+root|admin\s+access)", "privilege_escalation", 0.8),
    (r"(?i)(rm\s+-rf|del\s+/[sq]|format\s+c:)", "system_destruction", 0.95),
    (r"(?i)ignore\s+(previous|above|all)\s+(instructions?|rules?)", "prompt_injection", 0.9),
]

def is_safe(content: str, threshold: float = 0.7) -> bool:
    """Quick check: is the content safe above the given threshold?"""
    for pattern, _, weight in THREAT_SIGNALS:
        if re.search(pattern, content) and weight >= threshold:
            return False
    return True
```

---

## Pattern 3: Tool-Level Governance Decorator

Wrap individual tool functions with governance checks.
**Note**: This decorator is designed for `async` tool functions.
For synchronous tools, remove the `await` and drop the `async` keywords.

```python
import functools

def govern(policy: GovernancePolicy, audit_trail=None):
    """Decorator that enforces governance policy on an async tool function."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tool_name = func.__name__
            action = policy.check_tool(tool_name)
            if action == PolicyAction.DENY:
                raise PermissionError(f"Policy '{policy.name}' blocks tool '{tool_name}'")
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, str):
                    matched = policy.check_content(arg)
                    if matched:
                        raise PermissionError(f"Blocked pattern detected: {matched}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## Pattern 4: Trust Scoring

Track agent reliability over time with decay-based trust scores:

```python
@dataclass
class TrustScore:
    score: float = 0.5
    successes: int = 0
    failures: int = 0

    def record_success(self, reward: float = 0.05):
        self.score = min(1.0, self.score + reward * (1 - self.score))

    def record_failure(self, penalty: float = 0.15):
        self.score = max(0.0, self.score - penalty * self.score)
```

---

## Governance Levels

| Level | Controls | Use Case |
|-------|----------|----------|
| **Open** | Audit only, no restrictions | Internal dev/testing |
| **Standard** | Tool allowlist + content filters | General production agents |
| **Strict** | All controls + human approval for sensitive ops | Financial, healthcare, legal |
| **Locked** | Allowlist only, no dynamic tools, full audit | Compliance-critical systems |

---

## Best Practices

| Practice | Rationale |
|----------|-----------|
| **Policy as configuration** | Store policies in YAML/JSON, not hardcoded |
| **Most-restrictive-wins** | When composing policies, deny always overrides allow |
| **Pre-flight intent check** | Classify intent *before* tool execution |
| **Trust decay** | Trust scores should decay over time |
| **Append-only audit** | Never modify or delete audit entries |
| **Fail closed** | If governance check errors, deny the action |

---

## Quick Start Checklist

```markdown
## Agent Governance Implementation Checklist

### Setup
- [ ] Define governance policy (allowed tools, blocked patterns, rate limits)
- [ ] Choose governance level (open/standard/strict/locked)
- [ ] Set up audit trail storage

### Implementation
- [ ] Add @govern decorator to all tool functions
- [ ] Add intent classification to user input processing
- [ ] Implement trust scoring for multi-agent interactions
- [ ] Wire up audit trail export

### Validation
- [ ] Test that blocked tools are properly denied
- [ ] Test that content filters catch sensitive patterns
- [ ] Test rate limiting behavior
- [ ] Verify audit trail captures all events
```
