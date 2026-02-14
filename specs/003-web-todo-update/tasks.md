# Tasks: Phase II Web Update (Constitution Alignment)

**Input**: Design documents from `/specs/003-web-todo-update/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and constitution alignment

- [x] T001 Create `phase-2-web/` directory structure per implementation plan
- [x] T002 Initialize Python backend with UV: `uv init phase-2-web/backend`
- [x] T003 Initialize Next.js frontend: `npx create-next-app@latest phase-2-web/frontend --typescript --tailwind --app`
- [x] T004 [P] Configure `phase-2-web/backend/pyproject.toml` with FastAPI and SQLModel dependencies
- [x] T005 [P] Setup `phase-2-web/frontend/app/globals.css` with CSS variables from constitution

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user stories

- [x] T006 Setup database connection in `phase-2-web/backend/src/db.py` using Neon PostgreSQL string
- [x] T007 Implement stateless JWT verification logic in `phase-2-web/backend/src/auth.py`
- [x] T008 [P] Configure environment variable loading with `pydantic-settings` in `phase-2-web/backend/src/config.py`
- [x] T009 [P] Extend Tailwind theme in `phase-2-web/frontend/tailwind.config.js` to use CSS variables
- [x] T010 Setup API routing and CORS middleware in `phase-2-web/backend/src/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Registration with Modern UI (Priority: P1) 🎯 MVP

**Goal**: Enable secure signup with brand-aligned UI

**Independent Test**: Verify signup page reflects High-Contrast theme and successfully creates a user record via API.

- [x] T011 [P] [US1] Create User model in `phase-2-web/backend/src/models/user.py`
- [x] T012 [US1] Implement `/api/auth/signup` endpoint in `phase-2-web/backend/src/api/auth.py`
- [x] T013 [US1] Create Registration page in `phase-2-web/frontend/app/signup/page.tsx`
- [x] T014 [US1] Style Signup components using `--background` and `--foreground` variables
- [x] T015 [US1] Integrate Signup page with backend API using `Better Auth` pattern

---

## Phase 4: User Story 2 - Task Management in Dedicated Folders (Priority: P1)

**Goal**: Core task operations within the new directory structure

**Independent Test**: Verify Task CRUD operations work correctly when code is resides in `phase-2-web/`.

- [x] T016 [P] [US2] Create Task model in `phase-2-web/backend/src/models/task.py`
- [x] T017 [US2] Implement Task CRUD endpoints in `phase-2-web/backend/src/api/tasks.py`
- [x] T018 [US2] Create Tasks list page in `phase-2-web/frontend/app/tasks/page.tsx`
- [x] T019 [US2] Implement Task Card component with `--primary` and `--secondary` accent colors
- [x] T020 [US2] Handle task state (completion toggle) in `phase-2-web/frontend/lib/api-client.ts`

---

## Phase 5: User Story 3 - Python Project Management via UV (Priority: P1)

**Goal**: Ensure ultra-fast, reproducible builds for the backend

**Independent Test**: Run `uv sync` from `phase-2-web/backend/` and verify successful dependency locking.

- [x] T021 [US3] Generate `phase-2-web/backend/uv.lock` by running `uv sync`
- [x] T022 [US3] Add `uv run` scripts to `pyproject.toml` for common dev commands (start, test)
- [x] T023 [US3] Verify Python 3.13+ requirement is enforced in `pyproject.toml`

---

## Phase N: Polish & Cross-Cutting Concerns

- [x] T024 [P] Run `quickstart.md` validation to ensure setup works end-to-end
- [x] T025 [P] Audit all Next.js components for CSS variable consistency
- [x] T026 Final review of folder structure alignment with Constitution Section V.3

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** → **Foundational (Phase 2)**.
2. **Foundational** blocks all **User Stories**.
3. **User Stories (US1, US2, US3)** can run in parallel after Foundation is complete.
4. **Polish** runs after all User Stories are verified.

## Parallel Execution Examples

```bash
# Setup parallel tasks
T004 [P] backend dependencies & T005 [P] frontend CSS variables

# Foundational parallel tasks
T008 [P] backend config & T009 [P] tailwind theme update
```

## Implementation Strategy

### MVP First (User Story 1 - Secure Layout)
1. Complete T001-T010 (Setup + Foundation).
2. Complete T011-T015 (User Story 1).
3. **Validate**: Page load shows correct colors; user creation works.
