# Implementation Plan: Phase II - Full-Stack Web Todo Application

**Branch**: `002-web-todo` | **Date**: 2025-12-30 | **Spec**: [`spec.md`](./spec.md)

## Summary

Transform Phase I console Todo application into a multi-user, full-stack web application with persistent storage (Neon PostgreSQL), JWT-based authentication via Better Auth, and RESTful APIs built with FastAPI (backend) and Next.js 16+ App Router (frontend).

**Key Capabilities:**
- User registration and sign-in with JWT authentication
- User-scoped task CRUD operations
- Multi-user isolation and access control
- Responsive web UI
- Persistent data storage with SQLModel ORM

## Technical Context

**Language/Version**: Python 3.13+ (backend), Node.js with Next.js 16+ (frontend)
**Primary Dependencies**: FastAPI, Better Auth, SQLModel, Neon PostgreSQL, Next.js 16+ (App Router)
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web browser (desktop, tablet, mobile)
**Project Type**: Full-stack web application (monorepo with backend and frontend)
**Performance Goals**: API p95 latency <200ms, UI page load <2s, support 100+ concurrent users
**Constraints**: Stateless backend (JWT only), CORS-enabled for cross-origin requests, bcrypt cost factor 12, JWT expiration 24 hours
**Scale/Scope**: Single database with User and Task tables, 5 API endpoints, 3 UI pages (signup, signin, tasks)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Spec-Driven Development Mandatory | ✅ PASS | All implementation will trace to spec and tasks |
| AI-First, Agentic Development | ✅ PASS | Claude Code is primary implementation agent |
| Deterministic & Auditable Process | ✅ PASS | Every task traces to spec, every spec trace to user stories |
| Progressive Evolution | ✅ PASS | Phase II builds on Phase I without over-engineering |
| Phase Isolation via Specifications | ✅ PASS | Scope limited to web todo, no future-phase features |
| No Premature Complexity | ✅ PASS | Minimal viable web app, no refresh tokens, 2FA, etc. |
| UI Consistency | ✅ PASS | Global UI principles followed, consistent component design |
| Predictable Interaction | ✅ PASS | Same patterns across all CRUD operations |
| Accessibility & Clarity | ✅ PASS | Clear UI text, accessible design patterns |
| Responsiveness Where UI Exists | ✅ PASS | Tailwind breakpoints for mobile/tablet/desktop |
| Device-Agnostic Design | ✅ PASS | Responsive layout specified |
| Clarity Over Cleverness | ✅ PASS | Direct REST API, simple ORM usage |
| Single Responsibility | ✅ PASS | Separate frontend/backend routes, models, services |
| Loose Coupling, Strong Contracts | ✅ PASS | API contracts defined, JWT as interface |

## Project Structure

### Documentation (this feature)

```text
specs/002-web-todo/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (/sp.specify command output)
├── data-model.md         # Data model and schema (this file, below)
├── quickstart.md         # Quick start guide (this file, below)
└── contracts/            # API contracts
    └── web-todo-api.md   # REST API contract (this file, below)
```

### Source Code (repository root)

```text
phase-2-web/
├── backend/
│   ├── CLAUDE.md
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Configuration and environment variables
│   ├── db.py                        # Database connection and session
│   ├── models.py                     # SQLModel models (User, Task)
│   ├── auth.py                       # JWT utilities (decode, verify, extract)
│   ├── deps.txt                      # Python dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py                   # Task CRUD routes
│   │   └── auth.py                    # Authentication routes
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_auth.py
│       └── test_tasks.py
├── frontend/
│   ├── CLAUDE.md
│   ├── app.json                     # Next.js configuration
│   ├── next.config.js               # Next.js configuration
│   ├── package.json                 # Node.js dependencies
│   ├── tsconfig.json                # TypeScript configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── app/
│   │   ├── layout.tsx                # Root layout with auth state
│   │   ├── page.tsx                 # Home/redirect page
│   │   ├── signin/
│   │   │   └── page.tsx             # Sign-in page
│   │   ├── signup/
│   │   │   └── page.tsx             # Sign-up page
│   │   └── tasks/
│   │       ├── page.tsx             # Tasks list page
│   │       └── loading.tsx           # Loading state
│   ├── components/
│   │   ├── ui/                     # Base UI components (buttons, inputs, etc.)
│   │   ├── auth/                   # Auth-related components
│   │   └── tasks/                  # Task-related components
│   ├── lib/
│   │   ├── api-client.ts             # API client with JWT injection
│   │   └── auth-store.ts            # Auth state management
│   └── tests/
│       └── components/
```

**Structure Decision**: Monorepo with `phase-2-web/` as parent directory for backend and frontend. Backend is Python/FastAPI, frontend is Next.js 16+ with App Router. This separation enables independent development and deployment while maintaining clear module boundaries.

## Architecture Overview

### High-Level Components

```
┌─────────────────────────────────────────────────────────┐
│                         Frontend                          │
│                    (Next.js 16+ App Router)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │   Sign-in    │  │   Sign-up    │  │   Tasks      ││
│  │   Page       │  │   Page       │  │   Page       ││
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘│
│         │                    │                    │          │
│         └────────┬───────────┴────────────────────┘          │
│                  │                                        │
│         ┌────────▼────────┐                           │
│         │  API Client      │                           │
│         │  (JWT attach)  │                           │
│         └────────┬────────┘                           │
└──────────────────┼──────────────────────────────────────────┘
                   │ HTTP/JSON
         ┌───────────▼────────────┐
         │   Backend                │
         │   (FastAPI)             │
         │                          │
         │  ┌────────────────────┐ │
         │  │  Auth Middleware    │ │
         │  │  (JWT verify)       │ │
         │  └────────┬───────────┘ │
         │           │              │
         │  ┌────────▼──────────┐│
         │  │  Routes            ││
         │  │  /api/{uid}/tasks ││
         │  │  /api/{uid}/...  ││
         │  └────────┬──────────┘│
         │           │              │
         │  ┌────────▼──────────┐│
         │  │  SQLModel ORM      ││
         │  └────────┬──────────┘│
         └───────────┼────────────┘
                     │
         ┌───────────▼────────────┐
         │   Neon PostgreSQL        │
         │   Serverless            │
         └────────────────────────┘
```

### Authentication Flow

```
1. User opens signup/signin page
   ↓
2. User enters credentials
   ↓
3. Frontend calls Better Auth signup/signin
   ↓
4. Better Auth validates and creates JWT (24h expiration, shared secret)
   ↓
5. Frontend stores JWT in localStorage
   ↓
6. Frontend redirects to /tasks page
   ↓
7. User interacts with tasks (CRUD operations)
   ↓
8. API Client attaches JWT to each request: Authorization: Bearer <token>
   ↓
9. Backend Auth Middleware:
   - Extracts JWT from header
   - Verifies signature with shared secret
   - Extracts user_id from payload
   ↓
10. Route handler executes:
    - Validates user_id in URL matches authenticated user
    - Performs operation with SQLModel
    - Returns filtered response
```

### Data Flow (Task CRUD Example)

```
User Action (Add Task)
   ↓
Frontend: User enters title/description, clicks submit
   ↓
Frontend: API client calls POST /api/{user_id}/tasks
   ↓
Frontend: JWT injected in Authorization header
   ↓
Backend: Auth Middleware verifies JWT
   ↓
Backend: Validates user_id in URL matches token payload
   ↓
Backend: Validates title is non-empty
   ↓
Backend: Creates Task via SQLModel (user_id from JWT)
   ↓
Backend: Returns 201 with created task
   ↓
Frontend: Updates UI with new task
```

## Component Responsibilities

### Frontend (Next.js 16+)

**Responsibilities:**
- Render signin/signup pages with Better Auth integration
- Store JWT in localStorage after successful auth
- Attach JWT to all API requests via API client
- Render responsive task list with add/edit/delete/toggle actions
- Display clear error messages for failed operations
- Redirect unauthenticated users to signin page
- Follow global UI principles for consistency

**Key Modules:**
- `lib/api-client.ts`: HTTP client with JWT injection, error handling
- `lib/auth-store.ts`: Auth state (loading, authenticated, user, token)
- `app/signin/page.tsx`: Better Auth signin form
- `app/signup/page.tsx`: Better Auth signup form with validation
- `app/tasks/page.tsx`: Main task list and management UI
- `components/ui/`: Reusable UI components (buttons, inputs, cards)
- `components/tasks/`: Task-specific components (TaskItem, TaskForm, TaskList)

### Backend (FastAPI)

**Responsibilities:**
- Verify JWT signature on every request
- Extract authenticated user identity from JWT
- Enforce user_id in URL matches authenticated user
- Validate request data (non-empty title, email format, password length)
- Perform CRUD operations via SQLModel ORM
- Return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- Provide OpenAPI/Swagger documentation

**Key Modules:**
- `main.py`: FastAPI app, CORS configuration, route registration
- `config.py`: Environment variables (DATABASE_URL, JWT_SECRET)
- `db.py`: Neon PostgreSQL connection, SQLModel session
- `models.py`: User and Task SQLModel definitions
- `auth.py`: JWT decode, verify, extract utilities
- `routes/tasks.py`: Task CRUD endpoints
- `routes/auth.py`: Authentication endpoints (if needed beyond Better Auth)

### Database (Neon PostgreSQL)

**Responsibilities:**
- Persist User and Task entities
- Enforce referential integrity (user_id foreign key)
- Provide transactional operations

**Tables:**
- `users`: id (UUID v4), email (unique), password_hash (bcrypt), created_at
- `tasks`: id (UUID v4), user_id (FK), title, description, is_complete, created_at, updated_at

## API Contracts

See [`contracts/web-todo-api.md`](./contracts/web-todo-api.md) for detailed API contracts.

### Endpoints Summary

| Method | Path | Description | Auth | Ownership Check |
|--------|------|-------------|-------|------------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user | JWT | user_id must match |
| POST | `/api/{user_id}/tasks` | Create new task | JWT | user_id must match |
| GET | `/api/{user_id}/tasks/{id}` | Get specific task | JWT | task must belong to user |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | JWT | task must belong to user |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | JWT | task must belong to user |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | JWT | task must belong to user |

### Request/Response Formats

**Create Task Request:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Task Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": false,
  "created_at": "2025-12-30T12:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Error Response:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired JWT token"
}
```

## Security Considerations

### JWT Security

- **Algorithm**: HS256 with shared secret
- **Expiration**: 24 hours
- **Secret**: Configured via `JWT_SECRET` environment variable
- **Payload**: Contains `user_id` and `exp` (expiration timestamp)
- **Verification**: Backend rejects invalid/expired signatures with 401

### Password Security

- **Hashing**: bcrypt with cost factor 12
- **Storage**: Only hash stored, never plaintext
- **Validation**: Minimum 8 characters during signup
- **Error Messages**: Generic "invalid credentials" to prevent email enumeration

### Access Control

- **User Isolation**: All queries filtered by `user_id`
- **URL Validation**: `user_id` in URL must match JWT payload
- **Task Ownership**: CRUD operations verify task belongs to authenticated user
- **Response Filtering**: Never return data from other users

### CORS

- Frontend origin must be allowed in CORS configuration
- Credentials not required (JWT in Authorization header)

## Error Handling

### HTTP Status Codes

| Code | Usage | Example |
|------|--------|----------|
| 200 | Success (GET, PUT, PATCH) | Task updated successfully |
| 201 | Created (POST) | Task created successfully |
| 400 | Bad Request | Invalid input (empty title, short password, invalid email) |
| 401 | Unauthorized | Missing, invalid, or expired JWT |
| 403 | Forbidden | user_id mismatch, accessing another user's task |
| 404 | Not Found | Task ID doesn't exist |
| 500 | Internal Server Error | Database connection failure |

### Error Response Format

```json
{
  "error": "error_type",
  "message": "Human-readable error message",
  "details": {}  // Optional additional context
}
```

## Non-Functional Requirements

### Performance

- **API p95 latency**: <200ms for CRUD operations
- **Page load time**: <2s initial render
- **JWT verification**: <10ms per request
- **bcrypt hashing**: ~500ms (cost factor 12, acceptable for signup)

### Reliability

- **Database connection retry**: 3 retries with exponential backoff
- **Graceful degradation**: Database errors return 500 with logging
- **Stateless**: No server-side sessions, backend scales horizontally

### Observability

- **Logging**: Structured JSON logging for all requests, errors
- **OpenAPI**: Auto-generated documentation at `/docs`
- **Error tracking**: All 4xx/5xx responses logged with context

## Dependencies and External Services

### Backend Dependencies

| Package | Version | Purpose |
|---------|----------|---------|
| fastapi | Latest | Web framework |
| uvicorn | Latest | ASGI server |
| pydantic | Latest | Request/response validation |
| sqlmodel | Latest | ORM for PostgreSQL |
| psycopg2-binary | Latest | PostgreSQL driver |
| python-jose[cryptography] | Latest | JWT encode/decode |
| passlib[bcrypt] | Latest | Password hashing |
| python-multipart | Latest | Form data parsing |
| pytest | Latest | Testing framework |
| httpx | Latest | Test client |

### Frontend Dependencies

| Package | Version | Purpose |
|---------|----------|---------|
| next | 16+ | React framework |
| better-auth | Latest | Authentication |
| react | Latest | UI library |
| @types/react | Latest | TypeScript types |
| axios | Latest | HTTP client |
| tailwindcss | Latest | Styling |
| @types/node | Latest | TypeScript types |
| typescript | Latest | TypeScript compiler |
| jest | Latest | Testing framework |
| @testing-library/react | Latest | Component testing |

### External Services

- **Neon PostgreSQL**: Cloud-hosted PostgreSQL database
- No additional external services (Better Auth runs client-side with shared secret)

## Deployment Considerations

### Environment Variables

**Backend (.env):**
```bash
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here  # Must match backend JWT_SECRET
```

### Startup Sequence

1. **Database**: Neon is always-on, no provisioning needed
2. **Backend**: Start with `uvicorn main:app --reload`
3. **Frontend**: Start with `npm run dev`

### Migration

Database schema managed via SQLModel. Initial schema created on first connection with `create_all()`.

## Testing Strategy

### Backend Tests

- **Unit tests**: Model validation, JWT utilities
- **Integration tests**: API endpoints with test database
- **Auth tests**: JWT verification, ownership enforcement
- **Coverage**: Minimum 80% critical paths

### Frontend Tests

- **Component tests**: UI rendering, user interactions
- **Auth tests**: Signin/signup flows, JWT storage
- **API client tests**: Request formatting, error handling

## Risk Analysis

| Risk | Mitigation |
|------|-------------|
| JWT secret exposed | Environment variables only, never in code/repo |
| Database connection loss | Retry logic, graceful 500 responses |
| Cross-user data leakage | Double-check: user_id in URL + task ownership |
| Session hijacking | Short 24h expiration, HTTPS in production |
| Password hash compromise | bcrypt with cost factor 12 |
| Better Auth version changes | Pin specific version, test on upgrade |

## Success Metrics

- **Functional**: All 8 user stories passing acceptance tests
- **Security**: 0 cross-user access vulnerabilities found
- **Performance**: API p95 <200ms, UI load <2s
- **Reliability**: Database retry handles transient failures
- **Usability**: Signup <2min, signin <30s, task operations <30s

## Complexity Tracking

> No constitution violations requiring justification.

| Principle | How We Comply |
|-----------|----------------|
| No Premature Complexity | No refresh tokens, 2FA, real-time updates |
| Single Responsibility | Clear separation: frontend UI, backend API, database storage |
| Clarity Over Cleverness | Direct REST, simple queries, no abstractions |
| Loose Coupling | JWT as contract, API as interface |
