# Task Manager Internal API Contract

**Date**: 2025-12-30
**Feature**: 001-console-todo
**Component**: `manager.py`

## Overview

This document defines the internal API contract for the TaskManager class. This is not a REST API but an internal Python interface contract that the CLI layer uses to interact with task data.

---

## TaskManager Class

### Constructor

```python
def __init__(self) -> None
```

Initializes an empty task manager with no tasks and ID counter at 1.

**Post-conditions**:
- `get_all()` returns empty list
- Next created task will have ID 1

---

## Operations

### add_task

```python
def add_task(self, title: str, description: str = "") -> Task
```

Creates a new task and adds it to the collection.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| title | str | Yes | Task title (must be non-empty) |
| description | str | No | Task description (default: "") |

**Returns**: `Task` - The newly created task with assigned ID

**Pre-conditions**:
- `title.strip()` is non-empty

**Post-conditions**:
- New task exists in collection
- Task has unique sequential ID
- Task `completed` is `False`
- ID counter incremented

**Errors**:
- `ValueError` if title is empty or whitespace-only

**Example**:
```python
task = manager.add_task("Buy groceries", "Milk, eggs")
# Returns: Task(id=1, title="Buy groceries", description="Milk, eggs", completed=False)
```

---

### get_all_tasks

```python
def get_all_tasks(self) -> list[Task]
```

Returns all tasks in the collection.

**Parameters**: None

**Returns**: `list[Task]` - List of all tasks (may be empty)

**Post-conditions**:
- Returns copy or view, not internal reference
- Order: by creation time (oldest first)

**Example**:
```python
tasks = manager.get_all_tasks()
# Returns: [Task(id=1, ...), Task(id=2, ...)]
```

---

### get_task_by_id

```python
def get_task_by_id(self, task_id: int) -> Task | None
```

Finds a task by its ID.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | int | Yes | The task ID to find |

**Returns**: `Task | None` - The task if found, None otherwise

**Example**:
```python
task = manager.get_task_by_id(1)
# Returns: Task(id=1, ...) or None
```

---

### update_task

```python
def update_task(self, task_id: int, title: str | None = None, description: str | None = None) -> Task | None
```

Updates a task's title and/or description.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | int | Yes | The task ID to update |
| title | str \| None | No | New title (None = keep current) |
| description | str \| None | No | New description (None = keep current) |

**Returns**: `Task | None` - The updated task, or None if not found

**Pre-conditions**:
- If title provided, `title.strip()` must be non-empty

**Post-conditions**:
- Only specified fields are updated
- Unspecified fields retain original values
- ID and completed status unchanged

**Errors**:
- `ValueError` if title is provided but empty/whitespace-only

**Example**:
```python
task = manager.update_task(1, title="Updated title")
# Updates only title, keeps description
```

---

### delete_task

```python
def delete_task(self, task_id: int) -> bool
```

Removes a task from the collection.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | int | Yes | The task ID to delete |

**Returns**: `bool` - True if deleted, False if not found

**Post-conditions**:
- Task no longer in collection
- ID will not be reused

**Example**:
```python
success = manager.delete_task(1)
# Returns: True if task existed, False otherwise
```

---

### toggle_task_status

```python
def toggle_task_status(self, task_id: int) -> Task | None
```

Toggles a task's completion status.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | int | Yes | The task ID to toggle |

**Returns**: `Task | None` - The updated task, or None if not found

**Post-conditions**:
- If was `completed=False`, now `completed=True`
- If was `completed=True`, now `completed=False`

**Example**:
```python
task = manager.toggle_task_status(1)
# Toggles completed: False → True or True → False
```

---

## Error Handling Summary

| Method | Error Condition | Behavior |
|--------|-----------------|----------|
| add_task | Empty title | Raise `ValueError` |
| get_task_by_id | Not found | Return `None` |
| update_task | Not found | Return `None` |
| update_task | Empty title provided | Raise `ValueError` |
| delete_task | Not found | Return `False` |
| toggle_task_status | Not found | Return `None` |

---

## Thread Safety

This implementation is NOT thread-safe. It is designed for single-user, single-process operation as specified in the requirements.
