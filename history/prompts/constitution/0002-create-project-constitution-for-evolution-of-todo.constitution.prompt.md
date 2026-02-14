---
id: "0002"
title: "Create project constitution for evolution of todo"
stage: "constitution"
date: "2026-01-01"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "002-web-todo"
user: "default"
command: "/sp.constitution"
labels: ["constitution", "hackathon", "architectural-principles", "sdd"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests:
  - "manual validation of template placeholders"
---

## Prompt

Generate a project constitution for the "Evolution of Todo" hackathon.

  Theme: "From CLI to Distributed Cloud-Native AI Systems".
  The project must evolve through 5 distinct phases with consistency in logic and design.

  1. TECH STACK & VERSIONS:
  - Phase I: Python 3.13+, UV package manager (Standard Library Only).
  - Phase II: Next.js 16+ (App Router), FastAPI (Python), SQLModel, Neon Serverless Postgres, Better Auth (JWT).
  - Phase III: OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK.
  - Phase IV: Containerization (Docker/Gordon), Kubernetes (Minikube), Helm Charts, AIOps (kubectl-ai, kagent).
  - Phase V: Kafka (Redpanda/Strimzi), Dapr (Distributed Runtime), Azure/GKE/DigitalOcean Kubernetes.

  2. DESIGN THEME & CONSISTENCY:
  - Use a unified "Modern Dark/High-Contrast" theme.
  - CSS Variables: Define a central `:root` palette in the frontend:
    - --primary: #3b82f6 (Bright Blue)
    - --secondary: #10b981 (Emerald)
    - --accent: #8b5cf6 (Violet)
    - --background: #0f172a (Deep Slate)
    - --foreground: #f8fafc (Ghost White)
    - --error: #ef4444
  - All components must use these variables for colors, spacing, and transitions to ensure Phase II-V look like a single continuous evolution.

  3. ARCHITECTURAL PRINCIPLES:
  - Spec-Driven Development: No code without a task. No task without a plan.
  - Statelessness: The backend remains stateless (Phase III+ stores chat state in DB).
  - Event-Driven: Transition to Pub/Sub via Dapr/Kafka in Phase V.
  - Clean Code: Follow Pythonic standards (PEP 8) and Next.js Best Practices.

  4. NON-NEGOTIABLES:
  - No manual code writing; refine specs until Claude Code generates implementation.
  - Every user input must result in a Prompt History Record (PHR).
  - Architectural Decision Records (ADR) must be suggested for stack changes.

## Response snapshot

I have generated the project constitution for the "Evolution of Todo" hackathon.

Key updates:
- Defined the 5-phase tech stack evolution (CLI → Distributed Cloud-Native AI).
- Established the "Modern Dark/High-Contrast" theme with central CSS variables.
- Codified architectural principles (SDD, Statelessness, Event-Driven).
- Set non-negotiables for agentic development, PHR capture, and ADR suggestions.

Modified files:
- `.specify/memory/constitution.md` (Version 1.1.0)

## Outcome

- ✅ Impact: High - Defines the governing principles for the entire hackathon.
- 🧪 Tests: Manual verification of principle alignment with user requirements.
- 📁 Files: Updated .specify/memory/constitution.md.
- 🔁 Next prompts: Continue with feature specifications for current phase.
- 🧠 Reflection: The expansion from the generic template to a phased tech stack provides clear direction for future evolution.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
