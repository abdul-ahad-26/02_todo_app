# Tasks: Phase I - In-Memory Console Todo Application

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/

**Tests**: Tests are included as the plan.md specifies pytest for unit and integration tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure:
- **Source code**: `phase-1-console/src/todo/`
- **Tests**: `phase-1-console/tests/`
- **Config**: `phase-1-console/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize UV project and create directory structure

- [x] T001 Create project directory structure: `phase-1-console/src/todo/` and `phase-1-console/tests/`
- [x] T002 Create `phase-1-console/pyproject.toml` with Python 3.13+ requirement and pytest dev dependency per research.md
- [x] T003 [P] Create `phase-1-console/src/todo/__init__.py` with package initialization
- [x] T004 [P] Create `phase-1-console/tests/__init__.py` for test package
- [x] T005 Run `uv sync` in `phase-1-console/` to initialize virtual environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: Task model and CLI main structure must be complete before user stories

- [x] T006 Create Task dataclass in `phase-1-console/src/todo/models.py` with id (int), title (str), description (str), completed (bool) fields per data-model.md
- [x] T007 Add title validation to Task model - raise ValueError if title is empty/whitespace per contracts/task-manager-api.md
- [x] T008 Create TaskManager class skeleton in `phase-1-console/src/todo/manager.py` with `__init__`, `_tasks` list, and `_next_id` counter
- [x] T009 Create CLI main structure in `phase-1-console/src/todo/cli.py` with main menu display, menu loop, and exit handling per contracts/cli-interface.md
- [x] T010 Implement keyboard interrupt (Ctrl+C) handling in cli.py per contracts/cli-interface.md
- [x] T011 Implement invalid menu option error handling in cli.py per contracts/cli-interface.md
- [x] T012 [P] Create `phase-1-console/tests/test_models.py` with test for Task creation and field access
- [x] T013 [P] Create `phase-1-console/tests/test_manager.py` with test for TaskManager initialization

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and description, getting unique ID and success confirmation

**Independent Test**: Run app, select "Add Task", enter title/description, verify task created with ID and "incomplete" status

### Tests for User Story 1

- [x] T014 [P] [US1] Write unit test for `add_task` method in `phase-1-console/tests/test_manager.py` - verify task created with sequential ID, title, description, completed=False
- [x] T015 [P] [US1] Write unit test for `add_task` with empty description in `phase-1-console/tests/test_manager.py`
- [x] T016 [P] [US1] Write unit test for `add_task` with empty title - expect ValueError in `phase-1-console/tests/test_manager.py`

### Implementation for User Story 1

- [x] T017 [US1] Implement `add_task(title, description)` method in `phase-1-console/src/todo/manager.py` per contracts/task-manager-api.md
- [x] T018 [US1] Implement Add Task flow in `phase-1-console/src/todo/cli.py` - prompts for title/description per contracts/cli-interface.md
- [x] T019 [US1] Add title validation in Add Task CLI flow - display "Error: Title is required" for empty title per contracts/cli-interface.md
- [x] T020 [US1] Add success message display "Success! Task added with ID: {id}" per contracts/cli-interface.md

**Checkpoint**: User Story 1 complete - can add tasks

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can view all tasks in formatted list with ID, title, description, and status

**Independent Test**: Add several tasks, select "View Tasks", verify all tasks display with correct format

### Tests for User Story 2

- [x] T021 [P] [US2] Write unit test for `get_all_tasks` method in `phase-1-console/tests/test_manager.py` - returns list of all tasks
- [x] T022 [P] [US2] Write unit test for `get_all_tasks` on empty manager - returns empty list in `phase-1-console/tests/test_manager.py`

### Implementation for User Story 2

- [x] T023 [US2] Implement `get_all_tasks()` method in `phase-1-console/src/todo/manager.py` per contracts/task-manager-api.md
- [x] T024 [US2] Implement View Tasks flow in `phase-1-console/src/todo/cli.py` - formatted list per contracts/cli-interface.md
- [x] T025 [US2] Add task display formatting with `[id] [status] title` and description per contracts/cli-interface.md
- [x] T026 [US2] Add status indicators `[ ]` for incomplete, `[X]` for complete per data-model.md
- [x] T027 [US2] Add empty state message "No tasks yet. Add a task to get started!" per contracts/cli-interface.md
- [x] T028 [US2] Add task count summary "Total: N tasks (X completed, Y pending)" per contracts/cli-interface.md

**Checkpoint**: User Stories 1 + 2 complete - core MVP (add and view tasks)

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status between complete and incomplete

**Independent Test**: Add task, toggle status to complete, verify status changed, toggle back, verify again

### Tests for User Story 3

- [x] T029 [P] [US3] Write unit test for `toggle_task_status` method - incomplete to complete in `phase-1-console/tests/test_manager.py`
- [x] T030 [P] [US3] Write unit test for `toggle_task_status` method - complete to incomplete in `phase-1-console/tests/test_manager.py`
- [x] T031 [P] [US3] Write unit test for `toggle_task_status` with non-existent ID - returns None in `phase-1-console/tests/test_manager.py`

### Implementation for User Story 3

- [x] T032 [US3] Implement `get_task_by_id(task_id)` method in `phase-1-console/src/todo/manager.py` per contracts/task-manager-api.md
- [x] T033 [US3] Implement `toggle_task_status(task_id)` method in `phase-1-console/src/todo/manager.py` per contracts/task-manager-api.md
- [x] T034 [US3] Implement Toggle Status flow in `phase-1-console/src/todo/cli.py` - prompt for task ID per contracts/cli-interface.md
- [x] T035 [US3] Add ID validation helper function in cli.py - check numeric and positive integer
- [x] T036 [US3] Add success messages "Task {id} marked as complete/incomplete" per contracts/cli-interface.md
- [x] T037 [US3] Add error handling for task not found and invalid ID format per contracts/cli-interface.md

**Checkpoint**: User Story 3 complete - can track progress by toggling status

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Users can update task title and/or description by ID

**Independent Test**: Add task, update title only, verify change; update description only, verify; update both, verify

### Tests for User Story 4

- [x] T038 [P] [US4] Write unit test for `update_task` with title only in `phase-1-console/tests/test_manager.py`
- [x] T039 [P] [US4] Write unit test for `update_task` with description only in `phase-1-console/tests/test_manager.py`
- [x] T040 [P] [US4] Write unit test for `update_task` with both title and description in `phase-1-console/tests/test_manager.py`
- [x] T041 [P] [US4] Write unit test for `update_task` with non-existent ID - returns None in `phase-1-console/tests/test_manager.py`
- [x] T042 [P] [US4] Write unit test for `update_task` with empty title - expect ValueError in `phase-1-console/tests/test_manager.py`

### Implementation for User Story 4

- [x] T043 [US4] Implement `update_task(task_id, title, description)` method in `phase-1-console/src/todo/manager.py` per contracts/task-manager-api.md
- [x] T044 [US4] Implement Update Task flow in `phase-1-console/src/todo/cli.py` - prompt for ID, show current values per contracts/cli-interface.md
- [x] T045 [US4] Add prompts for new title/description with "press Enter to keep current" per contracts/cli-interface.md
- [x] T046 [US4] Add partial update handling - only update fields that were provided per spec.md FR-010
- [x] T047 [US4] Add success message "Task {id} updated" and error handling per contracts/cli-interface.md

**Checkpoint**: User Story 4 complete - can update task details

---

## Phase 7: User Story 5 - Delete a Task (Priority: P3)

**Goal**: Users can permanently remove tasks by ID

**Independent Test**: Add task, delete by ID, verify not in task list

### Tests for User Story 5

- [x] T048 [P] [US5] Write unit test for `delete_task` method - returns True on success in `phase-1-console/tests/test_manager.py`
- [x] T049 [P] [US5] Write unit test for `delete_task` with non-existent ID - returns False in `phase-1-console/tests/test_manager.py`
- [x] T050 [P] [US5] Write unit test verifying deleted task no longer in `get_all_tasks` result in `phase-1-console/tests/test_manager.py`

### Implementation for User Story 5

- [x] T051 [US5] Implement `delete_task(task_id)` method in `phase-1-console/src/todo/manager.py` per contracts/task-manager-api.md
- [x] T052 [US5] Implement Delete Task flow in `phase-1-console/src/todo/cli.py` - prompt for task ID per contracts/cli-interface.md
- [x] T053 [US5] Add success message "Task {id} deleted" and error handling per contracts/cli-interface.md

**Checkpoint**: User Story 5 complete - can remove unwanted tasks

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cleanup, and final validation

- [x] T054 [P] Create `phase-1-console/README.md` with setup and run instructions per quickstart.md
- [x] T055 [P] Write CLI integration test in `phase-1-console/tests/test_cli.py` - test full add/view flow using monkeypatch
- [x] T056 [P] Write CLI integration test for toggle/update/delete flows in `phase-1-console/tests/test_cli.py`
- [x] T057 Run all tests with `uv run pytest -v` and verify all pass
- [x] T058 Run quickstart.md validation - verify app runs with `uv run python -m todo.cli`
- [x] T059 Manual testing: Execute all acceptance scenarios from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1 (Setup) ──────────────────────────┐
                                          ▼
Phase 2 (Foundational) ──────────┬────────┤
         │                       │        │
         │    ┌──────────────────┤        │
         │    │                  │        │
         ▼    ▼                  ▼        ▼
Phase 3 (US1) ───► Phase 4 (US2) ───► Phase 5 (US3) ───► Phase 6 (US4) ───► Phase 7 (US5)
         │                  │                  │                  │                  │
         └──────────────────┴──────────────────┴──────────────────┴──────────────────┘
                                          │
                                          ▼
                              Phase 8 (Polish)
```

### User Story Dependencies

- **US1 (Add Task)**: Depends on Foundational only - No dependencies on other stories
- **US2 (View Tasks)**: Depends on Foundational only - Can test independently (will show empty state)
- **US3 (Toggle Status)**: Depends on Foundational + requires `get_task_by_id` helper - Independently testable
- **US4 (Update Task)**: Depends on Foundational + requires `get_task_by_id` helper - Independently testable
- **US5 (Delete Task)**: Depends on Foundational only - Independently testable

**Note**: While stories can technically run in parallel after Foundational, they share files (manager.py, cli.py), so sequential execution by priority order is recommended for a single developer.

### Within Each User Story

1. Write tests FIRST - ensure they FAIL before implementation
2. Implement manager method
3. Implement CLI flow
4. Add validation and error handling
5. Verify tests pass
6. Story complete

### Parallel Opportunities

**Phase 1 Setup**:
- T003 and T004 can run in parallel (different __init__.py files)

**Phase 2 Foundational**:
- T012 and T013 can run in parallel (different test files)

**Each User Story Phase**:
- All test tasks marked [P] within a story can run in parallel
- Tests should run first, fail, then implementation proceeds

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 tests together:
Task T014: "Unit test for add_task method in tests/test_manager.py"
Task T015: "Unit test for add_task with empty description in tests/test_manager.py"
Task T016: "Unit test for add_task with empty title in tests/test_manager.py"

# Then implement sequentially:
Task T017 → T018 → T019 → T020
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Test adding and viewing tasks
6. Deploy/demo if ready - this is a functional MVP!

### Full Feature Delivery

1. Complete MVP (Phases 1-4)
2. Add Phase 5: User Story 3 (Toggle Status)
3. Add Phase 6: User Story 4 (Update Task)
4. Add Phase 7: User Story 5 (Delete Task)
5. Complete Phase 8: Polish
6. All acceptance scenarios pass

---

## Summary

| Phase | Tasks | Purpose |
|-------|-------|---------|
| Phase 1: Setup | T001-T005 (5) | Project initialization |
| Phase 2: Foundational | T006-T013 (8) | Core infrastructure |
| Phase 3: US1 Add Task | T014-T020 (7) | MVP - Add capability |
| Phase 4: US2 View Tasks | T021-T028 (8) | MVP - View capability |
| Phase 5: US3 Toggle Status | T029-T037 (9) | Progress tracking |
| Phase 6: US4 Update Task | T038-T047 (10) | Edit capability |
| Phase 7: US5 Delete Task | T048-T053 (6) | Remove capability |
| Phase 8: Polish | T054-T059 (6) | Documentation & validation |

**Total Tasks**: 59
**MVP Tasks**: 28 (Phases 1-4)
**Parallel Opportunities**: 22 tasks marked [P]

---

## Notes

- All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
- Tests are written first per TDD approach - verify they fail before implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- ID validation helper (T035) is reused across US3, US4, US5 flows
