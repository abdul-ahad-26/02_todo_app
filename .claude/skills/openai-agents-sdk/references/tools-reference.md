# Tools Reference

Complete guide to tools in the OpenAI Agents SDK.

## Table of Contents

1. [Function Tools](#function-tools)
2. [Hosted Tools](#hosted-tools)
3. [Agents as Tools](#agents-as-tools)
4. [Custom Tool Implementation](#custom-tool-implementation)
5. [Tool Configuration](#tool-configuration)

## Function Tools

Convert Python functions to agent tools using the `@function_tool` decorator.

### Basic Usage

```python
from agents import function_tool

@function_tool
def calculate_price(quantity: int, unit_price: float, discount: float = 0) -> float:
    """Calculate total price with optional discount.

    Args:
        quantity: Number of items
        unit_price: Price per item
        discount: Discount percentage (0-100)

    Returns:
        Final price after discount
    """
    total = quantity * unit_price
    return total * (1 - discount / 100)
```

The SDK automatically:
- Extracts function name as tool identifier
- Parses docstring for description (using `griffe` library)
- Generates JSON schema from type hints
- Creates argument descriptions from docstring

### Async Function Tools

```python
@function_tool
async def fetch_user_data(user_id: str) -> dict:
    """Fetch user data from the database."""
    async with db.connection() as conn:
        return await conn.get_user(user_id)
```

### Context-Aware Tools

Access runtime context via `RunContextWrapper`:

```python
from agents import function_tool, RunContextWrapper

@function_tool
def get_user_preferences(context: RunContextWrapper[AppContext]) -> dict:
    """Get current user's preferences."""
    user_id = context.context.user_id
    return context.context.db.get_preferences(user_id)
```

### ToolContext for Metadata

Access tool execution metadata:

```python
from agents import function_tool, ToolContext

@function_tool
def log_and_execute(context: ToolContext, query: str) -> str:
    """Execute query with logging."""
    print(f"Tool: {context.tool_name}")
    print(f"Call ID: {context.tool_call_id}")
    print(f"Arguments: {context.tool_arguments}")
    return execute_query(query)
```

### Error Handling

Custom error messages for the LLM:

```python
@function_tool(failure_error_function=lambda ctx, err: f"Database error: {err}")
def query_database(sql: str) -> list:
    """Execute SQL query."""
    return db.execute(sql)
```

## Hosted Tools

OpenAI-managed tools available with `OpenAIResponsesModel`.

### WebSearchTool

```python
from agents.tools import WebSearchTool

agent = Agent(
    name="researcher",
    tools=[WebSearchTool()]
)
```

### CodeInterpreterTool

Execute Python code in sandboxed environment:

```python
from agents.tools import CodeInterpreterTool

agent = Agent(
    name="analyst",
    tools=[CodeInterpreterTool()]
)
```

### FileSearchTool

Search OpenAI Vector Stores:

```python
from agents.tools import FileSearchTool

agent = Agent(
    name="doc_searcher",
    tools=[FileSearchTool(vector_store_ids=["vs_abc123"])]
)
```

### ImageGenerationTool

Generate images from prompts:

```python
from agents.tools import ImageGenerationTool

agent = Agent(
    name="artist",
    tools=[ImageGenerationTool()]
)
```

### LocalShellTool

Run shell commands locally:

```python
from agents.tools import LocalShellTool

agent = Agent(
    name="sysadmin",
    tools=[LocalShellTool()]
)
```

### ComputerTool

Automate computer use tasks:

```python
from agents.tools import ComputerTool

agent = Agent(
    name="automation",
    tools=[ComputerTool()]
)
```

### HostedMCPTool

Expose remote MCP server tools:

```python
from agents.tools import HostedMCPTool

agent = Agent(
    name="mcp_agent",
    tools=[HostedMCPTool(server_label="my-server")]
)
```

## Agents as Tools

Use specialized agents without full handoff:

```python
# Specialist agent
math_expert = Agent(
    name="math_expert",
    instructions="You are a mathematics expert. Solve problems step by step."
)

# Main agent uses specialist as tool
main_agent = Agent(
    name="assistant",
    instructions="Help users with various tasks.",
    tools=[
        math_expert.as_tool(
            tool_name="solve_math",
            tool_description="Get help solving mathematical problems"
        )
    ]
)
```

### Custom Output Extraction

```python
def extract_answer(output: str) -> str:
    """Extract just the final answer."""
    lines = output.strip().split('\n')
    return lines[-1]

main_agent = Agent(
    name="assistant",
    tools=[
        math_expert.as_tool(
            tool_name="solve_math",
            tool_description="Solve math problems",
            custom_output_extractor=extract_answer
        )
    ]
)
```

### Streaming Events

```python
async def handle_events(event):
    print(f"Expert event: {event}")

main_agent = Agent(
    name="assistant",
    tools=[
        expert.as_tool(
            tool_name="consult_expert",
            on_stream=handle_events
        )
    ]
)
```

### Conditional Enabling

```python
def should_enable_expert(context) -> bool:
    return context.context.user_tier == "premium"

main_agent = Agent(
    name="assistant",
    tools=[
        expert.as_tool(
            tool_name="premium_expert",
            is_enabled=should_enable_expert
        )
    ]
)
```

## Custom Tool Implementation

For advanced scenarios, create `FunctionTool` directly:

```python
from agents import FunctionTool

async def custom_invoke(context, args: str) -> str:
    import json
    params = json.loads(args)
    # Custom logic here
    return f"Processed: {params}"

custom_tool = FunctionTool(
    name="custom_processor",
    description="Process data with custom logic",
    params_json_schema={
        "type": "object",
        "properties": {
            "data": {"type": "string"},
            "format": {"type": "string", "enum": ["json", "xml", "csv"]}
        },
        "required": ["data"]
    },
    on_invoke_tool=custom_invoke
)
```

## Tool Configuration

### Tool Choice

Control tool usage behavior:

```python
agent = Agent(
    name="assistant",
    tools=[tool1, tool2],
    tool_choice="auto"       # LLM decides (default)
    # tool_choice="required" # Must use a tool
    # tool_choice="none"     # No tools
    # tool_choice={"type": "function", "function": {"name": "tool1"}}  # Specific tool
)
```

### Tool Use Behavior

Control what happens after tool execution:

```python
agent = Agent(
    name="assistant",
    tools=[tool1],
    tool_use_behavior="run_llm_again"  # Continue with LLM (default)
    # tool_use_behavior="stop_on_first_tool"  # Return tool output directly
)
```

### Combining Multiple Tool Types

```python
from agents import Agent, function_tool
from agents.tools import WebSearchTool, CodeInterpreterTool

@function_tool
def get_company_data(company_id: str) -> dict:
    """Get internal company data."""
    return internal_db.get(company_id)

specialist = Agent(name="analyst", instructions="Analyze financial data.")

main_agent = Agent(
    name="assistant",
    tools=[
        # Function tool
        get_company_data,
        # Hosted tools
        WebSearchTool(),
        CodeInterpreterTool(),
        # Agent as tool
        specialist.as_tool(
            tool_name="analyze_finances",
            tool_description="Get detailed financial analysis"
        )
    ]
)
```
