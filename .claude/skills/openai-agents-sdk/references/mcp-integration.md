# MCP Integration Guide

Complete guide to integrating Model Context Protocol (MCP) servers with the OpenAI Agents SDK.

## Table of Contents

1. [Overview](#overview)
2. [Server Types](#server-types)
3. [Tool Filtering](#tool-filtering)
4. [Prompts](#prompts)
5. [Configuration Options](#configuration-options)
6. [Common Patterns](#common-patterns)

## Overview

MCP standardizes how applications expose tools and context to LLMs. The SDK supports four transport types:

| Type | Class | Use Case |
|------|-------|----------|
| Hosted | `HostedMCPTool` | Remote servers via OpenAI infrastructure |
| Streamable HTTP | `MCPServerStreamableHttp` | HTTP servers you control |
| SSE | `MCPServerSse` | Server-Sent Events transport |
| Stdio | `MCPServerStdio` | Local subprocess servers |

## Server Types

### Hosted MCP Servers

Use OpenAI's infrastructure to connect to remote MCP servers:

```python
from agents.tools import HostedMCPTool

# Basic usage
tool = HostedMCPTool(server_label="filesystem")

# With authentication (for connector-backed servers)
tool = HostedMCPTool(
    server_label="my-connector",
    server_url="https://api.example.com/mcp",
    require_approval="never"  # "always" | "never" | custom function
)

agent = Agent(name="assistant", tools=[tool])
```

**Approval workflows:**

```python
# Always require approval
tool = HostedMCPTool(server_label="dangerous", require_approval="always")

# Never require approval
tool = HostedMCPTool(server_label="safe", require_approval="never")

# Custom approval logic
async def should_approve(tool_name: str, args: dict) -> bool:
    if tool_name == "delete_file":
        return False  # Never approve deletions
    return True

tool = HostedMCPTool(server_label="filesystem", require_approval=should_approve)
```

### Streamable HTTP Servers

Connect to HTTP-based MCP servers:

```python
from agents.mcp import MCPServerStreamableHttp

server = MCPServerStreamableHttp(
    name="api_server",
    url="https://api.example.com/mcp",
    headers={"Authorization": "Bearer token"},
    timeout=30.0,
    cache_tools_list=True  # Cache tool list for performance
)

async with server:
    tools = await server.list_tools()
    agent = Agent(name="assistant", tools=tools)
    result = await Runner.run(agent, "Use the API")
```

**Configuration options:**

```python
server = MCPServerStreamableHttp(
    name="configured_server",
    url="https://api.example.com/mcp",

    # Authentication
    headers={"Authorization": "Bearer token", "X-API-Key": "key"},

    # Timeouts
    timeout=60.0,

    # Caching
    cache_tools_list=True,

    # Retry configuration
    max_retries=3,
    retry_backoff=1.0
)
```

### SSE Servers

Connect via Server-Sent Events:

```python
from agents.mcp import MCPServerSse

server = MCPServerSse(
    name="sse_server",
    url="https://api.example.com/sse",
    headers={"Authorization": "Bearer token"},
    timeout=30.0
)

async with server:
    tools = await server.list_tools()
    agent = Agent(name="assistant", tools=tools)
```

### Stdio Servers

Launch local MCP servers as subprocesses:

```python
from agents.mcp import MCPServerStdio

# Using npx
server = MCPServerStdio(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
)

# Using Python
server = MCPServerStdio(
    name="custom",
    command="python",
    args=["-m", "my_mcp_server"],
    env={"API_KEY": "secret"}
)

async with server:
    tools = await server.list_tools()
    agent = Agent(name="assistant", tools=tools)
    result = await Runner.run(agent, "List files in the directory")
```

**Popular MCP servers via npx:**

```python
# Filesystem access
filesystem = MCPServerStdio(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path"]
)

# GitHub integration
github = MCPServerStdio(
    name="github",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]}
)

# PostgreSQL
postgres = MCPServerStdio(
    name="postgres",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-postgres"],
    env={"DATABASE_URL": os.environ["DATABASE_URL"]}
)
```

## Tool Filtering

Control which MCP tools are exposed to agents.

### Static Filtering

Allow/block specific tools:

```python
from agents.mcp import create_static_tool_filter

# Allow only specific tools
allow_filter = create_static_tool_filter(
    allowed_tool_names=["read_file", "list_directory"]
)

# Block specific tools
block_filter = create_static_tool_filter(
    blocked_tool_names=["delete_file", "write_file"]
)

# Combine allow and block
combined_filter = create_static_tool_filter(
    allowed_tool_names=["read_file", "write_file", "list_directory"],
    blocked_tool_names=["delete_file"]
)

tools = await server.list_tools(tool_filter=allow_filter)
```

### Dynamic Filtering

Context-aware filtering:

```python
from agents.mcp import ToolFilterContext

def dynamic_filter(context: ToolFilterContext) -> bool:
    tool_name = context.tool_name

    # Block dangerous operations for non-admin users
    if tool_name in ["delete_file", "execute_command"]:
        return context.run_context.context.is_admin

    # Allow all other tools
    return True

tools = await server.list_tools(tool_filter=dynamic_filter)
```

### Role-Based Filtering

```python
def role_based_filter(context: ToolFilterContext) -> bool:
    user_role = context.run_context.context.user_role
    tool = context.tool_name

    role_permissions = {
        "viewer": ["read_file", "list_directory", "search"],
        "editor": ["read_file", "list_directory", "search", "write_file"],
        "admin": ["read_file", "list_directory", "search", "write_file", "delete_file"]
    }

    allowed = role_permissions.get(user_role, [])
    return tool in allowed

tools = await server.list_tools(tool_filter=role_based_filter)
```

## Prompts

MCP servers can provide dynamic prompts for agents.

### Listing Prompts

```python
async with server:
    prompts = await server.list_prompts()
    for prompt in prompts:
        print(f"- {prompt.name}: {prompt.description}")
```

### Using Prompts

```python
async with server:
    # Get a specific prompt
    prompt = await server.get_prompt(
        name="code_review",
        arguments={"language": "python", "style": "detailed"}
    )

    # Use prompt content in agent instructions
    agent = Agent(
        name="reviewer",
        instructions=prompt.content
    )
```

### Dynamic Instructions from MCP

```python
async def get_dynamic_instructions(agent, context):
    # Fetch latest prompt from MCP server
    prompt = await context.context.mcp_server.get_prompt(
        name="assistant_prompt",
        arguments={"user_tier": context.context.user_tier}
    )
    return prompt.content

agent = Agent(
    name="assistant",
    instructions=get_dynamic_instructions
)
```

## Configuration Options

### Caching

Enable tool list caching for frequently-used servers:

```python
server = MCPServerStreamableHttp(
    name="cached_server",
    url="https://api.example.com/mcp",
    cache_tools_list=True  # Cache tool definitions
)
```

### Timeouts

Configure connection and operation timeouts:

```python
server = MCPServerStreamableHttp(
    name="server",
    url="https://api.example.com/mcp",
    timeout=60.0  # 60 second timeout
)
```

### Retries

Configure retry behavior for transient failures:

```python
server = MCPServerStreamableHttp(
    name="resilient_server",
    url="https://api.example.com/mcp",
    max_retries=5,
    retry_backoff=2.0  # Exponential backoff base
)
```

## Common Patterns

### Multiple MCP Servers

Combine tools from multiple servers:

```python
async def create_agent_with_mcp():
    filesystem = MCPServerStdio(
        name="filesystem",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/data"]
    )

    database = MCPServerStreamableHttp(
        name="database",
        url="https://db.example.com/mcp"
    )

    async with filesystem, database:
        fs_tools = await filesystem.list_tools()
        db_tools = await database.list_tools()

        agent = Agent(
            name="data_assistant",
            instructions="Help users work with files and database.",
            tools=fs_tools + db_tools
        )

        return await Runner.run(agent, "Query the database and save to file")
```

### MCP with Context

Pass application context to MCP tool execution:

```python
from dataclasses import dataclass

@dataclass
class AppContext:
    user_id: str
    permissions: list[str]
    mcp_server: MCPServerStreamableHttp

async def main():
    server = MCPServerStreamableHttp(
        name="api",
        url="https://api.example.com/mcp"
    )

    async with server:
        tools = await server.list_tools(
            tool_filter=lambda ctx: ctx.tool_name in ctx.run_context.context.permissions
        )

        ctx = AppContext(
            user_id="123",
            permissions=["read", "list"],
            mcp_server=server
        )

        agent = Agent(name="assistant", tools=tools)
        result = await Runner.run(agent, "Show my data", context=ctx)
```

### MCP Server Management

Create a manager for multiple servers:

```python
class MCPManager:
    def __init__(self):
        self.servers = {}

    async def add_server(self, name: str, server):
        self.servers[name] = server
        await server.__aenter__()

    async def get_all_tools(self, filter_func=None):
        all_tools = []
        for server in self.servers.values():
            tools = await server.list_tools(tool_filter=filter_func)
            all_tools.extend(tools)
        return all_tools

    async def close_all(self):
        for server in self.servers.values():
            await server.__aexit__(None, None, None)

# Usage
manager = MCPManager()
await manager.add_server("fs", filesystem_server)
await manager.add_server("db", database_server)

tools = await manager.get_all_tools()
agent = Agent(name="assistant", tools=tools)
```

### Error Handling

Handle MCP server errors gracefully:

```python
from agents.mcp import MCPServerError

async def safe_mcp_operation():
    try:
        async with server:
            tools = await server.list_tools()
            agent = Agent(name="assistant", tools=tools)
            return await Runner.run(agent, input)
    except MCPServerError as e:
        print(f"MCP server error: {e}")
        # Fall back to agent without MCP tools
        fallback = Agent(name="assistant", instructions="...")
        return await Runner.run(fallback, input)
    except ConnectionError:
        print("Could not connect to MCP server")
        raise
```

### Tracing MCP Operations

MCP activity is automatically traced:

```python
from agents import RunConfig

config = RunConfig(
    tracing_disabled=False,
    trace_include_sensitive_data=True,
    workflow_name="mcp_workflow"
)

async with server:
    tools = await server.list_tools()
    agent = Agent(name="assistant", tools=tools)
    result = await Runner.run(agent, input, run_config=config)

# Traces include:
# - Tool listing operations
# - Tool execution details
# - Server connection events
```
