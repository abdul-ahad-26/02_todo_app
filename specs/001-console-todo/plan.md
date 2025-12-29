# Implementation Plan: Phase I - In-Memory Console Todo Application

**Branch**: `001-console-todo` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo/spec.md`

## Summary

Build a Python-based console Todo application that allows users to manage tasks (add, view, update, delete, toggle completion) with all data stored in memory. The application follows a layered architecture with Task models, an in-memory Task Manager, and a CLI interface layer, managed through UV for Python environment and dependencies.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (no external packages required)
**Storage**: In-memory data structures (Python list/dict)
**Testing**: pytest (for unit and integration tests)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows with terminal)
**Project Type**: Single project (console application)
**Performance Goals**: Interactive response (<100ms for all operations)
**Constraints**: No persistence, no external dependencies beyond standard library
**Scale/Scope**: Single user, single session, <1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I.1 Spec-Driven Development** | ✅ PASS | Following Constitution → Specify → Plan → Tasks → Implement workflow |
| **I.2 AI-First Development** | ✅ PASS | Claude Code as implementation agent, human as architect |
| **I.3 Deterministic Process** | ✅ PASS | All implementation traces to tasks, tasks trace to spec |
| **II.1 Progressive Evolution** | ✅ PASS | Phase I is isolated, minimal scope |
| **II.2 Phase Isolation** | ✅ PASS | No cross-phase assumptions, Phase I is standalone |
| **II.3 No Premature Complexity** | ✅ PASS | Standard library only, simple layered architecture |
| **III.1 UI Consistency** | ✅ PASS | Consistent CLI prompts, formatting, status indicators specified |
| **III.2 Predictable Interaction** | ✅ PASS | Menu-driven flow, consistent behavior patterns |
| **III.3 Accessibility & Clarity** | ✅ PASS | Clear prompts, unambiguous messages |
| **V.1 Clarity Over Cleverness** | ✅ PASS | Simple module structure, no abstractions |
| **V.2 Single Responsibility** | ✅ PASS | models.py, manager.py, cli.py each have one purpose |
| **V.3 Loose Coupling** | ✅ PASS | CLI → Manager → Models with clear interfaces |
| **VI Quality & Reliability** | ✅ PASS | Error handling, input validation, no silent failures |

**Gate Status**: ✅ ALL GATES PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (internal API contracts)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
phase-1-console/
├── src/
│   └── todo/
│       ├── __init__.py      # Package initialization
│       ├── models.py        # Task data model
│       ├── manager.py       # In-memory task manager
│       └── cli.py           # CLI interface and main loop
├── tests/
│   ├── __init__.py
│   ├── test_models.py       # Unit tests for Task model
│   ├── test_manager.py      # Unit tests for TaskManager
│   └── test_cli.py          # Integration tests for CLI
├── pyproject.toml           # UV/Python project configuration
└── README.md                # Setup and run instructions
```

**Structure Decision**: Single project structure with source code in `phase-1-console/src/todo/` following the user-provided layout. Tests mirror source structure under `phase-1-console/tests/`.

## Component Design

### 1. Task Model (`models.py`)

**Responsibility**: Define the Task data structure with fields and validation.

- Fields: id (int), title (str), description (str), completed (bool)
- Validation: title must be non-empty
- Immutable ID once created

### 2. Task Manager (`manager.py`)

**Responsibility**: Maintain in-memory task collection and provide CRUD operations.

- Internal storage: Python list of Task objects
- ID generation: Sequential counter, not reused after deletion
- Operations: add, get_all, get_by_id, update, delete, toggle_status

### 3. CLI Interface (`cli.py`)

**Responsibility**: Handle user interaction, input validation, and output formatting.

- Main menu loop with numbered options
- Input prompts with validation
- Formatted task display with consistent status indicators
- Error and success message display
- Clean exit handling

## Data Flow

```text
User Input (keyboard)
    │
    ▼
┌─────────────────┐
│   CLI Layer     │  ← Input validation, formatting
│   (cli.py)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Task Manager   │  ← Business logic, state management
│  (manager.py)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Task Model    │  ← Data structure, validation rules
│  (models.py)    │
└─────────────────┘
         │
         ▼
    In-Memory State (Python list)
         │
         ▼
    CLI Output (terminal)
```

## Complexity Tracking

> No violations detected - no justification needed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *N/A* | *N/A* |

## Error Handling Strategy

| Error Type | Layer | Handling |
|------------|-------|----------|
| Empty title | CLI | Display error, re-prompt |
| Invalid ID format | CLI | Display error, re-prompt |
| Task not found | Manager → CLI | Return None/raise, display error |
| Invalid menu option | CLI | Display error, re-prompt |
| Keyboard interrupt | CLI | Clean exit with message |

## Testing Strategy

| Test Type | Scope | Examples |
|-----------|-------|----------|
| Unit | models.py | Task creation, validation, field access |
| Unit | manager.py | Add/get/update/delete/toggle operations |
| Integration | cli.py | Full user flows with simulated input |

## Dependencies

- **Runtime**: Python 3.13+
- **Development**: UV (package manager), pytest (testing)
- **No external packages**: Standard library only for production code
