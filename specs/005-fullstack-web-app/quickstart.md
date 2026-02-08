# Quickstart: Phase II - Full-Stack Web Application

**Feature**: 005-fullstack-web-app
**Date**: 2026-02-08

## Prerequisites

- Python 3.13+ with UV installed
- Node.js 20+ with npm or pnpm
- Neon PostgreSQL account (free tier: https://neon.tech)
- Git

## 1. Project Setup

```bash
# Create phase directory
mkdir -p phase-2-web/{frontend,backend}
```

## 2. Backend Setup (FastAPI)

```bash
cd phase-2-web/backend

# Initialize Python project with UV
uv init --name todo-api
uv add fastapi sqlmodel pyjwt uvicorn python-dotenv

# Create source directory
mkdir -p src/{models,api/routers,crud}
touch src/__init__.py src/models/__init__.py src/api/__init__.py src/api/routers/__init__.py src/crud/__init__.py
```

Create `.env` from `.env.example`:
```bash
cp .env.example .env
# Edit .env with your Neon DATABASE_URL and BETTER_AUTH_SECRET
```

Run the backend:
```bash
uv run uvicorn src.main:app --reload --port 8000
```

Verify: `curl http://localhost:8000/health` → `{"status":"healthy"}`

## 3. Frontend Setup (Next.js)

```bash
cd phase-2-web/frontend

# Create Next.js app
npx create-next-app@latest . --typescript --tailwind --app --src-dir --eslint

# Install Better Auth
npm install better-auth

# Generate Better Auth database tables
npx @better-auth/cli generate
```

Create `.env.local` from `.env.local.example`:
```bash
cp .env.local.example .env.local
# Edit with DATABASE_URL, BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL
```

Run the frontend:
```bash
npm run dev
```

Verify: Open `http://localhost:3000`

## 4. Environment Variables

### Backend (`backend/.env`)

```bash
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-shared-secret-minimum-32-characters
ALLOWED_ORIGINS=http://localhost:3000
DEBUG=true
```

### Frontend (`frontend/.env.local`)

```bash
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-shared-secret-minimum-32-characters
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**CRITICAL**: `BETTER_AUTH_SECRET` MUST be identical in both frontend and backend.

## 5. Database Setup

1. Create a Neon project at https://console.neon.tech
2. Copy the connection string to both `.env` files
3. Better Auth tables are created by running `npx @better-auth/cli generate` + `npx @better-auth/cli migrate`
4. The `task` table is created automatically when FastAPI starts (via `SQLModel.metadata.create_all`)

## 6. Development Workflow

```bash
# Terminal 1: Backend
cd phase-2-web/backend
uv run uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd phase-2-web/frontend
npm run dev
```

## 7. Verify Full Stack

1. Open `http://localhost:3000`
2. Sign up with email + password
3. Verify redirect to dashboard
4. Create a task
5. Toggle task completion
6. Refresh page — verify task persists
7. Sign out and sign in as different user — verify data isolation
