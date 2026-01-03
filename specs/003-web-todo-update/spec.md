# Feature Specification: Phase II - Full-Stack Web Todo Application (Updated)

**Feature Branch**: `003-web-todo-update`
**Created**: 2026-01-02
**Status**: Draft
**Input**: Update Phase 2 Web spec to include dedicated folder for docs, use UV for Python management, and align UI requirements with constitution.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration with Modern UI (Priority: P1)

As a new user, I want to create an account using a high-contrast dark interface so that I can securely start tracking my tasks in a professional environment.

**Why this priority**: Authentication is the foundation for multi-user support. The UI must align with the constitution's high-contrast theme from the start to ensure brand consistency.

**Independent Test**: Can be fully tested by visiting the signup page, verifying the `--background` and `--foreground` CSS variables are applied, and completing registration.

**Acceptance Scenarios**:

1. **Given** I am on the signup page, **When** I view the page, **Then** the background is Deep Slate (#0f172a) and text is Ghost White (#f8fafc).
2. **Given** I am on the signup page, **When** I enter valid credentials, **Then** a new user account is created and I am redirected to the tasks page.

---

### User Story 2 - Task Management in Dedicated Phase Folder (Priority: P1)

As a developer/architect, I want the Phase 2 application to reside in its own `phase-2-web/` directory so that the project history and evolution are clearly structured as per the constitution.

**Why this priority**: The constitution mandates a phase-based project structure. Failure to organize code in dedicated folders violates the core architectural principles of the evolution.

**Independent Test**: Can be verified by checking the file system for the existence of `phase-2-web/` and ensuring it contains all relevant source code.

**Acceptance Scenarios**:

1. **Given** the repository root, **When** listing files, **Then** a `phase-2-web/` directory exists containing the Next.js and FastAPI projects.
2. **Given** the documentation for Phase 2, **When** referenced, **Then** all paths are relative to the `specs/003-web-todo-update/` or the phase-specific source folder.

---

### User Story 3 - Python Project Management via UV (Priority: P1)

As a developer, I want to manage the backend dependencies using UV so that I have ultra-fast, reproducible builds that align with the project's technical standard.

**Why this priority**: UV is the mandated package manager for Python projects in this evolution (as per Constitution Section II).

**Independent Test**: Can be verified by the presence of a `pyproject.toml` and `uv.lock` file in the backend directory.

**Acceptance Scenarios**:

1. **Given** the backend project directory, **When** I check for dependency management, **Then** UV-specific configuration files are present.
2. **Given** a new environment, **When** I run `uv sync`, **Then** all FastAPI, SQLModel, and Better Auth dependencies are installed correctly.

---

### Edge Cases

- What happens if a developer tries to use standard `pip` instead of `uv`? -> The environment should be restricted or documented to only support UV to ensure lockfile consistency.
- How does the UI handle low-contrast scenarios? -> The constitution mandates a "Modern Dark/High-Contrast" theme; accessibility checks must ensure `--foreground` and `--background` maintain sufficient contrast ratios.

## Requirements *(mandatory)*

### Functional Requirements

**Project Structure & Docs:**
- **FR-001**: System MUST be contained entirely within the `phase-2-web/` top-level directory.
- **FR-002**: Specification, Plan, and Task artifacts for this phase MUST be stored in `specs/003-web-todo-update/`.

**Tech Stack (Python):**
- **FR-003**: Backend MUST use UV for dependency management, virtual environments, and package execution.
- **FR-004**: System MUST use Python 3.13+ for all backend services.

**UI Design (Constitution Alignment):**
- **FR-005**: Frontend MUST implement a "Modern Dark/High-Contrast" theme using CSS variables.
- **FR-006**: System MUST define and use variables: `--primary: #3b82f6`, `--secondary: #10b981`, `--accent: #8b5cf6`, `--background: #0f172a`, `--foreground: #f8fafc`, `--error: #ef4444`.
- **FR-007**: Components MUST use these variables for all colors, spacing, and transitions to ensure a continuous product evolution look.

**Core Web Todo Features (Re-mapped):**
- **FR-008**: System MUST provide user signup, signin, and JWT issue via Better Auth integration.
- **FR-009**: Backend MUST expose RESTful endpoints for Task CRUD (POST, GET, PUT, DELETE, PATCH).
- **FR-010**: System MUST persist data to Neon Serverless PostgreSQL using SQLModel ORM.

### Key Entities

- **User**: Represents an authenticated entity. Attributes: UUID, Email, Password Hash, Timestamps.
- **Task**: Represents a user-owned todo item. Attributes: UUID, User ID (FK), Title, Description, Completion Status, Timestamps.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the Phase 2 source code is located in the `phase-2-web/` directory.
- **SC-002**: Backend environment can be fully initialized using `uv sync` in under 10 seconds (excluding download time).
- **SC-003**: 100% of UI components use the CSS variables defined in the constitution for their color palette.
- **SC-004**: Users see a consistent High-Contrast Dark theme across all pages (Signup, Signin, Tasks).
- **SC-005**: All specifications and documentation for this update are located in the designated `specs/003-web-todo-update/` folder.
- **SC-006**: The system successfully maintains user-task isolation (100% cross-user access attempts return 403 Forbidden).

## Assumptions

- UV is installed and available in the development/production environments.
- Next.js 16+ and FastAPI are compatible with the specified CSS variable strategy.
- Developers follow the phase-based directory structure for all future commits.
- Better Auth configuration supports the stateless JWT requirement with the shared secret.
