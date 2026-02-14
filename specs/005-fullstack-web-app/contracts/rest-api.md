# REST API Contract: Phase II - Full-Stack Web Application

**Feature**: 005-fullstack-web-app
**Base URL**: `http://localhost:8000`
**Auth**: JWT Bearer token required on all endpoints

## Authentication

All task endpoints require:
```
Authorization: Bearer <jwt_token>
```

Tokens are issued by Better Auth JWT plugin on the frontend. Verified by FastAPI using shared `BETTER_AUTH_SECRET` (HS256).

**Error Response** (all endpoints):
```json
{
  "detail": "string"
}
```

---

## Endpoints

### GET /api/{user_id}/tasks

**Description**: List all tasks for the authenticated user.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| user_id | path | string | yes | User ID (must match JWT sub) |

**Response 200** (application/json):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user_abc123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-08T12:00:00Z",
    "updated_at": "2026-02-08T12:00:00Z"
  }
]
```

| Status | Description |
|--------|-------------|
| 200 | Success — array of tasks (may be empty) |
| 401 | Missing/invalid/expired JWT token or user_id mismatch |

---

### POST /api/{user_id}/tasks

**Description**: Create a new task for the authenticated user.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| user_id | path | string | yes | User ID (must match JWT sub) |

**Request Body** (application/json):
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | yes | 1-200 characters, non-blank |
| description | string | no | max 1000 characters |

**Response 201** (application/json):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-08T12:00:00Z",
  "updated_at": "2026-02-08T12:00:00Z"
}
```

| Status | Description |
|--------|-------------|
| 201 | Task created successfully |
| 401 | Missing/invalid/expired JWT token or user_id mismatch |
| 422 | Validation error (missing title, title too long, etc.) |

---

### GET /api/{user_id}/tasks/{id}

**Description**: Get details of a single task.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| user_id | path | string | yes | User ID (must match JWT sub) |
| id | path | string | yes | Task ID |

**Response 200** (application/json):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-08T12:00:00Z",
  "updated_at": "2026-02-08T12:00:00Z"
}
```

| Status | Description |
|--------|-------------|
| 200 | Success |
| 401 | Missing/invalid/expired JWT token or user_id mismatch |
| 404 | Task not found |

---

### PUT /api/{user_id}/tasks/{id}

**Description**: Update a task's title and/or description.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| user_id | path | string | yes | User ID (must match JWT sub) |
| id | path | string | yes | Task ID |

**Request Body** (application/json):
```json
{
  "title": "Buy organic groceries",
  "description": "Organic milk, free-range eggs"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| title | string | no | 1-200 characters if provided |
| description | string | no | max 1000 characters if provided |

**Response 200** (application/json): Updated task object (same schema as GET).

| Status | Description |
|--------|-------------|
| 200 | Task updated successfully |
| 401 | Missing/invalid/expired JWT token or user_id mismatch |
| 404 | Task not found |
| 422 | Validation error |

---

### DELETE /api/{user_id}/tasks/{id}

**Description**: Permanently delete a task.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| user_id | path | string | yes | User ID (must match JWT sub) |
| id | path | string | yes | Task ID |

**Response 204**: No content.

| Status | Description |
|--------|-------------|
| 204 | Task deleted successfully |
| 401 | Missing/invalid/expired JWT token or user_id mismatch |
| 404 | Task not found |

---

### PATCH /api/{user_id}/tasks/{id}/complete

**Description**: Toggle task completion status (complete ↔ incomplete).

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| user_id | path | string | yes | User ID (must match JWT sub) |
| id | path | string | yes | Task ID |

**Request Body**: None.

**Response 200** (application/json): Updated task object (same schema as GET).

| Status | Description |
|--------|-------------|
| 200 | Completion status toggled |
| 401 | Missing/invalid/expired JWT token or user_id mismatch |
| 404 | Task not found |

---

### GET /health

**Description**: Health check endpoint (no authentication required).

**Response 200**:
```json
{
  "status": "healthy"
}
```

---

## Error Response Format

All errors follow FastAPI's standard format:

```json
{
  "detail": "Human-readable error message"
}
```

For validation errors (422):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "type": "string_too_short"
    }
  ]
}
```

## CORS Configuration

| Setting | Value |
|---------|-------|
| Allowed Origins | `http://localhost:3000` (dev), production frontend URL |
| Allowed Methods | GET, POST, PUT, PATCH, DELETE |
| Allow Credentials | true |
| Allowed Headers | * (includes Authorization) |
