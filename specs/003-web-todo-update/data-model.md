# Data Model: Phase II Web Update

## Entities

### User
Represents an application user who can own and manage tasks.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID (v4) | Unique identifier for the user |
| email | String | User's email address (unique) |
| password_hash | String | Securely hashed password (bcrypt) |
| created_at | DateTime | Timestamp of account creation |

### Task
Represents a user-owned todo item.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID (v4) | Unique identifier for the task |
| user_id | UUID (v4) | Reference to the owning user (Foreign Key) |
| title | String | Brief name/summary (required, non-empty) |
| description | String | Detailed information (optional) |
| is_completed | Boolean | Completion status |
| created_at | DateTime | Timestamp of creation |
| updated_at | DateTime | Timestamp of last update |

## Relationships
- **User (1) <-> (*) Task**: A User can own multiple Tasks. A Task belongs to exactly one User.

## Validation Rules
- **Email**: Must be a valid email format.
- **Password**: Minimum 8 characters.
- **Task Title**: Must not be empty or whitespace only.
- **UUID**: All IDs must be valid UUID v4.
