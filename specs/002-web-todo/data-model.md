# Data Model: Phase II Web Todo Application

**Feature**: 002-web-todo | **Date**: 2025-12-30

## Overview

The data model consists of two entities: `User` and `Task`. All data is persisted to Neon PostgreSQL using SQLModel ORM.

## Entity Definitions

### User

Represents an authenticated user who can own and manage tasks.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `id` | UUID v4 | Primary key, auto-generated | Unique user identifier |
| `email` | String (varchar) | Unique, indexed, email format | User's email address (for signin) |
| `password_hash` | String (varchar) | bcrypt hash | Securely hashed password |
| `created_at` | Timestamp | Auto-generated on create | When the account was created |

**SQLModel Definition:**
```python
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def set_password(self, password: str) -> None:
        """Hash and set password."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(password, self.password_hash)
```

### Task

Represents a to-do item owned by a user.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `id` | UUID v4 | Primary key, auto-generated | Unique task identifier |
| `user_id` | UUID v4 | Foreign key → users.id, indexed | Owning user's ID |
| `title` | String (varchar) | Not empty, max_length 255 | Brief task name |
| `description` | String (text) | Optional | Detailed task information |
| `is_complete` | Boolean | Default: false | Task completion status |
| `created_at` | Timestamp | Auto-generated on create | When task was created |
| `updated_at` | Timestamp | Auto-update on modification | When task was last updated |

**SQLModel Definition:**
```python
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default="", nullable=True)
    is_complete: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Optional relationship
    user: Optional["User"] = Relationship(back_populates="tasks")
```

**User with Relationship:**
```python
class User(SQLModel, table=True):
    # ... fields as above ...

    tasks: list["Task"] = Relationship(back_populates="user")
```

## Relationships

### User → Tasks

- **Type**: One-to-Many
- **Foreign Key**: `Task.user_id` references `User.id`
- **Cardinality**: One user has zero or more tasks
- **Cascade**: Tasks are deleted when user is deleted (ON DELETE CASCADE)

```
┌─────────────┐       ┌─────────────┐
│    User     │ 1   * │    Task     │
├─────────────┤───────├─────────────┤
│ id (PK)     │───────│ id (PK)     │
│ email       │       │ user_id (FK)│
│ password... │       │ title       │
│ created_at  │       │ description │
│             │       │ is_complete │
└─────────────┘       │ created_at  │
                      │ updated_at  │
                      └─────────────┘
```

## Indexes

| Table | Index | Type | Purpose |
|-------|-------|------|---------|
| `users` | `users_email_key` | Unique | Email uniqueness constraint |
| `users` | `ix_users_email` | B-tree | Fast lookup by email for auth |
| `tasks` | `ix_tasks_user_id` | B-tree | Filter tasks by user |
| `tasks` | `ix_tasks_is_complete` | B-tree | Filter by completion status |

## Schema Migration

### Initial Schema (DDL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    is_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_tasks_user_id ON tasks(user_id);
CREATE INDEX ix_tasks_is_complete ON tasks(is_complete);
```

### SQLModel Migration

On first application startup, SQLModel will create tables automatically:

```python
from sqlmodel import SQLModel, create_engine
from .models import User, Task

engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
```

## Validation Rules

### User Validation

| Field | Rule | Error Message |
|-------|------|----------------|
| `email` | Valid email format | "Invalid email format" |
| `email` | Unique (not already registered) | "Email already registered" |
| `password` | Minimum 8 characters | "Password must be at least 8 characters" |

### Task Validation

| Field | Rule | Error Message |
|-------|------|----------------|
| `title` | Non-empty | "Title is required" |
| `user_id` | Matches authenticated user | 403 Forbidden |
| `id` (for updates/deletes) | Must exist and belong to user | 404 Not Found or 403 Forbidden |

## Query Patterns

### Auth Queries

**Find user by email (signin):**
```python
def get_user_by_email(email: str, session: Session) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()
```

**Create new user (signup):**
```python
def create_user(email: str, password: str, session: Session) -> User:
    user = User(email=email)
    user.set_password(password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```

**Verify user credentials:**
```python
def verify_user(email: str, password: str, session: Session) -> Optional[User]:
    user = get_user_by_email(email, session)
    if user and user.verify_password(password):
        return user
    return None
```

### Task Queries

**List all tasks for user:**
```python
def list_tasks(user_id: UUID, session: Session) -> list[Task]:
    return session.exec(select(Task).where(Task.user_id == user_id)).all()
```

**Get single task (with ownership check):**
```python
def get_task(task_id: UUID, user_id: UUID, session: Session) -> Optional[Task]:
    return session.exec(
        select(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
    ).first()
```

**Create task:**
```python
def create_task(title: str, description: str, user_id: UUID, session: Session) -> Task:
    task = Task(title=title, description=description, user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Update task:**
```python
def update_task(task: Task, title: str, description: str, session: Session) -> Task:
    task.title = title
    task.description = description
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Toggle completion:**
```python
def toggle_task_completion(task: Task, session: Session) -> Task:
    task.is_complete = not task.is_complete
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Delete task:**
```python
def delete_task(task: Task, session: Session) -> None:
    session.delete(task)
    session.commit()
```

## Data Privacy

- **Passwords**: Never stored in plaintext; bcrypt hash only
- **User Isolation**: All task queries filtered by `user_id`
- **No Email Verification**: Emails stored as-is (Phase II scope)
- **No Personal Data**: No PII beyond email (Phase II scope)

## Audit Trail

### Timestamps

- `User.created_at`: Account creation time (immutable)
- `Task.created_at`: Task creation time (immutable)
- `Task.updated_at`: Last modification time (auto-updated)

### Usage Tracking (Future Phase)

Not in Phase II scope. Future phases may add:
- Last login timestamp
- Task completion history
- User activity logs
