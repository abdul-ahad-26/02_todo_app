# Tasks: Phase II - Full-Stack Web Application

**Input**: Design documents from `/specs/005-fullstack-web-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/rest-api.md, quickstart.md

**Tests**: Not explicitly requested in spec. Test tasks omitted. Manual E2E testing per quickstart.md verification steps.

**Organization**: Tasks grouped by user story. US7 (Multi-User Data Isolation) is a cross-cutting concern enforced in Foundational phase (JWT auth + ownership checks) rather than a separate phase.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `phase-2-web/backend/src/`
- **Frontend**: `phase-2-web/frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create monorepo structure, initialize both projects, configure environment

- [x] T001 Create monorepo directory structure: `phase-2-web/frontend/`, `phase-2-web/backend/src/{models,api/routers,crud}/` with all `__init__.py` files
- [x] T002 Initialize backend Python project with UV: `pyproject.toml` with fastapi, sqlmodel, pyjwt, uvicorn, python-dotenv dependencies in `phase-2-web/backend/`
- [x] T003 Initialize frontend Next.js 16 project with TypeScript, Tailwind CSS, App Router, src directory in `phase-2-web/frontend/`
- [x] T004 [P] Create backend `.env.example` with DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS, DEBUG in `phase-2-web/backend/.env.example`
- [x] T005 [P] Create frontend `.env.local.example` with DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL in `phase-2-web/frontend/.env.local.example`
- [x] T006 [P] Create backend `CLAUDE.md` with backend-specific agent instructions in `phase-2-web/backend/CLAUDE.md`
- [x] T007 [P] Create frontend `CLAUDE.md` with frontend-specific agent instructions in `phase-2-web/frontend/CLAUDE.md`
- [x] T008 [P] Create `phase-2-web/README.md` with setup instructions referencing quickstart.md

**Checkpoint**: Both projects initialized and runnable (empty). Directory structure matches plan.md.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database connection, config, JWT auth, CORS, Task model, CRUD — the core infrastructure that ALL user stories depend on. Also enforces US7 (Multi-User Data Isolation) via JWT ownership checks.

**CRITICAL**: No user story work can begin until this phase is complete.

### Backend Foundation

- [x] T009 Implement settings/config module loading env vars (DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS, DEBUG) in `phase-2-web/backend/src/config.py`
- [x] T010 Implement database engine and session dependency (create_engine with pool_pre_ping, get_session generator) in `phase-2-web/backend/src/db.py`
- [x] T011 Implement Task SQLModel models (Task, TaskBase, TaskCreate, TaskUpdate, TaskPublic) per data-model.md in `phase-2-web/backend/src/models/task.py`
- [x] T012 Implement TaskRepository with CRUD operations (create, get_by_id, get_all_by_user, update, delete, toggle_complete) in `phase-2-web/backend/src/crud/task.py`
- [x] T013 Implement JWT verification dependency (HTTPBearer, decode with BETTER_AUTH_SECRET/HS256, extract user_id from sub claim, validate user_id matches path param) in `phase-2-web/backend/src/api/auth.py`
- [x] T014 Implement task router with all 6 endpoints per contracts/rest-api.md (GET/POST tasks, GET/PUT/DELETE task by id, PATCH toggle complete) in `phase-2-web/backend/src/api/routers/tasks.py`
- [x] T015 Implement FastAPI app with CORS middleware, lifespan (create_all tables on startup), health endpoint, task router inclusion in `phase-2-web/backend/src/main.py`

### Frontend Foundation

- [x] T016 Implement CSS variables for Modern Dark/High-Contrast theme per constitution Section V in `phase-2-web/frontend/src/app/globals.css`
- [x] T017 Configure Tailwind to extend colors from CSS variables in `phase-2-web/frontend/tailwind.config.ts`
- [x] T018 Implement root layout with dark theme, Inter font, metadata in `phase-2-web/frontend/src/app/layout.tsx`
- [x] T019 Install better-auth package and implement Better Auth server config with jwt() + nextCookies() plugins, PostgreSQL database, emailAndPassword enabled in `phase-2-web/frontend/src/lib/auth.ts`
- [x] T020 Implement Better Auth client config with createAuthClient() + jwtClient() plugin in `phase-2-web/frontend/src/lib/auth-client.ts`
- [x] T021 Implement Better Auth catch-all route handler (toNextJsHandler) in `phase-2-web/frontend/src/app/api/auth/[...all]/route.ts`
- [x] T022 Implement centralized API client with base URL from NEXT_PUBLIC_API_URL, JWT token attachment via authClient.token(), typed request/response helpers in `phase-2-web/frontend/src/lib/api.ts`
- [x] T023 Implement auth protection middleware redirecting unauthenticated users to /sign-in for /dashboard routes in `phase-2-web/frontend/middleware.ts`

**Checkpoint**: Backend serves health endpoint. Frontend loads with dark theme. Better Auth tables created. JWT auth dependency works. Task CRUD operations functional via API. Foundation ready — user story implementation can now begin.

---

## Phase 3: User Story 1 — Sign Up and Sign In (Priority: P1)

**Goal**: Users can create accounts, sign in, sign out. Sessions persist. JWT tokens issued for API access.

**Independent Test**: Navigate to /sign-up, create account with email+password, verify redirect to dashboard. Sign out. Sign back in at /sign-in. Verify session established and dashboard accessible.

### Implementation for User Story 1

- [ ] T024 [P] [US1] Create sign-up form component with email, name, password fields, validation (min 8 chars password), error display, submit handler calling authClient.signUp.email() in `phase-2-web/frontend/src/components/auth/sign-up-form.tsx`
- [ ] T025 [P] [US1] Create sign-in form component with email, password fields, error display (generic "invalid credentials" message), submit handler calling authClient.signIn.email() in `phase-2-web/frontend/src/components/auth/sign-in-form.tsx`
- [ ] T026 [US1] Create sign-up page (Client Component) rendering SignUpForm, link to sign-in in `phase-2-web/frontend/src/app/(auth)/sign-up/page.tsx`
- [ ] T027 [US1] Create sign-in page (Client Component) rendering SignInForm, link to sign-up in `phase-2-web/frontend/src/app/(auth)/sign-in/page.tsx`
- [ ] T028 [US1] Implement landing page with redirect logic: authenticated users → /dashboard, unauthenticated → /sign-in in `phase-2-web/frontend/src/app/page.tsx`

**Checkpoint**: User can sign up, sign in, sign out. Session persists. Redirects work. Error messages shown for duplicate email, wrong credentials.

---

## Phase 4: User Story 2 — View My Task List (Priority: P1)

**Goal**: Signed-in users see all their tasks on a dashboard with title, completion status, and creation date. Empty state shown when no tasks exist.

**Independent Test**: Sign in, verify dashboard loads. Create tasks via API (or seed data), refresh, verify all tasks appear with correct details. Verify empty state message when no tasks.

**Dependencies**: US1 must be complete (need sign-in to access dashboard).

### Implementation for User Story 2

- [ ] T029 [P] [US2] Create empty-state component showing friendly message when user has no tasks in `phase-2-web/frontend/src/components/tasks/empty-state.tsx`
- [ ] T030 [P] [US2] Create task-item component displaying task title, completion status (checkbox), creation date, with slots for action buttons in `phase-2-web/frontend/src/components/tasks/task-item.tsx`
- [ ] T031 [US2] Create task-list component fetching tasks from API via lib/api.ts, rendering task-item for each task or empty-state when none in `phase-2-web/frontend/src/components/tasks/task-list.tsx`
- [ ] T032 [US2] Create dashboard layout with nav bar, user name display, sign-out button in `phase-2-web/frontend/src/app/dashboard/layout.tsx`
- [ ] T033 [US2] Create dashboard page composing task-list component, loading state, error handling in `phase-2-web/frontend/src/app/dashboard/page.tsx`

**Checkpoint**: Dashboard displays all user tasks. Empty state shown for new users. Unauthenticated access redirects to sign-in. Loading state displayed while fetching.

---

## Phase 5: User Story 3 — Add a New Task (Priority: P1)

**Goal**: Users can add tasks with a required title (1-200 chars) and optional description (max 1000 chars). New tasks appear immediately in the task list.

**Independent Test**: Sign in, click "Add Task", enter title and description, submit. Verify task appears in list. Try submitting without title — verify validation error. Try title >200 chars — verify error.

**Dependencies**: US2 must be complete (need dashboard/task list to see new tasks).

### Implementation for User Story 3

- [ ] T034 [US3] Create task-form component with title input (required, 1-200 chars), description textarea (optional, max 1000 chars), client-side validation, submit/cancel buttons, calling POST /api/{user_id}/tasks via lib/api.ts in `phase-2-web/frontend/src/components/tasks/task-form.tsx`
- [ ] T035 [US3] Integrate task-form into dashboard page with "Add Task" button that shows/hides the form, refresh task list on successful creation in `phase-2-web/frontend/src/app/dashboard/page.tsx`

**Checkpoint**: Users can create tasks with validation. New tasks appear in list immediately. Success/error feedback shown.

---

## Phase 6: User Story 4 — Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion with a single click. Visual indicator updates immediately. Change persists on refresh.

**Independent Test**: Create a task, click the completion toggle, verify visual indicator changes. Refresh page, verify status persisted. Toggle back to incomplete, verify.

**Dependencies**: US2 must be complete (need task-item component with checkbox).

### Implementation for User Story 4

- [ ] T036 [US4] Add toggle-complete click handler to task-item component calling PATCH /api/{user_id}/tasks/{id}/complete via lib/api.ts, update local state optimistically, show error on failure in `phase-2-web/frontend/src/components/tasks/task-item.tsx`

**Checkpoint**: Clicking checkbox toggles completion. Visual indicator (checkbox, strikethrough) updates. Status persists on refresh.

---

## Phase 7: User Story 5 — Update Task Details (Priority: P3)

**Goal**: Users can edit a task's title and/or description. Changes validated and persisted.

**Independent Test**: Create a task, click edit, change title, save. Verify updated title in list. Edit again, change only description. Verify. Try clearing title — verify validation error. Click cancel — verify no changes saved.

**Dependencies**: US2 must be complete (need task-item component). Reuses task-form from US3.

### Implementation for User Story 5

- [ ] T037 [US5] Add edit mode to task-form component: accept optional initial values (title, description) for pre-filling, call PUT /api/{user_id}/tasks/{id} on submit instead of POST, handle cancel in `phase-2-web/frontend/src/components/tasks/task-form.tsx`
- [ ] T038 [US5] Add edit button to task-item component that shows inline task-form with pre-filled values, refresh task list on successful update in `phase-2-web/frontend/src/components/tasks/task-item.tsx`

**Checkpoint**: Edit button opens form with current values. Save updates task. Cancel discards changes. Validation prevents blank title.

---

## Phase 8: User Story 6 — Delete a Task (Priority: P3)

**Goal**: Users can permanently delete tasks with a confirmation step.

**Independent Test**: Create a task, click delete, confirm deletion. Verify task removed from list and persists on refresh. Click delete, cancel confirmation — verify task remains.

**Dependencies**: US2 must be complete (need task-item component with delete button).

### Implementation for User Story 6

- [ ] T039 [US6] Add delete button to task-item component with confirmation prompt (confirm/cancel), calling DELETE /api/{user_id}/tasks/{id} via lib/api.ts, remove task from list on success, show error on failure in `phase-2-web/frontend/src/components/tasks/task-item.tsx`

**Checkpoint**: Delete button shows confirmation. Confirmed deletion removes task permanently. Cancel preserves task.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Responsive design, accessibility, error edge cases, final validation

- [ ] T040 [P] Ensure responsive layout works from 375px to 1920px: test sign-in, sign-up, dashboard pages with mobile-first Tailwind breakpoints in `phase-2-web/frontend/src/`
- [ ] T041 [P] Add loading spinners/skeletons for API calls (task list fetch, form submissions) across dashboard components in `phase-2-web/frontend/src/components/tasks/`
- [ ] T042 [P] Handle session expiry edge case: detect 401 responses in API client, redirect to /sign-in with "session expired" message in `phase-2-web/frontend/src/lib/api.ts`
- [ ] T043 [P] Handle database unavailability: show user-friendly error without exposing technical details in `phase-2-web/backend/src/main.py`
- [ ] T044 Validate full-stack flow per quickstart.md Section 7: sign up, create task, toggle, refresh, sign out, sign in as different user, verify data isolation
- [ ] T045 [P] Sanitize task title/description inputs to prevent XSS — ensure React's default escaping is active, validate no raw HTML rendering in `phase-2-web/frontend/src/components/tasks/`

**Checkpoint**: Application works end-to-end on mobile and desktop. Edge cases handled gracefully. All 7 verification steps from quickstart.md pass.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1: Auth)**: Depends on Phase 2 — BLOCKS US2 (need sign-in for dashboard)
- **Phase 4 (US2: View Tasks)**: Depends on Phase 3 — BLOCKS US3, US4, US5, US6 (need dashboard)
- **Phase 5 (US3: Add Task)**: Depends on Phase 4
- **Phase 6 (US4: Toggle Complete)**: Depends on Phase 4 — can run in parallel with US3
- **Phase 7 (US5: Update Task)**: Depends on Phase 4 + US3 (reuses task-form) — can run in parallel with US4, US6
- **Phase 8 (US6: Delete Task)**: Depends on Phase 4 — can run in parallel with US3, US4, US5
- **Phase 9 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1 (Setup)
  └─► Phase 2 (Foundational + US7 Data Isolation)
        └─► Phase 3 (US1: Auth) ─── MVP Auth
              └─► Phase 4 (US2: View Tasks) ─── MVP View
                    ├─► Phase 5 (US3: Add Task) ─── MVP Complete
                    ├─► Phase 6 (US4: Toggle) ─── [P] parallel with US3
                    ├─► Phase 7 (US5: Update) ─── [P] parallel with US4, US6
                    └─► Phase 8 (US6: Delete) ─── [P] parallel with US3, US4, US5
                          └─► Phase 9 (Polish)
```

### Within Each User Story

- Models/services before UI components
- UI components before page integration
- Core implementation before polish
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: T004–T008 can all run in parallel (different files)
- **Phase 2 Backend**: T009→T010→T011→T012→T013→T014→T015 (sequential — each depends on prior)
- **Phase 2 Frontend**: T016–T018 in parallel, then T019→T020→T021→T22→T23 (sequential auth setup)
- **Phase 2**: Backend and frontend foundation can be built in parallel
- **Phase 3**: T024 and T025 in parallel (different components)
- **Phase 4**: T029 and T030 in parallel (different components)
- **Phase 6–8**: US4, US5, US6 can run in parallel after US2 (different features, minimal file overlap)
- **Phase 9**: T040–T043, T045 can all run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Backend and frontend can be built simultaneously:

# Stream 1 (Backend): T009 → T010 → T011 → T012 → T013 → T014 → T015
# Stream 2 (Frontend): T016+T017+T018 (parallel) → T019 → T020 → T021 → T022 → T023
```

## Parallel Example: After US2 Complete

```bash
# These user stories can proceed in parallel (different features):

# Stream A: Phase 5 (US3: Add Task) — T034 → T035
# Stream B: Phase 6 (US4: Toggle) — T036
# Stream C: Phase 7 (US5: Update) — T037 → T038  (if task-form from US3 exists)
# Stream D: Phase 8 (US6: Delete) — T039
```

---

## Implementation Strategy

### MVP First (Setup + Auth + View + Add)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: US1 Sign Up/Sign In
4. Complete Phase 4: US2 View Task List
5. Complete Phase 5: US3 Add a New Task
6. **STOP and VALIDATE**: User can sign up, sign in, add tasks, view tasks
7. This is the minimum viable product

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 (Auth) → Users can sign up/in → Deploy
3. US2 (View) → Users see their tasks → Deploy
4. US3 (Add) → Users can add tasks → Deploy (MVP!)
5. US4 (Toggle) → Users can complete tasks → Deploy
6. US5 (Update) → Users can edit tasks → Deploy
7. US6 (Delete) → Users can remove tasks → Deploy
8. Polish → Production-ready → Final deploy

---

## Notes

- Total tasks: **45**
- US7 (Multi-User Data Isolation) is enforced in Phase 2 via JWT auth dependency (T013) and task router ownership checks (T014), not as a separate phase
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- Backend (T009–T015) and frontend (T016–T023) foundational work can proceed in parallel
