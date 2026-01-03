# Quickstart Guide: Phase I Console Todo Application

**Date**: 2025-12-30
**Feature**: 001-console-todo

## Prerequisites

- Python 3.13 or higher
- UV package manager installed ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

## Project Setup

### 1. Navigate to Project Directory

```bash
cd phase-1-console
```

### 2. Initialize UV Environment

```bash
uv sync
```

This creates a virtual environment and installs development dependencies (pytest).

### 3. Run the Application

```bash
uv run python -m todo.cli
```

Or alternatively:

```bash
uv run python src/todo/cli.py
```

## Usage

### Main Menu

When the application starts, you'll see:

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

Enter your choice (1-6):
```

### Quick Examples

**Add a task**:
1. Select option `1`
2. Enter title: `Buy groceries`
3. Enter description: `Milk, eggs, bread`

**View all tasks**:
1. Select option `2`

**Mark task complete**:
1. Select option `5`
2. Enter task ID: `1`

**Exit**:
1. Select option `6`

## Running Tests

```bash
cd phase-1-console
uv run pytest
```

### Run with verbose output:

```bash
uv run pytest -v
```

### Run specific test file:

```bash
uv run pytest tests/test_models.py
uv run pytest tests/test_manager.py
uv run pytest tests/test_cli.py
```

## Project Structure

```text
phase-1-console/
├── src/
│   └── todo/
│       ├── __init__.py      # Package initialization
│       ├── models.py        # Task data model
│       ├── manager.py       # In-memory task manager
│       └── cli.py           # CLI interface and entry point
├── tests/
│   ├── __init__.py
│   ├── test_models.py       # Task model unit tests
│   ├── test_manager.py      # TaskManager unit tests
│   └── test_cli.py          # CLI integration tests
├── pyproject.toml           # UV project configuration
└── README.md                # Project documentation
```

## Important Notes

- **In-Memory Only**: All tasks are stored in memory. When you exit the application, all tasks are lost. This is expected behavior for Phase I.
- **Single Session**: The application is designed for single-user, single-session use.
- **No External Dependencies**: The application uses only Python standard library for production code.

## Troubleshooting

### "Python version not found"

Ensure Python 3.13+ is installed:
```bash
python --version
```

If using pyenv or similar:
```bash
pyenv install 3.13.0
pyenv local 3.13.0
```

### "UV not found"

Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### "Module not found"

Ensure you're in the `phase-1-console` directory and have run `uv sync`:
```bash
cd phase-1-console
uv sync
uv run python -m todo.cli
```
