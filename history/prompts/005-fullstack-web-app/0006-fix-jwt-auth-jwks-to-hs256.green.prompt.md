---
id: "0006"
title: "Fix JWT Auth JWKS to HS256 Shared Secret"
stage: green
date: 2026-02-12
surface: agent
model: claude-opus-4-6
feature: 005-fullstack-web-app
branch: 005-fullstack-web-app
user: abdul
command: /sp.implement
labels: ["jwt", "hs256", "auth", "better-auth", "fastapi", "security"]
links:
  spec: specs/005-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-2-web/backend/src/api/auth.py
  - phase-2-web/backend/src/config.py
  - phase-2-web/frontend/src/lib/auth.ts
  - phase-2-web/frontend/package.json
tests:
  - "Manual E2E: sign in, verify JWT issued with HS256, make API call, verify backend decodes token with shared secret"
---

## Prompt

implement fast api in this way:
Securing the REST API
Better Auth + FastAPI Integration
The Challenge
Better Auth is a JavaScript/TypeScript authentication library that runs on your Next.js frontend. However, your FastAPI backend is a separate Python service that needs to verify which user is making API requests.
The Solution: JWT Tokens
Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.
How It Works
User logs in on Frontend → Better Auth creates a session and issues a JWT token
Frontend makes API call → Includes the JWT token in the Authorization: Bearer <token> header
Backend receives request → Extracts token from header, verifies signature using shared secret
Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
Backend filters data → Returns only tasks belonging to that user

also read this disccusion:
Short answer: the architecture is correct in principle, but there are a few common reasons it "doesn't work" in practice.
[Discussion about HS256 vs JWKS, proper FastAPI setup, user_id in URL design]

scan the code and fix the previous not working better auth implementation.

## Response snapshot

Replaced JWKS-based asymmetric JWT verification with HS256 shared-secret approach across frontend and backend:

1. **Backend `auth.py`**: Removed PyJWKClient, JWKS URL fetching, and EdDSA/ES256/RS256 algorithms. Now uses simple `jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])`.
2. **Backend `config.py`**: Removed `BETTER_AUTH_URL` setting (no longer needed for JWKS endpoint).
3. **Frontend `auth.ts`**: Added custom `sign` function to JWT plugin using `jose`'s `SignJWT` with HS256 algorithm and `BETTER_AUTH_SECRET`. Added `definePayload` to include `sub`, `email`, `name` claims.
4. **Frontend `package.json`**: Added `jose` as direct dependency for JWT signing.

## Outcome

- Impact: JWT auth flow now uses HS256 shared secret — no network dependency between backend→frontend for key verification
- Tests: Manual E2E testing required (sign in, create task, verify auth works)
- Files: 4 files modified
- Next prompts: Test locally, verify full auth flow works end-to-end
- Reflection: Previous implementation used JWKS (asymmetric keys) which required backend to fetch keys from frontend — fragile and unnecessary when both services share BETTER_AUTH_SECRET

## Evaluation notes (flywheel)

- Failure modes observed: JWKS approach required backend→frontend network call, wrong algorithm list (EdDSA/ES256/RS256 vs HS256)
- Graders run and results (PASS/FAIL): Code review PASS — all changes consistent with HS256 shared-secret pattern
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test full auth flow locally to verify tokens are issued and verified correctly
