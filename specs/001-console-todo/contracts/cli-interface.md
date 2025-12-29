# CLI Interface Contract

**Date**: 2025-12-30
**Feature**: 001-console-todo
**Component**: `cli.py`

## Overview

This document defines the user interface contract for the console application, specifying the exact menu structure, prompts, and output formats.

---

## Main Menu

### Display Format

```text
========================================
         TODO APPLICATION
========================================

Please select an option:

  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Toggle Complete/Incomplete
  6. Exit

Enter your choice (1-6): _
```

### Menu Options

| Option | Action | Next Screen |
|--------|--------|-------------|
| 1 | Add new task | Add Task flow |
| 2 | Display all tasks | Task List display |
| 3 | Update existing task | Update Task flow |
| 4 | Delete task | Delete Task flow |
| 5 | Toggle completion status | Toggle Status flow |
| 6 | Exit application | Clean exit |

### Invalid Input

```text
Error: Invalid option. Please enter a number between 1 and 6.
```

---

## Operation Flows

### 1. Add Task Flow

**Prompts**:
```text
--- Add New Task ---

Enter task title: _
Enter task description (press Enter to skip): _
```

**Success Output**:
```text
Success! Task added with ID: 1
```

**Error - Empty Title**:
```text
Error: Title is required. Task not created.
```

---

### 2. View Tasks Flow

**With Tasks**:
```text
--- Your Tasks ---

[1] [ ] Buy groceries
    Description: Milk, eggs, bread

[2] [X] Call dentist
    Description: Schedule annual checkup

[3] [ ] Review specs
    Description: (none)

Total: 3 tasks (1 completed, 2 pending)
```

**Empty State**:
```text
--- Your Tasks ---

No tasks yet. Add a task to get started!
```

---

### 3. Update Task Flow

**Prompts**:
```text
--- Update Task ---

Enter task ID to update: _
```

**If Task Found**:
```text
Current task:
  Title: Buy groceries
  Description: Milk, eggs, bread

Enter new title (press Enter to keep current): _
Enter new description (press Enter to keep current): _
```

**Success Output**:
```text
Success! Task 1 updated.
```

**Error - Task Not Found**:
```text
Error: Task with ID 99 not found.
```

**Error - Invalid ID Format**:
```text
Error: Invalid task ID. Please enter a positive number.
```

**Error - Empty Title**:
```text
Error: Title cannot be empty. Task not updated.
```

---

### 4. Delete Task Flow

**Prompts**:
```text
--- Delete Task ---

Enter task ID to delete: _
```

**Success Output**:
```text
Success! Task 1 deleted.
```

**Error - Task Not Found**:
```text
Error: Task with ID 99 not found.
```

**Error - Invalid ID Format**:
```text
Error: Invalid task ID. Please enter a positive number.
```

---

### 5. Toggle Status Flow

**Prompts**:
```text
--- Toggle Task Status ---

Enter task ID to toggle: _
```

**Success Output (Incomplete → Complete)**:
```text
Success! Task 1 marked as complete.
```

**Success Output (Complete → Incomplete)**:
```text
Success! Task 1 marked as incomplete.
```

**Error - Task Not Found**:
```text
Error: Task with ID 99 not found.
```

**Error - Invalid ID Format**:
```text
Error: Invalid task ID. Please enter a positive number.
```

---

### 6. Exit Flow

**Output**:
```text
Goodbye! Your tasks have not been saved (in-memory only).
```

---

## Keyboard Interrupt Handling

When user presses Ctrl+C:

```text

Operation cancelled. Returning to main menu...
```

At main menu:
```text

Goodbye! Your tasks have not been saved (in-memory only).
```

---

## Formatting Standards

### Status Indicators

| Status | Display |
|--------|---------|
| Incomplete | `[ ]` |
| Complete | `[X]` |

### Task Display Format

```text
[{id}] [{status}] {title}
    Description: {description or "(none)"}
```

### Message Types

| Type | Format | Example |
|------|--------|---------|
| Success | `Success! {message}` | `Success! Task added with ID: 1` |
| Error | `Error: {message}` | `Error: Task not found.` |
| Info | Plain text | `No tasks yet.` |

### Section Headers

```text
--- {Section Name} ---
```

### Separators

```text
========================================
```

---

## Return to Menu

After every operation (success or error), the application returns to the main menu automatically. No explicit "Press Enter to continue" prompt is needed.
