# Phase I - In-Memory Console Todo Application

A Python-based console Todo application for managing tasks in-memory.

## Features

- **Add Task**: Create tasks with title and description
- **View Tasks**: Display all tasks with status indicators
- **Toggle Status**: Mark tasks as complete/incomplete
- **Update Task**: Edit task title and/or description
- **Delete Task**: Permanently remove tasks

## Requirements

- Python 3.13+
- UV package manager

## Setup

```bash
cd phase-1-console
uv sync
```

## Run

```bash
uv run python -m todo.cli
```

## Test

```bash
uv run pytest -v
```

## Usage

The application presents a menu-driven interface:

```
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

Enter your choice (1-6):
```

### Task Display Format

Tasks are displayed with:
- ID number in brackets `[id]`
- Status indicator: `[ ]` for incomplete, `[X]` for complete
- Title and description

Example:
```
[1] [ ] Buy groceries
    Description: Milk, eggs, bread

[2] [X] Call dentist
    Description: Schedule annual checkup

Total: 2 tasks (1 completed, 1 pending)
```

## Notes

- All data is stored in-memory only
- Tasks are lost when the application exits
- Use Ctrl+C to exit at any time
