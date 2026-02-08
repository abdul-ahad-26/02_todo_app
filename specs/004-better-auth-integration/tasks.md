# Tasks: Better Auth Integration

**Input**: Design documents from `/specs/004-better-auth-integration/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/auth-endpoints.md

**Tests**: No test tasks — not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phase-2-web/backend/`, `phase-2-web/frontend/`
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure Better Auth foundation

- [x] T001 Install `better-auth` npm package in phase-2-web/frontend/package.json
- [x] T002 [P] Replace `python-jose[cryptography]` and `bcrypt` with `PyJWT[crypto]` in phase-2-web/backend/pyproject.toml
- [x] T003 [P] Update phase-2-web/frontend/next.config.ts to add `serverExternalPackages: ['better-auth']`
- [x] T004 Update phase-2-web/frontend/.env.local to add `DATABASE_URL` and `BETTER_AUTH_SECRET` variables
- [x] T005 [P] Update phase-2-web/backend/.env and phase-2-web/backend/.env.example to replace `JWT_SECRET`/`JWT_ALGORITHM`/`JWT_EXPIRATION_HOURS` with `JWKS_URL` and `JWT_ISSUER`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Better Auth server config and backend JWT verification that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create Better Auth server configuration in phase-2-web/frontend/src/lib/auth.ts with `betterAuth()`, `nextCookies()` plugin, `jwt()` plugin, PostgreSQL database via `pg` Pool, and `emailAndPassword` enabled with `minPasswordLength: 8`
- [x] T007 Create Better Auth client configuration in phase-2-web/frontend/src/lib/auth-client.ts with `createAuthClient()`, `jwtClient()` plugin, and export `useSession`, `signIn`, `signUp`, `signOut` hooks
- [x] T008 Create Better Auth catch-all route handler in phase-2-web/frontend/src/app/api/auth/[...all]/route.ts using `toNextJsHandler(auth)`
- [x] T009 Generate Better Auth database schema by running `npx @better-auth/cli migrate` — created `user`, `session`, `account`, `verification`, `jwks` tables in Neon PostgreSQL
- [x] T010 Rewrite phase-2-web/backend/src/auth.py to use `PyJWT[crypto]` with `PyJWKClient` for JWKS-based JWT verification — `jwks_client` singleton and `get_user_id_from_token()` FastAPI dependency that extracts `sub` from JWT payload and returns user ID string
- [x] T011 Update phase-2-web/backend/src/config.py to remove `jwt_secret`, `jwt_algorithm`, `jwt_expiration_hours` settings and add `jwks_url` and `jwt_issuer`
- [x] T012 Modify Task model in phase-2-web/backend/src/models/task.py to change `user_id` field type from `UUID` to `str` (matching Better Auth string user IDs)
- [x] T013 Remove phase-2-web/backend/src/models/user.py (Better Auth owns user management)
- [x] T014 Remove phase-2-web/backend/src/api/auth.py (Better Auth handles signup/signin)
- [x] T015 Update phase-2-web/backend/src/main.py to remove the auth router import and registration, remove User model import from `models/__init__.py`, and ensure only the tasks router is mounted at `/api`
- [x] T016 Backend tasks.py already uses `get_user_id_from_token` — now returns `str` instead of `UUID`, compatible with updated Task model
- [x] T017 Backend db.py — no User model references to remove; `SQLModel.metadata.create_all` creates `task` table only

**Checkpoint**: Better Auth server running with JWT + JWKS endpoints exposed. Backend verifies JWTs via JWKS. Task model uses string user IDs. Old custom auth completely removed.

---

## Phase 3: User Story 1 & 2 — Sign Up + Sign In (Priority: P1)

**Goal**: Users can create accounts and sign in via Better Auth email/password. Sessions are managed by httpOnly cookies.

**Independent Test**: Navigate to /signup, create an account, verify redirect to /tasks. Navigate to /signin, sign in, verify redirect to /tasks.

### Implementation for User Stories 1 & 2

- [x] T018 [US1] Rewrite phase-2-web/frontend/src/app/signup/page.tsx to use `signUp.email()` from `@/lib/auth-client` — form submits name, email, password; on success redirect to `/tasks`; on error display message
- [x] T019 [US2] Rewrite phase-2-web/frontend/src/app/signin/page.tsx to use `signIn.email()` from `@/lib/auth-client` — form submits email, password; on success redirect to `/tasks`; on error display "Invalid credentials"
- [x] T020 [P] [US1] Navigation links between sign-in and sign-up pages already present in both pages

**Checkpoint**: Sign up creates a user in the database. Sign in establishes a session cookie. Both redirect to /tasks on success.

---

## Phase 4: User Story 3 — Protected API Access via JWT (Priority: P1)

**Goal**: Authenticated users can perform task CRUD operations. Frontend obtains JWT from Better Auth and sends it in Authorization header. Backend verifies via JWKS.

**Independent Test**: Sign in, create a task, verify it appears in the list. Try accessing /api/tasks without a token — verify 401. Sign in as different user — verify task isolation.

### Implementation for User Story 3

- [x] T021 [US3] Created API client at `src/lib/api-client.ts` using `authClient.token()` for JWT, `Authorization: Bearer` header, AUTH_REQUIRED error for 401, exported typed `apiClient` with all task CRUD methods
- [x] T022 [US3] Rewrote tasks page to use `useSession()` hook, removed all localStorage references, display user name, `apiClient` handles JWT automatically

**Checkpoint**: Full task CRUD works with Better Auth JWT. No localStorage tokens. Backend rejects unauthenticated requests with 401.

---

## Phase 5: User Story 4 — Sign Out (Priority: P2)

**Goal**: Users can sign out, terminating their session. After sign out, protected pages and API are inaccessible.

**Independent Test**: Sign in, click Sign Out, verify redirect to /signin. Try accessing /tasks — verify redirect. Try API call — verify 401.

### Implementation for User Story 4

- [x] T023 [US4] Sign out implemented in tasks page — "Sign Out" button calls `signOut()` from auth-client and redirects to `/signin`; localStorage.clear() removed

**Checkpoint**: Sign out clears session cookie. User redirected to sign-in. API calls fail with 401 after sign-out.

---

## Phase 6: User Story 5 — Route Protection Middleware (Priority: P2)

**Goal**: Protected pages redirect unauthenticated users to /signin. Auth pages redirect authenticated users to /tasks.

**Independent Test**: Without signing in, navigate to /tasks — verify redirect to /signin. While signed in, navigate to /signin — verify redirect to /tasks.

### Implementation for User Story 5

- [x] T024 [US5] Created `src/middleware.ts` with `getSessionCookie()` — unauthenticated users redirected from `/tasks/*` to `/signin`; authenticated users redirected from auth pages to `/tasks`

**Checkpoint**: Middleware guards all protected routes. Auth flow redirect works in both directions.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Cleanup, environment templates, documentation

- [x] T025 [P] Created `phase-2-web/frontend/.env.example` with `DATABASE_URL`, `BETTER_AUTH_SECRET`, `NEXT_PUBLIC_API_URL`
- [x] T026 [P] Updated `phase-2-web/backend/.env.example` with `DATABASE_URL`, `JWKS_URL`, `JWT_ISSUER`, `CORS_ORIGINS`
- [x] T027 [P] Dead code verified clean — no `localStorage`, `python-jose`, `bcrypt`, `create_token`, `JWT_SECRET` references remain
- [x] T028 Updated landing page footer; sign-in/sign-up links already correct
- [x] T029 Created `phase-2-web/backend/.gitignore` for Python project; skipped README per project policy (no proactive docs)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US1+US2 Sign Up/In (Phase 3)**: Depends on Phase 2 (Better Auth server + client must exist)
- **US3 JWT API (Phase 4)**: Depends on Phase 2 (JWKS verification must work) + Phase 3 (need sign-in to get JWT)
- **US4 Sign Out (Phase 5)**: Depends on Phase 3 (need sign-in to test sign-out)
- **US5 Middleware (Phase 6)**: Depends on Phase 2 (Better Auth cookies must work) — can run in parallel with Phases 3-5
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

```text
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundation) ──── BLOCKS ALL ────┐
    │                                     │
    ▼                                     ▼
Phase 3 (US1+US2: Sign Up/In)    Phase 6 (US5: Middleware)
    │                              [can run in parallel]
    ▼
Phase 4 (US3: JWT API Access)
    │
    ▼
Phase 5 (US4: Sign Out)
    │
    ▼
Phase 7 (Polish)
```

### Within Each Phase

- Tasks marked [P] can run in parallel
- Models before services
- Backend auth before frontend auth (JWKS must be verifiable)
- Core implementation before integration
- Phase complete before moving to next

### Parallel Opportunities

```text
# Phase 1 — all parallelizable:
T001, T002, T003, T004, T005

# Phase 2 — frontend and backend can partly overlap:
T006+T007+T008 (frontend) can run in parallel with T010+T011 (backend)
T012+T013+T014 must complete before T015+T016+T017

# Phase 3 — sign-up and sign-in pages are parallel:
T018 (signup) and T019 (signin) can run in parallel
T020 (nav links) depends on both T018 and T019

# Phase 6 — independent of Phases 3-5:
T024 can run in parallel with Phase 3, 4, or 5

# Phase 7 — all parallelizable:
T025, T026, T027, T028 can run in parallel
T029 depends on all prior phases
```

---

## Implementation Strategy

### MVP First (User Stories 1+2+3 Only)

1. Complete Phase 1: Setup (install deps, configure env)
2. Complete Phase 2: Foundational (Better Auth + JWKS)
3. Complete Phase 3: Sign Up + Sign In
4. Complete Phase 4: JWT API Access
5. **STOP and VALIDATE**: Full auth flow works end-to-end
6. Users can sign up, sign in, and manage tasks securely

### Incremental Delivery

1. Setup + Foundational → Auth infrastructure ready
2. Add US1+US2 (Sign Up/In) → Test independently → Users can authenticate
3. Add US3 (JWT API) → Test independently → Tasks work with JWT
4. Add US4 (Sign Out) → Test independently → Session lifecycle complete
5. Add US5 (Middleware) → Test independently → Route protection active
6. Polish → Cleanup + docs → Feature complete

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US1 and US2 are combined in Phase 3 because they share the same Better Auth infrastructure and are tightly coupled (sign-up leads to sign-in)
- Better Auth manages its own database tables — SQLModel only manages the `task` table
- The `user_id` type change (UUID → string) is the most impactful data model change
- Old auth files (`python-jose`, `bcrypt`, custom JWT) are fully removed in Phase 2
- Commit after each phase or logical group for clean git history
