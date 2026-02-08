<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version Change: 1.0.0 → 1.3.0 (MINOR - Major content expansion across
multiple releases; new sections for tech mandates, auth, design, structure)

Modified Principles:
  - "Core Development Philosophy" → removed (SDD, AI-First, Auditable
    Process now managed by SpecKit Plus / CLAUDE.md)
  - "Project Evolution Principles" → partially retained in
    VII.3 "Progressive Evolution"
  - "UI Principles" → replaced by V "Design Theme & Consistency"
  - "Responsive Design Principles" → removed (implicit in UI framework)
  - "Architectural Principles" → expanded into IV with 7 sub-sections
  - "Quality & Reliability" → replaced by VII "Code Quality"

Added Sections:
  - I. Hackathon Compliance & Feature Scope (feature matrix + deliverables)
  - II. Tech Stack Mandates (Phases I–V with exact versions)
  - III. Authentication & Security (Better Auth, JWT, Secrets, CORS)
  - IV.1 Statelessness
  - IV.2 Event-Driven Evolution (Phase V)
  - IV.3 API Contract Rules (REST pattern)
  - IV.4 Database & ORM Rules
  - IV.5 MCP & Agent Architecture Rules (Phase III+)
  - IV.6 Containerization & Orchestration (Phase IV+)
  - IV.7 Dapr Integration Rules (Phase V)
  - V. Design Theme & Consistency (CSS palette)
  - VI. Project Structure (phase dirs + monorepo layout)
  - VII. Code Quality (Python + TypeScript standards)

Removed Sections:
  - Spec-Kit Enforcement Rules (managed by SpecKit Plus)
  - Agent Behavior Rules (managed by CLAUDE.md)
  - IX. Constitution Hierarchy → renumbered to VIII

Templates Status:
  - .specify/templates/plan-template.md: ✅ Compatible
    (Constitution Check section exists; tech context aligns)
  - .specify/templates/spec-template.md: ✅ Compatible
    (User stories + requirements structure unchanged)
  - .specify/templates/tasks-template.md: ✅ Compatible
    (Phase-based task structure matches constitution phases)

Follow-up TODOs: None
================================================================================
-->

# Hackathon II – Evolution of Todo Constitution

**Purpose**: Define the immutable principles, constraints, and
non-negotiable rules governing the entire project lifecycle across
all 5 phases of the "Evolution of Todo" hackathon.

> This Constitution applies globally to all phases (Phase I–V)
> and is written once. It does NOT cover Spec-Driven Development
> workflow, PHR recording, or agentic tooling — those are managed
> by SpecKit Plus and CLAUDE.md.

---

## I. Hackathon Compliance & Feature Scope

### 1. Feature Scope per Phase

Every phase MUST implement the features defined in the hackathon
document. No features may be skipped or substituted.

**Basic Level (ALL phases MUST include):**

- Add Task (title + description)
- Delete Task (by ID)
- Update Task (modify title/description)
- View Task List (display all tasks with status)
- Mark as Complete / Incomplete (toggle)

**Intermediate Level (Phase V MUST include):**

- Priorities (high / medium / low)
- Tags / Categories (work / home / custom labels)
- Search by keyword
- Filter by status, priority, or date
- Sort by due date, priority, or alphabetically

**Advanced Level (Phase V MUST include):**

- Recurring Tasks (auto-reschedule repeating tasks)
- Due Dates & Time Reminders (with browser notifications)

### 2. Deliverables per Phase

Each phase MUST produce:

| Artifact | Description |
|----------|-------------|
| `specs/<feature>/spec.md` | Feature specification |
| `specs/<feature>/plan.md` | Architecture plan |
| `specs/<feature>/tasks.md` | Actionable task list |
| Source code in phase directory | Working implementation |
| `README.md` update | Setup instructions for the phase |

### 3. No Manual Code

All implementation code MUST be generated via Claude Code from
specifications. If Claude Code generates incorrect output, the
specification MUST be refined — not the code manually edited.

---

## II. Tech Stack Mandates

The following technology choices are **non-negotiable**. Agents
MUST NOT substitute, downgrade, or skip any listed technology
unless a hackathon amendment explicitly permits it.

### 1. Phase I: Console Todo

| Component | Requirement |
|-----------|-------------|
| Language | Python 3.13+ |
| Package Manager | UV |
| Dependencies | Standard library ONLY (no pip packages) |
| Storage | In-memory (Python list/dict) |

### 2. Phase II: Full-Stack Web Application

| Component | Requirement |
|-----------|-------------|
| Frontend | Next.js 16+ (App Router) |
| Frontend Language | TypeScript (strict mode) |
| CSS | Tailwind CSS |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (with JWT plugin) |
| Package Manager (Python) | UV |
| Package Manager (Node) | npm or pnpm |

### 3. Phase III: AI-Powered Chatbot

| Component | Requirement |
|-----------|-------------|
| Chat Frontend | OpenAI ChatKit (`@openai/chatkit`) |
| Chat Backend | ChatKit Python SDK (`chatkit-python`) |
| AI Framework | OpenAI Agents SDK (`openai-agents`) |
| MCP Server | Official MCP Python SDK (`mcp`) |
| MCP Transport | Streamable HTTP via FastMCP |
| Backend | Python FastAPI (same as Phase II) |
| Database | Neon Serverless PostgreSQL (same) |
| Authentication | Better Auth with JWT (same) |

### 4. Phase IV: Local Kubernetes Deployment

| Component | Requirement |
|-----------|-------------|
| Containerization | Docker (Dockerfile per service) |
| Docker AI | Gordon (Docker AI Agent) where available |
| Orchestration | Kubernetes via Minikube |
| Package Manager | Helm Charts |
| AI DevOps | kubectl-ai and/or kagent |

### 5. Phase V: Advanced Cloud Deployment

| Component | Requirement |
|-----------|-------------|
| Event Streaming | Apache Kafka (Strimzi on K8s or Redpanda Cloud) |
| Distributed Runtime | Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation) |
| Cloud Provider | Azure AKS / Google GKE / DigitalOcean DOKS / Oracle OKE |
| CI/CD | GitHub Actions |
| Monitoring | Configured logging and observability |

---

## III. Authentication & Security

### 1. Better Auth Configuration

- Better Auth MUST be initialized in `lib/auth.ts` with the
  `nextCookies()` plugin and the `jwt()` plugin.
- API route handler MUST be at `app/api/auth/[...all]/route.ts`
  using `toNextJsHandler(auth)`.
- Client auth MUST use `createAuthClient()` from
  `better-auth/react`.

### 2. JWT-Based API Security

- All FastAPI endpoints MUST require a valid JWT token in the
  `Authorization: Bearer <token>` header.
- The JWT MUST be verified using the shared `BETTER_AUTH_SECRET`
  environment variable.
- The backend MUST extract `user_id` from the JWT and enforce
  that it matches the `{user_id}` path parameter.
- Requests without a valid token MUST receive 401 Unauthorized.
- Each user MUST only see and modify their own tasks.

### 3. Secrets Management

- NEVER hardcode secrets, API keys, tokens, or connection strings.
- All secrets MUST be in `.env` files (excluded from git via
  `.gitignore`).
- Provide `.env.example` files documenting required variables.
- In Phase IV/V, use Kubernetes Secrets or Dapr Secrets store.

### 4. CORS

- Backend MUST configure CORS to allow the frontend origin.
- In production, CORS MUST NOT use wildcard (`*`) for origins.

---

## IV. Architectural Principles

### 1. Statelessness

- The backend MUST remain stateless. No in-process session
  storage (except Phase I in-memory by design).
- From Phase III onwards, conversation state and chat history
  MUST be persisted exclusively in the database.
- Any server instance MUST be able to handle any request.

### 2. Event-Driven Evolution (Phase V)

- Phase V MUST use Kafka topics for: `task-events`,
  `reminders`, `task-updates`.
- Producers and consumers MUST be decoupled microservices.
- Dapr Pub/Sub MUST abstract Kafka client code — application
  code MUST NOT import kafka-python directly when Dapr is
  available.

### 3. API Contract Rules

- All REST endpoints MUST follow this pattern:
  - `GET /api/{user_id}/tasks` — List tasks
  - `POST /api/{user_id}/tasks` — Create task
  - `GET /api/{user_id}/tasks/{id}` — Get task detail
  - `PUT /api/{user_id}/tasks/{id}` — Update task
  - `DELETE /api/{user_id}/tasks/{id}` — Delete task
  - `PATCH /api/{user_id}/tasks/{id}/complete` — Toggle completion
- Phase III adds: `POST /api/{user_id}/chat` — Chat endpoint.
- All endpoints MUST return JSON responses.
- All endpoints MUST use Pydantic/SQLModel for request/response
  validation.
- Errors MUST use `HTTPException` with appropriate status codes.

### 4. Database & ORM Rules

- SQLModel MUST be the ORM for all database operations.
- Database connection MUST use `DATABASE_URL` environment variable.
- Neon Serverless PostgreSQL MUST be the database provider.
- Schema changes MUST be managed via migrations (Alembic or
  SQLModel create_all for initial setup).

### 5. MCP & Agent Architecture Rules (Phase III+)

- The MCP server MUST be built with the Official MCP Python SDK
  (`mcp` package) using `FastMCP`.
- MCP transport MUST be Streamable HTTP.
- The MCP server MUST expose exactly these tools:
  `add_task`, `list_tasks`, `complete_task`, `delete_task`,
  `update_task`.
- Each MCP tool MUST accept `user_id` as a required parameter.
- The OpenAI Agents SDK MUST be used for agent logic.
- The agent MUST connect to the MCP server via
  `MCPServerStreamableHttp`.
- Conversation flow MUST be stateless per request:
  1. Receive message
  2. Fetch history from DB
  3. Run agent with MCP tools
  4. Store response in DB
  5. Return response

### 6. Containerization & Orchestration (Phase IV+)

- Each service MUST have its own `Dockerfile`.
- Images MUST use multi-stage builds for production.
- Helm Charts MUST be used for Kubernetes deployment.
- All configuration MUST be externalized via ConfigMaps
  and Secrets.
- Health check endpoints (`/health`) MUST be implemented
  for liveness and readiness probes.

### 7. Dapr Integration Rules (Phase V)

- Dapr MUST be used as a sidecar for all services.
- Application code MUST interact with Kafka, state stores,
  and secrets exclusively through Dapr HTTP APIs
  (`http://localhost:3500/v1.0/...`).
- Dapr components MUST be defined in YAML configuration files.
- Service-to-service communication MUST use Dapr service
  invocation for built-in retries and mTLS.

---

## V. Design Theme & Consistency

All components from Phase II onwards MUST use a unified
"Modern Dark/High-Contrast" theme defined by central CSS
variables.

### 1. CSS Palette (Frontend)

- `--primary`: `#3b82f6` (Bright Blue)
- `--secondary`: `#10b981` (Emerald)
- `--accent`: `#8b5cf6` (Violet)
- `--background`: `#0f172a` (Deep Slate)
- `--foreground`: `#f8fafc` (Ghost White)
- `--error`: `#ef4444`

### 2. Consistency Guarantee

- All components MUST use these variables for colors, spacing,
  and transitions.
- All phases MUST look like a single continuous evolution of the
  same product.
- ChatKit UI in Phase III MUST be themed to match these
  variables.

---

## VI. Project Structure

### 1. Phase-Based Directories

Each phase MUST be contained in its own dedicated top-level
directory to preserve the history of the evolution.

Directory naming convention:
`phase-<N>-<slug>/` (e.g., `phase-1-console/`, `phase-2-web/`)

### 2. Monorepo Layout (Phase II+)

```text
phase-2-web/
├── frontend/          # Next.js 16+ App
│   ├── CLAUDE.md
│   ├── src/ or app/
│   └── ...
├── backend/           # FastAPI Server
│   ├── CLAUDE.md
│   ├── src/ or app/
│   └── ...
├── docker-compose.yml
└── README.md
```

### 3. Specs Organization

```text
specs/<feature-name>/
├── spec.md
├── plan.md
├── tasks.md
├── research.md       (optional)
├── data-model.md     (optional)
└── contracts/        (optional)
```

---

## VII. Code Quality

### 1. Backend (Python)

- Follow PEP 8 and Pythonic standards.
- Use type hints for all function signatures.
- Use `async/await` for all I/O operations in FastAPI.
- Use Pydantic models for all request/response schemas.

### 2. Frontend (TypeScript)

- TypeScript strict mode MUST be enabled.
- Use Next.js 16+ App Router patterns (server components
  by default, client components only for interactivity).
- All API calls MUST go through a centralized API client
  (`lib/api.ts` or similar).
- Use Tailwind CSS — no inline styles.

### 3. Progressive Evolution

- Each phase MUST build upon the logic of the previous phase
  while introducing new capabilities.
- Future-phase concerns MUST NOT influence current-phase design
  unless explicitly specified in the hackathon document.
- Each phase MUST remain minimal and purpose-driven.

---

## VIII. Constitution Hierarchy

In case of conflict, the following precedence applies:

```
Constitution > Specify > Plan > Tasks > Implementation
```

---

## Governance

### Amendment Procedure

1. Proposed amendments MUST be documented with rationale.
2. All amendments require version increment per semantic
   versioning:
   - **MAJOR**: Backward-incompatible principle removals or
     redefinitions
   - **MINOR**: New principles or materially expanded guidance
   - **PATCH**: Clarifications, wording, typo fixes

### Compliance Review

- PRs MUST verify compliance with tech stack mandates.
- Use of unauthorized technologies is a blocking violation.
- CSS variables MUST be verified in frontend PRs.
- JWT auth MUST be verified in API endpoint PRs.

---

**Version**: 1.3.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2026-02-08
