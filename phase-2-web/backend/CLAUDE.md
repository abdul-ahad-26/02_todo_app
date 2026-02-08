# Backend Agent Instructions

## Context
This is the FastAPI backend for the Phase II Full-Stack Todo Application.

## Tech Stack
- Python 3.13+ with FastAPI
- SQLModel ORM with Neon PostgreSQL
- PyJWT for JWT verification (HS256, shared BETTER_AUTH_SECRET)
- UV package manager

## Key Patterns
- All endpoints require JWT Bearer token authentication
- JWT `sub` claim contains user_id; must match path parameter
- Sync SQLModel sessions (FastAPI runs in thread pool)
- UUID string IDs for tasks
- Pydantic/SQLModel models for all request/response validation

## API Structure
- `src/main.py` — FastAPI app, CORS, lifespan
- `src/config.py` — Settings from environment variables
- `src/db.py` — Database engine and session dependency
- `src/models/task.py` — Task SQLModel definitions
- `src/crud/task.py` — TaskRepository (DB operations)
- `src/api/auth.py` — JWT verification dependency
- `src/api/routers/tasks.py` — All 6 task endpoints

## Running
```bash
uv run uvicorn src.main:app --reload --port 8000
```
