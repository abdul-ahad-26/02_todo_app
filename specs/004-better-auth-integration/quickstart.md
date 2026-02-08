# Quickstart: Better Auth Integration

**Feature Branch**: `004-better-auth-integration`
**Prerequisites**: Node.js 18+, Python 3.13+, UV, Neon PostgreSQL

## 1. Install Frontend Dependencies

```bash
cd phase-2-web/frontend
npm install better-auth
```

## 2. Configure Better Auth Server

Create `phase-2-web/frontend/lib/auth.ts`:

```typescript
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
```

## 3. Create Auth Route Handler

Create `phase-2-web/frontend/src/app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

## 4. Create Auth Client

Create `phase-2-web/frontend/lib/auth-client.ts`:

```typescript
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [jwtClient()],
});

export const { useSession, signIn, signUp, signOut } = authClient;
```

## 5. Generate Database Schema

```bash
cd phase-2-web/frontend
npx @better-auth/cli generate
```

This creates the `user`, `session`, `account`, and `verification`
tables in your Neon PostgreSQL database.

## 6. Update Backend Dependencies

```bash
cd phase-2-web/backend
uv remove python-jose bcrypt
uv add PyJWT[crypto]
```

## 7. Update Backend JWT Verification

Replace `phase-2-web/backend/src/auth.py` with JWKS-based
verification using `PyJWKClient`.

## 8. Environment Variables

**Frontend** (`.env.local`):
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-secret-at-least-32-chars
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Backend** (`.env`):
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
JWKS_URL=http://localhost:3000/api/auth/jwks
JWT_ISSUER=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
```

## 9. Run

```bash
# Terminal 1: Frontend
cd phase-2-web/frontend
npm run dev

# Terminal 2: Backend
cd phase-2-web/backend
uv run uvicorn src.main:app --reload --port 8000
```

## 10. Verify

1. Open http://localhost:3000/signup — create an account
2. Sign in at http://localhost:3000/signin
3. Verify tasks page loads at http://localhost:3000/tasks
4. Check JWKS at http://localhost:3000/api/auth/jwks
5. Create a task and verify it appears in the list
