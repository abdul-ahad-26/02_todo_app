# Data Model: Phase II - Full-Stack Web Application

**Feature**: 005-fullstack-web-app
**Date**: 2026-02-08
**Database**: Neon Serverless PostgreSQL
**ORM**: SQLModel

## Entity Relationship Overview

```
┌──────────────────────┐         ┌──────────────────────┐
│        user           │         │       session         │
│ (Better Auth managed) │◄────────│ (Better Auth managed) │
├──────────────────────┤    1:N  ├──────────────────────┤
│ id (PK, text)        │         │ id (PK, text)        │
│ name (text)          │         │ userId (FK → user.id) │
│ email (text, unique) │         │ token (text)         │
│ emailVerified (bool) │         │ expiresAt (timestamp)│
│ image (text, null)   │         │ ipAddress (text)     │
│ createdAt (timestamp)│         │ userAgent (text)     │
│ updatedAt (timestamp)│         └──────────────────────┘
└──────────┬───────────┘
           │
           │ 1:N
           │
┌──────────▼───────────┐         ┌──────────────────────┐
│       account         │         │        task           │
│ (Better Auth managed) │         │  (App managed)        │
├──────────────────────┤         ├──────────────────────┤
│ id (PK, text)        │         │ id (PK, text/UUID)   │
│ userId (FK → user.id)│         │ user_id (FK → user.id)│
│ accountId (text)     │         │ title (text, 1-200)  │
│ providerId (text)    │         │ description (text,   │
│ accessToken (text)   │         │   null, max 1000)    │
│ refreshToken (text)  │         │ completed (bool,     │
│ ...                  │         │   default false)     │
└──────────────────────┘         │ created_at (timestamp)│
                                 │ updated_at (timestamp)│
                                 └──────────────────────┘
```

## Tables

### `user` (Managed by Better Auth)

Better Auth auto-creates and manages this table. **Do not create manually.**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PK | Unique user identifier (Better Auth generated) |
| name | TEXT | NOT NULL | Display name |
| email | TEXT | UNIQUE, NOT NULL | Login email |
| emailVerified | BOOLEAN | DEFAULT FALSE | Email verification status |
| image | TEXT | NULLABLE | Profile image URL |
| createdAt | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updatedAt | TIMESTAMP | DEFAULT NOW() | Last update time |

### `session` (Managed by Better Auth)

Better Auth auto-creates and manages this table. **Do not create manually.**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PK | Session identifier |
| userId | TEXT | FK → user.id | Associated user |
| token | TEXT | NOT NULL | Session token |
| expiresAt | TIMESTAMP | NOT NULL | Session expiry |
| ipAddress | TEXT | NULLABLE | Client IP |
| userAgent | TEXT | NULLABLE | Client user agent |

### `account` (Managed by Better Auth)

Better Auth auto-creates and manages this table. **Do not create manually.**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PK | Account identifier |
| userId | TEXT | FK → user.id | Associated user |
| accountId | TEXT | NOT NULL | Provider account ID |
| providerId | TEXT | NOT NULL | Auth provider name |
| accessToken | TEXT | NULLABLE | OAuth access token |
| refreshToken | TEXT | NULLABLE | OAuth refresh token |

### `task` (Application Managed)

This is the only table the application creates and manages directly via SQLModel.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PK | Unique task identifier |
| user_id | TEXT | FK → user.id, INDEX, NOT NULL | Task owner |
| title | VARCHAR(200) | NOT NULL, min_length=1 | Task title |
| description | VARCHAR(1000) | NULLABLE | Optional description |
| completed | BOOLEAN | DEFAULT FALSE, NOT NULL | Completion status |
| created_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW(), NOT NULL | Last update timestamp |

**Indexes**:
- `ix_task_user_id` on `user_id` — Fast lookup of user's tasks
- `ix_task_completed` on `completed` — Future filter support (Phase V)

## SQLModel Definitions

### Task Models

```python
# backend/src/models/task.py
import uuid
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from typing import Optional


class TaskBase(SQLModel):
    """Shared fields for task creation and updates."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class Task(TaskBase, table=True):
    """Database table model for tasks."""
    __tablename__ = "task"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    user_id: str = Field(foreign_key="user.id", index=True, nullable=False)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class TaskCreate(TaskBase):
    """Request body for POST /api/{user_id}/tasks."""
    pass


class TaskUpdate(SQLModel):
    """Request body for PUT /api/{user_id}/tasks/{id}. All fields optional."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskPublic(TaskBase):
    """Response model for all task endpoints."""
    id: str
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

## State Transitions

### Task Lifecycle

```
                    ┌─────────────┐
    POST /tasks     │  INCOMPLETE  │  ◄── Default state on creation
                    │ completed=F  │
                    └──────┬──────┘
                           │
              PATCH /{id}/complete
                           │
                    ┌──────▼──────┐
                    │  COMPLETED   │
                    │ completed=T  │
                    └──────┬──────┘
                           │
              PATCH /{id}/complete  (toggle back)
                           │
                    ┌──────▼──────┐
                    │  INCOMPLETE  │
                    │ completed=F  │
                    └──────┬──────┘
                           │
                 DELETE /{id}
                           │
                    ┌──────▼──────┐
                    │   DELETED    │
                    │  (removed)   │
                    └─────────────┘
```

## Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| title | Required, 1-200 characters | "Title is required" / "Title must be between 1 and 200 characters" |
| title | Whitespace-only rejected | "Title cannot be blank" |
| description | Optional, max 1000 characters | "Description must be 1000 characters or fewer" |
| user_id | Must match JWT sub claim | 401 Unauthorized |
| id | Must exist in database | 404 Not Found |
| id | Must belong to requesting user | 401 Unauthorized |

## Migration Strategy

For Phase II initial setup, use `SQLModel.metadata.create_all(engine)` on application startup. This creates the `task` table if it doesn't exist. Better Auth creates its own tables (`user`, `session`, `account`) via its CLI: `npx @better-auth/cli generate`.

For future schema changes (Phase III+), migrate to Alembic for versioned migrations.
