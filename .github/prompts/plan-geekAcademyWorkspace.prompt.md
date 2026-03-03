### Plan: GeekAcademy Agent Workspace Setup

**1. Install Sub-Agents from Awesome Copilot**
Fetch `.agent.md` files directly from the Awesome Copilot repository and place them in an `agents/` folder in the workspace:
* **Sensei Junior Mentor (`mentoring-juniors.agent.md`)**: A Socratic mentor for Computer Engineering students that guides you to the answer instead of blindly printing code.
* **SWE Subagent (`swe-subagent.agent.md`)**: A Senior Software Engineer agent for feature development and clean code.
* **Security Reviewer (`se-security-reviewer.agent.md`)**: Your Code Reviewer focused on OWASP, Zero Trust, and best practices.
* **Polyglot Test Generator (`polyglot-test-generator.agent.md`)**: Analyzes code, plans, and writes unit tests in C++ or Python.

**2. Scaffold the MCP Server**
Create the `mcp-server/` directory and install the official `@modelcontextprotocol/sdk`. This will serve as a blank canvas allowing your agents to dynamically query the GeekAcademy course materials moving forward.

**3. Execution Script**
```bash
# 1. Create the agents directory and download the awesome-copilot agents
mkdir -p agents
echo "Downloading Custom Agents..."
curl -s -o agents/mentoring-juniors.agent.md https://raw.githubusercontent.com/github/awesome-copilot/main/agents/mentoring-juniors.agent.md
curl -s -o agents/se-security-reviewer.agent.md https://raw.githubusercontent.com/github/awesome-copilot/main/agents/se-security-reviewer.agent.md
curl -s -o agents/polyglot-test-generator.agent.md https://raw.githubusercontent.com/github/awesome-copilot/main/agents/polyglot-test-generator.agent.md
curl -s -o agents/swe-subagent.agent.md https://raw.githubusercontent.com/github/awesome-copilot/main/agents/swe-subagent.agent.md

# 2. Scaffold the basic MCP Server for future RAG / Document querying
echo "Scaffolding MCP Server environment..."
mkdir -p mcp-server/src
cd mcp-server

# Initialize Node.js project and install MCP SDK dependencies
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node

# Create boilerplate MCP Server logic
cat << 'EOF' > src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
    name: "geekacademy-rag-server",
    version: "1.0.0",
}, {
    capabilities: { tools: {} }
});

async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("GeekAcademy RAG MCP Server running on stdio");
}

main().catch(console.error);
EOF

echo "All complete! The agents are installed and the MCP server is initialized."
```
