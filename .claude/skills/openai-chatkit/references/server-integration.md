# Server Integration Reference

Complete reference for ChatKit Python SDK server-side implementation.

## ChatKitServer

The base class for handling ChatKit requests.

### Constructor

```python
from chatkit.server import ChatKitServer
from chatkit.types import Store, FileStore

class MyChatKitServer(ChatKitServer):
    def __init__(self, store: Store, file_store: FileStore | None = None):
        super().__init__(store, file_store)
```

### Methods to Override

#### respond()

Called when user sends a message:

```python
async def respond(
    self,
    thread: ThreadMetadata,
    input: UserMessageItem | None,
    context: Any,
) -> AsyncIterator[ThreadStreamEvent]:
    """
    Stream response events for a user message.

    Args:
        thread: Current thread metadata
        input: User's message (None for initial load)
        context: Request context from process()

    Yields:
        ThreadStreamEvent objects
    """
    # Your implementation
    yield ThreadItemAddedEvent(item=...)
    yield ThreadItemDoneEvent(id=...)
```

#### action()

Called when user triggers a widget action:

```python
async def action(
    self,
    thread: ThreadMetadata,
    action_type: str,
    payload: dict,
    context: Any,
) -> AsyncIterator[ThreadStreamEvent]:
    """
    Handle widget actions without user message.

    Args:
        thread: Current thread metadata
        action_type: Action identifier (e.g., "button.click")
        payload: Action payload from widget
        context: Request context

    Yields:
        ThreadStreamEvent objects
    """
    if action_type == "select_option":
        option = payload.get("option")
        # Handle selection
        yield ThreadItemAddedEvent(...)
```

## Store Interface

Required interface for data persistence:

```python
from chatkit.types import Store, ThreadMetadata, ThreadItem
from typing import Optional
from abc import ABC, abstractmethod

class Store(ABC):
    @abstractmethod
    async def load_thread(self, thread_id: str) -> Optional[ThreadMetadata]:
        """Load thread by ID."""
        ...

    @abstractmethod
    async def save_thread(self, thread: ThreadMetadata) -> None:
        """Save or update thread."""
        ...

    @abstractmethod
    async def load_threads(self, limit: int = 50) -> list[ThreadMetadata]:
        """List threads (for sidebar)."""
        ...

    @abstractmethod
    async def load_thread_items(self, thread_id: str) -> list[ThreadItem]:
        """Load all items in a thread."""
        ...

    @abstractmethod
    async def add_thread_item(self, thread_id: str, item: ThreadItem) -> None:
        """Add new item to thread."""
        ...

    @abstractmethod
    async def save_item(self, thread_id: str, item: ThreadItem) -> None:
        """Update existing item."""
        ...

    @abstractmethod
    async def load_item(self, thread_id: str, item_id: str) -> Optional[ThreadItem]:
        """Load single item by ID."""
        ...

    @abstractmethod
    async def delete_thread(self, thread_id: str) -> None:
        """Delete thread and all items."""
        ...

    @abstractmethod
    async def delete_thread_item(self, thread_id: str, item_id: str) -> None:
        """Delete single item from thread."""
        ...

    @abstractmethod
    async def generate_id(self, prefix: str) -> str:
        """Generate unique ID with prefix."""
        ...
```

### SQLite Store Example

```python
import aiosqlite
import json
from chatkit.types import Store, ThreadMetadata, ThreadItem

class SQLiteStore(Store):
    def __init__(self, db_path: str = "chatkit.db"):
        self.db_path = db_path

    async def _get_db(self):
        db = await aiosqlite.connect(self.db_path)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS threads (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TEXT,
                updated_at TEXT,
                metadata TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS thread_items (
                id TEXT PRIMARY KEY,
                thread_id TEXT,
                type TEXT,
                content TEXT,
                created_at TEXT,
                FOREIGN KEY (thread_id) REFERENCES threads(id)
            )
        """)
        await db.commit()
        return db

    async def load_thread(self, thread_id: str) -> Optional[ThreadMetadata]:
        async with await self._get_db() as db:
            async with db.execute(
                "SELECT * FROM threads WHERE id = ?", (thread_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return ThreadMetadata(
                        id=row[0],
                        title=row[1],
                        created_at=row[2],
                        updated_at=row[3],
                    )
        return None

    async def save_thread(self, thread: ThreadMetadata) -> None:
        async with await self._get_db() as db:
            await db.execute("""
                INSERT OR REPLACE INTO threads (id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (thread.id, thread.title, thread.created_at, thread.updated_at))
            await db.commit()

    # ... implement remaining methods
```

### PostgreSQL Store Example

```python
import asyncpg
from chatkit.types import Store, ThreadMetadata, ThreadItem

class PostgresStore(Store):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._pool = None

    async def _get_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self.connection_string)
        return self._pool

    async def load_thread(self, thread_id: str) -> Optional[ThreadMetadata]:
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM threads WHERE id = $1", thread_id
            )
            if row:
                return ThreadMetadata(**dict(row))
        return None

    async def generate_id(self, prefix: str) -> str:
        import uuid
        return f"{prefix}_{uuid.uuid4().hex[:12]}"
```

## FileStore Interface

Optional interface for file uploads:

```python
from chatkit.types import FileStore, FileMetadata
from abc import ABC, abstractmethod

class FileStore(ABC):
    @abstractmethod
    async def upload(self, file_id: str, content: bytes, metadata: FileMetadata) -> str:
        """
        Upload file and return URL.

        For direct uploads, client POSTs file to your endpoint.
        """
        ...

    @abstractmethod
    async def get_upload_url(self, file_id: str, metadata: FileMetadata) -> str:
        """
        Get signed URL for two-phase upload.

        Client requests URL, then uploads directly to cloud storage.
        """
        ...

    @abstractmethod
    async def get_preview_url(self, file_id: str) -> str:
        """Return URL for inline thumbnail preview."""
        ...

    @abstractmethod
    async def delete(self, file_id: str) -> None:
        """Delete file (called when thread is removed)."""
        ...
```

### S3 FileStore Example

```python
import boto3
from botocore.config import Config

class S3FileStore(FileStore):
    def __init__(self, bucket: str, region: str = "us-east-1"):
        self.bucket = bucket
        self.s3 = boto3.client("s3", region_name=region)

    async def get_upload_url(self, file_id: str, metadata: FileMetadata) -> str:
        return self.s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": f"uploads/{file_id}",
                "ContentType": metadata.content_type,
            },
            ExpiresIn=3600,
        )

    async def get_preview_url(self, file_id: str) -> str:
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": f"uploads/{file_id}"},
            ExpiresIn=3600,
        )

    async def delete(self, file_id: str) -> None:
        self.s3.delete_object(Bucket=self.bucket, Key=f"uploads/{file_id}")
```

## Thread Stream Events

### ThreadItemAddedEvent

Introduce a new item:

```python
from chatkit.types import (
    ThreadItemAddedEvent,
    AssistantMessageItem,
    TextContent,
)

event = ThreadItemAddedEvent(
    item=AssistantMessageItem(
        id="msg_123",
        type="assistant_message",
        content=[TextContent(type="text", text="Hello!")],
    )
)
```

### ThreadItemUpdatedEvent

Update pending item (streaming):

```python
from chatkit.types import ThreadItemUpdatedEvent, TextDelta

# Stream text incrementally
event = ThreadItemUpdatedEvent(
    id="msg_123",
    delta=TextDelta(type="text_delta", text=" world"),
)
```

### ThreadItemDoneEvent

Mark item complete:

```python
from chatkit.types import ThreadItemDoneEvent

event = ThreadItemDoneEvent(id="msg_123")
```

### ThreadItemRemovedEvent

Delete an item:

```python
from chatkit.types import ThreadItemRemovedEvent

event = ThreadItemRemovedEvent(id="msg_123")
```

### ThreadItemReplacedEvent

Replace item in place:

```python
from chatkit.types import ThreadItemReplacedEvent

event = ThreadItemReplacedEvent(
    id="msg_123",
    item=new_item,
)
```

### ProgressUpdateEvent

Show transient status:

```python
from chatkit.types import ProgressUpdateEvent

event = ProgressUpdateEvent(message="Searching database...")
```

### ErrorEvent

User-facing error:

```python
from chatkit.types import ErrorEvent

event = ErrorEvent(
    message="Unable to process request",
    code="processing_error",
    retryable=True,
)
```

### ClientEffectEvent

Trigger client-side behavior:

```python
from chatkit.types import ClientEffectEvent

event = ClientEffectEvent(
    type="open_dialog",
    payload={"dialog_id": "settings"},
)
```

### StreamOptionsEvent

Configure stream behavior:

```python
from chatkit.types import StreamOptionsEvent

event = StreamOptionsEvent(
    allow_cancel=True,
)
```

## AgentContext Reference

### Properties

```python
agent_context.thread      # ThreadMetadata
agent_context.store       # Store instance
agent_context.request_context  # Context from process()
```

### Methods

```python
# Generate unique ID
id = agent_context.generate_id("msg")  # "msg_abc123"
id = agent_context.generate_id("widget", thread=other_thread)

# Stream events
agent_context.stream(event)

# Stream widget
agent_context.stream_widget(widget, copy_text="Plain text version")

# Workflow management
agent_context.start_workflow(workflow)
agent_context.add_workflow_task(task)
agent_context.update_workflow_task(task, task_index=0)
agent_context.end_workflow(summary="Completed", expanded=False)
```

## Agents SDK Helpers

### simple_to_agent_input()

Convert user input to agent format:

```python
from chatkit.agents import simple_to_agent_input

agent_input = await simple_to_agent_input(user_message_item)
```

### stream_agent_response()

Convert agent stream to ChatKit events:

```python
from chatkit.agents import stream_agent_response

result = Runner.run_streamed(agent, input, context=agent_context)

async for event in stream_agent_response(agent_context, result):
    yield event
```

### ThreadItemConverter

Custom conversion logic:

```python
from chatkit.agents import ThreadItemConverter

converter = ThreadItemConverter(
    # Convert file attachments
    attachment_to_message_content=lambda att: {
        "type": "file",
        "file_id": att.file_id,
    },

    # Convert @mentions to context
    tag_to_message_content=lambda tag: {
        "type": "text",
        "text": f"[Reference: {tag.entity_type}/{tag.entity_id}]",
    },

    # Convert generated images
    generated_image_to_input=lambda item: {...},

    # Convert hidden context items
    hidden_context_to_input=lambda item: {...},

    # Convert task items
    task_to_input=lambda item: {...},

    # Convert workflow items
    workflow_to_input=lambda item: {...},

    # Convert widget items
    widget_to_input=lambda item: {...},
)

# Use with to_agent_input
agent_input = await converter.to_agent_input(thread_items)
```

### ResponseStreamConverter

Custom response handling:

```python
from chatkit.agents import ResponseStreamConverter

converter = ResponseStreamConverter(
    partial_images=3,  # Number of partial image updates
)

async for event in stream_agent_response(
    agent_context,
    result,
    converter=converter,
):
    yield event
```

## FastAPI Integration

### Complete Server Setup

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from chatkit.server import ChatKitServer, StreamingResult

app = FastAPI()

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server = MyChatKitServer(store=MyStore())

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    # Extract context from headers
    context = {
        "headers": dict(request.headers),
        "user_id": request.headers.get("x-user-id"),
    }

    result = await server.process(await request.body(), context=context)

    if isinstance(result, StreamingResult):
        return StreamingResponse(
            result,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
    return Response(content=result.json, media_type="application/json")

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### With Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Verify JWT or session token
    user = await verify_jwt(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.post("/chatkit")
async def chatkit_endpoint(request: Request, user = Depends(verify_token)):
    context = {
        "user_id": user.id,
        "user_email": user.email,
    }
    result = await server.process(await request.body(), context=context)
    # ...
```

## Error Handling

```python
from chatkit.types import ErrorEvent

async def respond(self, thread, input, context):
    try:
        # Your logic
        async for event in stream_agent_response(agent_context, result):
            yield event
    except RateLimitError:
        yield ErrorEvent(
            message="Rate limit exceeded. Please try again later.",
            code="rate_limit",
            retryable=True,
        )
    except ValidationError as e:
        yield ErrorEvent(
            message=f"Invalid input: {e}",
            code="validation_error",
            retryable=False,
        )
    except Exception as e:
        logger.exception("Unexpected error")
        yield ErrorEvent(
            message="An unexpected error occurred.",
            code="internal_error",
            retryable=True,
        )
```
