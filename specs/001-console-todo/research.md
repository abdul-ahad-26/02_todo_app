# Research: Phase I - In-Memory Console Todo Application

**Date**: 2025-12-30
**Feature**: 001-console-todo
**Status**: Complete

## Overview

This document captures research findings and decisions for the Phase I console Todo application. All technical context items were clearly specified in the requirements, so this research focuses on best practices and implementation patterns.

---

## Research Topics

### 1. Python CLI Best Practices

**Research Question**: What are best practices for building interactive CLI applications in Python?

**Decision**: Use a menu-driven loop with numbered options and input validation.

**Rationale**:
- Simple numbered menus are intuitive for users
- Input validation at the CLI layer prevents invalid data from reaching business logic
- Clear prompts and consistent formatting improve user experience
- Standard library `input()` function is sufficient for simple console apps

**Alternatives Considered**:
- **argparse**: Rejected - designed for command-line arguments, not interactive menus
- **click**: Rejected - external dependency, overkill for simple menu-driven app
- **prompt_toolkit**: Rejected - external dependency, unnecessary complexity

**Best Practices to Follow**:
- Use clear, consistent prompt wording
- Provide numbered menu options (1, 2, 3...) not letters
- Show current state after operations
- Handle Ctrl+C gracefully
- Use consistent formatting for task display

---

### 2. Python Data Classes vs Named Tuples

**Research Question**: What is the best way to represent the Task data model in Python 3.13+?

**Decision**: Use `@dataclass` decorator from the standard library.

**Rationale**:
- Built-in to Python 3.7+ (no external dependencies)
- Automatic `__init__`, `__repr__`, `__eq__` generation
- Type hints for IDE support and documentation
- Mutable by default (needed for status updates)
- Clear, readable code

**Alternatives Considered**:
- **Named tuples**: Rejected - immutable, harder to update fields
- **Plain classes**: Rejected - more boilerplate code
- **Pydantic models**: Rejected - external dependency
- **TypedDict**: Rejected - less structured, no method support

**Implementation Pattern**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool = False
```

---

### 3. In-Memory Storage Strategy

**Research Question**: How should tasks be stored in memory for efficient CRUD operations?

**Decision**: Use a Python list for storage with a separate counter for ID generation.

**Rationale**:
- List provides ordered iteration for display
- Linear search is acceptable for <1000 tasks (O(n) is fine)
- Simple implementation aligns with "No Premature Complexity"
- Counter ensures unique, sequential IDs

**Alternatives Considered**:
- **Dictionary by ID**: Rejected - loses insertion order (though preserved in Python 3.7+), premature optimization
- **SQLite in-memory**: Rejected - overkill, adds complexity
- **Collections.OrderedDict**: Rejected - unnecessary abstraction

**Implementation Pattern**:
```python
class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1
```

---

### 4. Input Validation Strategy

**Research Question**: Where and how should input validation occur?

**Decision**: Validate at CLI layer before calling manager methods.

**Rationale**:
- Keeps manager logic clean and focused on business rules
- CLI is the boundary between user and system
- Allows for user-friendly error messages
- Prevents invalid data from entering the system

**Validation Rules**:
| Input | Validation | Error Message |
|-------|------------|---------------|
| Title | Non-empty string | "Error: Title is required" |
| Task ID | Positive integer | "Error: Invalid task ID format" |
| Menu choice | Valid option number | "Error: Invalid option. Please try again." |

---

### 5. UV Project Configuration

**Research Question**: How should the UV project be configured for this application?

**Decision**: Minimal pyproject.toml with Python 3.13+ requirement and pytest dev dependency.

**Rationale**:
- UV uses pyproject.toml as the standard configuration
- No production dependencies needed (standard library only)
- pytest as dev dependency for testing

**Configuration Pattern**:
```toml
[project]
name = "todo"
version = "0.1.0"
description = "Phase I In-Memory Console Todo Application"
requires-python = ">=3.13"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = ["pytest>=8.0"]
```

---

### 6. Testing Approach

**Research Question**: How should the console application be tested?

**Decision**: Unit tests for models and manager, integration tests for CLI using monkeypatch.

**Rationale**:
- Unit tests verify individual components in isolation
- pytest's `monkeypatch` can mock `input()` and capture `print()` output
- Integration tests verify full user flows

**Testing Patterns**:
- **Model tests**: Direct instantiation and field access
- **Manager tests**: CRUD operations on isolated manager instance
- **CLI tests**: Use `monkeypatch.setattr('builtins.input', mock_input)` to simulate user input

---

## Summary of Decisions

| Topic | Decision | Key Reason |
|-------|----------|------------|
| CLI Pattern | Menu-driven with numbered options | Simplicity, user-friendly |
| Data Model | Python dataclass | Standard library, clean code |
| Storage | List with ID counter | Simple, sufficient for scale |
| Validation | At CLI boundary | Clean separation, good UX |
| Project Config | Minimal pyproject.toml | UV standard, no extra deps |
| Testing | pytest with monkeypatch | Standard, effective |

## Open Questions

*None - all technical decisions resolved.*

## References

- Python dataclasses documentation: https://docs.python.org/3/library/dataclasses.html
- UV documentation: https://docs.astral.sh/uv/
- pytest documentation: https://docs.pytest.org/
