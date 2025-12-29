---
name: uv-package-manager
description: Expert guidance for UV, the ultra-fast Python package and project manager written in Rust. Use this skill when working with Python projects that use UV, managing Python dependencies, creating virtual environments, running Python scripts with inline dependencies, installing Python versions, managing development tools (uvx), or migrating from pip/poetry/pipenv to UV. Covers project initialization, dependency management, lockfiles, workspaces, tool installation, and the pip-compatible interface.
---

# UV Package Manager Skill

UV is an extremely fast Python package and project manager (10-100x faster than pip), written in Rust. It unifies functionality from pip, pip-tools, pipx, poetry, pyenv, and virtualenv.

## Installation

```bash
# macOS/Linux (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Homebrew
brew install uv

# pipx (if already installed)
pipx install uv
```

## Quick Reference

| Task | Command |
|------|---------|
| Create project | `uv init [project-name]` |
| Add dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |
| Remove dependency | `uv remove <package>` |
| Run script/command | `uv run <script.py>` or `uv run <command>` |
| Sync dependencies | `uv sync` |
| Run tool temporarily | `uvx <tool>` |
| Install tool permanently | `uv tool install <tool>` |
| Install Python version | `uv python install <version>` |
| Create venv | `uv venv` |
| Lock dependencies | `uv lock` |
| Build package | `uv build` |

## Project Management

### Initialize a Project

```bash
# Create new project directory
uv init my-project
cd my-project

# Or initialize in existing directory
uv init
```

Generated structure:
```
my-project/
├── .gitignore
├── .python-version      # Python version pin
├── .venv/               # Virtual environment (auto-created)
├── README.md
├── pyproject.toml       # Project config and dependencies
├── uv.lock              # Cross-platform lockfile
└── src/my_project/
    └── __init__.py
```

### Project Types

```bash
# Application (default) - no build system
uv init my-app

# Library with build system
uv init --lib my-lib

# Packaged application
uv init --package my-app

# With specific Python version
uv init --python 3.12 my-project
```

## Dependency Management

### Adding Dependencies

```bash
# Basic
uv add requests

# With version constraint
uv add 'requests>=2.28.0,<3.0'
uv add 'requests==2.31.0'

# Development dependency
uv add --dev pytest ruff mypy

# Optional/extra dependency
uv add --optional web fastapi uvicorn

# From git
uv add git+https://github.com/user/repo
uv add git+https://github.com/user/repo@v1.0.0

# From local path
uv add ./path/to/local/package

# Migrate from requirements.txt
uv add -r requirements.txt
```

### Removing and Upgrading

```bash
# Remove
uv remove requests

# Upgrade specific package
uv lock --upgrade-package requests

# Upgrade all
uv lock --upgrade
```

### Dependency Groups

In `pyproject.toml`:
```toml
[project]
dependencies = ["fastapi", "uvicorn"]

[project.optional-dependencies]
dev = ["pytest", "ruff"]
test = ["pytest", "pytest-cov"]

[dependency-groups]
dev = ["ruff", "mypy"]
```

```bash
# Install with extras
uv sync --extra dev

# Install dependency group
uv sync --group dev
```

## Running Commands

```bash
# Run Python script
uv run python script.py

# Run module
uv run python -m pytest

# Run any command in project environment
uv run pytest
uv run ruff check .

# Pass arguments
uv run python script.py --arg value
```

### Manual Venv Activation

```bash
# Create venv (if not exists)
uv venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

## Scripts with Inline Dependencies (PEP 723)

Create standalone scripts with embedded dependencies:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.28",
#   "rich",
# ]
# ///

import requests
from rich import print

response = requests.get("https://api.github.com")
print(response.json())
```

```bash
# Run script (auto-installs deps in isolated env)
uv run script.py

# Add dependency to script
uv add --script script.py pandas

# Lock script dependencies
uv lock --script script.py
```

## Tool Management (uvx)

Run CLI tools without installation:

```bash
# Run tool temporarily
uvx ruff check .
uvx black .
uvx pytest

# Specific version
uvx ruff@0.4.0 check .

# Different package name than command
uvx --from httpie http GET https://api.github.com

# With extras
uvx --from 'mypy[faster-cache]' mypy .

# Additional dependencies
uvx --with pytest-cov pytest
```

### Persistent Tool Installation

```bash
# Install to PATH
uv tool install ruff
uv tool install 'httpie>=3.0'

# Upgrade
uv tool upgrade ruff
uv tool upgrade --all

# List installed
uv tool list

# Uninstall
uv tool uninstall ruff
```

## Python Version Management

```bash
# Install Python version
uv python install 3.12
uv python install 3.11 3.12 3.13

# Install PyPy
uv python install pypy@3.10

# List versions
uv python list

# Pin version for project
uv python pin 3.12

# Upgrade patch version
uv python upgrade 3.12
```

UV auto-downloads Python when needed. Disable with `--no-managed-python`.

## Pip-Compatible Interface

For migration or compatibility:

```bash
# Install packages
uv pip install requests
uv pip install -r requirements.txt
uv pip install -e .

# Compile requirements
uv pip compile requirements.in -o requirements.txt

# Sync from lockfile
uv pip sync requirements.txt

# Show package info
uv pip show requests

# List installed
uv pip list
uv pip freeze

# Uninstall
uv pip uninstall requests
```

## Common Workflows

### New Project Setup

```bash
uv init my-project
cd my-project
uv add fastapi uvicorn sqlalchemy
uv add --dev pytest ruff mypy
uv run python -m pytest
```

### Migrate from pip

```bash
cd existing-project
uv init
uv add -r requirements.txt
uv add --dev -r requirements-dev.txt
rm requirements*.txt  # Optional
```

### Migrate from Poetry

```bash
cd poetry-project
uv init
# UV reads pyproject.toml dependencies automatically
uv lock
uv sync
```

### CI/CD

```bash
# Install dependencies only (no dev)
uv sync --no-dev

# With specific extras
uv sync --extra test

# Frozen install (exact versions)
uv sync --frozen
```

## Configuration

In `pyproject.toml`:

```toml
[tool.uv]
# Python version
python = "3.12"

# Index configuration
index-url = "https://pypi.org/simple"
extra-index-url = ["https://download.pytorch.org/whl/cpu"]

# Dev dependencies
dev-dependencies = ["pytest", "ruff"]
```

Environment variables:
- `UV_PYTHON` - Default Python version
- `UV_INDEX_URL` - Package index URL
- `UV_CACHE_DIR` - Cache directory

## Detailed References

For framework-specific patterns and advanced topics, see:
- `references/advanced-features.md` - Workspaces, resolution strategies, caching
