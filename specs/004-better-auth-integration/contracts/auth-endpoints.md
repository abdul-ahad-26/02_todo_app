# Auth Endpoint Contracts

**Feature Branch**: `004-better-auth-integration`

## Better Auth Endpoints (Managed by Better Auth — Frontend Only)

These endpoints are automatically provided by Better Auth via
the catch-all route handler at `/api/auth/[...all]/route.ts`.
They are consumed by the Next.js frontend only.

### POST /api/auth/sign-up/email

Create a new user account with email and password.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (200)**:
```json
{
  "user": {
    "id": "abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2026-02-06T12:00:00.000Z",
    "updatedAt": "2026-02-06T12:00:00.000Z"
  },
  "session": {
    "id": "sess_xyz",
    "userId": "abc123",
    "token": "session-token-value",
    "expiresAt": "2026-02-13T12:00:00.000Z"
  }
}
```

**Errors**:
- 422: Invalid email format or password too short
- 409: Email already registered

### POST /api/auth/sign-in/email

Authenticate an existing user.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200)**:
```json
{
  "user": { ... },
  "session": { ... }
}
```
Sets httpOnly session cookie.

**Errors**:
- 401: Invalid credentials

### POST /api/auth/sign-out

Terminate the current session.

**Request**: No body (session identified by cookie).

**Response (200)**:
```json
{ "success": true }
```
Clears session cookie.

### GET /api/auth/get-session

Get the current session for the authenticated user.

**Response (200)** (if session exists):
```json
{
  "user": { ... },
  "session": { ... }
}
```

**Response (200)** (if no session):
```json
null
```

### GET /api/auth/token

Get a JWT for use with external APIs (FastAPI backend).

**Response (200)**:
```json
{
  "token": "eyJhbGciOiJFZERTQSIs..."
}
```

Requires valid session cookie. Returns a short-lived JWT
(default 15 minutes) signed with Ed25519.

### GET /api/auth/jwks

Get the JSON Web Key Set for JWT verification.

**Response (200)**:
```json
{
  "keys": [
    {
      "crv": "Ed25519",
      "x": "base64url-encoded-public-key",
      "kty": "OKP",
      "kid": "key-id-uuid"
    }
  ]
}
```

Public endpoint — no authentication required. Keys can be
cached indefinitely by consumers.

---

## FastAPI Backend Endpoints (Unchanged API Contract)

These endpoints remain the same. The only change is the auth
middleware: JWT verification switches from HS256 shared secret
to JWKS-based Ed25519 verification.

### Auth Dependency

All task endpoints require:
```
Authorization: Bearer <jwt-from-better-auth>
```

The JWT payload contains:
```json
{
  "sub": "user-id-string",
  "iss": "http://localhost:3000",
  "aud": "http://localhost:3000",
  "iat": 1707177600,
  "exp": 1707178500
}
```

### GET /api/tasks

List all tasks for the authenticated user.

**Headers**: `Authorization: Bearer <token>`

**Response (200)**:
```json
[
  {
    "id": "uuid-string",
    "user_id": "better-auth-user-id",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_complete": false,
    "created_at": "2026-02-06T12:00:00",
    "updated_at": "2026-02-06T12:00:00"
  }
]
```

**Errors**:
- 401: Missing or invalid JWT

### POST /api/tasks

Create a new task.

**Headers**: `Authorization: Bearer <token>`

**Request**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response (201)**:
```json
{
  "id": "uuid-string",
  "user_id": "better-auth-user-id",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": false,
  "created_at": "2026-02-06T12:00:00",
  "updated_at": "2026-02-06T12:00:00"
}
```

**Errors**:
- 400: Empty title
- 401: Missing or invalid JWT

### GET /api/tasks/{task_id}

Get a specific task.

**Errors**:
- 401: Missing or invalid JWT
- 404: Task not found or not owned by user

### PUT /api/tasks/{task_id}

Update a task.

**Request**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "is_complete": true
}
```
All fields optional.

**Errors**:
- 401: Missing or invalid JWT
- 404: Task not found or not owned by user

### PATCH /api/tasks/{task_id}/complete

Toggle task completion status.

**Errors**:
- 401: Missing or invalid JWT
- 404: Task not found or not owned by user

### DELETE /api/tasks/{task_id}

Delete a task.

**Response (200)**:
```json
{ "message": "Task deleted successfully" }
```

**Errors**:
- 401: Missing or invalid JWT
- 404: Task not found or not owned by user
