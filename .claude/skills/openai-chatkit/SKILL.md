---
name: openai-chatkit
description: Build custom chat interfaces using OpenAI ChatKit with advanced integration (self-hosted backend). Use this skill when building chat applications with ChatKit Python SDK, FastAPI backends with ChatKitServer, React frontends with ChatKit.js, rich interactive widgets, streaming responses, file uploads, entity tagging, or custom action handling. Supports OpenAI Agents SDK integration for AI-powered conversational experiences.
---

# OpenAI ChatKit - Advanced Integration

Build production-ready chat interfaces with full control over backend, UI, and data using ChatKit Python SDK and ChatKit.js React bindings.

## Overview

Advanced integration lets you:
- Run ChatKit on your own infrastructure
- Use any backend framework (FastAPI recommended)
- Custom authentication and data residency
- Bespoke agent orchestration with OpenAI Agents SDK
- Rich interactive widgets and actions

## Installation

### Backend (Python)

```bash
pip install openai-chatkit
```

Or with uv:
```bash
uv add openai-chatkit
```

### Frontend (React)

```bash
npm install @openai/chatkit-react
```

Or include via CDN:
```html
<script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"></script>
```

## Quick Start

### 1. Backend Server (FastAPI)

Create `server.py`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from chatkit.server import ChatKitServer, StreamingResult
from chatkit.types import ThreadMetadata, ThreadStreamEvent, UserMessageItem
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from agents import Agent, Runner
from collections.abc import AsyncIterator
from typing import Any

app = FastAPI()

class MyChatKitServer(ChatKitServer):
    def __init__(self, store):
        super().__init__(store)
        self.agent = Agent(
            name="assistant",
            model="gpt-4.1",
            instructions="You are a helpful assistant."
        )

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )
        result = Runner.run_streamed(
            self.agent,
            await simple_to_agent_input(input) if input else [],
            context=agent_context,
        )
        async for event in stream_agent_response(agent_context, result):
            yield event

# Initialize server with store
server = MyChatKitServer(store=InMemoryStore())

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), context={})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

### 2. Implement Store Interface

```python
from chatkit.types import Store, ThreadMetadata, ThreadItem
from typing import Optional

class InMemoryStore(Store):
    def __init__(self):
        self._threads: dict[str, ThreadMetadata] = {}
        self._items: dict[str, list[ThreadItem]] = {}

    async def load_thread(self, thread_id: str) -> Optional[ThreadMetadata]:
        return self._threads.get(thread_id)

    async def save_thread(self, thread: ThreadMetadata) -> None:
        self._threads[thread.id] = thread

    async def load_threads(self, limit: int = 50) -> list[ThreadMetadata]:
        return list(self._threads.values())[:limit]

    async def load_thread_items(self, thread_id: str) -> list[ThreadItem]:
        return self._items.get(thread_id, [])

    async def add_thread_item(self, thread_id: str, item: ThreadItem) -> None:
        if thread_id not in self._items:
            self._items[thread_id] = []
        self._items[thread_id].append(item)

    async def save_item(self, thread_id: str, item: ThreadItem) -> None:
        items = self._items.get(thread_id, [])
        for i, existing in enumerate(items):
            if existing.id == item.id:
                items[i] = item
                return
        items.append(item)
        self._items[thread_id] = items

    async def load_item(self, thread_id: str, item_id: str) -> Optional[ThreadItem]:
        for item in self._items.get(thread_id, []):
            if item.id == item_id:
                return item
        return None

    async def delete_thread(self, thread_id: str) -> None:
        self._threads.pop(thread_id, None)
        self._items.pop(thread_id, None)

    async def delete_thread_item(self, thread_id: str, item_id: str) -> None:
        items = self._items.get(thread_id, [])
        self._items[thread_id] = [i for i in items if i.id != item_id]

    async def generate_id(self, prefix: str) -> str:
        import uuid
        return f"{prefix}_{uuid.uuid4().hex[:12]}"
```

### 3. Frontend (React)

Create `App.tsx`:

```tsx
import { ChatKit, useChatKit } from "@openai/chatkit-react";

export function App() {
  const { control } = useChatKit({
    api: {
      url: "http://localhost:8000/chatkit",
      domainKey: "local-dev",
    },
  });

  return (
    <ChatKit
      control={control}
      className="h-screen w-full"
    />
  );
}
```

### 4. Run the Application

```bash
# Terminal 1: Start backend
uvicorn server:app --reload --port 8000

# Terminal 2: Start frontend
npm run dev
```

## Core Concepts

### ChatKitServer

The `ChatKitServer` base class handles request processing. Override `respond` to provide responses:

```python
class ChatKitServer:
    def __init__(self, data_store: Store, file_store: FileStore | None = None):
        ...

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Override to stream response events."""
        ...

    async def action(
        self,
        thread: ThreadMetadata,
        action_type: str,
        payload: dict,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Override to handle widget actions."""
        ...

    async def process(self, body: bytes, context: Any) -> StreamingResult | JSONResult:
        """Process incoming requests. Don't override."""
        ...
```

### AgentContext

Manages agent execution state and event streaming:

```python
from chatkit.agents import AgentContext

agent_context = AgentContext(
    thread=thread,
    store=self.store,
    request_context=context,
)

# Key methods
agent_context.generate_id("msg")           # Generate unique ID
agent_context.stream(event)                 # Queue event for streaming
agent_context.stream_widget(widget)         # Stream widget to UI
agent_context.start_workflow(workflow)      # Begin workflow
agent_context.add_workflow_task(task)       # Add task to workflow
agent_context.end_workflow(summary)         # Complete workflow
```

### Thread Stream Events

Events streamed from server to client:

| Event | Purpose |
|-------|---------|
| `ThreadItemAddedEvent` | Introduce new item (message, widget, etc.) |
| `ThreadItemUpdatedEvent` | Update pending item (stream text deltas) |
| `ThreadItemDoneEvent` | Mark item complete and persist |
| `ThreadItemRemovedEvent` | Delete item by ID |
| `ThreadItemReplacedEvent` | Swap item in place |
| `ErrorEvent` | User-facing error with retry options |
| `ProgressUpdateEvent` | Transient status during operations |
| `ClientEffectEvent` | Fire-and-forget client behavior |
| `StreamOptionsEvent` | Configure stream behavior |

### Agents SDK Integration

Convert Agents SDK responses to ChatKit events:

```python
from chatkit.agents import (
    AgentContext,
    simple_to_agent_input,
    stream_agent_response,
    ThreadItemConverter,
    ResponseStreamConverter,
)
from agents import Agent, Runner

# Simple integration
async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    result = Runner.run_streamed(
        self.agent,
        await simple_to_agent_input(input) if input else [],
        context=agent_context,
    )

    async for event in stream_agent_response(agent_context, result):
        yield event
```

**Custom converters** for advanced scenarios:

```python
# Custom thread item conversion
converter = ThreadItemConverter(
    attachment_to_message_content=my_attachment_handler,
    tag_to_message_content=my_tag_handler,
)

# Custom response streaming (e.g., partial images)
response_converter = ResponseStreamConverter(partial_images=3)
```

## Adding Tools

Define tools for your agent:

```python
from agents import Agent, function_tool
from chatkit.agents import AgentContext

@function_tool
def search_knowledge_base(query: str, limit: int = 5) -> list[dict]:
    """Search the knowledge base for relevant articles."""
    # Implementation
    return results

@function_tool
def create_ticket(
    context: RunContextWrapper[AgentContext],
    title: str,
    description: str,
    priority: str = "medium"
) -> dict:
    """Create a support ticket."""
    # Access thread context
    thread_id = context.context.thread.id
    return {"ticket_id": "T-123", "status": "created"}

agent = Agent(
    name="support_agent",
    instructions="Help users with their questions. Create tickets when needed.",
    tools=[search_knowledge_base, create_ticket],
)
```

## Environment Variables

```env
OPENAI_API_KEY=sk-...

# Optional: Database (for persistent store)
DATABASE_URL=postgresql://user:pass@localhost:5432/chatkit

# Optional: File storage
S3_BUCKET=my-chatkit-uploads
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

## Project Structure

```
my-chatkit-app/
├── backend/
│   ├── server.py           # FastAPI app with ChatKitServer
│   ├── agent.py            # Agent definition with tools
│   ├── store.py            # Store implementation
│   ├── file_store.py       # FileStore implementation (optional)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main app with ChatKit
│   │   ├── ChatPanel.tsx   # ChatKit configuration
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Reference Documentation

For detailed API information, see:

- **[references/server-integration.md](references/server-integration.md)** - ChatKitServer, Store, FileStore, event handling
- **[references/widgets-and-actions.md](references/widgets-and-actions.md)** - Widget types, ActionConfig, form handling
- **[references/frontend-integration.md](references/frontend-integration.md)** - useChatKit, ChatKit component, event handlers

## Common Patterns

### Progress Updates During Tool Execution

```python
from chatkit.types import ProgressUpdateEvent

@function_tool
async def long_running_task(context: RunContextWrapper[AgentContext], query: str):
    """Perform a long-running search."""
    ctx = context.context

    # Stream progress
    ctx.stream(ProgressUpdateEvent(message="Searching..."))
    results = await search(query)

    ctx.stream(ProgressUpdateEvent(message="Processing results..."))
    processed = await process(results)

    return processed
```

### Custom Headers for Context

Pass page context from frontend to backend:

```tsx
// Frontend
const { control } = useChatKit({
  api: {
    url: "/api/chatkit",
    headers: () => ({
      "x-page-id": currentPageId,
      "x-user-timezone": Intl.DateTimeFormat().resolvedOptions().timeZone,
    }),
  },
});
```

```python
# Backend
async def respond(self, thread, input, context):
    page_id = context.get("headers", {}).get("x-page-id")
    # Use page_id to scope responses
```

### Streaming Widgets

```python
from chatkit.widgets import Card, Text, Button

async def respond(self, thread, input, context):
    agent_context = AgentContext(thread=thread, store=self.store, request_context=context)

    # Stream a card widget
    widget = Card(
        title="Welcome!",
        children=[
            Text(content="How can I help you today?"),
            Button(label="Get Started", action="get_started"),
        ]
    )
    agent_context.stream_widget(widget)

    # Continue with agent response...
```

## Resources

- [ChatKit Python SDK Docs](https://openai.github.io/chatkit-python/)
- [ChatKit.js Docs](https://openai.github.io/chatkit-js/)
- [Advanced Samples Repository](https://github.com/openai/openai-chatkit-advanced-samples)
- [Starter App](https://github.com/openai/openai-chatkit-starter-app)
- [OpenAI Platform Docs](https://platform.openai.com/docs/guides/custom-chatkit)
