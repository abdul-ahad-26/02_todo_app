# Phase II: Full-Stack Web Application

A multi-user todo application with a Next.js 16+ frontend and Python FastAPI backend.

## Architecture

- **Frontend**: Next.js 16+ (TypeScript, Tailwind CSS, Better Auth)
- **Backend**: Python FastAPI (SQLModel, PyJWT, Uvicorn)
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth with JWT plugin (shared secret between frontend and backend)

## Setup

See [quickstart.md](../specs/005-fullstack-web-app/quickstart.md) for detailed setup instructions.

### Quick Start

1. **Database**: Create a Neon PostgreSQL project at https://console.neon.tech

2. **Backend**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET
   uv run uvicorn src.main:app --reload --port 8000
   ```

3. **Frontend**:
   ```bash
   cd frontend
   cp .env.local.example .env.local
   # Edit .env.local with your DATABASE_URL, BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL
   npm install
   npx @better-auth/cli generate
   npx @better-auth/cli migrate
   npm run dev
   ```

4. Open http://localhost:3000

## Environment Variables

**CRITICAL**: `BETTER_AUTH_SECRET` must be identical in both frontend and backend.

### Backend (`backend/.env`)
- `DATABASE_URL` — Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` — Shared secret for JWT verification
- `ALLOWED_ORIGINS` — CORS allowed origins (e.g., `http://localhost:3000`)
- `DEBUG` — Enable debug mode

### Frontend (`frontend/.env.local`)
- `DATABASE_URL` — Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` — Shared secret for JWT signing
- `BETTER_AUTH_URL` — Better Auth base URL
- `NEXT_PUBLIC_API_URL` — FastAPI backend URL
