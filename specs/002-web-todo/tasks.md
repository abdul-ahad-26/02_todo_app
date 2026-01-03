# Tasks: Phase II - Full-Stack Web Todo Application

**Input**: Design documents from `/specs/002-web-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md (entities), contracts/ (API endpoints), quickstart.md (test scenarios)

**Tests**: Tests are OPTIONAL - not explicitly requested in feature specification. Tests tasks are NOT included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/`, `frontend/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`

Paths below use the web app structure defined in plan.md.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure per implementation plan (backend/, backend/routes/, backend/tests/)
- [ ] T002 Create frontend directory structure per implementation plan (frontend/app/, frontend/components/, frontend/lib/, frontend/tests/)
- [ ] T003 [P] Create backend Python virtual environment at backend/venv
- [ ] T004 [P] Create backend dependencies file at backend/deps.txt
- [ ] T005 Install backend dependencies from backend/deps.txt
- [ ] T006 [P] Create frontend package.json at frontend/package.json
- [ ] T007 [P] Create frontend TypeScript config at frontend/tsconfig.json
- [ ] T008 [P] Create frontend Next.js config at frontend/next.config.mjs
- [ ] T009 [P] Create frontend Tailwind config at frontend/tailwind.config.js
- [ ] T010 [P] Create frontend PostCSS config at frontend/postcss.config.js
- [ ] T011 Install frontend dependencies from frontend/package.json
- [ ] T012 Create backend environment template at backend/.env.example
- [ ] T013 Create frontend environment template at frontend/.env.local.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T014 Create backend configuration module at backend/config.py (load DATABASE_URL, JWT_SECRET, CORS_ORIGINS)
- [ ] T015 Create database connection module at backend/db.py (SQLModel engine, session, init_db function)
- [ ] T016 Create User SQLModel at backend/models.py (UUID v4, email, password_hash, created_at, set_password, verify_password methods)
- [ ] T017 Create Task SQLModel at backend/models.py (UUID v4, user_id FK, title, description, is_complete, created_at, updated_at)
- [ ] T018 Create JWT utilities module at backend/auth.py (decode_token, verify_token, create_token, get_user_id_from_token functions)
- [ ] T019 Create FastAPI application at backend/main.py (FastAPI app, CORS middleware, include_router for tasks)
- [ ] T020 Create backend routes __init__.py at backend/routes/__init__.py
- [ ] T021 Create backend auth routes module at backend/routes/auth.py (JWT verification dependency)
- [ ] T022 [P] Create frontend API client at frontend/lib/api-client.ts (axios instance, JWT injection, error handling)
- [ ] T023 [P] Create frontend auth store at frontend/lib/auth-store.ts (React context for auth state, token storage in localStorage)
- [ ] T024 Create frontend root layout at frontend/app/layout.tsx (AuthProvider, auth state initialization, redirect unauthenticated users)
- [ ] T025 Create frontend home page at frontend/app/page.tsx (redirect to signin if not authenticated, redirect to tasks if authenticated)
- [ ] T026 [P] Create frontend loading state at frontend/app/tasks/loading.tsx (loading UI while fetching tasks)
- [ ] T027 [P] Create frontend PostCSS config at frontend/postcss.config.js
- [ ] T028 [P] Create frontend globals.css at frontend/app/globals.css (Tailwind directives, base styles)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts via Better Auth integration with JWT token issuance

**Independent Test**: Can be fully tested by visiting signup page, providing valid email/password, and verifying account creation with JWT redirect

### Implementation for User Story 1

- [ ] T029 [US1] Create signup page at frontend/app/signup/page.tsx (Better Auth signup form, email/password inputs, validation, error display)
- [ ] T030 [US1] Create signup form component at frontend/components/auth/SignupForm.tsx (form state, Better Auth signUp call, token storage, redirect on success)

**Checkpoint**: At this point, User Story 1 (registration) should be fully functional

---

## Phase 4: User Story 2 - User Sign-In (Priority: P1) 🎯 MVP

**Goal**: Enable returning users to authenticate with existing credentials via Better Auth

**Independent Test**: Can be fully tested by visiting signin page with existing account, entering credentials, and verifying auth succeeds with JWT redirect

### Implementation for User Story 2

- [ ] T031 [US2] Create signin page at frontend/app/signin/page.tsx (Better Auth signin form, email/password inputs, error display)
- [ ] T032 [US2] Create signin form component at frontend/components/auth/SigninForm.tsx (form state, Better Auth signIn call, token storage, redirect on success)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Add a New Task via Web Interface (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create tasks with title and description

**Independent Test**: Can be fully tested by signing in, clicking "Add Task", entering title/description, and verifying task creation and persistence

### Implementation for User Story 3

- [ ] T033 [US3] Create Task API routes at backend/routes/tasks.py (POST /api/{user_id}/tasks, JWT middleware, title validation, Task creation via SQLModel)
- [ ] T034 [US3] Add task list route at backend/routes/tasks.py (GET /api/{user_id}/tasks, JWT middleware, user filtering, return tasks array)
- [ ] T035 [US3] Register tasks routes in backend/main.py (include_router for tasks)
- [ ] T036 [US3] Create tasks page at frontend/app/tasks/page.tsx (TaskList component, TaskForm component, task fetching via API client)
- [ ] T037 [US3] Create TaskForm component at frontend/components/tasks/TaskForm.tsx (title/description inputs, submit handler, API call via api-client)
- [ ] T038 [US3] Create TaskList component at frontend/components/tasks/TaskList.tsx (render tasks array, empty state message, loading state)
- [ ] T039 [US3] Create TaskItem component at frontend/components/tasks/TaskItem.tsx (display task details, completion indicator, edit/delete actions)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - View Tasks via Web Interface (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to view all their tasks with completion status

**Independent Test**: Can be fully tested by creating tasks, refreshing tasks page, and verifying all tasks appear correctly

### Implementation for User Story 4

- [ ] T040 [US4] Enhance TaskList component at frontend/components/tasks/TaskList.tsx (group by completion status, visual indicators, sorting by created_at)
- [ ] T041 [US4] Add empty state UI at frontend/components/tasks/TaskList.tsx (friendly message when no tasks exist, link to add first task)

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Update Task via Web Interface (Priority: P2)

**Goal**: Enable authenticated users to modify task title and/or description

**Independent Test**: Can be fully tested by creating a task, clicking edit, modifying fields, and verifying persistence

### Implementation for User Story 5

- [ ] T042 [US5] Add update task route at backend/routes/tasks.py (PUT /api/{user_id}/tasks/{id}, JWT middleware, ownership check, Task update via SQLModel)
- [ ] T043 [US5] Add get single task route at backend/routes/tasks.py (GET /api/{user_id}/tasks/{id}, JWT middleware, ownership check, return task)
- [ ] T044 [US5] Create EditTaskForm component at frontend/components/tasks/EditTaskForm.tsx (pre-filled inputs, save handler, API call)
- [ ] T045 [US5] Add edit mode to TaskItem at frontend/components/tasks/TaskItem.tsx (toggle edit form, call EditTaskForm component)
- [ ] T046 [US5] Create edit modal/page at frontend/app/tasks/edit/[id]/page.tsx (or integrate edit as modal in tasks page)

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Mark Task Complete/Incomplete via Web Interface (Priority: P2)

**Goal**: Enable authenticated users to toggle task completion status

**Independent Test**: Can be fully tested by creating a task, toggling complete/incomplete, and verifying status change persists

### Implementation for User Story 6

- [ ] T047 [US6] Add toggle completion route at backend/routes/tasks.py (PATCH /api/{user_id}/tasks/{id}/complete, JWT middleware, ownership check, toggle is_complete)
- [ ] T048 [US6] Add checkbox/button to TaskItem at frontend/components/tasks/TaskItem.tsx (click handler, API call via api-client)
- [ ] T049 [US6] Update TaskItem styling at frontend/components/tasks/TaskItem.tsx (completed task visual distinction, strikethrough, checkmark)

**Checkpoint**: At this point, User Stories 1-6 should all work independently

---

## Phase 9: User Story 7 - Delete Task via Web Interface (Priority: P2)

**Goal**: Enable authenticated users to permanently remove tasks

**Independent Test**: Can be fully tested by creating a task, deleting with confirmation, and verifying removal

### Implementation for User Story 7

- [ ] T050 [US7] Add delete task route at backend/routes/tasks.py (DELETE /api/{user_id}/tasks/{id}, JWT middleware, ownership check, task deletion)
- [ ] T051 [US7] Add delete button to TaskItem at frontend/components/tasks/TaskItem.tsx (confirmation dialog, API call via api-client)
- [ ] T052 [US7] Create DeleteConfirmation component at frontend/components/tasks/DeleteConfirmation.tsx (modal/dialog, cancel/confirm actions)

**Checkpoint**: At this point, User Stories 1-7 should all work independently

---

## Phase 10: User Story 8 - Access Control and User Isolation (Priority: P1)

**Goal**: Ensure all API endpoints enforce JWT authentication and user ownership to prevent data leakage

**Independent Test**: Can be fully tested by creating two users, having each create tasks, and verifying each user can only access their own data

### Implementation for User Story 8

- [ ] T053 [US8] Create JWT authentication middleware at backend/auth.py (extract token, verify signature, extract user_id, 401/403 error handling)
- [ ] T054 [US8] Add ownership verification helper at backend/routes/tasks.py (verify task.user_id == authenticated user_id, return 403 if mismatch)
- [ ] T055 [US8] Apply auth middleware to all task routes at backend/routes/tasks.py (Depends on JWT verification)
- [ ] T056 [US8] Add user_id validation at backend/routes/tasks.py (verify path parameter matches authenticated user_id, return 403 if mismatch)
- [ ] T057 [US8] Test cross-user access at backend routes (User A cannot access User B's tasks, returns 403)
- [ ] T058 [US8] Ensure api-client attaches JWT to all requests at frontend/lib/api-client.ts (Authorization header from localStorage)
- [ ] T059 [US8] Add 401/403 error handling at frontend (redirect to signin on 401, show error on 403)

**Checkpoint**: At this point, ALL user stories should be fully functional with proper security

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T060 [P] Create backend CLAUDE.md at backend/CLAUDE.md (agent instructions, tech stack, testing commands)
- [ ] T061 [P] Create frontend CLAUDE.md at frontend/CLAUDE.md (agent instructions, tech stack, testing commands)
- [ ] T062 Add consistent UI styling at frontend/components/ui/ (Button, Input, Card components with Tailwind)
- [ ] T063 [P] Add error boundary at frontend/app/error.tsx (catch and display errors gracefully)
- [ ] T064 [P] Add not-found page at frontend/app/not-found.tsx (handle 404s gracefully)
- [ ] T065 [P] Update quickstart.md validation in specs/002-web-todo/quickstart.md (verify all steps work)
- [ ] T066 [P] Test responsive design on mobile/tablet/desktop at frontend (Tailwind breakpoints verification)
- [ ] T067 [P] Verify OpenAPI docs at backend (http://localhost:8000/docs shows all endpoints)
- [ ] T068 [P] Validate environment variables (backend .env, frontend .env.local match requirements)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if team capacity allows)
  - Recommended order for incremental delivery: US1 → US2 → US3 → US4 → US5 → US6 → US7 → US8
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (US1 - Registration)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (US2 - Sign-In)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (US3 - Add Task)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 auth
- **User Story 4 (US4 - View Tasks)**: Can start after Foundational (Phase 2) - Depends on US3 for task data, but can build UI in parallel
- **User Story 5 (US5 - Update Task)**: Can start after Foundational (Phase 2) - Depends on US3/US4 for existing tasks
- **User Story 6 (US6 - Toggle Completion)**: Can start after Foundational (Phase 2) - Depends on US3/US4 for existing tasks
- **User Story 7 (US7 - Delete Task)**: Can start after Foundational (Phase 2) - Depends on US3/US4 for existing tasks
- **User Story 8 (US8 - Access Control)**: Can start after Foundational (Phase 2) - Applies to all stories, but can be implemented and tested independently

### Within Each Phase

- Setup tasks marked [P] can run in parallel
- Foundational tasks marked [P] can run in parallel (within Phase 2)
- Models before routes
- Routes before UI
- Auth middleware before user story endpoints
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T003-T010) marked [P] can run in parallel
- All Foundational tasks (T022-T026) marked [P] can run in parallel
- Once Foundational phase completes, user stories can be worked on in parallel by different developers
- Different user stories can be worked on in parallel (e.g., US5, US6, US7 after US3/US4 complete)
- Polish tasks (T060-T068) marked [P] can run in parallel

---

## Parallel Example: Foundational Phase (Phase 2)

```bash
# Launch all frontend infrastructure tasks together:
Task: "T022 [P] Create frontend API client at frontend/lib/api-client.ts"
Task: "T023 [P] Create frontend auth store at frontend/lib/auth-store.ts"
Task: "T024 [P] Create frontend root layout at frontend/app/layout.tsx"
Task: "T025 [P] Create frontend home page at frontend/app/page.tsx"
Task: "T026 [P] Create frontend loading state at frontend/app/tasks/loading.tsx"
Task: "T027 [P] Create frontend PostCSS config at frontend/postcss.config.js"
Task: "T028 [P] Create frontend globals.css at frontend/app/globals.css"

# Launch all backend models and utilities together:
Task: "T014 Create backend configuration module at backend/config.py"
Task: "T015 Create database connection module at backend/db.py"
Task: "T016 Create User SQLModel at backend/models.py"
Task: "T017 Create Task SQLModel at backend/models.py"
Task: "T018 Create JWT utilities module at backend/auth.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1-4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 - Registration
4. Complete Phase 4: User Story 2 - Sign-In
5. Complete Phase 5: User Story 3 - Add Task
6. Complete Phase 6: User Story 4 - View Tasks
7. **STOP and VALIDATE**: Test User Stories 1-4 independently (can register, signin, add, view tasks)
8. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Registration) → Test independently
3. Add User Story 2 (Sign-In) → Test independently → Auth complete!
4. Add User Story 3 (Add Task) → Test independently → Basic CRUD works!
5. Add User Story 4 (View Tasks) → Test independently → MVP complete!
6. Add User Story 5 (Update Task) → Test independently
7. Add User Story 6 (Toggle Completion) → Test independently
8. Add User Story 7 (Delete Task) → Test independently
9. Add User Story 8 (Access Control) → Test independently → Security complete!
10. Complete Polish phase → Production ready!

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Stories 1-2 (Auth)
   - Developer B: User Stories 3-4 (Core CRUD)
   - Developer C: User Stories 5-7 (Advanced features)
3. Developer D: User Story 8 + Polish (Security + cross-cutting)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are NOT included (not requested in spec)
