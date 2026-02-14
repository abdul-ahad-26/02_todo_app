---
id: 0004
title: Replace passlib with direct bcrypt for Python 3.14 compatibility
stage: green
date: 2026-01-02
surface: agent
model: claude-opus-4.5
feature: 003-web-todo-update
branch: 003-web-todo-update
user: abdul
command: /sp.implement fix-auth
labels: ["bugfix", "auth", "bcrypt", "python3.14"]
links:
  spec: specs/003-web-todo-update/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/backend/src/models/user.py
  - phase-2-web/backend/pyproject.toml
tests:
  - curl signup test
---

## Prompt

ValueError: password cannot be longer than 72 bytes, truncate manually if necessary

## Response snapshot

I replaced the unmaintained `passlib` library with the `bcrypt` library directly to resolve `ValueError` and compatibility issues on Python 3.14. I also implemented 72-byte truncation for the password inside the `User` model.

## Outcome

- ✅ Impact: users can now successfully signup and signin without 500 errors.
- 🧪 Tests: verified with a successful manual signup via `curl`.
- 📁 Files: src/models/user.py, pyproject.toml
- 🔁 Next prompts: none
- 🧠 Reflection: passlib is prone to breakage on new Python versions; direct library usage is more reliable for simple needs.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
