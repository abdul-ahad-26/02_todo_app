# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `005-fullstack-web-app` | **Date**: 2026-02-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-fullstack-web-app/spec.md`

## Summary

Transform the Phase I console todo app concept into a multi-user web application with persistent storage. The system consists of a Next.js 16+ frontend (TypeScript, Tailwind CSS, Better Auth with JWT plugin) and a Python FastAPI backend (SQLModel, Neon PostgreSQL). Users sign up/sign in via Better Auth on the frontend, which issues JWT tokens. The frontend attaches these tokens to REST API calls to the FastAPI backend, which verifies them using the shared `BETTER_AUTH_SECRET`. All five core task operations (Add, View, Update, Delete, Toggle Complete) are implemented as RESTful endpoints with per-user data isolation.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript strict mode (frontend)
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, uvicorn (backend); Next.js 16+, Better Auth, Tailwind CSS (frontend)
**Storage**: Neon Serverless PostgreSQL (shared by frontend auth and backend tasks)
**Testing**: pytest + FastAPI TestClient (backend); manual E2E testing (frontend)
**Target Platform**: Web browsers (desktop + mobile, 375px–1920px)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**: Dashboard loads < 3s for 100 tasks, task operations < 2s
**Constraints**: Stateless backend (no in-process sessions), JWT-only auth, no wildcard CORS
**Scale/Scope**: Up to 100 tasks per user, multi-user with complete data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Constitution Rule | Status | Evidence |
|---|------------------|--------|----------|
| 1 | **Tech Stack (II.2)**: Next.js 16+, TypeScript strict, Tailwind CSS, FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT, UV, npm/pnpm | PASS | All technologies used as mandated |
| 2 | **Better Auth Config (III.1)**: `lib/auth.ts` with `nextCookies()` + `jwt()` plugins, route at `app/api/auth/[...all]/route.ts`, client via `createAuthClient()` | PASS | See research.md R-001 |
| 3 | **JWT Security (III.2)**: All FastAPI endpoints require Bearer token, verified with `BETTER_AUTH_SECRET`, user_id from JWT matches path param, 401 for invalid tokens | PASS | See contracts/rest-api.md, research.md R-002 |
| 4 | **Secrets (III.3)**: No hardcoded secrets, `.env` files, `.env.example` provided | PASS | See quickstart.md |
| 5 | **CORS (III.4)**: Explicit allowed origins, no wildcard in production | PASS | See contracts/rest-api.md CORS section |
| 6 | **Statelessness (IV.1)**: Backend is stateless, no in-process session storage | PASS | JWT-only auth, no server-side sessions |
| 7 | **API Contracts (IV.3)**: REST pattern follows mandated URL structure exactly | PASS | See contracts/rest-api.md — all 6 endpoints match |
| 8 | **Database & ORM (IV.4)**: SQLModel ORM, `DATABASE_URL` env var, Neon PostgreSQL | PASS | See data-model.md |
| 9 | **Design Theme (V)**: CSS variables for Modern Dark/High-Contrast palette | PASS | See research.md R-006 |
| 10 | **Project Structure (VI)**: `phase-2-web/` directory with `frontend/` + `backend/`, each with `CLAUDE.md` | PASS | See research.md R-005 |
| 11 | **Code Quality (VII.1)**: PEP 8, type hints, async/await, Pydantic models | PASS | Enforced via SQLModel/Pydantic patterns |
| 12 | **Code Quality (VII.2)**: TypeScript strict, App Router, centralized API client, Tailwind CSS | PASS | See research.md R-003 |
| 13 | **Feature Scope (I.1)**: All 5 Basic Level features implemented | PASS | See spec.md FR-009 through FR-015 |
| 14 | **No Manual Code (I.3)**: All code generated via Claude Code | PASS | SDD workflow enforced |

**Post-Phase 1 Re-check**: All 14 gates pass. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/005-fullstack-web-app/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Technology research
├── data-model.md        # Phase 1: Database schema & SQLModel definitions
├── quickstart.md        # Phase 1: Setup instructions
├── contracts/
│   └── rest-api.md      # Phase 1: REST API contract
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
phase-2-web/
├── frontend/                          # Next.js 16+ App
│   ├── CLAUDE.md                      # Frontend-specific agent instructions
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   ├── middleware.ts                  # Auth protection middleware
│   ├── .env.local.example
│   ├── src/
│   │   ├── app/
│   │   │   ├── globals.css            # CSS variables (theme)
│   │   │   ├── layout.tsx             # Root layout (dark theme, fonts)
│   │   │   ├── page.tsx               # Landing → redirect to dashboard or sign-in
│   │   │   ├── (auth)/
│   │   │   │   ├── sign-in/
│   │   │   │   │   └── page.tsx       # Sign-in form (Client Component)
│   │   │   │   └── sign-up/
│   │   │   │       └── page.tsx       # Sign-up form (Client Component)
│   │   │   ├── dashboard/
│   │   │   │   ├── layout.tsx         # Dashboard layout (nav, sign-out)
│   │   │   │   └── page.tsx           # Task list + add/edit/delete UI
│   │   │   └── api/
│   │   │       └── auth/
│   │   │           └── [...all]/
│   │   │               └── route.ts   # Better Auth handler
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── sign-in-form.tsx   # Sign-in form component
│   │   │   │   └── sign-up-form.tsx   # Sign-up form component
│   │   │   └── tasks/
│   │   │       ├── task-list.tsx       # Task list display
│   │   │       ├── task-item.tsx       # Single task with toggle/edit/delete
│   │   │       ├── task-form.tsx       # Add/edit task form
│   │   │       └── empty-state.tsx     # No tasks message
│   │   └── lib/
│   │       ├── auth.ts                # Better Auth server config
│   │       ├── auth-client.ts         # Better Auth client config
│   │       └── api.ts                 # Centralized API client for FastAPI
│   └── public/
├── backend/                           # FastAPI Server
│   ├── CLAUDE.md                      # Backend-specific agent instructions
│   ├── pyproject.toml
│   ├── .env.example
│   └── src/
│       ├── __init__.py
│       ├── main.py                    # FastAPI app, CORS, lifespan
│       ├── config.py                  # Settings from env vars
│       ├── db.py                      # Engine, session dependency
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py                # Task, TaskCreate, TaskUpdate, TaskPublic
│       ├── api/
│       │   ├── __init__.py
│       │   ├── auth.py                # JWT verification dependency
│       │   └── routers/
│       │       ├── __init__.py
│       │       └── tasks.py           # All 6 task endpoints
│       └── crud/
│           ├── __init__.py
│           └── task.py                # TaskRepository (DB operations)
├── docker-compose.yml                 # Optional: local dev services
└── README.md                          # Setup instructions
```

**Structure Decision**: Web application monorepo under `phase-2-web/` as mandated by Constitution Section VI. Frontend and backend are separate projects with independent dependencies and CLAUDE.md files. This allows Claude Code to work on both in a single repository context.

## Complexity Tracking

> No constitution violations detected. All design decisions align with mandated technology and architecture choices.

| Aspect | Decision | Justification |
|--------|----------|---------------|
| Sync SQLModel (not async) | Simpler for Phase II scale | Async migration possible in Phase IV/V if needed |
| UUID string IDs for tasks | Consistent with Better Auth's string user IDs | Avoids auto-increment ID leaking count info |
| Direct frontend→backend API calls | Simpler than proxying through Next.js Route Handlers | FastAPI URL is public anyway; JWT handles security |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Browser                                                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Next.js 16+ Frontend (http://localhost:3000)            │   │
│  │                                                           │   │
│  │  ┌─────────────────┐  ┌────────────────────────────┐    │   │
│  │  │  Better Auth     │  │  Task Dashboard             │    │   │
│  │  │  (sign-in/up/out)│  │  (add/view/edit/delete/     │    │   │
│  │  │                  │  │   toggle tasks)              │    │   │
│  │  └────────┬─────────┘  └────────────┬───────────────┘    │   │
│  │           │                          │                     │   │
│  │    Session + JWT               JWT in Auth header          │   │
│  │    (managed by                 (via lib/api.ts)            │   │
│  │     Better Auth)                     │                     │   │
│  └──────────┼───────────────────────────┼────────────────────┘   │
│             │                           │                         │
└─────────────┼───────────────────────────┼─────────────────────────┘
              │                           │
              ▼                           ▼
┌──────────────────────┐   ┌──────────────────────────────────────┐
│  Better Auth API     │   │  FastAPI Backend (http://localhost:8000) │
│  (Next.js Route      │   │                                      │
│   Handler)           │   │  ┌─────────────────────────────┐     │
│                      │   │  │  JWT Verification           │     │
│  POST /api/auth/*    │   │  │  (verify_jwt_token dep)     │     │
│                      │   │  └──────────────┬──────────────┘     │
└──────────┬───────────┘   │                 │                     │
           │               │  ┌──────────────▼──────────────┐     │
           │               │  │  Task Router                 │     │
           │               │  │  GET/POST/PUT/DELETE/PATCH    │     │
           │               │  │  /api/{user_id}/tasks/*       │     │
           │               │  └──────────────┬──────────────┘     │
           │               │                 │                     │
           │               │  ┌──────────────▼──────────────┐     │
           │               │  │  SQLModel + TaskRepository   │     │
           │               │  └──────────────┬──────────────┘     │
           │               └─────────────────┼────────────────────┘
           │                                 │
           ▼                                 ▼
┌────────────────────────────────────────────────────────────────┐
│  Neon Serverless PostgreSQL                                     │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  user         │  │  session      │  │  task                │ │
│  │  (Better Auth)│  │  (Better Auth)│  │  (App managed)       │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
│  ┌──────────────┐                                               │
│  │  account      │                                               │
│  │  (Better Auth)│                                               │
│  └──────────────┘                                               │
└────────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

| Decision | Rationale | Reference |
|----------|-----------|-----------|
| Better Auth JWT plugin (not Bearer plugin) | JWT tokens are self-contained and verifiable by FastAPI without calling Next.js | research.md R-001 |
| HS256 with shared secret (not JWKS) | Simpler for monorepo where both services share `BETTER_AUTH_SECRET` | research.md R-002 |
| Server Components for page shells, Client Components for interactivity | Reduces JavaScript bundle; forms/toggles need `useState`/event handlers | research.md R-003 |
| Sync SQLModel (not async) | Sufficient for Phase II scale; FastAPI thread pool handles sync I/O | research.md R-004 |
| UUID string task IDs | Consistent with Better Auth's string user IDs; no count leakage | research.md R-004 |
| Centralized API client (`lib/api.ts`) | Single place to manage base URL, JWT token attachment, error handling | research.md R-003 |
| CSS variables for theme | Constitution mandates specific palette; Tailwind extends from variables | research.md R-006 |

## Artifacts Generated

| Artifact | Path | Description |
|----------|------|-------------|
| Research | [research.md](research.md) | 6 research decisions (auth, JWT, Next.js, SQLModel, structure, theme) |
| Data Model | [data-model.md](data-model.md) | 4 tables (3 Better Auth + 1 app), SQLModel definitions, validation rules |
| API Contract | [contracts/rest-api.md](contracts/rest-api.md) | 7 endpoints with request/response schemas, status codes, CORS config |
| Quickstart | [quickstart.md](quickstart.md) | Setup instructions for backend + frontend + database |

## Next Steps

Run `/sp.tasks` to generate the implementation task list from this plan.
