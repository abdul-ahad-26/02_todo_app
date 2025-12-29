# Next.js 16.1.1 Advanced Topics

## Table of Contents

- [Next.js 16.1 New Features](#nextjs-161-new-features)
- [`use cache` Directive (Deep Dive)](#use-cache-directive-deep-dive)
- [Parallel Routes](#parallel-routes)
- [Intercepting Routes](#intercepting-routes)
- [Streaming and Suspense](#streaming-and-suspense)
- [Internationalization](#internationalization)
- [Authentication Patterns](#authentication-patterns)
- [Testing](#testing)
- [Deployment](#deployment)
- [Performance Optimization](#performance-optimization)

---

## Next.js 16.1 New Features

### Turbopack File System Caching (Stable)

Enabled by default - compiler artifacts stored on disk for faster dev server restarts.

**Performance improvements:**
- react.dev: ~10x faster (3.7s → 380ms cached)
- nextjs.org: ~5x faster (3.5s → 700ms cached)
- Large apps: ~14x faster (15s → 1.1s cached)

```js
// next.config.js - disable if needed (not recommended)
module.exports = {
  turbopack: {
    unstable_fileSystemCache: false,
  },
}
```

### Bundle Analyzer (Experimental)

```bash
# Analyze production bundles
next experimental-analyze
```

Features:
- Interactive UI for bundle inspection
- Filter bundles by route
- View full import chains
- Trace server-to-client boundary imports
- View CSS and asset sizes

### Debugging with --inspect

```bash
# New simplified debugging
next dev --inspect

# Previously required
NODE_OPTIONS=--inspect next dev
```

### Improved serverExternalPackages

Now handles transitive dependencies automatically:

```js
// next.config.js
module.exports = {
  serverExternalPackages: ['sqlite'], // Works for transitive deps
}
```

### Upgrade Command

```bash
# Simplified version upgrades
next upgrade

# Or with codemod
npx @next/codemod@canary upgrade latest
```

---

## `use cache` Directive (Deep Dive)

### Enable Cache Components

```js
// next.config.js
module.exports = {
  cacheComponents: true,
}
```

### Cache Profiles

```tsx
import { cacheLife } from 'next/cache'

async function getData() {
  'use cache'
  cacheLife('hours')  // Built-in: 'seconds', 'minutes', 'hours', 'days', 'weeks', 'max'
  return fetch('/api/data')
}
```

### Custom Cache Profiles

```js
// next.config.js
module.exports = {
  cacheComponents: true,
  cacheLife: {
    custom: {
      stale: 300,      // Client cache: 5 minutes
      revalidate: 900, // Server revalidate: 15 minutes
      expire: 3600,    // Expire after 1 hour
    },
  },
}
```

```tsx
cacheLife('custom')  // Use custom profile
```

### Cache Key Generation

Cache keys are generated from:
1. Build ID
2. Function location hash
3. Serializable arguments

```tsx
async function UserData({ userId }: { userId: string }) {
  async function getData(filter: string) {
    'use cache'
    // Cache key includes: userId (from closure) + filter (argument)
    return fetch(`/api/users/${userId}?filter=${filter}`)
  }
  return getData('active')
}
```

### Constraints

Cannot access dynamic APIs inside `use cache`:

```tsx
// ❌ Invalid
async function Cached() {
  'use cache'
  const cookieStore = cookies()  // Error!
}

// ✅ Valid - pass values from outside
async function Page() {
  const token = (await cookies()).get('token')?.value
  return <CachedComponent token={token} />
}

async function CachedComponent({ token }: { token?: string }) {
  'use cache'
  // Use token as cache key component
}
```

### Tagging and Invalidation

```tsx
import { cacheTag, updateTag } from 'next/cache'

// Tag cached data
async function getProducts(category: string) {
  'use cache'
  cacheTag('products', `category-${category}`)
  return db.products.findMany({ where: { category } })
}

// Invalidate (Server Action)
'use server'
export async function updateProduct() {
  await db.products.update(...)
  updateTag('products')  // Clears all products caches
}
```

### Remote Caching

For persistent cache across serverless functions:

```tsx
async function getData() {
  'use cache: remote'  // Persists to external cache (may incur costs)
  return fetch('/api/data')
}
```

---

## Parallel Routes

Display multiple pages simultaneously in the same layout using named slots.

```
app/
├── layout.tsx
├── page.tsx
├── @team/
│   └── page.tsx
└── @analytics/
    └── page.tsx
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode
  team: React.ReactNode
  analytics: React.ReactNode
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2">
        {team}
        {analytics}
      </div>
    </div>
  )
}
```

### Conditional Rendering

```tsx
// app/layout.tsx
import { getUser } from '@/lib/auth'

export default async function Layout({
  children,
  admin,
  user,
}: {
  children: React.ReactNode
  admin: React.ReactNode
  user: React.ReactNode
}) {
  const role = await getUser()

  return (
    <div>
      {children}
      {role === 'admin' ? admin : user}
    </div>
  )
}
```

### Default Slots

```tsx
// app/@team/default.tsx
export default function Default() {
  return null // or loading state
}
```

---

## Intercepting Routes

Intercept routes to show modals while preserving URL context.

```
app/
├── feed/
│   └── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx      # Full page view
└── @modal/
    └── (.)photo/
        └── [id]/
            └── page.tsx  # Modal view
```

### Convention

- `(.)` - Same level
- `(..)` - One level up
- `(..)(..)` - Two levels up
- `(...)` - From root

### Modal Implementation

```tsx
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from '@/components/modal'
import { getPhoto } from '@/lib/data'

export default async function PhotoModal({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const photo = await getPhoto(id)

  return (
    <Modal>
      <img src={photo.url} alt={photo.title} />
    </Modal>
  )
}

// components/modal.tsx
'use client'
import { useRouter } from 'next/navigation'

export function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter()

  return (
    <div className="fixed inset-0 bg-black/50" onClick={() => router.back()}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )
}
```

---

## Streaming and Suspense

### Page-level Streaming

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />
}
```

### Component-level Streaming

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>

      <Suspense fallback={<ChartSkeleton />}>
        <Chart />
      </Suspense>
    </div>
  )
}

async function Stats() {
  const stats = await fetchStats() // Streams when ready
  return <StatsDisplay stats={stats} />
}
```

### Parallel Data Fetching

```tsx
export default async function Page() {
  // Start both fetches in parallel
  const postsPromise = getPosts()
  const usersPromise = getUsers()

  return (
    <div>
      <Suspense fallback={<PostsSkeleton />}>
        <Posts promise={postsPromise} />
      </Suspense>

      <Suspense fallback={<UsersSkeleton />}>
        <Users promise={usersPromise} />
      </Suspense>
    </div>
  )
}

async function Posts({ promise }: { promise: Promise<Post[]> }) {
  const posts = await promise
  return <PostList posts={posts} />
}
```

---

## Internationalization

### Middleware-based Routing

```tsx
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

const locales = ['en', 'es', 'fr']
const defaultLocale = 'en'

function getLocale(request: NextRequest): string {
  const acceptLanguage = request.headers.get('accept-language')
  // Parse and match against supported locales
  return defaultLocale
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  const pathnameHasLocale = locales.some(
    locale => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  )

  if (pathnameHasLocale) return

  const locale = getLocale(request)
  request.nextUrl.pathname = `/${locale}${pathname}`

  return NextResponse.redirect(request.nextUrl)
}

export const config = {
  matcher: ['/((?!_next|api|.*\\..*).*)']
}
```

### Localized Routes

```
app/
└── [lang]/
    ├── layout.tsx
    ├── page.tsx
    └── about/
        └── page.tsx
```

```tsx
// app/[lang]/page.tsx
import { getDictionary } from '@/lib/dictionaries'

export default async function Page({
  params,
}: {
  params: Promise<{ lang: string }>
}) {
  const { lang } = await params
  const dict = await getDictionary(lang)

  return <h1>{dict.home.title}</h1>
}

// lib/dictionaries.ts
const dictionaries = {
  en: () => import('@/dictionaries/en.json').then(m => m.default),
  es: () => import('@/dictionaries/es.json').then(m => m.default),
}

export const getDictionary = async (locale: string) => {
  return dictionaries[locale as keyof typeof dictionaries]()
}
```

### Generate Static Params

```tsx
export async function generateStaticParams() {
  return [{ lang: 'en' }, { lang: 'es' }, { lang: 'fr' }]
}
```

---

## Authentication Patterns

### Middleware Protection

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { verifyToken } from '@/lib/auth'

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  try {
    await verifyToken(token)
    return NextResponse.next()
  } catch {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*']
}
```

### Server Component Auth Check

```tsx
// app/dashboard/page.tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { verifySession } from '@/lib/auth'

export default async function DashboardPage() {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) {
    redirect('/login')
  }

  const user = await verifySession(session.value)

  return <Dashboard user={user} />
}
```

### Auth Context Pattern

```tsx
// lib/auth-context.tsx
'use client'
import { createContext, useContext } from 'react'

type User = { id: string; name: string; email: string }

const AuthContext = createContext<User | null>(null)

export function AuthProvider({
  children,
  user,
}: {
  children: React.ReactNode
  user: User | null
}) {
  return <AuthContext.Provider value={user}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}

// app/layout.tsx
import { AuthProvider } from '@/lib/auth-context'
import { getUser } from '@/lib/auth'

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const user = await getUser()

  return (
    <html>
      <body>
        <AuthProvider user={user}>{children}</AuthProvider>
      </body>
    </html>
  )
}
```

---

## Testing

### Jest Configuration

```js
// jest.config.js
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
}

module.exports = createJestConfig(customJestConfig)
```

### Component Testing

```tsx
// __tests__/page.test.tsx
import { render, screen } from '@testing-library/react'
import Page from '@/app/page'

describe('Page', () => {
  it('renders heading', () => {
    render(<Page />)
    expect(screen.getByRole('heading')).toBeInTheDocument()
  })
})
```

### Server Component Testing

```tsx
// __tests__/server-page.test.tsx
import { render, screen } from '@testing-library/react'

// Mock the async function
jest.mock('@/lib/data', () => ({
  getPosts: jest.fn().mockResolvedValue([
    { id: '1', title: 'Test Post' }
  ])
}))

describe('ServerPage', () => {
  it('renders posts', async () => {
    const Page = (await import('@/app/posts/page')).default
    const result = await Page()
    render(result)
    expect(screen.getByText('Test Post')).toBeInTheDocument()
  })
})
```

### E2E Testing with Playwright

```ts
// e2e/home.spec.ts
import { test, expect } from '@playwright/test'

test('homepage loads', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading')).toBeVisible()
})

test('navigation works', async ({ page }) => {
  await page.goto('/')
  await page.click('text=About')
  await expect(page).toHaveURL('/about')
})
```

---

## Deployment

### Vercel (Recommended)

```bash
npm i -g vercel
vercel
```

### Docker

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

```js
// next.config.js (for Docker)
module.exports = {
  output: 'standalone',
}
```

### Static Export

```js
// next.config.js
module.exports = {
  output: 'export',
}
```

```bash
npm run build
# Output in /out directory
```

---

## Performance Optimization

### Bundle Analysis

```bash
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // config
})

# Run
ANALYZE=true npm run build
```

### Code Splitting

```tsx
import dynamic from 'next/dynamic'

// Client-side only component
const Chart = dynamic(() => import('@/components/chart'), {
  ssr: false,
  loading: () => <ChartSkeleton />,
})

// With named exports
const Modal = dynamic(() =>
  import('@/components/modal').then(mod => mod.Modal)
)
```

### Font Optimization

```tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

### Script Optimization

```tsx
import Script from 'next/script'

export default function Page() {
  return (
    <>
      {/* Load after page is interactive */}
      <Script
        src="https://analytics.example.com/script.js"
        strategy="afterInteractive"
      />

      {/* Load during idle time */}
      <Script
        src="https://widget.example.com/widget.js"
        strategy="lazyOnload"
      />

      {/* Web Worker */}
      <Script
        src="https://heavy.example.com/process.js"
        strategy="worker"
      />
    </>
  )
}
```

### Cache Headers

```tsx
// app/api/data/route.ts
export async function GET() {
  const data = await fetchData()

  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300',
    },
  })
}
```

### Prefetching Control

```tsx
// Disable prefetching
<Link href="/heavy-page" prefetch={false}>
  Heavy Page
</Link>

// Manual prefetching
'use client'
import { useRouter } from 'next/navigation'

export function PrefetchButton() {
  const router = useRouter()

  return (
    <button onMouseEnter={() => router.prefetch('/dashboard')}>
      Go to Dashboard
    </button>
  )
}
```
