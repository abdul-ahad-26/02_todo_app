# Quickstart: Phase II Web Update

## Prerequisites
- **UV**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Node.js**: v18+
- **Neon Postgres**: Valid connection string

## Backend Setup
1. Navigate to `phase-2-web/backend/`.
2. Initialize project: `uv init`.
3. Sync dependencies: `uv sync`.
4. Run locally: `uv run uvicorn src.main:app --reload`.

## Frontend Setup
1. Navigate to `phase-2-web/frontend/`.
2. Install deps: `npm install`.
3. Run locally: `npm run dev`.

## CSS Variables
Ensure `frontend/app/globals.css` contains:
```css
:root {
  --primary: #3b82f6;
  --background: #0f172a;
  --foreground: #f8fafc;
  /* ... other variables as per constitution */
}
```
