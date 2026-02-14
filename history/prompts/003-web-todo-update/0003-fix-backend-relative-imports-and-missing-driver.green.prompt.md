---
id: 0003
title: Fix backend relative imports and missing driver
stage: green
date: 2026-01-02
surface: agent
model: claude-opus-4.5
feature: 003-web-todo-update
branch: 003-web-todo-update
user: abdul
command: /sp.implement fix-backend
labels: ["bugfix", "backend", "fastapi"]
links:
  spec: specs/003-web-todo-update/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/backend/src/db.py
  - phase-2-web/backend/src/auth.py
  - phase-2-web/backend/pyproject.toml
tests:
  - backend server startup check
---

## Prompt

ModuleNotFoundError: No module named 'config'

## Response snapshot

I fixed the `ModuleNotFoundError` by changing absolute imports to relative imports in `src/db.py` and `src/auth.py`. additionally, I resolved a missing `psycopg2` driver by adding `psycopg2-binary` to `pyproject.toml`.

## Outcome

- ✅ Impact: backend server now starts correctly and connects to the database.
- 🧪 Tests: verified by starting the server and checking SQL engine logs.
- 📁 Files: src/db.py, src/auth.py, pyproject.toml
- 🔁 Next prompts: none
- 🧠 Reflection: relative imports are necessary when running the application as a package.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
