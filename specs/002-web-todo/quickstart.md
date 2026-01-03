# Quick Start: Phase II Web Todo Application

**Feature**: 002-web-todo | **Date**: 2025-12-30

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ installed
- Neon PostgreSQL account (free tier works)
- Better Auth installed and configured
- Git (for version control)

## 1. Environment Setup

### 1.1 Create Feature Branch

```bash
git checkout -b 002-web-todo
```

### 1.2 Backend Setup

```bash
cd backend
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r deps.txt
```

Create `.env` in `backend/`:
```bash
DATABASE_URL=postgresql://user:password@ep-cool-region-123456.aws.neon.tech/neondb
JWT_SECRET=your-super-secret-jwt-key-at-least-32-characters
CORS_ORIGINS=http://localhost:3000
```

### 1.3 Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local` in `frontend/`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-at-least-32-characters
```

**Important:** `BETTER_AUTH_SECRET` MUST match backend's `JWT_SECRET`.

## 2. Database Setup

### 2.1 Create Neon Database

1. Go to [neon.tech](https://neon.tech)
2. Sign up/login
3. Create a new project
4. Copy the connection string
5. Add to backend `.env` as `DATABASE_URL`

### 2.2 Initialize Schema

The backend will auto-create tables on first run (via `SQLModel.metadata.create_all()`).

## 3. Start Development Servers

### 3.1 Start Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3.2 Start Frontend

```bash
cd frontend
npm run dev
```

Frontend runs at: `http://localhost:3000`

## 4. Verify Setup

### 4.1 Test Backend Health

```bash
curl http://localhost:8000/docs
```

Should show Swagger UI.

### 4.2 Test Frontend

Open browser to `http://localhost:3000`.

You should see:
- Sign-in page (or redirect to signin if not authenticated)
- Sign-up link available
- After signin, tasks page with empty state

### 4.3 Test Authentication Flow

1. Click "Sign Up" on signin page
2. Enter email: `test@example.com`
3. Enter password: `testPassword123` (8+ chars)
4. Submit
5. Should redirect to `/tasks` page

## 5. API Testing

Use the Swagger UI at `http://localhost:8000/docs` for interactive testing.

### 5.1 Manual API Test

```bash
# After signin, get JWT from browser localStorage
TOKEN="your-jwt-token"
USER_ID="your-user-id-uuid"

# List tasks
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/$USER_ID/tasks

# Create task
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test description"}' \
  http://localhost:8000/api/$USER_ID/tasks
```

## 6. Development Workflow

### 6.1 Backend Development

1. Make changes in `backend/`
2. Backend auto-reloads (uvicorn `--reload`)
3. Test via Swagger UI or curl
4. Run tests: `pytest`

### 6.2 Frontend Development

1. Make changes in `frontend/`
2. Frontend hot-reloads (Next.js dev mode)
3. Test in browser
4. Run tests: `npm test`

### 6.3 Making Changes

```bash
git status
git add .
git commit -m "feat: describe changes"
```

## 7. Common Issues

### Issue: Database Connection Error

**Solution:** Verify `DATABASE_URL` in backend `.env` is correct. Test with:
```bash
psql "$DATABASE_URL" -c "SELECT 1;"
```

### Issue: CORS Error

**Solution:** Verify `CORS_ORIGINS` includes `http://localhost:3000` in backend `.env`.

### Issue: JWT Verification Fails

**Solution:** Verify `BETTER_AUTH_SECRET` (frontend) matches `JWT_SECRET` (backend) exactly.

### Issue: User ID Mismatch

**Solution:** Ensure JWT payload contains correct `user_id`. The frontend's Better Auth should include `user_id` in the token.

## 8. Project Structure Quick Reference

```
├── backend/
│   ├── main.py          # FastAPI app entry
│   ├── models.py        # User, Task SQLModels
│   ├── auth.py          # JWT utilities
│   ├── config.py        # Environment config
│   ├── db.py            # Database connection
│   └── routes/          # API endpoints
│       ├── tasks.py
│       └── auth.py
└── frontend/
    ├── app/
    │   ├── signin/page.tsx
    │   ├── signup/page.tsx
    │   └── tasks/page.tsx
    ├── components/
    │   ├── ui/
    │   ├── auth/
    │   └── tasks/
    └── lib/
        ├── api-client.ts
        └── auth-store.ts
```

## 9. Next Steps

After setup:

1. Review [`spec.md`](./spec.md) for requirements
2. Review [`plan.md`](./plan.md) for architecture
3. Review [`data-model.md`](./data-model.md) for database schema
4. Review [`contracts/web-todo-api.md`](./contracts/web-todo-api.md) for API details
5. Run `/sp.tasks` to generate implementation tasks
