# Better Auth Framework Integration

## Table of Contents

- [Next.js](#nextjs)
- [Remix](#remix)
- [Astro](#astro)
- [SvelteKit](#sveltekit)
- [Nuxt](#nuxt)
- [SolidStart](#solidstart)
- [Hono](#hono)
- [Elysia](#elysia)

---

## Next.js

### App Router Setup

**1. Server Config** (`lib/auth.ts`):

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL,
  },
  emailAndPassword: { enabled: true },
});
```

**2. Route Handler** (`app/api/auth/[...all]/route.ts`):

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

**3. Client** (`lib/auth-client.ts`):

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient();
export const { useSession, signIn, signUp, signOut } = authClient;
```

**4. Server Component Session**:

```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export default async function Page() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  // ...
}
```

**5. Client Component Session**:

```tsx
"use client";
import { useSession } from "@/lib/auth-client";

export function UserProfile() {
  const { data: session, isPending } = useSession();
  if (isPending) return <div>Loading...</div>;
  if (!session) return <div>Not authenticated</div>;
  return <div>Welcome, {session.user.name}</div>;
}
```

**6. Middleware** (`middleware.ts`):

```typescript
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

### Pages Router Setup

**Route Handler** (`pages/api/auth/[...all].ts`):

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export default toNextJsHandler(auth);
```

---

## Remix

**1. Server Config** (`app/lib/auth.server.ts`):

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { provider: "postgresql", url: process.env.DATABASE_URL },
  emailAndPassword: { enabled: true },
});
```

**2. Resource Route** (`app/routes/api.auth.$.tsx`):

```typescript
import { auth } from "~/lib/auth.server";
import type { ActionFunctionArgs, LoaderFunctionArgs } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  return auth.handler(request);
}

export async function action({ request }: ActionFunctionArgs) {
  return auth.handler(request);
}
```

**3. Client** (`app/lib/auth-client.ts`):

```typescript
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient();
```

**4. Sign In Component**:

```tsx
import { Form } from "@remix-run/react";
import { useState } from "react";
import { authClient } from "~/lib/auth-client";

export default function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const signIn = async () => {
    await authClient.signIn.email(
      { email, password },
      {
        onSuccess: () => window.location.href = "/dashboard",
        onError: (ctx) => alert(ctx.error.message),
      }
    );
  };

  return (
    <Form onSubmit={signIn}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Sign In</button>
    </Form>
  );
}
```

---

## Astro

**1. Server Config** (`src/lib/auth.ts`):

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { provider: "postgresql", url: import.meta.env.DATABASE_URL },
  emailAndPassword: { enabled: true },
});
```

**2. API Route** (`src/pages/api/auth/[...all].ts`):

```typescript
import { auth } from "../../../lib/auth";
import type { APIRoute } from "astro";

export const ALL: APIRoute = async (ctx) => {
  return auth.handler(ctx.request);
};
```

**3. Client** (`src/lib/auth-client.ts`):

```typescript
// Vanilla JS
import { createAuthClient } from "better-auth/client";

// Or React
import { createAuthClient } from "better-auth/react";

// Or Vue
import { createAuthClient } from "better-auth/vue";

// Or Svelte
import { createAuthClient } from "better-auth/svelte";

export const authClient = createAuthClient();
```

**4. Server-side Session** (`.astro` file):

```astro
---
import { auth } from "../lib/auth";

const session = await auth.api.getSession({
  headers: Astro.request.headers,
});
---

{session ? (
  <p>Welcome, {session.user.name}</p>
) : (
  <a href="/login">Sign In</a>
)}
```

---

## SvelteKit

**1. Server Config** (`src/lib/server/auth.ts`):

```typescript
import { betterAuth } from "better-auth";
import { DATABASE_URL } from "$env/static/private";

export const auth = betterAuth({
  database: { provider: "postgresql", url: DATABASE_URL },
  emailAndPassword: { enabled: true },
});
```

**2. Hook Handler** (`src/hooks.server.ts`):

```typescript
import { auth } from "$lib/server/auth";
import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
  // Handle auth routes
  if (event.url.pathname.startsWith("/api/auth")) {
    return auth.handler(event.request);
  }

  // Add session to locals
  event.locals.session = await auth.api.getSession({
    headers: event.request.headers,
  });

  return resolve(event);
};
```

**3. Client** (`src/lib/auth-client.ts`):

```typescript
import { createAuthClient } from "better-auth/svelte";

export const authClient = createAuthClient();
```

**4. Svelte Component**:

```svelte
<script lang="ts">
  import { authClient } from "$lib/auth-client";

  const session = authClient.useSession();

  async function signOut() {
    await authClient.signOut();
    window.location.href = "/";
  }
</script>

{#if $session.data}
  <p>Welcome, {$session.data.user.name}</p>
  <button on:click={signOut}>Sign Out</button>
{:else}
  <a href="/login">Sign In</a>
{/if}
```

---

## Nuxt

**1. Server Config** (`server/utils/auth.ts`):

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { provider: "postgresql", url: process.env.DATABASE_URL },
  emailAndPassword: { enabled: true },
});
```

**2. API Handler** (`server/api/auth/[...all].ts`):

```typescript
import { auth } from "../../utils/auth";

export default defineEventHandler((event) => {
  return auth.handler(toWebRequest(event));
});
```

**3. Client** (`composables/useAuth.ts`):

```typescript
import { createAuthClient } from "better-auth/vue";

export const authClient = createAuthClient();

export const useAuth = () => {
  return authClient.useSession();
};
```

**4. Vue Component**:

```vue
<script setup lang="ts">
import { authClient } from "~/composables/useAuth";

const session = authClient.useSession();

const signOut = async () => {
  await authClient.signOut();
  navigateTo("/");
};
</script>

<template>
  <div v-if="session.data">
    <p>Welcome, {{ session.data.user.name }}</p>
    <button @click="signOut">Sign Out</button>
  </div>
  <NuxtLink v-else to="/login">Sign In</NuxtLink>
</template>
```

---

## SolidStart

**1. Server Config** (`src/lib/auth.ts`):

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { provider: "postgresql", url: process.env.DATABASE_URL },
  emailAndPassword: { enabled: true },
});
```

**2. API Route** (`src/routes/api/auth/[...all].ts`):

```typescript
import { auth } from "~/lib/auth";
import type { APIEvent } from "@solidjs/start/server";

export async function GET(event: APIEvent) {
  return auth.handler(event.request);
}

export async function POST(event: APIEvent) {
  return auth.handler(event.request);
}
```

**3. Client** (`src/lib/auth-client.ts`):

```typescript
import { createAuthClient } from "better-auth/solid";

export const authClient = createAuthClient();
```

---

## Hono

```typescript
import { Hono } from "hono";
import { betterAuth } from "better-auth";

const auth = betterAuth({
  database: { provider: "postgresql", url: process.env.DATABASE_URL },
  emailAndPassword: { enabled: true },
});

const app = new Hono();

app.on(["GET", "POST"], "/api/auth/**", (c) => {
  return auth.handler(c.req.raw);
});

export default app;
```

---

## Elysia

```typescript
import { Elysia } from "elysia";
import { betterAuth } from "better-auth";

const auth = betterAuth({
  database: { provider: "postgresql", url: process.env.DATABASE_URL },
  emailAndPassword: { enabled: true },
});

const app = new Elysia()
  .all("/api/auth/*", ({ request }) => auth.handler(request))
  .listen(3000);

console.log(`Server running at ${app.server?.hostname}:${app.server?.port}`);
```

---

## Client Import Reference

Choose the correct import based on your framework:

| Framework | Import Path |
|-----------|-------------|
| Vanilla JS | `better-auth/client` |
| React | `better-auth/react` |
| Vue | `better-auth/vue` |
| Svelte | `better-auth/svelte` |
| Solid | `better-auth/solid` |
| Next.js Server | `better-auth/client` |
| Next.js Client | `better-auth/react` |
