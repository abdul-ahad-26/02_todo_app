# Research: Phase II - Full-Stack Web Application

**Feature**: 005-fullstack-web-app
**Date**: 2026-02-08

## R-001: Better Auth JWT Plugin + Next.js Integration

**Decision**: Use Better Auth with `jwt()` plugin on the server and `jwtClient()` on the client. The frontend retrieves JWT tokens via `authClient.token()` and attaches them to FastAPI API calls in the `Authorization: Bearer <token>` header.

**Rationale**: The JWT plugin provides a dedicated `/token` endpoint and JWKS endpoint for token verification. This is the recommended pattern for authenticating with external services (FastAPI backend) while Better Auth manages sessions on the Next.js side. The Bearer plugin is an alternative but JWT plugin provides standard JWKS verification.

**Alternatives Considered**:
- **Bearer plugin only**: Simpler but uses session tokens directly. Requires calling `auth.api.getSession()` on every request, which couples the backend to the Next.js auth server. Rejected for not being stateless.
- **Cookie-based sessions shared between frontend and backend**: Not viable since frontend (Next.js) and backend (FastAPI) are separate services on different ports/domains.

**Key Implementation Details**:
- Server: `lib/auth.ts` — `betterAuth({ plugins: [jwt(), nextCookies()] })`
- Client: `lib/auth-client.ts` — `createAuthClient({ plugins: [jwtClient()] })`
- Token retrieval: `const { data } = await authClient.token()` → `data.token`
- Route handler: `app/api/auth/[...all]/route.ts` → `toNextJsHandler(auth)`
- Better Auth auto-creates tables: `user` (id, name, email, emailVerified, image, createdAt, updatedAt), `session` (id, userId, token, expiresAt, ipAddress, userAgent), `account` (id, userId, accountId, providerId, accessToken, refreshToken)

---

## R-002: FastAPI JWT Verification Strategy

**Decision**: Use PyJWT library to verify JWT tokens signed by Better Auth using the shared `BETTER_AUTH_SECRET` environment variable with HS256 algorithm. Implement as a FastAPI dependency (`Depends(verify_jwt_token)`).

**Rationale**: Better Auth's JWT plugin signs tokens with the `BETTER_AUTH_SECRET`. PyJWT can verify these tokens without needing to call the Next.js server, keeping the backend stateless. The dependency injection pattern in FastAPI makes it clean to apply to all task endpoints.

**Alternatives Considered**:
- **JWKS verification (asymmetric keys)**: Better Auth supports JWKS endpoint but requires public key fetching. Adds complexity. HS256 with shared secret is simpler and sufficient for a monorepo where both services share the same secret.
- **Calling Better Auth API from FastAPI**: Would add latency and create a dependency on the frontend server being available. Rejected for violating statelessness principle.

**Key Implementation Details**:
- Dependency: `HTTPBearer` security scheme → extract token → `jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])`
- The JWT `sub` claim contains the user ID
- Every endpoint validates `user_id` path parameter matches JWT `sub` claim
- Returns 401 for missing/invalid/expired tokens

---

## R-003: Next.js 16 App Router Architecture

**Decision**: Use Next.js 16 App Router with Server Components by default, Client Components only for interactive forms/toggles. The frontend calls the FastAPI backend directly from Client Components via a centralized API client (`lib/api.ts`).

**Rationale**: Server Components reduce JavaScript bundle size and are ideal for initial page loads. Client Components handle interactivity (forms, toggles). Direct calls to FastAPI from the client (with JWT token in header) is simpler than proxying through Next.js Route Handlers, and aligns with the architecture where Better Auth handles sessions on the frontend and JWT tokens authenticate with the backend.

**Alternatives Considered**:
- **Proxy through Next.js Route Handlers**: Would add an extra hop for every API call. More secure (backend URL hidden) but adds complexity and latency. Not needed since the FastAPI URL will be public for deployment anyway.
- **Server Actions for all mutations**: Possible but adds coupling between frontend rendering and backend API calls. Direct REST calls are more portable and align with Phase III where the same API serves the chatbot.

**Key Implementation Details**:
- `app/layout.tsx` — Root layout with dark theme, auth provider
- `app/page.tsx` — Landing/redirect to dashboard or sign-in
- `app/(auth)/sign-in/page.tsx` — Sign-in form (Client Component)
- `app/(auth)/sign-up/page.tsx` — Sign-up form (Client Component)
- `app/dashboard/page.tsx` — Task list (Server Component fetches, Client Component renders interactive elements)
- `app/api/auth/[...all]/route.ts` — Better Auth handler
- `lib/api.ts` — Centralized API client with JWT token attachment
- `lib/auth.ts` — Better Auth server config
- `lib/auth-client.ts` — Better Auth client config
- `middleware.ts` — Redirect unauthenticated users to sign-in

---

## R-004: SQLModel + Neon PostgreSQL Data Layer

**Decision**: Use synchronous SQLModel with standard `Session` (not async). Use `create_engine` with `pool_pre_ping=True` for Neon serverless connection resilience. Task IDs use UUID strings (not auto-increment integers) to avoid conflicts.

**Rationale**: Sync SQLModel is simpler and FastAPI automatically runs sync database operations in a thread pool. For Phase II scale (<1000 users), the performance difference is negligible. Neon's serverless connection pooling handles cold starts; `pool_pre_ping=True` ensures stale connections are detected.

**Alternatives Considered**:
- **Async SQLModel with asyncpg**: More performant under high concurrency but significantly more complex setup. Overkill for Phase II. Can be migrated to in Phase IV/V if needed.
- **Auto-increment integer IDs**: Simpler but UUID strings are more portable and don't leak information about task counts. Better Auth uses string IDs for users, so string task IDs maintain consistency.

**Key Implementation Details**:
- Engine: `create_engine(DATABASE_URL, pool_pre_ping=True)`
- Session dependency: `get_session()` yields `Session(engine)`
- Tables created via `SQLModel.metadata.create_all(engine)` on startup
- Better Auth manages its own tables (user, session, account) in the same database
- Task table has `user_id` FK referencing Better Auth's `user.id`

---

## R-005: Project Structure (Monorepo)

**Decision**: Use the constitution-mandated monorepo layout with `phase-2-web/frontend/` and `phase-2-web/backend/` directories. Each has its own `CLAUDE.md` for context-specific instructions.

**Rationale**: Constitution Section VI mandates phase-based directories (`phase-<N>-<slug>/`) and monorepo layout for Phase II+. This keeps the codebase organized and allows Claude Code to navigate both frontend and backend in a single context.

**Key Implementation Details**:
```
phase-2-web/
├── frontend/                 # Next.js 16+ App
│   ├── CLAUDE.md
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   ├── middleware.ts
│   ├── .env.local.example
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── (auth)/
│   │   │   │   ├── sign-in/page.tsx
│   │   │   │   └── sign-up/page.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── layout.tsx
│   │   │   │   └── page.tsx
│   │   │   └── api/
│   │   │       └── auth/
│   │   │           └── [...all]/route.ts
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── auth/
│   │   │   └── tasks/
│   │   └── lib/
│   │       ├── auth.ts
│   │       ├── auth-client.ts
│   │       └── api.ts
│   └── public/
├── backend/                  # FastAPI Server
│   ├── CLAUDE.md
│   ├── pyproject.toml
│   ├── .env.example
│   └── src/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── db.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   └── routers/
│       │       ├── __init__.py
│       │       └── tasks.py
│       └── crud/
│           ├── __init__.py
│           └── task.py
├── docker-compose.yml
└── README.md
```

---

## R-006: Design Theme Integration

**Decision**: Implement the constitution's Modern Dark/High-Contrast theme using Tailwind CSS custom properties. Define CSS variables in `globals.css` and extend Tailwind config to reference them.

**Rationale**: Constitution Section V mandates specific CSS palette variables. Tailwind CSS is mandated for styling. Using CSS variables as Tailwind theme extensions ensures consistency and allows future phases to inherit the same theme.

**Key Implementation Details**:
- CSS variables in `globals.css`: `--primary: #3b82f6`, `--secondary: #10b981`, `--accent: #8b5cf6`, `--background: #0f172a`, `--foreground: #f8fafc`, `--error: #ef4444`
- Tailwind config extends `colors` to reference these variables
- All components use Tailwind classes, no inline styles
