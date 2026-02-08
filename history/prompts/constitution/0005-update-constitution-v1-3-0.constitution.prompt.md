---
id: 0005
title: Update Constitution v1.3.0
stage: constitution
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: none
branch: 001-console-todo
user: architect
command: /sp.constitution
labels: ["constitution", "governance", "tech-mandates", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

update constiturtion

/sp.constitution update constiturtion # Hackathon II – Evolution of Todo Constitution

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

(Better Auth, JWT, Secrets Management, CORS rules)

## IV. Architectural Principles

(Statelessness, Event-Driven Evolution, API Contract Rules, Database & ORM Rules, MCP & Agent Architecture, Containerization & Orchestration, Dapr Integration)

## V. Design Theme & Consistency

(CSS palette, Consistency Guarantee)

## VI. Project Structure

(Phase-Based Directories, Monorepo Layout, Specs Organization)

## VII. Code Quality

(Backend Python, Frontend TypeScript, Progressive Evolution)

## VIII. Constitution Hierarchy

Constitution > Specify > Plan > Tasks > Implementation

## Governance

(Amendment Procedure, Compliance Review)

**Version**: 1.3.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2026-02-08

## Response snapshot

Updated constitution from v1.0.0 to v1.3.0. Major restructuring:
- Removed SpecKit-managed sections (SDD workflow, Agent Behavior Rules) to avoid duplication with CLAUDE.md
- Added 8 new top-level sections: Hackathon Compliance & Feature Scope, Tech Stack Mandates (Phases I-V), Authentication & Security, expanded Architectural Principles (7 sub-sections), Design Theme & Consistency, Project Structure, Code Quality
- Validated compatibility with plan-template.md, spec-template.md, and tasks-template.md
- Updated Last Amended date to 2026-02-08
- Created Sync Impact Report as HTML comment at top of file

## Outcome

- Impact: Constitution fully restructured from generic principles to actionable, phase-specific mandates covering tech stack, auth, API contracts, design theme, and project structure
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md
- Next prompts: Run `/sp.specify` for Phase I console-todo feature spec; consider committing constitution update
- Reflection: User provided complete constitution content — applied as-is with sync report and validation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation PASS — no unresolved placeholders, version matches, dates in ISO format
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
