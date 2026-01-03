---
id: 0002
title: create-web-todo-plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-opus-4.5-20251101
feature: 002-web-todo
branch: 001-console-todo
user: unspecified
command: /sp.plan
labels: ["planning","architecture","web-todo","phase-ii"]
links:
  spec: specs/002-web-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-web-todo/plan.md
  - specs/002-web-todo/data-model.md
  - specs/002-web-todo/contracts/web-todo-api.md
  - specs/002-web-todo/quickstart.md
tests:
  - None created (planning phase)
---

## Prompt

Phase: Phase II – Full-Stack Web Todo Application

Goal:
Define architecture, monorepo structure, and system responsibilities
for Phase II full-stack Todo application.

────────────────────────────────────────
MONOREPO STRUCTURE
────────────────────────────────────────
/
├── .spec-kit/
│   └── config.yaml
├── specs/                  # Global Spec-Kit specs
│   ├── overview.md
│   ├── features/
│   ├── api/
│   ├── database/
│   └── ui/
├── frontend/               # Next.js App Router
│   ├── CLAUDE.md
│   └── app/
├── backend/                # FastAPI server
│   ├── CLAUDE.md
│   ├── main.py
│   ├── routes/
│   ├── models.py
│   └── db.py
├── CLAUDE.md               # Root instructions
└── README.md

────────────────────────────────────────
ARCHITECTURAL OVERVIEW
────────────────────────────────────────

- Frontend: Next.js web client with Better Auth
- Backend: FastAPI REST API
- Database: Neon PostgreSQL via SQLModel
- Auth: JWT-based stateless authentication

────────────────────────────────────────
COMPONENT RESPONSIBILITIES
────────────────────────────────────────

Frontend:
- Handle authentication via Better Auth
- Store and attach JWT to API requests
- Render responsive UI
- Call backend via API client

Backend:
- Verify JWT tokens
- Extract authenticated user
- Enforce task ownership
- Perform CRUD operations via SQLModel

Database:
- Persist users and tasks
- Enforce relational integrity

────────────────────────────────────────
AUTHENTICATION FLOW
────────────────────────────────────────

1. User logs in via frontend
2. Better Auth issues JWT
3. Frontend sends JWT with API requests
4. Backend verifies token and extracts user
5. Backend filters all data by user ID

────────────────────────────────────────
DATA FLOW
────────────────────────────────────────

User Action
→ Frontend UI
→ Authenticated API Request
→ FastAPI Route
→ SQLModel ORM
→ Neon PostgreSQL
→ Filtered Response
→ UI Update

────────────────────────────────────────
IMPLEMENTATION CONSTRAINTS
────────────────────────────────────────

- No manual coding
- All work must trace to specs
- No cross-phase features
- No deviation from defined stack

End of Plan.

## Response snapshot

Created comprehensive implementation plan for Phase II web todo application with the following deliverables:

1. **plan.md**: Complete architectural plan including:
   - Technical context (Python 3.13+, Next.js 16+, FastAPI, Better Auth, SQLModel, Neon PostgreSQL)
   - Constitution compliance check (all principles passed)
   - Monorepo structure with backend/ and frontend/ directories
   - High-level architecture diagram with component relationships
   - Authentication and data flow diagrams
   - Component responsibilities for frontend, backend, and database
   - Security considerations (JWT, bcrypt, access control, CORS)
   - Error handling with HTTP status codes
   - Non-functional requirements (performance, reliability, observability)
   - Dependencies and external services
   - Testing strategy
   - Risk analysis and success metrics

2. **data-model.md**: Complete data model specification:
   - User entity (UUID v4, email, bcrypt password hash, created_at)
   - Task entity (UUID v4, user_id FK, title, description, is_complete, timestamps)
   - One-to-Many User→Tasks relationship with CASCADE delete
   - Indexes on email, user_id, is_complete
   - SQLModel definitions with methods (set_password, verify_password)
   - Database schema DDL for Neon PostgreSQL
   - Query patterns for auth and CRUD operations
   - Validation rules for users and tasks
   - Data privacy considerations

3. **contracts/web-todo-api.md**: Complete REST API contract:
   - 6 endpoints: List, Create, Get, Update, Delete, Toggle Completion
   - Request/response schemas with TypeScript interfaces
   - JWT authentication format and requirements
   - All HTTP status codes documented (200, 201, 400, 401, 403, 404, 500)
   - Error response format
   - CORS configuration
   - OpenAPI/Swagger documentation locations

4. **quickstart.md**: Developer quick start guide:
   - Prerequisites checklist
   - Environment setup instructions
   - Database setup with Neon
   - Development server startup
   - Verification steps
   - API testing examples
   - Development workflow
   - Common issues and solutions

## Outcome

- 🧪 Tests: None created (planning phase)
- 📁 Files: Created 4 planning documents in specs/002-web-todo/
- 🔁 Next prompts: Run /sp.tasks to generate implementation tasks
- 🧠 Reflection: Architecture follows constitution principles with no violations. Clear separation of concerns between frontend (Next.js), backend (FastAPI), and database (Neon PostgreSQL). JWT-based stateless authentication ensures scalability.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task generation (/sp.tasks)
