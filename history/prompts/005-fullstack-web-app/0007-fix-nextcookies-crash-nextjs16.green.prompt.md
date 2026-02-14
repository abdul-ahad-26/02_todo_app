---
id: 0007
title: Fix nextCookies crash on Next.js 16
stage: green
date: 2026-02-14
surface: agent
model: claude-opus-4-6
feature: 005-fullstack-web-app
branch: 005-fullstack-web-app
user: abdul
command: none
labels: ["better-auth", "nextCookies", "next.js-16", "session-management", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/frontend/src/lib/auth.ts
  - phase-2-web/frontend/src/lib/auth-client.ts
  - phase-2-web/frontend/.env.local
tests:
  - Manual HTTP test: POST /api/auth/sign-up (returns 200, sets session cookie)
  - Manual HTTP test: POST /api/auth/sign-in (returns 200, sets session cookie)
  - Manual HTTP test: GET /api/auth/get-session (returns 200 with session data)
  - Manual HTTP test: POST /api/auth/generate-token (returns 200 with JWT)
---

## Prompt

i have implemented better auth in phase 2 full stack web app but the session is expiring immediately after signing in it logs out.

## Response snapshot

**Root cause identified:** The `nextCookies()` plugin from `better-auth/next-js` is incompatible with Next.js 16's async `cookies()` API. When Better Auth attempted to set session cookies during sign-in/sign-up, `nextCookies()` threw an error because it tried to access `cookies()` synchronously. This caused silent 500 errors on every auth request that sets cookies, so the session cookie was never sent to the browser.

**Fix applied:**

1. **Removed `nextCookies()` plugin** from server auth config (`phase-2-web/frontend/src/lib/auth.ts`)
   - This plugin is only needed for server-side rendering with `getServerSideProps`, which we don't use
   - Our auth flow is fully client-side (sign-in/sign-up on client → session cookie → client-side session reads)

2. **Added required Better Auth config** to ensure proper cookie handling:
   - Server: `baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL` and `trustedOrigins: [process.env.NEXT_PUBLIC_BETTER_AUTH_URL]`
   - Client: `baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL`
   - Environment: `NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000` in `.env.local`

3. **Verified with HTTP tests** (curl and Node.js):
   - Sign-up: Returns 200, sets `better-auth.session_token` cookie with 7-day expiry
   - Sign-in: Returns 200, sets `better-auth.session_token` cookie with 7-day expiry
   - Get-session: Returns 200 with user session data when cookie is present
   - Generate-token (JWT): Returns 200 with valid JWT token

The fix ensures cookies are set correctly without relying on Next.js-specific plugins that break on async APIs.

## Outcome

- ✅ Impact: Session authentication now works end-to-end. Users can sign up, sign in, and maintain sessions for 7 days. Silent 500 errors on auth endpoints eliminated.
- 🧪 Tests: Manual HTTP tests confirm sign-up, sign-in, get-session, and JWT generation all return 200 with correct cookies/tokens.
- 📁 Files: Modified 3 files (auth.ts, auth-client.ts, .env.local) to remove nextCookies() and add baseURL config.
- 🔁 Next prompts: Test UI sign-in/sign-up flow in browser to confirm session persistence across page reloads.
- 🧠 Reflection: Better Auth documentation doesn't clearly warn about nextCookies() incompatibility with Next.js 16. The plugin is only needed for server-side rendering patterns (getServerSideProps), not client-side auth flows. Always check plugin requirements against framework versions.

## Evaluation notes (flywheel)

- Failure modes observed: Silent 500 errors on cookie-setting endpoints caused by sync/async API mismatch. Error was not visible in browser (redirect intercepted response). Required terminal curl tests to diagnose.
- Graders run and results (PASS/FAIL): PASS - All manual HTTP tests pass (sign-up, sign-in, get-session, generate-token). Session cookies set with correct expiry (7 days).
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Test UI flow in browser; add automated E2E tests for auth flow to catch cookie-setting regressions.
