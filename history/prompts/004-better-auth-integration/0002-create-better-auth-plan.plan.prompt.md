---
id: 0002
title: Create Better Auth Integration Plan
stage: plan
date: 2026-02-06
surface: agent
model: claude-opus-4-6
feature: 004-better-auth-integration
branch: 004-better-auth-integration
user: abdul
command: /sp.plan
labels: ["plan", "better-auth", "jwt", "jwks", "pyjwt", "architecture"]
links:
  spec: specs/004-better-auth-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-better-auth-integration/plan.md
  - specs/004-better-auth-integration/research.md
  - specs/004-better-auth-integration/data-model.md
  - specs/004-better-auth-integration/quickstart.md
  - specs/004-better-auth-integration/contracts/auth-endpoints.md
tests:
  - null
---

## Prompt

/sp.plan (no additional arguments — plan for current feature branch 004-better-auth-integration)

## Response snapshot

Created comprehensive implementation plan for Better Auth integration. Key artifacts:

**research.md** — 7 research decisions:
- R1: PyJWT[crypto] with PyJWKClient for JWKS-based JWT verification (Ed25519)
- R2: Better Auth user IDs are strings (not UUIDs) — task model migration needed
- R3: Better Auth uses direct PostgreSQL connection to Neon DB
- R4: Session cookies + on-demand JWT fetching replaces localStorage
- R5: Keep flat API URL pattern (defer {user_id} path migration)
- R6: Standard Better Auth + Next.js setup with nextCookies() + jwt() plugins
- R7: getSessionCookie() middleware for route protection

**data-model.md** — Entity relationship diagram:
- 4 Better Auth tables: user, session, account, verification
- 1 modified SQLModel table: task (user_id UUID → string)

**contracts/auth-endpoints.md** — Full API contracts:
- 6 Better Auth endpoints (sign-up, sign-in, sign-out, get-session, token, jwks)
- 6 existing FastAPI task endpoints (unchanged contract, new auth dependency)

**plan.md** — Implementation plan:
- 19 files affected (4 NEW, 11 MODIFY, 2 REMOVE, 2 REWRITE)
- Constitution check: 20 gates PASS, 2 documented deviations (API URL pattern deferred, JWKS supersedes shared secret)

**quickstart.md** — 10-step setup instructions

## Outcome

- Impact: Complete architecture plan ready for task generation
- Tests: N/A (planning phase)
- Files: plan.md, research.md, data-model.md, quickstart.md, contracts/auth-endpoints.md
- Next prompts: /sp.tasks to generate actionable task list
- Reflection: JWKS-based verification with Ed25519 is the correct approach for Better Auth JWT plugin. PyJWT[crypto] replaces both python-jose and bcrypt dependencies.

## Evaluation notes (flywheel)

- Failure modes observed: Constitution III.2 mentions shared secret but spec FR-005 mandates JWKS — documented as superseded deviation
- Graders run and results (PASS/FAIL): Constitution check PASS (20/20 gates + 2 justified deviations)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify Ed25519 algorithm name in PyJWT ("EdDSA" vs "Ed25519")
