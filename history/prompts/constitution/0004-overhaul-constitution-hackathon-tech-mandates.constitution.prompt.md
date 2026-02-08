---
id: 0004
title: Overhaul Constitution with Hackathon Tech Mandates
stage: constitution
date: 2026-02-06
surface: agent
model: claude-opus-4-6
feature: none
branch: 003-web-todo-update
user: abdul
command: /sp.constitution
labels: ["constitution", "tech-stack", "hackathon-compliance", "better-auth", "chatkit", "mcp-sdk", "openai-agents-sdk"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

read hackathon document from @HACKATHON.md and after that write un negotiable rules which will help in development all over. avoid wrtiting spec driven development, Knowledge Capture (PHR), AI-First, Agentic Development  as the speckit handles it itself. read existing and then improve the constitution. I want requirements of hackathon to be strictly folowed for example specific framework and version. for example this hackathon consists of new technologies e.g. better auth, chatkit, mcp sdk, openai agents sdk so they are necassary for you to implement, for this you have to take additional context from tools, mcp, or skills.

## Response snapshot

Updated constitution from v1.2.0 to v1.3.0 (MINOR bump). Key changes:

1. **Removed** sections handled by SpecKit: SDD workflow (I.1), AI-First/Agentic Development (I.2), Knowledge Capture/PHR (I.3), Spec-Kit Enforcement Rules (VI), Agent Behavior Rules (VII).

2. **Added Hackathon Compliance (Section I)**: Feature scope mandates (Basic/Intermediate/Advanced per phase), deliverables per phase, no-manual-code rule.

3. **Added Tech Stack Mandates (Section II)**: Exact package names and versions for all 5 phases including Better Auth with JWT plugin, OpenAI ChatKit (`@openai/chatkit`), ChatKit Python SDK, OpenAI Agents SDK (`openai-agents`), Official MCP Python SDK (`mcp` with FastMCP), Dapr, Kafka/Strimzi/Redpanda.

4. **Added Authentication & Security (Section III)**: Better Auth config pattern (nextCookies + jwt plugins, toNextJsHandler), JWT verification rules, secrets management, CORS rules.

5. **Expanded Architecture (Section IV)**: API contract patterns with exact endpoint paths, SQLModel/Neon DB rules, MCP tool specifications (add_task, list_tasks, complete_task, delete_task, update_task), stateless conversation flow, containerization rules, Dapr integration rules.

6. **Preserved**: Design theme, project structure, code quality, constitution hierarchy, governance.

Research conducted via Context7 MCP for Better Auth (JWT plugin, Next.js integration), OpenAI Agents SDK (MCP server connection via MCPServerStreamableHttp), and MCP Python SDK (FastMCP with Streamable HTTP transport).

## Outcome

- Impact: Major constitution overhaul — all hackathon technology requirements now codified as non-negotiable rules
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md
- Next prompts: Update CLAUDE.md Active Technologies for current phase; begin Phase III spec work
- Reflection: Separating SpecKit-managed concerns from project-specific rules reduces duplication and keeps the constitution focused on what agents must build, not how the workflow operates

## Evaluation notes (flywheel)

- Failure modes observed: Previous constitution mixed workflow rules (PHR, SDD) with product rules, causing redundancy with CLAUDE.md
- Graders run and results (PASS/FAIL): Manual validation PASS — no unresolved placeholders, all tech mandates traceable to HACKATHON.md
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate that plan-template Constitution Check section correctly references new section numbers
