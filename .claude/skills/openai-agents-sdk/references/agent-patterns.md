# OpenAI Agents SDK - Core Patterns

## Table of Contents

1. [Agent Architecture](#agent-architecture)
2. [Stateless Agent Design](#stateless-agent-design)
3. [Tool Integration](#tool-integration)
4. [Conversation Management](#conversation-management)
5. [Error Handling](#error-handling)

## Agent Architecture

### Basic Agent Structure

An OpenAI agent consists of:
- **Agent Definition**: Instructions and behavior
- **Tools**: Functions the agent can call
- **Runner**: Executes the agent with conversation history

```python
from openai import OpenAI
from openai.agents import Agent, Runner

client = OpenAI(api_key="your-api-key")

# Define agent
agent = Agent(
    name="todo-assistant",
    instructions="You are a helpful assistant that manages todo tasks.",
    model="gpt-4o",
    tools=[]  # MCP tools go here
)

# Run agent
runner = Runner(client=client, agent=agent)
response = runner.run(messages=messages)
```

### Agent Instructions Pattern

**Best Practice**: Write clear, specific instructions that define:
1. **Role**: What the agent is
2. **Capabilities**: What it can do
3. **Behavior**: How it should respond
4. **Tool Usage**: When to use which tools

```python
instructions = """
You are a Todo Assistant that helps users manage their tasks through natural language.

CAPABILITIES:
- Create new tasks from user requests
- List tasks with filtering (all, pending, completed)
- Mark tasks as complete
- Update task details
- Delete tasks

BEHAVIOR:
- Always confirm actions with friendly responses
- When listing tasks, format them clearly with status indicators
- If a request is ambiguous, ask for clarification
- Use the provided MCP tools to interact with the todo database

TOOL USAGE:
- Use add_task when user wants to create/add/remember something
- Use list_tasks when user asks to see/show/list tasks
- Use complete_task when user says done/complete/finished
- Use delete_task when user says delete/remove/cancel
- Use update_task when user says change/update/rename
"""
```

## Stateless Agent Design

### Why Stateless?

Stateless agents don't hold conversation state in memory. Instead:
- Conversation history is stored in a database
- Each request loads history from database
- Agent processes request with full context
- Response is saved to database
- Server holds NO state between requests

**Benefits**:
- **Scalability**: Any server instance can handle any request
- **Resilience**: Server restarts don't lose conversations
- **Horizontal scaling**: Load balancer can route anywhere
- **Testability**: Each request is independent and reproducible

### Request Cycle Pattern

```python
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from openai.agents import Agent, Runner

app = FastAPI()

@app.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest, session: Session):
    """Stateless chat endpoint - fetches history, runs agent, saves response."""

    # 1. Get or create conversation
    conversation = get_or_create_conversation(session, user_id, request.conversation_id)

    # 2. Fetch conversation history from database
    messages = fetch_conversation_history(session, conversation.id)

    # 3. Add new user message
    user_message = {
        "role": "user",
        "content": request.message
    }
    messages.append(user_message)

    # 4. Store user message in database
    save_message(session, conversation.id, user_message)

    # 5. Run agent with MCP tools
    runner = Runner(client=client, agent=agent)
    response = runner.run(messages=messages)

    # 6. Extract assistant response
    assistant_message = response.messages[-1]

    # 7. Store assistant response in database
    save_message(session, conversation.id, assistant_message)

    # 8. Return response (server now ready for next request)
    return {
        "conversation_id": conversation.id,
        "response": assistant_message["content"],
        "tool_calls": extract_tool_calls(response)
    }
```

### Database Models for Stateless Design

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    """Conversation session."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    """Individual message in conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

## Tool Integration

### Tool Definition Pattern

Tools are functions the agent can call. Define them with:
- **Name**: Function name (snake_case)
- **Description**: What the tool does (agent uses this to decide when to call)
- **Parameters**: JSON schema defining inputs

```python
def create_tool_definition(name: str, description: str, parameters: dict) -> dict:
    """Create OpenAI tool definition."""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters
        }
    }

# Example: add_task tool
add_task_tool = create_tool_definition(
    name="add_task",
    description="Create a new task in the todo list",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The user ID"
            },
            "title": {
                "type": "string",
                "description": "The task title"
            },
            "description": {
                "type": "string",
                "description": "Optional task description"
            }
        },
        "required": ["user_id", "title"]
    }
)
```

### Tool Execution Pattern

When the agent calls a tool:
1. OpenAI returns a `tool_call` with function name and arguments
2. Execute the actual function
3. Return the result to the agent
4. Agent uses result to formulate response

```python
def execute_tool(tool_call, user_id: str, session: Session) -> str:
    """Execute a tool call and return result."""

    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # Route to appropriate handler
    if function_name == "add_task":
        return add_task_handler(user_id, arguments, session)
    elif function_name == "list_tasks":
        return list_tasks_handler(user_id, arguments, session)
    elif function_name == "complete_task":
        return complete_task_handler(user_id, arguments, session)
    # ... other tools

    return json.dumps({"error": f"Unknown tool: {function_name}"})

def add_task_handler(user_id: str, args: dict, session: Session) -> str:
    """Handle add_task tool call."""
    try:
        task = Task(
            user_id=user_id,
            title=args["title"],
            description=args.get("description", ""),
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return json.dumps({
            "task_id": task.id,
            "status": "created",
            "title": task.title
        })
    except Exception as e:
        return json.dumps({"error": str(e)})
```

### Multi-Turn Tool Execution

The agent may call multiple tools in sequence:

```python
runner = Runner(client=client, agent=agent)
response = runner.run(messages=messages)

# Process tool calls iteratively
while response.status == "requires_action":
    tool_outputs = []

    for tool_call in response.required_action.submit_tool_outputs.tool_calls:
        output = execute_tool(tool_call, user_id, session)
        tool_outputs.append({
            "tool_call_id": tool_call.id,
            "output": output
        })

    # Submit tool outputs and continue
    response = runner.submit_tool_outputs(
        tool_outputs=tool_outputs
    )

# Final response after all tools executed
final_message = response.messages[-1]
```

## Conversation Management

### Loading History Pattern

```python
def fetch_conversation_history(session: Session, conversation_id: int) -> List[dict]:
    """Load conversation history from database."""
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()

    return [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in messages
    ]
```

### Saving Messages Pattern

```python
def save_message(session: Session, conversation_id: int, message: dict):
    """Save message to database."""
    msg = Message(
        conversation_id=conversation_id,
        role=message["role"],
        content=message["content"]
    )
    session.add(msg)
    session.commit()
```

### Conversation Resumption

Since history is in the database, conversations can resume after:
- Server restarts
- Session timeouts
- User returns days later

```python
# User returns to existing conversation
@app.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest):
    if request.conversation_id:
        # Resume existing conversation
        conversation = get_conversation(session, request.conversation_id)
        messages = fetch_conversation_history(session, conversation.id)
    else:
        # Start new conversation
        conversation = create_conversation(session, user_id)
        messages = []

    # Continue from where user left off
    # ...
```

## Error Handling

### Tool Error Pattern

```python
def execute_tool_safely(tool_call, user_id: str, session: Session) -> str:
    """Execute tool with error handling."""
    try:
        return execute_tool(tool_call, user_id, session)
    except ValidationError as e:
        return json.dumps({
            "error": "Invalid input",
            "details": str(e)
        })
    except NotFoundError as e:
        return json.dumps({
            "error": "Resource not found",
            "details": str(e)
        })
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return json.dumps({
            "error": "Operation failed",
            "message": "Please try again or contact support"
        })
```

### Agent Error Responses

Teach the agent to handle tool errors gracefully in instructions:

```python
instructions = """
...

ERROR HANDLING:
- If a tool returns an error, explain what went wrong in friendly terms
- For "not found" errors, suggest the user check their request
- For validation errors, explain what needs to be corrected
- Never expose raw error messages to users
- Always offer next steps or alternatives
"""
```

### Request Validation

```python
from pydantic import BaseModel, validator

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

    @validator("message")
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        return v

@app.post("/api/{user_id}/chat")
async def chat(user_id: str, request: ChatRequest):
    try:
        # Process request
        pass
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```
