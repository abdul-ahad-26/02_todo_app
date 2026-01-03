<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version Change: 1.1.0 → 1.2.0 (PATCH - Added mandate for phase-based folders)

Modified Principles:
  - III.1. UI Consistency (Expanded with CSS variables)
  - V. Architectural Principles (Added Event-Driven and Statelessness)
  - V.3. Phase-Based Project Structure (NEW)

Added Sections:
  - II. Tech Stack & Evolution Phases
  - III. Design Theme & Consistency
  - V.3. Phase-Based Project Structure

Templates Status:
  - .specify/templates/plan-template.md: ✅ Updated (Added tech stack placeholders)
  - .specify/templates/spec-template.md: ✅ Compatible
  - .specify/templates/tasks-template.md: ✅ Compatible

Follow-up TODOs:
  - Ensure all Phase II+ design implementations use the defined CSS variables.
================================================================================
-->

# Hackathon II – Evolution of Todo Constitution

**Purpose**: Define the immutable principles, constraints, and rules governing the entire project lifecycle across all 5 phases of the "Evolution of Todo" hackathon.

> This Constitution applies globally to all phases (Phase I–V) and is written once.

---

## I. Core Development Philosophy

### 1. Spec-Driven Development Is Mandatory

All work MUST follow the lifecycle:

**Constitution → Specify → Plan → Tasks → Implement**

- No implementation may begin until specifications and tasks are complete and approved.
- No code without a task. No task without a plan.
- Ambiguity MUST be resolved by refining specifications, never by improvising code.
- Every implementation must trace to a task.
- Every task must trace to a specification.

**Rationale**: Ensures deterministic, auditable, and reproducible system evolution.

### 2. AI-First, Agentic Development

- Claude Code is the primary implementation agent.
- The human acts as system architect and spec author, not a manual coder.
- No manual code writing; refine specs until Claude Code generates implementation.

**Rationale**: Maximizes consistency and reduces human error in implementation.

### 3. Knowledge Capture (PHR)

- Every user input MUST result in a Prompt History Record (PHR).
- Architectural Decision Records (ADR) MUST be suggested for all stack changes or significant design shifts.

**Rationale**: Enables auditable decision tracking and historical context preservation.

---

## II. Tech Stack & Evolution Phases

The project evolves through 5 distinct phases with consistency in logic and design.

| Phase | Description | Tech Stack |
|-------|-------------|------------|
| **Phase I** | Console Todo | Python 3.13+, UV (Standard Library Only) |
| **Phase II** | Web Todo | Next.js 16+, FastAPI, SQLModel, Neon Postgres, Better Auth |
| **Phase III** | AI-Agentic Todo | OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK |
| **Phase IV** | Cloud-Native Todo | Docker, Kubernetes (Minikube), Helm Charts, AIOps |
| **Phase V** | Distributed Todo | Kafka (Redpanda), Dapr, Azure/GKE/DO Kubernetes |

---

## III. Design Theme & Consistency

All components from Phase II onwards MUST use a unified "Modern Dark/High-Contrast" theme defined by central CSS variables.

### 1. CSS Palette (Frontend)

- `--primary`: `#3b82f6` (Bright Blue)
- `--secondary`: `#10b981` (Emerald)
- `--accent`: `#8b5cf6` (Violet)
- `--background`: `#0f172a` (Deep Slate)
- `--foreground`: `#f8fafc` (Ghost White)
- `--error`: `#ef4444`

### 2. Consistency Guarantee

- All components MUST use these variables for colors, spacing, and transitions.
- All phases MUST look like a single continuous evolution of the same product.

---

## IV. Architectural Principles

### 1. Statelessness

- The backend remains stateless.
- From Phase III onwards, chat/agent state is stored exclusively in the database.

### 2. Event-Driven Evolution

- Transition to Pub/Sub architecture via Dapr or Kafka in Phase V.
- Prefer asynchronous communication for distributed components.

### 3. Clean Code & Best Practices

- Follow Pythonic standards (PEP 8) for all backend code.
- Adhere to Next.js 16 App Router best practices for the frontend.

---

## V. Project Evolution Principles

### 1. Progressive Evolution

- The system evolves incrementally across the defined 5 phases.
- Each phase MUST build upon the logic of the previous one while introducing new capabilities.

### 2. No Premature Complexity

- Future-phase concerns MUST NOT influence current-phase design decisions unless specified.
- Each phase MUST remain minimal and purpose-driven.

### 3. Phase-Based Project Structure

- Each phase MUST be contained in its own dedicated top-level directory to preserve the history of the evolution.
- Directory naming convention: `phase-<N>-<slug>/` (e.g., `phase-1-console/`, `phase-2-web/`).

---

## VI. Spec-Kit Enforcement Rules

| Rule | Description |
|------|-------------|
| **No Task = No Implementation** | Code cannot be written without a corresponding task |
| **Verification First** | Use MCP tools and CLI commands for all information gathering |
| **PHR for Every Input** | Every user message MUST be recorded in a PHR |
| **ADR for Stack Changes** | Suggest ADR when changing technologies between phases |

---

## VII. Agent Behavior Rules

AI agents MUST:

1. **Never invent requirements** - All requirements come from specifications.
2. **Never bypass specifications** - The spec is the source of truth.
3. **Never implement without tasks** - Tasks authorize implementation.
4. **Stop and request clarification** - Ambiguity blocks progress.

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
2. All amendments require version increment per semantic versioning.
3. **MAJOR**: Backward-incompatible principle changes; **MINOR**: New principles or expanded guidance.

### Compliance Review

- PRs MUST verify compliance with CSS variables and architectural principles.
- Use of external libraries in Phase I is a blocking violation.

---

**Version**: 1.2.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2026-01-01
