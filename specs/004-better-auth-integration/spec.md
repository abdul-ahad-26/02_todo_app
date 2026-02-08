# Feature Specification: Better Auth Integration

**Feature Branch**: `004-better-auth-integration`
**Created**: 2026-02-06
**Status**: Draft
**Input**: User description: "Integrate Better Auth as the authentication authority for an existing application, enabling secure user authentication, session management, and protected API access using JWT-based stateless authorization."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sign Up with Email & Password (Priority: P1)

A new user visits the application and creates an account by providing
their email address and a password. The system creates the user via
Better Auth, establishes a session, and redirects them to the task
dashboard.

**Why this priority**: Without account creation, no other
authentication feature can function. This is the entry point for
all new users.

**Independent Test**: Can be fully tested by navigating to the
sign-up page, entering an email and password, submitting the form,
and verifying that a session is created and the user lands on the
task dashboard.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user on the sign-up page,
   **When** they submit a valid email and password (8+ characters),
   **Then** a user account is created, a session is established,
   and the user is redirected to the task dashboard.

2. **Given** an unauthenticated user on the sign-up page,
   **When** they submit an email that already exists,
   **Then** the system displays an error message indicating the
   email is already registered.

3. **Given** an unauthenticated user on the sign-up page,
   **When** they submit a password shorter than 8 characters,
   **Then** the system displays a validation error for the
   password field.

---

### User Story 2 - Sign In with Email & Password (Priority: P1)

An existing user visits the application and signs in with their
email and password. The system verifies credentials via Better Auth,
creates a session, and redirects them to the task dashboard.

**Why this priority**: Sign-in is equally critical to sign-up —
returning users need immediate access. Tied at P1 with sign-up.

**Independent Test**: Can be tested by signing in with previously
created credentials and verifying a session is established and the
task dashboard loads with the user's data.

**Acceptance Scenarios**:

1. **Given** a registered user on the sign-in page,
   **When** they submit valid email and password,
   **Then** a session is created and they are redirected to the
   task dashboard.

2. **Given** a user on the sign-in page,
   **When** they submit an incorrect password,
   **Then** the system displays a generic "Invalid credentials"
   error (not revealing whether email or password was wrong).

3. **Given** a user on the sign-in page,
   **When** they submit a non-existent email,
   **Then** the system displays the same generic "Invalid
   credentials" error.

---

### User Story 3 - Protected API Access via JWT (Priority: P1)

When an authenticated user performs task operations (create, read,
update, delete), the frontend obtains a JWT from Better Auth and
sends it to the FastAPI backend. The backend verifies the JWT using
Better Auth's JWKS endpoint and authorizes the request.

**Why this priority**: The entire task management functionality
depends on secure API authorization. Without JWT verification, the
backend cannot trust any request.

**Independent Test**: Can be tested by signing in, performing a
task operation, and verifying that (a) the request includes a JWT
in the Authorization header, (b) the backend accepts it, and
(c) task data is scoped to the authenticated user.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a valid session,
   **When** they request their task list,
   **Then** the frontend sends a JWT in the Authorization header
   and the backend returns only that user's tasks.

2. **Given** an unauthenticated request (no token),
   **When** the backend receives it,
   **Then** it responds with 401 Unauthorized.

3. **Given** a request with an expired or tampered JWT,
   **When** the backend verifies it,
   **Then** it responds with 401 Unauthorized.

4. **Given** an authenticated user,
   **When** they attempt to access another user's tasks via URL
   manipulation,
   **Then** the backend rejects the request with 403 Forbidden.

---

### User Story 4 - Sign Out (Priority: P2)

An authenticated user clicks "Sign Out" and their session is
terminated. They are redirected to the sign-in page and can no
longer access protected pages or APIs without signing in again.

**Why this priority**: Important for security and shared-device
scenarios, but secondary to the core auth flow.

**Independent Test**: Can be tested by signing in, clicking
sign out, then verifying the session is cleared, the user is
redirected, and attempting to access the task dashboard redirects
to sign-in.

**Acceptance Scenarios**:

1. **Given** an authenticated user on any page,
   **When** they click "Sign Out",
   **Then** their session is terminated, localStorage/cookies are
   cleared, and they are redirected to the sign-in page.

2. **Given** a signed-out user,
   **When** they attempt to access the task dashboard directly,
   **Then** they are redirected to the sign-in page.

---

### User Story 5 - Route Protection via Middleware (Priority: P2)

Protected pages (task dashboard, settings) are guarded by
middleware. Unauthenticated users are automatically redirected
to the sign-in page. Authenticated users on auth pages (sign-in,
sign-up) are redirected to the dashboard.

**Why this priority**: Improves user experience and prevents
unauthorized access at the page level, complementing API-level JWT
protection.

**Independent Test**: Can be tested by attempting to access
protected URLs without a session and verifying redirect behavior
in both directions.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user,
   **When** they navigate to `/tasks`,
   **Then** they are redirected to `/signin`.

2. **Given** an authenticated user,
   **When** they navigate to `/signin` or `/signup`,
   **Then** they are redirected to `/tasks`.

---

### Edge Cases

- What happens when the Better Auth database is unreachable during
  sign-in? The system MUST display a user-friendly error message,
  not a raw server error.
- What happens when a JWT expires mid-session while the user is
  actively using the app? The frontend MUST detect the 401 response
  and redirect to sign-in.
- What happens when the JWKS endpoint is temporarily unavailable?
  The backend MUST return 503 Service Unavailable, not silently
  accept unverified tokens.
- What happens when a user has multiple tabs open and signs out in
  one? Other tabs MUST detect the session change on their next API
  call and redirect to sign-in.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use Better Auth as the sole
  authentication authority for user registration and sign-in.
- **FR-002**: System MUST enable email/password authentication
  with a minimum password length of 8 characters.
- **FR-003**: System MUST use the Better Auth JWT plugin to issue
  JWT tokens for API authorization.
- **FR-004**: System MUST expose a JWKS endpoint via Better Auth
  at `/api/auth/jwks` for public key distribution.
- **FR-005**: FastAPI backend MUST verify JWT tokens by fetching
  the public key from the JWKS endpoint (not via a shared secret).
- **FR-006**: FastAPI backend MUST extract the user identity from
  the verified JWT payload and enforce ownership on all task
  operations.
- **FR-007**: All task API endpoints MUST reject requests without
  a valid JWT with 401 Unauthorized.
- **FR-008**: System MUST manage user sessions via Better Auth
  session cookies (httpOnly, secure, sameSite).
- **FR-009**: Frontend MUST obtain a JWT from Better Auth's
  `/api/auth/token` endpoint before making API calls to the
  backend.
- **FR-010**: Frontend MUST include the JWT in the
  `Authorization: Bearer <token>` header for all backend requests.
- **FR-011**: System MUST redirect unauthenticated users away from
  protected pages via Next.js middleware.
- **FR-012**: System MUST redirect authenticated users away from
  auth pages (sign-in, sign-up) to the dashboard.
- **FR-013**: System MUST replace the existing custom JWT
  implementation (python-jose, bcrypt) with Better Auth as the
  single source of truth for authentication.
- **FR-014**: Better Auth MUST store its user, session, and account
  data in the same Neon PostgreSQL database used by the application.

### Key Entities

- **User**: A person who registers and authenticates with the
  system. Managed by Better Auth. Key attributes: id, name, email,
  emailVerified, image, createdAt, updatedAt.
- **Session**: A server-side record of an active authentication
  session. Managed by Better Auth. Key attributes: id, userId,
  token, expiresAt, ipAddress, userAgent.
- **Account**: Links a user to an authentication provider
  (email/password in this case). Managed by Better Auth. Key
  attributes: id, userId, accountId, providerId.
- **Task**: A todo item owned by a user. Managed by the FastAPI
  backend. Existing entity — unchanged by this feature except that
  `user_id` now references the Better Auth user ID.

### Assumptions

- The application uses Neon PostgreSQL as its database, and Better
  Auth will use the same database via direct connection (not an ORM
  adapter).
- Better Auth's user ID format (string) is compatible with the
  existing task table's `user_id` column (currently UUID). A data
  migration may be required.
- Email verification is not required for initial registration
  (users can sign in immediately after sign-up). This can be
  enabled later.
- Social/OAuth providers (GitHub, Google) are out of scope for this
  feature. Only email/password is implemented now.
- Password reset / forgot password flow is out of scope for this
  feature and can be added as a separate feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account creation (sign-up) in
  under 30 seconds from landing on the sign-up page.
- **SC-002**: Users can sign in and see their task dashboard in
  under 5 seconds from form submission.
- **SC-003**: 100% of task API requests without a valid JWT are
  rejected with 401 Unauthorized.
- **SC-004**: 100% of task API requests are scoped to the
  authenticated user — no cross-user data leakage.
- **SC-005**: Unauthenticated users are redirected to sign-in
  within 1 second of accessing a protected page.
- **SC-006**: The existing custom auth (python-jose, bcrypt,
  localStorage tokens) is fully removed — no dead code remains.
- **SC-007**: All authentication state is managed by Better Auth —
  no custom user table or password hashing in the backend.
