# Phase III: Todo AI Chatbot

**Status:** 🚧 In Development
**Due Date:** December 21, 2025
**Points:** 200

## Overview

AI-powered chatbot interface for managing todos through natural language using:
- OpenAI Agents SDK for AI logic
- MCP (Model Context Protocol) server for tool operations
- OpenAI ChatKit for frontend UI
- Stateless architecture with database-backed conversations

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth |

## Features

### Basic Level Functionality
- ✅ Add tasks via natural language
- ✅ List and filter tasks
- ✅ Mark tasks complete
- ✅ Delete tasks
- ✅ Update task details
- ✅ Conversational interface with context

### MCP Tools
- `add_task` - Create new tasks
- `list_tasks` - Retrieve tasks with filters
- `complete_task` - Mark tasks as done
- `delete_task` - Remove tasks
- `update_task` - Modify task details

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  ChatKit UI │────▶│  FastAPI Server  │────▶│   Neon DB   │
│  (Frontend) │     │  + Agents SDK    │     │ (PostgreSQL)│
│             │     │  + MCP Tools     │     │             │
└─────────────┘     └──────────────────┘     └─────────────┘
```

## Project Structure

```
phase-3-chatbot/
├── frontend/          # OpenAI ChatKit UI
├── backend/           # FastAPI + Agents SDK + MCP
├── specs/             # Feature specifications
├── docker-compose.yml # Local development setup
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- OpenAI API key
- Neon database connection string

### Installation

```bash
# Backend setup
cd backend
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

### Environment Variables

Create `.env` files in both frontend and backend:

**Backend `.env`:**
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
BETTER_AUTH_SECRET=...
```

**Frontend `.env`:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...
```

### Running Locally

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## Natural Language Commands

| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | Creates task with MCP tool |
| "Show me all my tasks" | Lists all tasks |
| "Mark task 3 as complete" | Completes task #3 |
| "Delete the meeting task" | Finds and deletes task |

## Deployment

- **Frontend:** Vercel
- **Backend:** Railway / Render / Fly.io
- **Database:** Neon Serverless PostgreSQL

## Submission Requirements

- ✅ GitHub repository link
- ✅ Deployed chatbot URL
- ✅ Demo video (max 90 seconds)
- ✅ WhatsApp number for presentation

## Resources

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-sdk)
- [MCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI ChatKit](https://platform.openai.com/docs/guides/chatkit)
- [Neon Database](https://neon.tech)

---

**Hackathon:** GIAIC Hackathon II - The Evolution of Todo
**Repository:** https://github.com/abdul-ahad-26/02_todo_app
