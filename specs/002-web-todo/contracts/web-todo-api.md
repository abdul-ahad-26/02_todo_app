# Web Todo API Contract

**Feature**: 002-web-todo | **Version**: 1.0.0 | **Date**: 2025-12-30

## Overview

RESTful API for the full-stack Todo application. All endpoints require JWT authentication and enforce user-scoped access control.

**Base URL:** `http://localhost:8000/api`

**Authentication:** Bearer Token (JWT)
```
Authorization: Bearer <jwt_token>
```

## Data Types

### Task

```typescript
interface Task {
  id: string;              // UUID v4
  user_id: string;         // UUID v4
  title: string;           // Non-empty, max 255 chars
  description?: string;    // Optional
  is_complete: boolean;    // Default: false
  created_at: string;      // ISO 8601 timestamp
  updated_at: string;      // ISO 8601 timestamp
}
```

### Error

```typescript
interface ErrorResponse {
  error: string;           // Error type (e.g., "Unauthorized", "Forbidden")
  message: string;         // Human-readable message
  details?: Record<string, any>;  // Optional additional context
}
```

## Endpoints

### 1. List Tasks

List all tasks for a specific user.

**Endpoint:** `GET /api/{user_id}/tasks`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID v4 | Authenticated user's ID (must match JWT payload) |

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "is_complete": false,
      "created_at": "2025-12-30T12:00:00Z",
      "updated_at": "2025-12-30T12:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Write documentation",
      "description": "Update API docs",
      "is_complete": true,
      "created_at": "2025-12-30T11:00:00Z",
      "updated_at": "2025-12-30T13:00:00Z"
    }
  ]
}
```

**Error Responses:**
| Status | Error | Message |
|--------|-------|---------|
| 401 | Unauthorized | Invalid or expired JWT token |
| 403 | Forbidden | user_id does not match authenticated user |

**Empty Response (200 OK):**
```json
{
  "tasks": []
}
```

---

### 2. Create Task

Create a new task for the authenticated user.

**Endpoint:** `POST /api/{user_id}/tasks`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID v4 | Authenticated user's ID (must match JWT payload) |

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Fields:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | Non-empty, max 255 chars |
| `description` | string | No | Optional |

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": false,
  "created_at": "2025-12-30T12:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Error Responses:**
| Status | Error | Message |
|--------|-------|---------|
| 400 | Bad Request | Title is required |
| 401 | Unauthorized | Invalid or expired JWT token |
| 403 | Forbidden | user_id does not match authenticated user |

---

### 3. Get Task

Retrieve a specific task by ID.

**Endpoint:** `GET /api/{user_id}/tasks/{id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID v4 | Authenticated user's ID (must match JWT payload) |
| `id` | UUID v4 | Task ID |

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": false,
  "created_at": "2025-12-30T12:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Error Responses:**
| Status | Error | Message |
|--------|-------|---------|
| 401 | Unauthorized | Invalid or expired JWT token |
| 403 | Forbidden | user_id does not match authenticated user |
| 403 | Forbidden | Task does not belong to user |
| 404 | Not Found | Task not found |

---

### 4. Update Task

Update an existing task's title and/or description.

**Endpoint:** `PUT /api/{user_id}/tasks/{id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID v4 | Authenticated user's ID (must match JWT payload) |
| `id` | UUID v4 | Task ID |

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Fields:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | Non-empty, max 255 chars |
| `description` | string | No | Optional |

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated title",
  "description": "Updated description",
  "is_complete": false,
  "created_at": "2025-12-30T12:00:00Z",
  "updated_at": "2025-12-30T12:30:00Z"
}
```

**Error Responses:**
| Status | Error | Message |
|--------|-------|---------|
| 400 | Bad Request | Title is required |
| 401 | Unauthorized | Invalid or expired JWT token |
| 403 | Forbidden | Task does not belong to user |
| 404 | Not Found | Task not found |

---

### 5. Delete Task

Permanently delete a task.

**Endpoint:** `DELETE /api/{user_id}/tasks/{id}`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID v4 | Authenticated user's ID (must match JWT payload) |
| `id` | UUID v4 | Task ID |

**Request Body:** None

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses:**
| Status | Error | Message |
|--------|-------|---------|
| 401 | Unauthorized | Invalid or expired JWT token |
| 403 | Forbidden | Task does not belong to user |
| 404 | Not Found | Task not found |

---

### 6. Toggle Task Completion

Toggle a task's completion status between true and false.

**Endpoint:** `PATCH /api/{user_id}/tasks/{id}/complete`

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID v4 | Authenticated user's ID (must match JWT payload) |
| `id` | UUID v4 | Task ID |

**Request Body:** None

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": true,
  "created_at": "2025-12-30T12:00:00Z",
  "updated_at": "2025-12-30T12:15:00Z"
}
```

**Error Responses:**
| Status | Error | Message |
|--------|-------|---------|
| 401 | Unauthorized | Invalid or expired JWT token |
| 403 | Forbidden | Task does not belong to user |
| 404 | Not Found | Task not found |

---

## Authentication

### JWT Token Format

JWT tokens are issued by Better Auth on the frontend and verified by the backend.

**Payload:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "exp": 1735584000
}
```

**Fields:**
| Field | Description |
|-------|-------------|
| `user_id` | Authenticated user's UUID |
| `exp` | Expiration timestamp (Unix epoch) |

**Token Expiration:** 24 hours

### Auth Headers

All API requests (except auth endpoints managed by Better Auth) must include:

```
Authorization: Bearer <jwt_token>
```

**Example:**
```http
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## HTTP Status Codes

| Code | Usage | Example |
|------|--------|----------|
| 200 | Success (GET, PUT, PATCH, DELETE) | Task retrieved/updated/deleted successfully |
| 201 | Created (POST) | Task created successfully |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing, invalid, or expired JWT |
| 403 | Forbidden | User ID mismatch or task ownership violation |
| 404 | Not Found | Task ID doesn't exist |
| 500 | Internal Server Error | Database connection failure |

---

## Error Response Format

All error responses follow this structure:

```json
{
  "error": "Error Type",
  "message": "Human-readable error message",
  "details": {}
}
```

**Example:**
```json
{
  "error": "Unauthorized",
  "message": "Token has expired",
  "details": {
    "token_exp": "2025-12-30T12:00:00Z",
    "current_time": "2025-12-30T13:00:00Z"
  }
}
```

---

## CORS Configuration

The backend accepts requests from configured origins (typically the frontend).

**Allowed Headers:**
- `Authorization`
- `Content-Type`

**Allowed Methods:**
- `GET`
- `POST`
- `PUT`
- `DELETE`
- `PATCH`
- `OPTIONS`

**Allow Credentials:** false (JWT in Authorization header, not cookies)

---

## OpenAPI Documentation

The FastAPI backend provides auto-generated OpenAPI/Swagger documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`
