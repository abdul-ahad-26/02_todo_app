# Implementation Plan: Better Auth Integration

**Branch**: `004-better-auth-integration` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-better-auth-integration/spec.md`

## Summary

Replace the existing custom JWT authentication (python-jose,
bcrypt, localStorage tokens) with Better Auth as the sole
authentication authority. Better Auth manages user registration,
sessions (httpOnly cookies), and JWT issuance (Ed25519 via JWT
plugin). The FastAPI backend verifies JWTs asymmetrically via
Better Auth's JWKS endpoint using PyJWT. Next.js middleware
provides route-level protection.

## Technical Context

**Language/Version**: TypeScript (Next.js 16+), Python 3.13+ (FastAPI)
**Primary Dependencies**:
  - Frontend: `better-auth`, `better-auth/react`, `better-auth/plugins` (JWT)
  - Backend: `PyJWT[crypto]` (replaces `python-jose[cryptography]` + `bcrypt`)
**Storage**: Neon Serverless PostgreSQL (shared by Better Auth and SQLModel)
**Testing**: Manual verification (quickstart.md)
**Target Platform**: Web (localhost:3000 frontend, localhost:8000 backend)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**: Sign-in < 5s, JWT verification < 50ms
**Constraints**: Ed25519 JWKS verification, httpOnly cookies, no localStorage tokens
**Scale/Scope**: Single-user dev environment, multi-user production

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Constitution Ref | Status |
|------|-----------------|--------|
| Better Auth as auth provider | II.2 (Phase II tech stack) | PASS |
| JWT plugin enabled | III.1 (Better Auth config) | PASS |
| `lib/auth.ts` with `nextCookies()` + `jwt()` | III.1 | PASS |
| `app/api/auth/[...all]/route.ts` handler | III.1 | PASS |
| `createAuthClient()` from `better-auth/react` | III.1 | PASS |
| JWT in `Authorization: Bearer` header | III.2 | PASS |
| Backend verifies JWT | III.2 | PASS |
| No hardcoded secrets | III.3 | PASS |
| `.env.example` provided | III.3 | PASS |
| CORS configured for frontend origin | III.4 | PASS |
| Backend stateless | IV.1 | PASS |
| JSON responses with Pydantic models | IV.3 | PASS |
| SQLModel ORM for tasks | IV.4 | PASS |
| `DATABASE_URL` env var | IV.4 | PASS |
| Neon PostgreSQL | IV.4 | PASS |
| CSS variables for auth UI | V.1 | PASS |
| Phase directory structure | VI.1 | PASS |
| PEP 8, type hints, async/await | VII.1 | PASS |
| TypeScript strict, Tailwind CSS | VII.2 | PASS |
| Centralized API client | VII.2 | PASS |

**Constitution deviation (documented)**:

| Gate | Constitution Ref | Status | Justification |
|------|-----------------|--------|---------------|
| API URL pattern `/api/{user_id}/tasks` | IV.3 | DEFERRED | Existing routes use `/api/tasks`. JWT enforces user isolation equivalently. URL restructuring is a separate task. |
| JWT verified via BETTER_AUTH_SECRET | III.2 | SUPERSEDED | Spec FR-005 mandates JWKS-based verification (asymmetric). This is more secure than shared secret. Constitution III.2 will be updated. |

## Project Structure

### Documentation (this feature)

```text
specs/004-better-auth-integration/
├── plan.md              # This file
├── research.md          # Phase 0: technology decisions
├── data-model.md        # Phase 1: entity relationships
├── quickstart.md        # Phase 1: setup instructions
├── contracts/
│   └── auth-endpoints.md  # Phase 1: API contracts
└── tasks.md             # Phase 2: /sp.tasks output
```

### Source Code (repository root)

```text
phase-2-web/
├── frontend/
│   ├── lib/
│   │   ├── auth.ts              # NEW: Better Auth server config
│   │   ├── auth-client.ts       # NEW: Better Auth client + hooks
│   │   └── api-client.ts        # MODIFIED: JWT token injection
│   ├── src/app/
│   │   ├── api/auth/
│   │   │   └── [...all]/
│   │   │       └── route.ts     # NEW: Better Auth route handler
│   │   ├── signin/page.tsx      # MODIFIED: Use Better Auth signIn
│   │   ├── signup/page.tsx      # MODIFIED: Use Better Auth signUp
│   │   └── tasks/page.tsx       # MODIFIED: Use useSession + JWT
│   ├── middleware.ts            # NEW: Route protection
│   ├── next.config.ts           # MODIFIED: serverExternalPackages
│   ├── package.json             # MODIFIED: Add better-auth
│   └── .env.local               # MODIFIED: Add DATABASE_URL, SECRET
├── backend/
│   ├── src/
│   │   ├── auth.py              # REWRITTEN: JWKS-based verification
│   │   ├── config.py            # MODIFIED: Remove JWT_*, add JWKS_URL
│   │   ├── main.py              # MODIFIED: Remove auth router
│   │   ├── api/
│   │   │   ├── auth.py          # REMOVED: Better Auth handles this
│   │   │   └── tasks.py         # MODIFIED: New auth dependency
│   │   └── models/
│   │       ├── user.py          # REMOVED: Better Auth owns users
│   │       └── task.py          # MODIFIED: user_id type to string
│   ├── pyproject.toml           # MODIFIED: Swap deps
│   └── .env                     # MODIFIED: Remove JWT_*, add JWKS_URL
└── docker-compose.yml
```

**Structure Decision**: Web application (Option 2). Modifies the
existing `phase-2-web/` monorepo in-place. No new top-level
directories.

### Files Summary

| Action | File | Reason |
|--------|------|--------|
| NEW | `frontend/lib/auth.ts` | Better Auth server config |
| NEW | `frontend/lib/auth-client.ts` | Better Auth client + hooks |
| NEW | `frontend/src/app/api/auth/[...all]/route.ts` | Catch-all handler |
| NEW | `frontend/middleware.ts` | Route protection |
| MODIFY | `frontend/lib/api-client.ts` | Add JWT token injection |
| MODIFY | `frontend/src/app/signin/page.tsx` | Use authClient.signIn |
| MODIFY | `frontend/src/app/signup/page.tsx` | Use authClient.signUp |
| MODIFY | `frontend/src/app/tasks/page.tsx` | Use useSession + signOut |
| MODIFY | `frontend/next.config.ts` | Add serverExternalPackages |
| MODIFY | `frontend/package.json` | Add better-auth dependency |
| MODIFY | `frontend/.env.local` | Add DATABASE_URL, SECRET |
| REWRITE | `backend/src/auth.py` | JWKS verification via PyJWT |
| MODIFY | `backend/src/config.py` | Replace JWT_* with JWKS_URL |
| MODIFY | `backend/src/main.py` | Remove auth router import |
| REMOVE | `backend/src/api/auth.py` | Better Auth handles auth |
| REMOVE | `backend/src/models/user.py` | Better Auth owns users |
| MODIFY | `backend/src/api/tasks.py` | New auth dependency |
| MODIFY | `backend/src/models/task.py` | user_id type to string |
| MODIFY | `backend/pyproject.toml` | Swap python-jose/bcrypt → PyJWT |
| MODIFY | `backend/.env` | Replace JWT_* with JWKS_URL |

## Complexity Tracking

| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| API URL pattern deferred | Scope creep risk; JWT already enforces isolation | Changing all URLs increases blast radius of this feature |
| JWKS instead of shared secret | Asymmetric verification is more secure and standard | Shared secret requires coordinating env vars across services |
