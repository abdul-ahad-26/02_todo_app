---
name: better-auth
description: Implement authentication and authorization using Better Auth, a framework-agnostic TypeScript library. Use this skill when adding user authentication (email/password, OAuth, social login), session management, two-factor authentication (2FA), passkeys, or any auth-related features to web applications. Supports Next.js, React, Vue, Svelte, Solid, Astro, Remix, and other frameworks with Prisma, Drizzle, or direct database adapters.
---

# Better Auth

Framework-agnostic authentication library for TypeScript with comprehensive features and plugin ecosystem.

## Installation

```bash
npm install better-auth
```

## Quick Start

### 1. Server Configuration

Create `lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "postgresql", // or "mysql", "sqlite"
    url: process.env.DATABASE_URL,
  },
  emailAndPassword: {
    enabled: true,
  },
});
```

### 2. Mount Auth Handler

**Next.js** (`app/api/auth/[...all]/route.ts`):

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### 3. Generate Database Schema

```bash
npx @better-auth/cli generate
```

For Drizzle:
```bash
npx drizzle-kit generate && npx drizzle-kit migrate
```

For Prisma:
```bash
npx prisma db push
```

### 4. Client Setup

Create `lib/auth-client.ts`:

```typescript
import { createAuthClient } from "better-auth/react"; // or /client, /vue, /svelte, /solid

export const authClient = createAuthClient();

// Export hooks for React
export const { useSession, signIn, signUp, signOut } = authClient;
```

## Core Authentication

### Email & Password

**Server config:**

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true, // optional
    minPasswordLength: 8,
    maxPasswordLength: 128,
    sendResetPassword: async ({ user, url, token }) => {
      // Send reset email (don't await to prevent timing attacks)
      void sendEmail({ to: user.email, subject: "Reset password", text: url });
    },
  },
});
```

**Client usage:**

```typescript
// Sign up
await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "John Doe",
});

// Sign in
await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
  rememberMe: true,
});

// Sign out
await authClient.signOut();

// Forgot password
await authClient.forgetPassword({ email: "user@example.com" });

// Reset password (with token from email)
await authClient.resetPassword({ newPassword: "newPassword123", token });
```

### Social/OAuth Providers

**Server config:**

```typescript
export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    discord: {
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    },
  },
});
```

**Client usage:**

```typescript
// Sign in with provider
await authClient.signIn.social({
  provider: "github", // or "google", "discord", etc.
  callbackURL: "/dashboard",
});

// Link additional account
await authClient.linkSocial({
  provider: "github",
  callbackURL: "/settings",
});

// List linked accounts
const { data } = await authClient.listAccounts();

// Unlink account
await authClient.unlinkAccount({ accountId: "acc_123" });
```

## Session Management

**React hook:**

```tsx
import { useSession } from "@/lib/auth-client";

function Profile() {
  const { data: session, isPending, error } = useSession();

  if (isPending) return <div>Loading...</div>;
  if (!session) return <div>Not authenticated</div>;

  return <div>Welcome, {session.user.name}</div>;
}
```

**Server Component (Next.js):**

```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export default async function Page() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) return <div>Not authenticated</div>;
  return <div>Welcome, {session.user.name}</div>;
}
```

## Database Adapters

### Direct Connection

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "postgresql", // "mysql", "sqlite"
    url: process.env.DATABASE_URL,
  },
});
```

### Drizzle Adapter

```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg", // "mysql", "sqlite"
  }),
});
```

### Prisma Adapter

```typescript
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
});
```

## Core Database Schema

Better Auth requires these tables (auto-generated via CLI):

- **user**: id, name, email, emailVerified, image, createdAt, updatedAt
- **session**: id, userId, token, expiresAt, ipAddress, userAgent
- **account**: id, userId, accountId, providerId, accessToken, refreshToken

## Plugins

Add plugins for extended functionality. See **[references/plugins.md](references/plugins.md)** for detailed plugin documentation including:

- Two-Factor Authentication (2FA/TOTP)
- Passkeys (WebAuthn)
- Username authentication
- Magic Link
- Organizations & Teams
- Admin dashboard

**Basic plugin setup:**

```typescript
// Server
import { betterAuth } from "better-auth";
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [twoFactor()],
});

// Client
import { createAuthClient } from "better-auth/react";
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [twoFactorClient()],
});
```

## Framework Integration

See **[references/frameworks.md](references/frameworks.md)** for framework-specific setup:

- Next.js (App Router & Pages Router)
- Remix
- Astro
- SvelteKit
- Nuxt
- SolidStart
- Hono / Elysia

## Environment Variables

```env
DATABASE_URL="postgresql://user:pass@localhost:5432/db"

# Social providers (as needed)
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
DISCORD_CLIENT_ID=""
DISCORD_CLIENT_SECRET=""

# Email (for password reset, verification)
SMTP_HOST=""
SMTP_PORT=""
SMTP_USER=""
SMTP_PASS=""
```

## CLI Commands

```bash
# Generate database schema for your ORM
npx @better-auth/cli generate

# Run migrations (Drizzle)
npx drizzle-kit generate && npx drizzle-kit migrate

# Run migrations (Prisma)
npx prisma db push
```

## Common Patterns

### Protected API Route (Next.js)

```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { NextResponse } from "next/server";

export async function GET() {
  const session = await auth.api.getSession({ headers: await headers() });

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  return NextResponse.json({ user: session.user });
}
```

### Auth Form Component

```tsx
"use client";
import { useState } from "react";
import { authClient } from "@/lib/auth-client";

export function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await authClient.signIn.email(
      { email, password },
      {
        onRequest: () => setLoading(true),
        onSuccess: () => window.location.href = "/dashboard",
        onError: (ctx) => {
          setLoading(false);
          alert(ctx.error.message);
        },
      }
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit" disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </form>
  );
}
```

### Middleware Protection (Next.js)

```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export async function requireAuth() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) redirect("/login");
  return session;
}
```
