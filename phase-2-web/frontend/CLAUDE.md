# Frontend Agent Instructions

## Context
This is the Next.js 16+ frontend for the Phase II Full-Stack Todo Application.

## Tech Stack
- Next.js 16+ with App Router
- TypeScript (strict mode)
- Tailwind CSS with CSS variable theme
- Better Auth (JWT plugin + nextCookies plugin)

## Key Patterns
- Server Components by default, Client Components for interactivity
- Better Auth handles sessions; JWT tokens authenticate with FastAPI backend
- Centralized API client (`lib/api.ts`) for all FastAPI calls
- Modern Dark/High-Contrast theme via CSS variables
- Middleware redirects unauthenticated users to /sign-in

## File Structure
- `src/app/layout.tsx` — Root layout (dark theme, Inter font)
- `src/app/page.tsx` — Landing with redirect logic
- `src/app/(auth)/` — Sign-in/sign-up pages
- `src/app/dashboard/` — Protected dashboard
- `src/app/api/auth/[...all]/route.ts` — Better Auth handler
- `src/components/auth/` — Auth form components
- `src/components/tasks/` — Task UI components
- `src/lib/auth.ts` — Better Auth server config
- `src/lib/auth-client.ts` — Better Auth client config
- `src/lib/api.ts` — Centralized API client

## Running
```bash
npm run dev
```
