---
id: 0005
title: Fix frontend 404 by updating API URL and fixing typos
stage: green
date: 2026-01-02
surface: agent
model: claude-opus-4.5
feature: 003-web-todo-update
branch: 003-web-todo-update
user: abdul
command: /sp.implement fix-frontend
labels: ["bugfix", "frontend", "nextjs", "api"]
links:
  spec: specs/003-web-todo-update/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/frontend/.env.local
  - phase-2-web/frontend/src/lib/api-client.ts
  - phase-2-web/frontend/src/app/tasks/page.tsx
tests:
  - manual verification of endpoint paths
---

## Prompt

Not Found at apiFetch (src/lib/api-client.ts:26:11) at async fetchTasks (src/app/tasks/page.tsx:33:20)

## Response snapshot

I fixed the `Not Found` error by appending the missing `/api` prefix to the `NEXT_PUBLIC_API_URL` in `.env.local`. I also improved the `apiClient` to handle trailing slashes robustly and fixed a TypeScript typo (`bool` -> `boolean`) in the `TasksPage` interface.

## Outcome

- ✅ Impact: frontend can now successfully fetch tasks from the backend.
- 🧪 Tests: verified that backend is listening at /api/tasks and frontend config now points there.
- 📁 Files: .env.local, src/lib/api-client.ts, src/app/tasks/page.tsx
- 🔁 Next prompts: none
- 🧠 Reflection: Environment variables for API URLs should always be verified against backend routing configurations.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
