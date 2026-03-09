---
id: "0011"
title: Clean Up Phase-2-Web Env Files & README
stage: refactor
date: 2026-03-09
surface: agent
model: claude-opus-4-6
feature: 005-fullstack-web-app
branch: 005-fullstack-web-app
user: abdul
command: implement plan
labels: ["cleanup", "env", "readme", "stale-files"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/frontend/.env.local
  - phase-2-web/backend/.env.example
  - phase-2-web/README.md
  - phase-2-web/frontend/CLAUDE.md
  - phase-2-web/frontend/src/app/signin/page.tsx (deleted)
  - phase-2-web/frontend/src/app/signup/page.tsx (deleted)
  - phase-2-web/frontend/src/lib/api-client.ts (deleted)
  - phase-2-web/frontend/src/app/tasks/page.tsx (deleted)
tests:
  - grep verification: NEXT_PUBLIC_BETTER_AUTH_URL — zero references (PASS)
  - grep verification: api-client imports — zero references (PASS)
  - .env.example completeness — all vars documented (PASS)
---

## Prompt

Implement the following plan:

# Plan: Clean Up phase-2-web Environment Files & README

## Context
The `phase-2-web` directory has accumulated inconsistencies across `.env` files, orphaned environment variables, stale deprecated files, and an outdated README. This cleanup ensures developers can set up the project correctly from `.env.example` files and README alone.

## Changes
1. Remove orphaned `NEXT_PUBLIC_BETTER_AUTH_URL` from `frontend/.env.local`
2. Add missing `BETTER_AUTH_URL` to `backend/.env.example`
3. Fix README.md (remove stale CLI commands, add BETTER_AUTH_URL to backend env docs)
4. Fix frontend CLAUDE.md (remove nextCookies plugin reference)
5. Delete stale deprecated files (signin, signup, api-client.ts)

## Response snapshot

Executed all 5 planned changes plus discovered and deleted an additional stale file (`tasks/page.tsx`) that imported the deleted `api-client.ts`. All verification grep checks passed: zero references to `NEXT_PUBLIC_BETTER_AUTH_URL` and `api-client` remain. Empty directories cleaned up.

## Outcome

- ✅ Impact: Environment files, README, and CLAUDE.md are now consistent and accurate; 4 stale files removed
- 🧪 Tests: All grep verifications passed — no orphaned references remain
- 📁 Files: 4 files edited, 4 files deleted, 3 empty directories removed
- 🔁 Next prompts: Commit changes, verify frontend builds cleanly
- 🧠 Reflection: Plan was comprehensive but missed the `tasks/page.tsx` dependency on `api-client.ts` — always check reverse dependencies when deleting modules

## Evaluation notes (flywheel)

- Failure modes observed: Plan missed a transitive dependency (tasks/page.tsx → api-client.ts)
- Graders run and results (PASS/FAIL): grep verification PASS, glob verification PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Include dependency graph analysis in cleanup plans
