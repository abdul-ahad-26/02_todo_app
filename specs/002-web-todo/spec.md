# Feature Specification: Phase II - Full-Stack Web Todo Application

**Feature Branch**: `002-web-todo`
**Created**: 2025-12-30
**Status**: Draft
**Input**: Phase II – Full-Stack Web Todo Application

## Clarifications

### Session 2025-12-30

- Q: User ID Primary Key Type → A: UUID (v4) for both User and Task IDs
- Q: Password Hashing Algorithm → B: bcrypt
- Q: JWT Token Expiration Time → A: 24 hours
- Q: Password Minimum Length → B: 8 characters
- Q: User Session Duration → B: 24 hours (matches JWT token expiration)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

As a new user, I want to create an account so that I can access the web-based Todo application and store my tasks.

**Why this priority**: Authentication is the foundation for multi-user support. Without account creation, users cannot access any task functionality, making it the most critical capability for this phase.

**Independent Test**: Can be fully tested by visiting the signup page, providing valid email and password credentials, and verifying a new user account is created with JWT token issued.

**Acceptance Scenarios**:

1. **Given** I am on the signup page, **When** I enter a valid email (test@example.com) and a strong password, **Then** a new user account is created, I am redirected to the tasks page, and I receive a JWT token that authenticates subsequent requests.

2. **Given** I am on the signup page, **When** I enter an email that already exists in the system, **Then** I see an error message indicating the email is already registered and the account is not created.

3. **Given** I am on the signup page, **When** I enter an invalid email format, an empty password, or a password with fewer than 8 characters, **Then** I see a validation error message and the account is not created.

---

### User Story 2 - User Sign-In (Priority: P1)

As a returning user, I want to sign in with my credentials so that I can access my existing tasks.

**Why this priority**: Sign-in is essential for returning users to access their data. Combined with registration, this completes the authentication foundation required for all other features.

**Independent Test**: Can be fully tested by visiting the signin page with an existing user account, entering valid credentials, and verifying authentication succeeds with JWT token issued.

**Acceptance Scenarios**:

1. **Given** I have a registered account, **When** I enter valid email and password on the signin page, **Then** I am authenticated, redirected to the tasks page, and receive a JWT token.

2. **Given** I am on the signin page, **When** I enter an email that does not exist in the system, **Then** I see an error message indicating invalid credentials.

3. **Given** I am on the signin page, **When** I enter a valid email but incorrect password, **Then** I see an error message indicating invalid credentials.

---

### User Story 3 - Add a New Task via Web Interface (Priority: P1)

As an authenticated user, I want to add a new task with title and description through the web interface so that I can track items I need to complete.

**Why this priority**: Adding tasks is the primary value proposition. After authentication, this is the most critical feature that enables the core todo functionality.

**Independent Test**: Can be fully tested by signing in, clicking "Add Task", entering title and description, and verifying the task is created, persisted, and appears in the task list.

**Acceptance Scenarios**:

1. **Given** I am authenticated and on the tasks page, **When** I click "Add Task", enter title "Buy groceries" and description "Milk, eggs, bread", and submit, **Then** a new task is created with a unique ID, the provided title and description, completion status set to false, and it persists to the database.

2. **Given** I am authenticated, **When** I add a task with only a title and leave the description empty, **Then** the task is created with an empty description.

3. **Given** I am not authenticated, **When** I attempt to add a task via API, **Then** I receive a 401 Unauthorized error and no task is created.

---

### User Story 4 - View Tasks via Web Interface (Priority: P1)

As an authenticated user, I want to view all my tasks through the web interface so that I can see what I need to do and track progress.

**Why this priority**: Viewing tasks is essential for users to understand their workload. Combined with adding tasks, this forms the minimum viable product for the web application.

**Independent Test**: Can be fully tested by creating several tasks, refreshing or navigating to the tasks page, and verifying all tasks appear with their details.

**Acceptance Scenarios**:

1. **Given** I am authenticated and have created multiple tasks, **When** I navigate to the tasks page, **Then** I see all my tasks displayed with ID, title, description, and completion status.

2. **Given** I am authenticated and have no tasks, **When** I navigate to the tasks page, **Then** I see a message indicating there are no tasks to display.

3. **Given** User A and User B both have tasks, **When** User A views their tasks, **Then** they see only their own tasks and not User B's tasks.

---

### User Story 5 - Update Task via Web Interface (Priority: P2)

As an authenticated user, I want to update a task's title and/or description so that I can correct mistakes or add more detail.

**Why this priority**: Updating tasks provides flexibility but depends on having tasks created first. Users can work around this by deleting and recreating tasks, making it lower priority than core CRUD operations.

**Independent Test**: Can be fully tested by creating a task, clicking "Edit", modifying the title and/or description, and verifying the changes persist.

**Acceptance Scenarios**:

1. **Given** I am authenticated and have a task with title "Original Title", **When** I click "Edit", update the title to "Updated Title", and save, **Then** the task title is updated in the database and displayed correctly.

2. **Given** I am authenticated, **When** I update only the description of a task, **Then** only the description changes while the title remains unchanged.

3. **Given** User A and User B have tasks, **When** User A attempts to update User B's task ID, **Then** they receive a 403 Forbidden error and the task is not updated.

---

### User Story 6 - Mark Task Complete/Incomplete via Web Interface (Priority: P2)

As an authenticated user, I want to toggle a task's completion status so that I can track my progress on tasks.

**Why this priority**: Marking tasks complete is the primary way users track progress. It's essential for the core workflow but depends on having tasks created first.

**Independent Test**: Can be fully tested by creating a task, clicking to mark it complete, verifying the status change, then clicking to mark it incomplete and verifying again.

**Acceptance Scenarios**:

1. **Given** I am authenticated and have an incomplete task, **When** I click to mark it complete, **Then** the task status changes to true and the UI reflects this change.

2. **Given** I am authenticated and have a completed task, **When** I click to mark it incomplete, **Then** the task status changes to false and the UI reflects this change.

3. **Given** I am not authenticated, **When** I attempt to toggle a task's completion status, **Then** I receive a 401 Unauthorized error.

---

### User Story 7 - Delete Task via Web Interface (Priority: P2)

As an authenticated user, I want to delete a task so that I can remove items I no longer need to track.

**Why this priority**: Deletion is useful for cleanup but not essential for the core workflow of tracking and completing tasks. Users can work around this by marking tasks complete and ignoring them.

**Independent Test**: Can be fully tested by creating a task, clicking "Delete", confirming the action, and verifying the task is removed from both the UI and database.

**Acceptance Scenarios**:

1. **Given** I am authenticated and have a task, **When** I click "Delete" and confirm, **Then** the task is permanently removed from the database and no longer appears in the task list.

2. **Given** I am not authenticated, **When** I attempt to delete a task via API, **Then** I receive a 401 Unauthorized error and no task is deleted.

3. **Given** User A and User B have tasks, **When** User A attempts to delete User B's task, **Then** they receive a 403 Forbidden error and the task is not deleted.

---

### User Story 8 - Access Control and User Isolation (Priority: P1)

As a user, I want my tasks to be private and accessible only to me so that my data remains secure.

**Why this priority**: Multi-user isolation is a core security requirement. Without proper isolation, users can access each other's data, which is a critical security vulnerability.

**Independent Test**: Can be fully tested by creating two user accounts, having each create tasks, and verifying each user can only access their own tasks via both UI and API.

**Acceptance Scenarios**:

1. **Given** User A and User B both have tasks, **When** User A calls GET /api/{user_b_id}/tasks, **Then** they receive a 403 Forbidden error (user_id must match authenticated user).

2. **Given** User A is authenticated with a JWT for user A, **When** User A calls GET /api/{user_a_id}/tasks, **Then** they receive only their own tasks in the response.

3. **Given** a task belongs to User A, **When** User B attempts to GET, PUT, DELETE, or PATCH that task's endpoint, **Then** they receive a 403 Forbidden error.

---

### Edge Cases

- What happens when a user tries to access a task with an ID that doesn't exist? → System returns a 404 Not Found error.

- What happens when a user signs up with a password shorter than 8 characters? → System returns a 400 Bad Request error with a validation message indicating minimum password length requirement.

- What happens when JWT token is expired? → System returns a 401 Unauthorized error with a message indicating that the token is expired; user must re-signin to obtain a new token (session duration is 24 hours, no refresh token support in this phase).

- What happens when the JWT signature is invalid? → System returns a 401 Unauthorized error.

- What happens when the user_id in the URL doesn't match the authenticated user's ID? → System returns a 403 Forbidden error.

- What happens when the database connection fails? → System returns a 500 Internal Server Error with appropriate logging.

- What happens when a user enters an extremely long title or description? → System accepts the input up to database field limits (text fields can handle large content).

- What happens when multiple users update the same task concurrently? → The last update wins (optimistic locking not required for this phase).

- What happens when a user's browser refreshes after an operation? → The UI reflects the current state from the API.

## Requirements *(mandatory)*

### Functional Requirements

**Authentication & Authorization:**

- **FR-001**: System MUST provide user signup via Better Auth frontend integration.

- **FR-002**: System MUST provide user signin via Better Auth frontend integration.

- **FR-003**: System MUST issue JWT tokens upon successful authentication via Better Auth.

- **FR-004**: JWT tokens MUST be included in API requests via `Authorization: Bearer <token>` header.

- **FR-005**: Backend MUST verify JWT signature using a shared secret before processing any API request.

- **FR-006**: Backend MUST extract authenticated user identity from the validated JWT.

- **FR-007**: Backend MUST enforce that user_id in URL matches authenticated user's ID.

- **FR-008**: System MUST reject unauthenticated API requests with 401 Unauthorized.

- **FR-009**: System MUST reject requests where user_id doesn't match authenticated user with 403 Forbidden.

- **FR-010**: System MUST validate that passwords are at least 8 characters long during signup.

- **FR-011**: System MUST validate email format during signup.

**Task Management (User-Scoped):**

- **FR-012**: System MUST allow authenticated users to add tasks via POST /api/{user_id}/tasks.

- **FR-013**: System MUST allow authenticated users to view their tasks via GET /api/{user_id}/tasks.

- **FR-014**: System MUST allow authenticated users to view a specific task via GET /api/{user_id}/tasks/{id}.

- **FR-015**: System MUST allow authenticated users to update tasks via PUT /api/{user_id}/tasks/{id}.

- **FR-016**: System MUST allow authenticated users to delete tasks via DELETE /api/{user_id}/tasks/{id}.

- **FR-017**: System MUST allow authenticated users to toggle task completion via PATCH /api/{user_id}/tasks/{id}/complete.

- **FR-018**: Task responses MUST only include tasks owned by the authenticated user.

- **FR-019**: System MUST require a non-empty title when creating a task.

- **FR-020**: System MUST allow an empty description when creating a task.

- **FR-021**: Attempting to access another user's task MUST return 403 Forbidden.

**Data Persistence:**

- **FR-022**: System MUST persist tasks to Neon Serverless PostgreSQL database.

- **FR-023**: System MUST use SQLModel ORM for database operations.

- **FR-024**: Tasks MUST be associated with a user ID for ownership tracking.

- **FR-025**: User accounts MUST be persisted to support multi-user access.

**Frontend UI:**

- **FR-026**: Frontend MUST be built with Next.js 16+ using App Router.

- **FR-027**: Frontend MUST display a signup page for new user registration.

- **FR-028**: Frontend MUST display a signin page for existing user authentication.

- **FR-029**: Frontend MUST display a tasks page for authenticated users.

- **FR-030**: Frontend MUST be responsive across all screen sizes.

- **FR-031**: Frontend MUST include the JWT token in all API requests.

- **FR-032**: Frontend MUST redirect unauthenticated users to signin page.

- **FR-033**: Frontend MUST provide clear error messages for failed operations.

- **FR-034**: Frontend MUST follow global UI principles for consistency.

**Backend API:**

- **FR-035**: Backend MUST be stateless (all session state in JWT, no server-side sessions).

- **FR-036**: API endpoints MUST follow RESTful conventions.

- **FR-037**: API responses MUST use appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500).

- **FR-038**: API MUST handle errors gracefully and return meaningful error messages.

### Non-Functional Requirements

- **NFR-001**: Backend MUST use Python 3.13+ with FastAPI framework.

- **NFR-002**: Frontend MUST use Next.js 16+ with App Router.

- **NFR-003**: Authentication MUST use Better Auth library.

- **NFR-004**: Database MUST use Neon Serverless PostgreSQL.

- **NFR-005**: ORM MUST use SQLModel.

- **NFR-006**: All data MUST persist across user sessions (no in-memory storage).

- **NFR-007**: JWT tokens MUST have an expiration time of 24 hours.

- **NFR-008**: JWT secret MUST be configurable via environment variable.

- **NFR-009**: API endpoints MUST be documented with OpenAPI/Swagger (built-in with FastAPI).

### Key Entities

**User:**

- Represents an application user who can own and manage tasks.
- Attributes:
  - ID: Unique identifier for the user (UUID v4)
  - Email: User's email address (unique, used for signin)
  - Password Hash: Securely hashed password (bcrypt)
  - Created At: Timestamp of account creation

**Task:**

- Represents an item to be tracked by a user.
- Attributes:
  - ID: Unique identifier for the task (UUID v4)
  - User ID: Reference to the owning user (foreign key, UUID v4)
  - Title: Brief name/summary of the task (required, non-empty string)
  - Description: Detailed information about the task (optional, can be empty string)
  - Completion Status: Whether the task is done (boolean)
  - Created At: Timestamp of task creation
  - Updated At: Timestamp of last update

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration in under 2 minutes.

- **SC-002**: Users can sign in with existing credentials in under 30 seconds.

- **SC-003**: Users can add a new task with title and description in under 30 seconds via web interface.

- **SC-004**: Users can view all their tasks and understand status at a glance within 5 seconds of page load.

- **SC-005**: Users can toggle any task's completion status in under 10 seconds.

- **SC-006**: Users can update any task's details in under 30 seconds.

- **SC-007**: Users can delete any task in under 10 seconds.

- **SC-008**: 100% of API endpoints require valid JWT authentication (no unauthenticated access to task operations).

- **SC-009**: 100% of cross-user access attempts return 403 Forbidden (no data leakage between users).

- **SC-010**: All tasks persist across user sessions and application restarts.

- **SC-011**: Frontend displays correctly on mobile, tablet, and desktop screen sizes.

- **SC-012**: All core features (Add, View, Update, Delete, Toggle Status) function correctly as specified in acceptance scenarios.

## Assumptions

- Users have email addresses and can set strong passwords (minimum 8 characters).

- User sessions last for 24 hours (JWT token expiration). No refresh token mechanism in this phase; users must sign in again after token expires.

- JWT secret is securely stored in environment variables and never exposed in client code.

- Neon PostgreSQL database connection is configured via environment variables (connection string).

- Better Auth is configured with the same JWT secret as the backend for token validation.

- Task IDs are generated by the database (auto-increment or UUID) and are unique across all users.

- The system does not require email verification for this phase (users can sign up and immediately use the app).

- Browser supports modern JavaScript and localStorage for token storage.

- API and frontend run on compatible origins (or CORS is configured appropriately).

## Out of Scope

- AI chatbot features (Phase III+)

- MCP tools integration (Phase III+)

- Kubernetes or cloud-native messaging (Phase IV+)

- Email verification for signup

- Password reset functionality

- Two-factor authentication (2FA)

- Social login (OAuth, SSO)

- Task categories, tags, or priorities

- Due dates or reminders

- Search or filter functionality

- Undo/redo operations

- Real-time updates or WebSockets

- File attachments to tasks

- Task sharing or collaboration between users

- Subtasks or task nesting

- Task archiving

## Dependencies

- Neon Serverless PostgreSQL account and connection string

- Better Auth library installed and configured

- FastAPI installed for backend

- Next.js 16+ installed for frontend

- SQLModel installed for ORM

- Python 3.13+ runtime environment

- Node.js runtime environment for frontend

- JWT secret configured in environment variables

- Database schema migration to Neon (User and Task tables)
