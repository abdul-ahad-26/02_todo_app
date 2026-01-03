#!/usr/bin/env python3
"""
Initialize a new OpenAI agent project with complete structure.

Usage:
    python init_agent_project.py <project-name> [--path output-directory]
"""

import argparse
import os
from pathlib import Path


def create_directory_structure(base_path: Path):
    """Create the project directory structure."""
    directories = [
        "backend",
        "backend/models",
        "backend/routes",
        "backend/mcp",
        "frontend",
        "frontend/app",
        "frontend/app/api",
        "frontend/components",
        "frontend/lib",
        "specs",
        ".claude",
    ]

    for directory in directories:
        (base_path / directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}/")


def create_backend_files(base_path: Path):
    """Create backend files."""

    # main.py
    main_content = '''"""
FastAPI backend with OpenAI Agents SDK and MCP integration.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from backend.database import get_session, init_db
from backend.routes.chat import router as chat_router
import uvicorn

app = FastAPI(title="Todo Agent API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        # Add production URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
    (base_path / "backend" / "main.py").write_text(main_content)

    # database.py
    database_content = '''"""
Database configuration and session management.
"""
from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
'''
    (base_path / "backend" / "database.py").write_text(database_content)

    # models/task.py
    task_model_content = '''"""
Task database model.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Todo task."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    """Chat conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    """Chat message."""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
'''
    (base_path / "backend" / "models" / "task.py").write_text(task_model_content)

    # routes/chat.py
    chat_route_content = '''"""
Chat API routes.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, List
from backend.database import get_session
from backend.models.task import Conversation, Message
from backend.agent import create_agent, run_agent_with_tools
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """Chat with the agent."""

    # Get or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Load conversation history
    messages_query = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    db_messages = session.exec(messages_query).all()

    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in db_messages
    ]

    # Add user message
    user_message = {"role": "user", "content": request.message}
    messages.append(user_message)

    # Save user message
    session.add(Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    ))
    session.commit()

    # Run agent
    agent = create_agent()
    response_content = await run_agent_with_tools(agent, messages, user_id, session)

    # Save assistant response
    session.add(Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_content
    ))
    session.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=response_content
    )
'''
    (base_path / "backend" / "routes" / "chat.py").write_text(chat_route_content)

    # agent.py
    agent_content = '''"""
OpenAI agent configuration and execution.
"""
from openai import OpenAI
from openai.agents import Agent, Runner
from sqlmodel import Session
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_agent() -> Agent:
    """Create the OpenAI agent with MCP tools."""
    from backend.mcp.tools import get_mcp_tools

    tools = get_mcp_tools()

    return Agent(
        name="todo-assistant",
        instructions="""
You are a helpful todo assistant that helps users manage their tasks.

CAPABILITIES:
- Create new tasks
- List tasks with filtering
- Mark tasks as complete
- Update task details
- Delete tasks

BEHAVIOR:
- Confirm actions with friendly responses
- Format task lists clearly
- Ask for clarification when needed
- Use provided tools to interact with database

TOOL USAGE:
- add_task: when user wants to create/add/remember something
- list_tasks: when user asks to see/show/list tasks
- complete_task: when user says done/complete/finished
- delete_task: when user says delete/remove/cancel
- update_task: when user says change/update/rename
        """,
        model="gpt-4o",
        tools=tools
    )

async def run_agent_with_tools(
    agent: Agent,
    messages: list,
    user_id: str,
    session: Session
) -> str:
    """Run agent and execute MCP tools."""
    from backend.mcp.executor import execute_tool

    runner = Runner(client=client, agent=agent)
    response = runner.run(messages=messages)

    # Execute tools
    while response.status == "requires_action":
        tool_outputs = []

        for tool_call in response.required_action.submit_tool_outputs.tool_calls:
            output = await execute_tool(tool_call, user_id, session)
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": output
            })

        response = runner.submit_tool_outputs(tool_outputs=tool_outputs)

    # Return final response
    return response.messages[-1]["content"]
'''
    (base_path / "backend" / "agent.py").write_text(agent_content)

    # mcp/tools.py
    mcp_tools_content = '''"""
MCP tool definitions.
"""

def get_mcp_tools() -> list:
    """Get all MCP tool definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Task title"},
                        "description": {"type": "string", "description": "Task description"}
                    },
                    "required": ["title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter by status"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Task ID"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Task ID"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update task details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Task ID"},
                        "title": {"type": "string", "description": "New title"},
                        "description": {"type": "string", "description": "New description"}
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]
'''
    (base_path / "backend" / "mcp" / "tools.py").write_text(mcp_tools_content)

    # mcp/executor.py
    mcp_executor_content = '''"""
MCP tool execution handlers.
"""
from sqlmodel import Session, select
from backend.models.task import Task
import json

async def execute_tool(tool_call, user_id: str, session: Session) -> str:
    """Execute MCP tool and return result."""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    try:
        if function_name == "add_task":
            return await add_task(user_id, arguments, session)
        elif function_name == "list_tasks":
            return await list_tasks(user_id, arguments, session)
        elif function_name == "complete_task":
            return await complete_task(user_id, arguments, session)
        elif function_name == "delete_task":
            return await delete_task(user_id, arguments, session)
        elif function_name == "update_task":
            return await update_task(user_id, arguments, session)
        else:
            return json.dumps({"error": f"Unknown tool: {function_name}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

async def add_task(user_id: str, args: dict, session: Session) -> str:
    """Create new task."""
    task = Task(
        user_id=user_id,
        title=args["title"],
        description=args.get("description", "")
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return json.dumps({
        "task_id": task.id,
        "status": "created",
        "title": task.title
    })

async def list_tasks(user_id: str, args: dict, session: Session) -> str:
    """List user tasks."""
    status = args.get("status", "all")

    query = select(Task).where(Task.user_id == user_id)
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    tasks = session.exec(query).all()

    return json.dumps([
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
        for task in tasks
    ])

async def complete_task(user_id: str, args: dict, session: Session) -> str:
    """Mark task complete."""
    task = session.exec(
        select(Task).where(Task.id == args["task_id"], Task.user_id == user_id)
    ).first()

    if not task:
        return json.dumps({"error": "Task not found"})

    task.completed = True
    session.add(task)
    session.commit()

    return json.dumps({
        "task_id": task.id,
        "status": "completed",
        "title": task.title
    })

async def delete_task(user_id: str, args: dict, session: Session) -> str:
    """Delete task."""
    task = session.exec(
        select(Task).where(Task.id == args["task_id"], Task.user_id == user_id)
    ).first()

    if not task:
        return json.dumps({"error": "Task not found"})

    title = task.title
    session.delete(task)
    session.commit()

    return json.dumps({
        "task_id": args["task_id"],
        "status": "deleted",
        "title": title
    })

async def update_task(user_id: str, args: dict, session: Session) -> str:
    """Update task."""
    task = session.exec(
        select(Task).where(Task.id == args["task_id"], Task.user_id == user_id)
    ).first()

    if not task:
        return json.dumps({"error": "Task not found"})

    if "title" in args:
        task.title = args["title"]
    if "description" in args:
        task.description = args["description"]

    session.add(task)
    session.commit()

    return json.dumps({
        "task_id": task.id,
        "status": "updated",
        "title": task.title
    })
'''
    (base_path / "backend" / "mcp" / "executor.py").write_text(mcp_executor_content)

    # requirements.txt
    requirements_content = '''fastapi==0.115.0
uvicorn==0.32.0
sqlmodel==0.0.22
openai==1.55.0
python-dotenv==1.0.1
pydantic==2.10.0
'''
    (base_path / "backend" / "requirements.txt").write_text(requirements_content)

    # .env.example
    env_content = '''DATABASE_URL=postgresql://user:password@localhost:5432/todo
OPENAI_API_KEY=sk-...
BETTER_AUTH_SECRET=your-secret-key
'''
    (base_path / "backend" / ".env.example").write_text(env_content)

    print("✅ Created backend files")


def create_frontend_files(base_path: Path):
    """Create frontend files."""

    # package.json
    package_json = '''{
  "name": "todo-agent-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "@openai/chatkit": "^1.0.0",
    "next": "15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "typescript": "^5"
  }
}
'''
    (base_path / "frontend" / "package.json").write_text(package_json)

    # app/page.tsx
    page_content = '''import ChatPage from '@/components/ChatPage'

export default function Home() {
  return <ChatPage />
}
'''
    (base_path / "frontend" / "app" / "page.tsx").write_text(page_content)

    # app/api/chat/route.ts
    api_route_content = '''import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { message, conversation_id } = await request.json()

    // TODO: Get user from auth
    const userId = 'demo_user'

    const response = await fetch(`${process.env.BACKEND_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, conversation_id })
    })

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    )
  }
}
'''
    chat_route_path = base_path / "frontend" / "app" / "api" / "chat"
    chat_route_path.mkdir(parents=True, exist_ok=True)
    (chat_route_path / "route.ts").write_text(api_route_content)

    # components/ChatPage.tsx
    chat_page_content = ''''use client'

import { ChatKit } from '@openai/chatkit'
import '@openai/chatkit/styles.css'

export default function ChatPage() {
  return (
    <div className="container mx-auto h-screen p-4">
      <ChatKit
        apiUrl="/api/chat"
        welcomeMessage="Welcome! I'm your todo assistant. Ask me to add tasks, list your todos, or mark them complete."
        placeholder="Type your message... (e.g., 'Add task to buy groceries')"
        streamingEnabled={true}
      />
    </div>
  )
}
'''
    (base_path / "frontend" / "components" / "ChatPage.tsx").write_text(chat_page_content)

    # .env.local.example
    env_local_content = '''BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
'''
    (base_path / "frontend" / ".env.local.example").write_text(env_local_content)

    print("✅ Created frontend files")


def create_project_files(base_path: Path, project_name: str):
    """Create root project files."""

    # README.md
    readme_content = f'''# {project_name}

OpenAI agent-powered todo application with MCP integration.

## Project Structure

```
{project_name}/
├── backend/           # FastAPI backend with OpenAI Agents SDK
├── frontend/          # Next.js frontend with ChatKit
├── specs/             # Spec-driven development artifacts
└── .claude/           # Claude Code configuration
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your backend URL
npm run dev
```

## Features

- ✅ OpenAI Agents SDK integration
- ✅ MCP (Model Context Protocol) tools
- ✅ Stateless agent architecture
- ✅ Database-backed conversation history
- ✅ OpenAI ChatKit UI
- ✅ RESTful API

## Development

Built using spec-driven development with Claude Code.

See specs/ directory for requirements and architecture.
'''
    (base_path / "README.md").write_text(readme_content)

    # .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.db

# Node
node_modules/
.next/
out/
build/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
'''
    (base_path / ".gitignore").write_text(gitignore_content)

    print("✅ Created project files")


def main():
    parser = argparse.ArgumentParser(description="Initialize OpenAI agent project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--path", default=".", help="Output directory (default: current)")

    args = parser.parse_args()

    # Create base path
    base_path = Path(args.path) / args.project_name
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Initializing project: {args.project_name}")
    print(f"   Location: {base_path.absolute()}\n")

    # Create structure
    create_directory_structure(base_path)
    create_backend_files(base_path)
    create_frontend_files(base_path)
    create_project_files(base_path, args.project_name)

    print(f"\n✅ Project '{args.project_name}' initialized successfully!")
    print(f"\nNext steps:")
    print(f"1. cd {args.project_name}")
    print(f"2. Set up backend: cd backend && pip install -r requirements.txt")
    print(f"3. Set up frontend: cd frontend && npm install")
    print(f"4. Configure environment variables (.env files)")
    print(f"5. Run backend: python backend/main.py")
    print(f"6. Run frontend: cd frontend && npm run dev")


if __name__ == "__main__":
    main()
