# Research: Better Auth Integration

**Feature Branch**: `004-better-auth-integration`
**Date**: 2026-02-06

## R1: JWT Verification Strategy (Backend)

**Decision**: Use `PyJWT[crypto]` with `PyJWKClient` to verify
Better Auth JWTs via the JWKS endpoint.

**Rationale**:
- Better Auth JWT plugin uses **Ed25519** (OKP key type) for
  signing, exposed via `GET /api/auth/jwks`.
- `PyJWT[crypto]` supports Ed25519 via the `cryptography` package.
- `PyJWKClient` fetches and caches JWKS automatically, resolving
  the correct key by `kid` from the JWT header.
- This replaces `python-jose[cryptography]` which was used for
  HS256 symmetric JWT.

**Alternatives considered**:
- `python-jose`: Supports JWKS but is less maintained than PyJWT.
  Does not natively support Ed25519 OKP keys.
- Shared secret (HS256): Simpler but the constitution spec
  (FR-005) mandates JWKS-based asymmetric verification.
- `joserfc`: Newer library but less ecosystem adoption.

**Implementation pattern**:
```python
import jwt
from jwt import PyJWKClient

# Singleton client with built-in caching
jwks_client = PyJWKClient("http://localhost:3000/api/auth/jwks")

async def verify_jwt(token: str) -> dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["EdDSA"],
        issuer="http://localhost:3000",
        audience="http://localhost:3000",
    )
    return payload
```

---

## R2: Better Auth User ID Format

**Decision**: Better Auth generates user IDs as short random
strings (not UUIDs). The existing Task model's `user_id` column
(currently UUID) must be changed to a plain string type.

**Rationale**:
- Better Auth `user` table has `id: string` (typically nanoid-like,
  e.g., `"abc123xyz"`).
- The existing `Task.user_id` is `UUID` with `foreign_key="user.id"`.
- Since Better Auth owns the `user` table, the Task model must
  reference Better Auth's string-based user ID.
- The foreign key relationship to the Better Auth `user` table is
  maintained by column type alignment.

**Alternatives considered**:
- Keep UUID and configure Better Auth to use UUIDs: Better Auth
  does not natively support UUID primary keys without plugin
  customization. Adds unnecessary complexity.
- Remove foreign key constraint: Loses referential integrity.
  Rejected.

---

## R3: Better Auth Database Integration

**Decision**: Better Auth connects to Neon PostgreSQL directly
using its built-in `postgresql` provider. Schema is generated
via `npx @better-auth/cli generate`.

**Rationale**:
- Better Auth manages its own tables: `user`, `session`, `account`,
  `verification`.
- It uses its own connection pool — separate from SQLModel's engine.
- Both connect to the same `DATABASE_URL` (Neon PostgreSQL).
- The `Task` table (managed by SQLModel) references Better Auth's
  `user.id` column.

**Alternatives considered**:
- Drizzle adapter: Adds Drizzle as a dependency. Unnecessary since
  direct connection works with PostgreSQL.
- Prisma adapter: Adds Prisma dependency. Overkill for this use
  case.

---

## R4: Frontend Auth Flow

**Decision**: Replace localStorage-based JWT storage with Better
Auth session cookies + on-demand JWT fetching.

**Rationale**:
- Better Auth manages sessions via httpOnly cookies automatically.
- The `useSession()` hook provides reactive session state.
- For API calls to FastAPI, the frontend calls
  `GET /api/auth/token` to obtain a short-lived JWT (15min default)
  and sends it in the Authorization header.
- This is more secure than localStorage (immune to XSS).

**Flow**:
1. User signs in → Better Auth sets session cookie
2. `useSession()` returns session state for UI
3. Before API call → `authClient.getToken()` fetches JWT
4. JWT sent in `Authorization: Bearer <token>` header
5. FastAPI verifies JWT via JWKS

**Alternatives considered**:
- Continue using localStorage: XSS vulnerable. Rejected.
- Send session cookie directly to FastAPI: Cross-origin cookies
  are unreliable and require complex CORS configuration. Rejected.

---

## R5: API Route URL Pattern

**Decision**: Keep the existing flat URL pattern
(`/api/tasks`, `/api/auth/*`) instead of migrating to the
constitution's `{user_id}` path pattern immediately.

**Rationale**:
- The constitution specifies `/api/{user_id}/tasks` URL pattern.
- However, this feature focuses on Better Auth integration, not
  API restructuring.
- The `user_id` is extracted from the JWT payload — it does not
  need to be in the URL path for security.
- URL restructuring can be a separate task if needed.
- The JWT enforcement achieves the same security guarantee
  (user isolation) as the path-based pattern.

**Alternatives considered**:
- Migrate to `/api/{user_id}/tasks` now: Increases scope and
  risk. Can be done separately.

---

## R6: Better Auth + Next.js Config

**Decision**: Use the standard Better Auth + Next.js integration
with `nextCookies()` plugin, JWT plugin, and catch-all route
handler.

**Rationale**:
- Constitution (III.1) mandates: `lib/auth.ts` with `nextCookies()`
  and `jwt()` plugins.
- Catch-all route at `app/api/auth/[...all]/route.ts`.
- Client via `createAuthClient()` from `better-auth/react`.
- `next.config.ts` must include `serverExternalPackages: ['better-auth']`.

**Key configuration**:
```typescript
// lib/auth.ts (server)
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  plugins: [nextCookies(), jwt()],
});

// lib/auth-client.ts (client)
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [jwtClient()],
});
export const { useSession, signIn, signUp, signOut } = authClient;
```

---

## R7: Middleware Strategy

**Decision**: Use Next.js middleware with `getSessionCookie()` from
`better-auth/cookies` for route protection.

**Rationale**:
- Better Auth provides `getSessionCookie(request)` for edge
  middleware.
- No database call needed — just checks for cookie presence.
- Protected routes: `/tasks/*`
- Auth routes (redirect if authenticated): `/signin`, `/signup`

**Implementation pattern**:
```typescript
import { NextRequest, NextResponse } from "next/server";
import { getSessionCookie } from "better-auth/cookies";

export function middleware(request: NextRequest) {
  const session = getSessionCookie(request);
  const isAuthPage = ["/signin", "/signup"].some(
    (p) => request.nextUrl.pathname.startsWith(p)
  );

  if (!session && !isAuthPage) {
    return NextResponse.redirect(new URL("/signin", request.url));
  }
  if (session && isAuthPage) {
    return NextResponse.redirect(new URL("/tasks", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/tasks/:path*", "/signin", "/signup"],
};
```
