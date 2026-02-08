---
id: "0004"
title: Implement Better Auth Integration
stage: green
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 004-better-auth-integration
branch: 004-better-auth-integration
user: abdul
command: /sp.implement
labels: ["better-auth", "jwt", "jwks", "authentication", "implementation"]
links:
  spec: specs/004-better-auth-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/frontend/src/lib/auth.ts
  - phase-2-web/frontend/src/lib/auth-client.ts
  - phase-2-web/frontend/src/lib/api-client.ts
  - phase-2-web/frontend/src/app/api/auth/[...all]/route.ts
  - phase-2-web/frontend/src/middleware.ts
  - phase-2-web/frontend/src/app/signup/page.tsx
  - phase-2-web/frontend/src/app/signin/page.tsx
  - phase-2-web/frontend/src/app/tasks/page.tsx
  - phase-2-web/frontend/src/app/page.tsx
  - phase-2-web/frontend/next.config.ts
  - phase-2-web/frontend/package.json
  - phase-2-web/frontend/.env.local
  - phase-2-web/frontend/.env.example
  - phase-2-web/backend/src/auth.py
  - phase-2-web/backend/src/config.py
  - phase-2-web/backend/src/main.py
  - phase-2-web/backend/src/models/task.py
  - phase-2-web/backend/src/models/__init__.py
  - phase-2-web/backend/src/api/__init__.py
  - phase-2-web/backend/pyproject.toml
  - phase-2-web/backend/.env
  - phase-2-web/backend/.env.example
  - phase-2-web/backend/.gitignore
  - specs/004-better-auth-integration/tasks.md
tests:
  - TypeScript type-check (tsc --noEmit): PASS
  - Backend import verification: PASS
---

## Prompt

/sp.implement

## Response snapshot

Executed all 29 tasks across 7 phases for the Better Auth integration feature:

**Phase 1 (Setup)**: Installed `better-auth` and `pg` in frontend, replaced `python-jose`/`bcrypt` with `PyJWT[crypto]` in backend, updated `next.config.ts` with `serverExternalPackages`, configured env files with `DATABASE_URL`, `BETTER_AUTH_SECRET`, `JWKS_URL`, `JWT_ISSUER`.

**Phase 2 (Foundational)**: Created Better Auth server config (`src/lib/auth.ts`) with `pg` Pool, `nextCookies()`, `jwt()` plugins. Created client config (`src/lib/auth-client.ts`) with `jwtClient()`. Created catch-all route handler. Ran `@better-auth/cli migrate` to create `user`, `session`, `account`, `verification`, `jwks` tables in Neon PostgreSQL (dropped old user/task tables first). Rewrote backend `auth.py` with `PyJWKClient` for EdDSA JWKS verification. Updated `config.py` to use `jwks_url`/`jwt_issuer`. Changed `Task.user_id` from UUID to str. Removed old `User` model, backend auth router.

**Phase 3 (US1+US2)**: Rewrote signup page with `signUp.email()` (name + email + password), signin page with `signIn.email()`. Both use Better Auth client, no localStorage.

**Phase 4 (US3)**: Created `api-client.ts` with `authClient.token()` for JWT injection in Authorization header. Rewrote tasks page with `useSession()` hook, session-based auth, user name display.

**Phase 5-6 (US4+US5)**: Sign out via `signOut()` already in tasks page. Created `middleware.ts` with `getSessionCookie()` for route protection.

**Phase 7 (Polish)**: Created frontend `.env.example`, verified dead code clean, updated landing page, created backend `.gitignore`.

## Outcome

- ✅ Impact: Full Better Auth integration replacing custom JWT auth — 5 user stories implemented
- 🧪 Tests: TypeScript compiles cleanly; backend imports verified; no runtime tests (not requested)
- 📁 Files: 24 files modified/created, 2 files removed (user.py, api/auth.py)
- 🔁 Next prompts: Run `/sp.git.commit_pr` to commit and create PR; manual E2E verification (signup → signin → tasks CRUD → signout → middleware redirects)
- 🧠 Reflection: Better Auth docs show `new Pool()` from `pg` for PostgreSQL — not `provider: "postgresql"` as initially assumed from research. Migration required dropping old user table due to missing `name` column. The `@/*` path alias maps to `./src/*`, so auth files placed in `src/lib/` not `lib/`.

## Evaluation notes (flywheel)

- Failure modes observed: (1) Better Auth CLI `generate` command requires interactive input — used `migrate` with piped `y` instead. (2) Migration failed on existing `user` table due to NULL `name` column — resolved by dropping old tables. (3) `pg` module missing type declarations — installed `@types/pg`.
- Graders run and results (PASS/FAIL): TypeScript tsc PASS, Python import PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Run E2E verification with both services running
