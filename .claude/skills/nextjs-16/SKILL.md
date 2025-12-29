---
name: nextjs-16
description: Build full-stack web applications with Next.js 16.1.1 using the App Router, React Server Components, and modern React 19 patterns. Use this skill when creating Next.js projects, implementing routing (layouts, pages, dynamic routes), data fetching (Server Components, caching, revalidation), Server Actions, Route Handlers, middleware, or configuring Next.js applications. Covers App Router architecture, Turbopack, TypeScript integration, and deployment patterns.
---

# Next.js 16.1.1

Next.js is a React framework for building full-stack web applications with automatic configuration, optimization, and React Server Components support.

## What's New in 16.x

- **`use cache` directive** - Component and function-level caching with `cacheLife` and `cacheTag`
- **Turbopack File System Caching** (stable) - Up to 14x faster dev server restarts
- **Bundle Analyzer** (experimental) - `next experimental-analyze` for bundle inspection
- **Debugging** - `next dev --inspect` for easier Node.js debugging
- **Improved `serverExternalPackages`** - Now handles transitive dependencies
- **`next upgrade` command** - Simplified version upgrades
- **`updateTag`** - Immediate cache expiry for read-your-own-writes

## Quick Start

```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

## Project Structure (App Router)

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── global-error.tsx    # Global error boundary
├── route.ts            # API route handler
├── (group)/            # Route groups (no URL impact)
│   └── page.tsx
├── [slug]/             # Dynamic segment
│   └── page.tsx
├── [...slug]/          # Catch-all segment
│   └── page.tsx
├── [[...slug]]/        # Optional catch-all
│   └── page.tsx
└── @parallel/          # Parallel routes
    └── page.tsx
```

## Root Layout

Every app requires a root layout with `<html>` and `<body>` tags:

```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
  description: 'App description',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

## Pages

```tsx
// app/page.tsx - Server Component by default
export default function HomePage() {
  return <h1>Home</h1>
}

// app/about/page.tsx -> /about
export default function AboutPage() {
  return <h1>About</h1>
}
```

## Server vs Client Components

### Server Components (Default)

- Direct database/filesystem access
- Keep sensitive data on server
- Reduce client JavaScript bundle
- Async/await for data fetching

```tsx
// Server Component (default)
import { db } from '@/lib/db'

export default async function Page() {
  const posts = await db.post.findMany()
  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  )
}
```

### Client Components

- Interactivity (onClick, onChange)
- React hooks (useState, useEffect)
- Browser APIs
- Third-party libraries requiring client

```tsx
'use client'

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```

### Composition Pattern

```tsx
// app/page.tsx (Server Component)
import LikeButton from '@/components/like-button'
import { getPost } from '@/lib/data'

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const post = await getPost(id)

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
      <LikeButton likes={post.likes} /> {/* Client Component */}
    </article>
  )
}

// components/like-button.tsx
'use client'
import { useState } from 'react'

export default function LikeButton({ likes }: { likes: number }) {
  const [count, setCount] = useState(likes)
  return <button onClick={() => setCount(c => c + 1)}>Likes: {count}</button>
}
```

## Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)

  return <article>{post.content}</article>
}

// Generate static params at build time
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map(post => ({ slug: post.slug }))
}
```

### Route Segment Config

```tsx
// Force dynamic rendering
export const dynamic = 'force-dynamic'

// Force static rendering
export const dynamic = 'force-static'

// Revalidate every 60 seconds
export const revalidate = 60

// Runtime: 'nodejs' | 'edge'
export const runtime = 'nodejs'
```

## Data Fetching

### In Server Components

```tsx
// Cached by default
async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

// With revalidation (ISR)
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Revalidate every hour
  })
  return res.json()
}

// No caching
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store'
  })
  return res.json()
}

// With tags for on-demand revalidation
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { tags: ['posts'] }
  })
  return res.json()
}
```

### Cache Revalidation

```tsx
'use server'
import { revalidatePath, revalidateTag, updateTag } from 'next/cache'

// Revalidate specific path
export async function updatePost() {
  await db.post.update(...)
  revalidatePath('/blog')
}

// Revalidate by tag (stale-while-revalidate)
export async function createPost() {
  await db.post.create(...)
  revalidateTag('posts')
}

// Immediate expiry (read-your-own-writes) - Server Actions only
export async function createPostImmediate() {
  const post = await db.post.create(...)
  updateTag('posts')  // Immediately expires cache
  redirect(`/posts/${post.id}`)
}
```

## `use cache` Directive (Next.js 16)

Enable in config:

```js
// next.config.js
module.exports = {
  cacheComponents: true,
}
```

### Cache a Component

```tsx
import { cacheLife, cacheTag } from 'next/cache'

export async function ProductList() {
  'use cache'
  cacheLife('hours')  // Cache profile
  cacheTag('products')  // Tag for invalidation

  const products = await db.product.findMany()
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>
}
```

### Cache a Function

```tsx
export async function getUser(id: string) {
  'use cache'
  cacheTag(`user-${id}`)
  return db.user.findUnique({ where: { id } })
}
```

### Cache Entire Route

```tsx
// app/page.tsx
'use cache'

export default async function Page() {
  const data = await fetch('/api/data')
  return <div>{/* ... */}</div>
}
```

### Invalidate Cache

```tsx
'use server'
import { updateTag } from 'next/cache'

export async function updateProduct(id: string) {
  await db.product.update(...)
  updateTag('products')
  updateTag(`product-${id}`)
}
```

## Server Actions

```tsx
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({ data: { title, content } })

  revalidatePath('/posts')
  redirect('/posts')
}

// Usage in form
// app/new-post/page.tsx
import { createPost } from '@/app/actions'

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

### With useActionState (Client Component)

```tsx
'use client'
import { useActionState } from 'react'
import { createPost } from '@/app/actions'

export default function PostForm() {
  const [state, formAction, pending] = useActionState(createPost, null)

  return (
    <form action={formAction}>
      <input name="title" disabled={pending} />
      <button disabled={pending}>
        {pending ? 'Creating...' : 'Create'}
      </button>
      {state?.error && <p>{state.error}</p>}
    </form>
  )
}
```

## Route Handlers (API Routes)

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET() {
  const posts = await db.post.findMany()
  return NextResponse.json(posts)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await db.post.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}
```

### Dynamic Route Handler

```tsx
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const post = await db.post.findUnique({ where: { id } })

  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }

  return NextResponse.json(post)
}
```

## Middleware

```tsx
// middleware.ts (root level)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
}
```

## Metadata & SEO

```tsx
// Static metadata
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: {
    title: 'OG Title',
    description: 'OG Description',
    images: ['/og-image.png'],
  },
}

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params
  const post = await getPost(id)

  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

## Loading & Error States

```tsx
// app/posts/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>
}

// app/posts/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}

// app/posts/not-found.tsx
export default function NotFound() {
  return <h2>Post not found</h2>
}
```

## Layouts

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard">
      <nav>Dashboard Nav</nav>
      <main>{children}</main>
    </div>
  )
}
```

### With Params

```tsx
// app/[team]/layout.tsx
export default async function TeamLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ team: string }>
}) {
  const { team } = await params

  return (
    <section>
      <h1>{team}'s Dashboard</h1>
      {children}
    </section>
  )
}
```

## Configuration

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
    ],
  },

  // Environment variables (public)
  env: {
    CUSTOM_VAR: 'value',
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/old-path',
        destination: '/new-path',
        permanent: true,
      },
    ]
  },

  // Rewrites
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.example.com/:path*',
      },
    ]
  },
}

module.exports = nextConfig
```

## Environment Variables

```bash
# .env.local
DATABASE_URL="postgresql://..."
API_KEY="secret"                    # Server only
NEXT_PUBLIC_API_URL="https://..."   # Client accessible
```

## Navigation

```tsx
import Link from 'next/link'
import { useRouter } from 'next/navigation'

// Declarative
<Link href="/about">About</Link>
<Link href={`/posts/${post.id}`}>Read more</Link>

// Programmatic (Client Component)
'use client'
const router = useRouter()
router.push('/dashboard')
router.replace('/login')
router.back()
```

## Image Optimization

```tsx
import Image from 'next/image'

<Image
  src="/hero.png"
  alt="Hero"
  width={800}
  height={400}
  priority  // Preload for LCP
/>

// Fill container
<div className="relative h-64">
  <Image
    src="/bg.jpg"
    alt="Background"
    fill
    className="object-cover"
  />
</div>
```

## Advanced Topics

See **[references/advanced.md](references/advanced.md)** for:
- Parallel Routes and Intercepting Routes
- Streaming and Suspense
- Internationalization (i18n)
- Authentication patterns
- Testing strategies
- Deployment options
