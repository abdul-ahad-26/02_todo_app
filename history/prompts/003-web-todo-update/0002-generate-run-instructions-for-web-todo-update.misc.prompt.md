---
id: 0002
title: Generate run instructions for web todo update
stage: misc
date: 2026-01-02
surface: agent
model: claude-opus-4.5
feature: 003-web-todo-update
branch: 003-web-todo-update
user: abdul
command: /sp.implement how to run the project
labels: ["documentation", "readme", "setup"]
links:
  spec: specs/003-web-todo-update/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/README.md
  - phase-2-web/backend/README.md
  - phase-2-web/frontend/README.md
tests:
  - none
---

## Prompt

how to run the project. frontend andd backend. you haven't created any readme file for both.

## Response snapshot

I've generated comprehensive README documentation for Phase 2 Web, including the root Phase 2 guide, the FastAPI backend setup using `uv`, and the Next.js frontend instructions aligned with the project constitution.

## Outcome

- ✅ Impact: users can now successfully set up and run the Phase 2 Web application.
- 🧪 Tests: none (documentation-only change)
- 📁 Files: created phase-2-web/README.md, updated backend and frontend READMEs.
- 🔁 Next prompts: none
- 🧠 Reflection: the documentation correctly reflects the constitution requirements such as Phase folders and UV management.

## Evaluation notes (flywheel)

- Failure modes observed: initially misidentified the feature slug.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
