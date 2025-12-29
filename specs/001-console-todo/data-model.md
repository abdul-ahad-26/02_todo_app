# Data Model: Phase I - In-Memory Console Todo Application

**Date**: 2025-12-30
**Feature**: 001-console-todo
**Status**: Complete

## Overview

This document defines the data model for the Phase I console Todo application. The model is intentionally simple, consisting of a single entity (Task) stored in memory.

---

## Entities

### Task

The core entity representing an item to be tracked.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `int` | Required, unique, auto-generated, immutable | Unique identifier for the task |
| `title` | `str` | Required, non-empty | Brief name/summary of the task |
| `description` | `str` | Optional (can be empty) | Detailed information about the task |
| `completed` | `bool` | Required, default: `False` | Whether the task is done |

#### Field Details

**id**
- Auto-generated sequential integer starting at 1
- Never reused after deletion
- Immutable once assigned
- Example values: 1, 2, 3, ...

**title**
- User-provided string
- Must be non-empty (whitespace-only is invalid)
- No maximum length constraint (in-memory storage)
- Supports all UTF-8 characters including special characters
- Example: "Buy groceries", "Call dentist"

**description**
- User-provided string
- Can be empty string
- No maximum length constraint
- Supports all UTF-8 characters
- Example: "Milk, eggs, bread", ""

**completed**
- Boolean flag
- Default value: `False` (incomplete)
- Can be toggled between `True` and `False`
- Display: `True` → "[X]", `False` → "[ ]"

---

## State Transitions

### Task Lifecycle

```text
┌──────────────┐
│   Created    │  ← Task added with completed=False
│  (Incomplete)│
└──────┬───────┘
       │
       │ toggle_status()
       ▼
┌──────────────┐
│  Completed   │  ← completed=True
│    [X]       │
└──────┬───────┘
       │
       │ toggle_status()
       ▼
┌──────────────┐
│  Incomplete  │  ← completed=False
│    [ ]       │
└──────────────┘
       │
       │ delete()
       ▼
┌──────────────┐
│   Deleted    │  ← Removed from memory
│  (Terminal)  │
└──────────────┘
```

### Valid Operations by State

| Current State | Valid Operations |
|---------------|------------------|
| Incomplete | View, Update, Toggle (→Complete), Delete |
| Complete | View, Update, Toggle (→Incomplete), Delete |
| Deleted | None (task no longer exists) |

---

## Validation Rules

### Creation Validation

| Rule | Condition | Error |
|------|-----------|-------|
| Title required | `title.strip() != ""` | "Error: Title is required" |

### Update Validation

| Rule | Condition | Error |
|------|-----------|-------|
| Task exists | `task_id in tasks` | "Error: Task not found" |
| Title not empty (if provided) | `new_title.strip() != ""` | "Error: Title cannot be empty" |

### ID Validation

| Rule | Condition | Error |
|------|-----------|-------|
| Valid format | `id.isdigit() and int(id) > 0` | "Error: Invalid task ID format" |
| Task exists | `task_id in tasks` | "Error: Task not found" |

---

## Storage Structure

### In-Memory Representation

```python
# Task storage
tasks: list[Task] = []

# ID generation
next_id: int = 1
```

### Example State

```python
# After adding 3 tasks, deleting task 2:
tasks = [
    Task(id=1, title="Buy groceries", description="Milk, eggs", completed=False),
    Task(id=3, title="Call dentist", description="", completed=True),
]
next_id = 4  # Next task will have ID 4 (ID 2 not reused)
```

---

## Display Format

### Task List Display

```text
=== Your Tasks ===

[1] [ ] Buy groceries
    Description: Milk, eggs, bread

[2] [X] Call dentist
    Description: (none)

[3] [ ] Review specs
    Description: Check all requirements are met
```

### Status Indicators

| Status | Display |
|--------|---------|
| Incomplete | `[ ]` |
| Complete | `[X]` |

### Empty State

```text
=== Your Tasks ===

No tasks yet. Add a task to get started!
```

---

## Relationships

This Phase I model has no relationships - Task is a standalone entity with no foreign keys or references to other entities.

Future phases may introduce:
- User → Task (ownership)
- Category → Task (classification)
- Task → Task (subtasks/dependencies)

These are explicitly out of scope for Phase I per the specification.
