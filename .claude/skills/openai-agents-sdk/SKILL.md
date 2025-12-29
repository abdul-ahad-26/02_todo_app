---
name: openai-agents-sdk
description: Build AI-powered chatbots and conversational interfaces using OpenAI Agents SDK with MCP (Model Context Protocol) integration. Use this skill when building AI chatbots with natural language interfaces, agents that need to call external tools/APIs, stateless agent architectures with database-backed conversations, applications integrating OpenAI Agents SDK with FastAPI backends, MCP servers that expose operations to agents, chat interfaces using OpenAI ChatKit, or multi-turn tool-calling workflows where agents execute multiple operations.
---

# OpenAI Agents SDK

Build production-ready AI agents with tools, handoffs, guardrails, and multi-agent orchestration.

## Quick Start

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 72°F"

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant.",
    tools=[get_weather]
)

result = Runner.run_sync(agent, "What's the weather in Tokyo?")
print(result.final_output)
```

## Core Concepts

### 1. Agents

Agents combine an LLM with instructions and tools:

```python
from agents import Agent, ModelSettings

agent = Agent(
    name="analyst",
    instructions="Analyze data and provide insights.",
    model="gpt-4o",
    model_settings=ModelSettings(temperature=0.7),
    tools=[my_tool],
    handoffs=[other_agent]
)
```

**Dynamic instructions** - personalize based on context:

```python
def get_instructions(agent, context):
    return f"Help {context.context.user_name} with their request."

agent = Agent(name="helper", instructions=get_instructions)
```

### 2. Tools

Three tool types available:

**Function tools** - Python functions as tools:

```python
from agents import function_tool

@function_tool
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database for matching records."""
    return db.search(query, limit=limit)
```

**Hosted tools** - OpenAI-managed tools:

```python
from agents import Agent
from agents.tools import WebSearchTool, CodeInterpreterTool

agent = Agent(
    name="researcher",
    tools=[WebSearchTool(), CodeInterpreterTool()]
)
```

**Agents as tools** - use agents without handoff:

```python
specialist = Agent(name="specialist", instructions="...")
main_agent = Agent(
    name="main",
    tools=[specialist.as_tool(
        tool_name="consult_specialist",
        tool_description="Get specialist advice"
    )]
)
```

### 3. Handoffs

Enable agent-to-agent delegation:

```python
from agents import Agent, handoff

refund_agent = Agent(name="refund_specialist", instructions="Handle refunds.")
support_agent = Agent(
    name="support",
    instructions="Route to specialists as needed.",
    handoffs=[refund_agent]  # Creates transfer_to_refund_specialist tool
)
```

**Custom handoffs** with callbacks:

```python
from agents import handoff
from pydantic import BaseModel

class EscalationReason(BaseModel):
    reason: str
    priority: int

def on_escalate(context, input_data: EscalationReason):
    log_escalation(input_data.reason, input_data.priority)

custom_handoff = handoff(
    agent=escalation_agent,
    on_handoff=on_escalate,
    input_type=EscalationReason
)
```

### 4. Running Agents

```python
from agents import Runner

# Async
result = await Runner.run(agent, "Hello!")

# Sync
result = Runner.run_sync(agent, "Hello!")

# Streaming
async for event in Runner.run_streamed(agent, "Hello!").stream_events():
    if event.type == "raw_response_event":
        print(event.data, end="", flush=True)
```

### 5. Context Management

Pass state to tools via context:

```python
from dataclasses import dataclass
from agents import Agent, Runner, function_tool, RunContextWrapper

@dataclass
class AppContext:
    user_id: str
    db: Database

@function_tool
def get_orders(context: RunContextWrapper[AppContext]) -> list:
    """Get user's orders."""
    return context.context.db.get_orders(context.context.user_id)

ctx = AppContext(user_id="123", db=my_db)
result = Runner.run_sync(agent, "Show my orders", context=ctx)
```

### 6. Guardrails

Validate inputs and outputs:

```python
from agents import Agent, input_guardrail, output_guardrail, GuardrailFunctionOutput

@input_guardrail
async def check_harmful(context, agent, input) -> GuardrailFunctionOutput:
    # Use classifier to detect harmful content
    is_harmful = await classify(input)
    return GuardrailFunctionOutput(
        output_info={"harmful": is_harmful},
        tripwire_triggered=is_harmful
    )

agent = Agent(
    name="safe_assistant",
    input_guardrails=[check_harmful]
)
```

## MCP Integration

Connect agents to MCP servers for extended capabilities.

**Stdio server** (local):

```python
from agents import Agent
from agents.mcp import MCPServerStdio

server = MCPServerStdio(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path"]
)

async with server:
    tools = await server.list_tools()
    agent = Agent(name="file_agent", tools=tools)
```

**HTTP server** (remote):

```python
from agents.mcp import MCPServerStreamableHttp

server = MCPServerStreamableHttp(
    name="api_server",
    url="https://api.example.com/mcp",
    headers={"Authorization": "Bearer token"}
)
```

**Tool filtering**:

```python
from agents.mcp import create_static_tool_filter

filter = create_static_tool_filter(
    allowed_tool_names=["read_file", "write_file"]
)
tools = await server.list_tools(tool_filter=filter)
```

## Multi-Agent Patterns

### Orchestrator Pattern

```python
triage = Agent(
    name="triage",
    instructions="Route requests to the appropriate specialist.",
    handoffs=[billing_agent, tech_agent, sales_agent]
)
```

### Pipeline Pattern

```python
async def pipeline(query: str):
    research = await Runner.run(researcher, query)
    analysis = await Runner.run(analyst, research.final_output)
    return await Runner.run(writer, analysis.final_output)
```

### Parallel Execution

```python
import asyncio

results = await asyncio.gather(
    Runner.run(agent1, task1),
    Runner.run(agent2, task2),
    Runner.run(agent3, task3)
)
```

## Sessions & Persistence

Automatic conversation management:

```python
from agents.extensions.sessions import SQLiteSession

session = SQLiteSession("conversations.db")

# First turn
result1 = await Runner.run(agent, "Hi, I'm Alice", session=session)

# Subsequent turn - history preserved
result2 = await Runner.run(agent, "What's my name?", session=session)
```

## Tracing & Debugging

Built-in observability:

```python
from agents import RunConfig

config = RunConfig(
    tracing_disabled=False,
    trace_include_sensitive_data=True
)
result = await Runner.run(agent, input, run_config=config)
```

Disable tracing: `OPENAI_AGENTS_DISABLE_TRACING=1`

## External Models (Non-OpenAI)

Use any LLM provider via `OpenAIChatCompletionsModel` with `AsyncOpenAI` client.

### Recommended Pattern

```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
import os

# 1. Create client with provider's base_url
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 2. Create model
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)

# 3. Configure RunConfig (disable tracing for non-OpenAI)
run_config = RunConfig(model=model, tracing_disabled=True)

# 4. Run agent
agent = Agent(name="assistant", instructions="You are helpful.")
result = await Runner.run(agent, "Hello!", run_config=run_config)
```

### Provider Base URLs

| Provider | Base URL | Model Example |
|----------|----------|---------------|
| Gemini | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-2.5-flash` |
| OpenRouter | `https://openrouter.ai/api/v1` | `anthropic/claude-3.5-sonnet` |
| Groq | `https://api.groq.com/openai/v1` | `llama-3.1-70b-versatile` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| Ollama | `http://localhost:11434/v1` | `llama3.1` |

### LiteLLM Alternative

```bash
pip install "openai-agents[litellm]"
```

```python
from agents.extensions.models.litellm_model import LitellmModel

agent = Agent(
    name="assistant",
    model=LitellmModel(model="anthropic/claude-3-5-sonnet-20240620")
)
```

See **[references/external-models.md](references/external-models.md)** for complete examples and troubleshooting.

## Reference Documentation

For detailed API information, see:

- **[references/tools-reference.md](references/tools-reference.md)** - Complete tools API, hosted tools, custom implementations
- **[references/multi-agent-patterns.md](references/multi-agent-patterns.md)** - Orchestration patterns, evaluation loops, agent chaining
- **[references/mcp-integration.md](references/mcp-integration.md)** - MCP server types, filtering, prompts, caching
- **[references/external-models.md](references/external-models.md)** - LiteLLM, OpenRouter, Anthropic, Gemini, local models

## Common Patterns

### Structured Output

```python
from pydantic import BaseModel

class Analysis(BaseModel):
    sentiment: str
    confidence: float
    summary: str

agent = Agent(
    name="analyzer",
    instructions="Analyze the sentiment.",
    output_type=Analysis
)

result = Runner.run_sync(agent, "I love this product!")
print(result.final_output.sentiment)  # "positive"
```

### Error Handling

```python
from agents.exceptions import (
    MaxTurnsExceeded,
    InputGuardrailTripwireTriggered,
    ModelBehaviorError
)

try:
    result = await Runner.run(agent, input)
except MaxTurnsExceeded:
    print("Agent reached turn limit")
except InputGuardrailTripwireTriggered:
    print("Input blocked by guardrail")
except ModelBehaviorError as e:
    print(f"Model error: {e}")
```

### Tool Error Handling

```python
@function_tool(failure_error_function=lambda ctx, err: f"Tool failed: {err}")
def risky_operation(data: str) -> str:
    """Perform operation that might fail."""
    return process(data)
```
