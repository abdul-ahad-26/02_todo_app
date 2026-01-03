# Todo Frontend (Phase 2)

Next.js 16 implementation for the Phase 2 Web application, featuring a modern high-contrast dark theme consistent with the project constitution.

## Prerequisites

- **Node.js**: 20.x or later
- **Package Manager**: `npm` (default) or `bun`/`pnpm`

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure Environment**:
   Create a `.env.local` file in this directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Running the Application

Start the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Tech Stack

- **Framework**: [Next.js 16](https://nextjs.org/) (App Router)
- **Styling**: Tailwind CSS 4 + CSS Variables (Modern Dark theme)
- **Language**: TypeScript
- **Auth**: [Better Auth](https://www.better-auth.com/) integration

## Design System

The application uses the mandated color palette via CSS variables:
- `--background`: `#0f172a` (Deep Slate)
- `--foreground`: `#f8fafc` (Ghost White)
- `--primary`: `#3b82f6` (Blue)
- `--secondary`: `#10b981` (Emerald)

## Project Structure

- `app/`: Next.js pages and layouts
- `components/`: Reusable UI components
- `lib/`: API client and shared logic
- `public/`: Static assets
