# Project Folder Structure

This document outlines the folder and file structure for the **enterprise-agent-platform/** project, detailing the architecture, components, and responsibilities of each directory and file as depicted in the project structure overview.

---

## Directory Tree

```text
enterprise-agent-platform/
├── README.md
├── CLAUDE.md
├── .env.example
├── agents/
│   ├── orchestrator/
│   │   ├── agent.py
│   │   └── policies.yaml
│   └── specialists/
│       ├── retrieval_agent/
│       ├── code_agent/
│       └── compliance_agent/
├── tools/
│   ├── registry.py
│   ├── definitions/
│   └── mcp_servers/
├── orchestration/
│   ├── graph.py
│   ├── state.py
│   └── router.py
├── prompts/
│   ├── library/
│   └── registry.yaml
├── api/
│   ├── routes/
│   ├── schemas/
│   ├── auth/
│   └── middleware/
├── governance/
│   ├── policies/
│   ├── guardrails/
│   └── audit/
├── evals/
│   ├── datasets/
│   ├── suites/
│   └── reports/
├── tests/
│   ├── unit/
│   └── integration/
└── docs/
    └── architecture/
```

---

## Component Overview & Descriptions

### Root Configuration Files

| File / Folder | Description |
| :--- | :--- |
| **`README.md`** | Project overview, setup instructions, architecture summary, and onboarding guide. |
| **`CLAUDE.md`** | AI coding assistant context including conventions, architecture rules, and development guidelines. |
| **`.env.example`** | Template of required environment variables without exposing secrets. |

---

### Core Directories & Subcomponents

#### `agents/`
Contains all AI agents including orchestration and specialized worker agents.

* **`orchestrator/`**: Central planner responsible for task decomposition, routing, and agent coordination.
  * `agent.py`
  * `policies.yaml`
* **`specialists/`**: Domain-specific agents that perform focused tasks such as retrieval, coding, and compliance checks.
  * `retrieval_agent/`
  * `code_agent/`
  * `compliance_agent/`

#### `tools/`
Registry and implementation of external tools, APIs, and MCP integrations available to agents.
* `registry.py`
* `definitions/`
* `mcp_servers/`

#### `orchestration/`
Defines agent workflows, execution graphs, routing logic, and shared runtime state.
* `graph.py`
* `state.py`
* `router.py`

#### `prompts/`
Centralized management of reusable prompts, templates, and prompt configurations.
* `library/`
* `registry.yaml`

#### `api/`
Service layer exposing agent capabilities through secure REST/streaming endpoints.
* `routes/`
* `schemas`
* `auth/`
* `middleware/`

#### `governance/`
Safety, compliance, auditing, and guardrail mechanisms for responsible AI operation.
* `policies/`
* `guardrails/`
* `audit/`

#### `evals/`
Evaluation framework for measuring agent performance, safety, accuracy, and regressions.
* `datasets/`
* `suites`
* `reports/`

#### `tests/`
Unit and integration tests ensuring reliability and correctness of platform components.
* `unit/`
* `integration/`

#### `docs/`
Architecture documentation, design decisions, and technical references.
* `architecture`
