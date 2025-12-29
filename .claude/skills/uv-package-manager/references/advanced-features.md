# UV Advanced Features Reference

## Table of Contents
- [Workspaces](#workspaces)
- [Resolution Strategies](#resolution-strategies)
- [Caching](#caching)
- [Environment Variables](#environment-variables)
- [Docker Integration](#docker-integration)
- [Lockfile Management](#lockfile-management)
- [Authentication](#authentication)

## Workspaces

Cargo-style workspaces for monorepos with multiple Python packages.

### Structure

```
my-workspace/
├── pyproject.toml       # Root workspace config
├── uv.lock              # Shared lockfile
├── packages/
│   ├── core/
│   │   ├── pyproject.toml
│   │   └── src/core/
│   ├── api/
│   │   ├── pyproject.toml
│   │   └── src/api/
│   └── cli/
│       ├── pyproject.toml
│       └── src/cli/
```

### Root pyproject.toml

```toml
[tool.uv.workspace]
members = ["packages/*"]

# Shared dependencies across workspace
[tool.uv]
dev-dependencies = ["pytest", "ruff"]
```

### Member pyproject.toml

```toml
[project]
name = "api"
dependencies = [
    "core",           # Reference workspace member
    "fastapi",
]

[tool.uv.sources]
core = { workspace = true }
```

### Workspace Commands

```bash
# Sync all workspace members
uv sync

# Run in specific package
uv run --package api pytest

# Add dep to specific package
uv add --package api uvicorn
```

## Resolution Strategies

### Override Dependencies

Force specific versions regardless of constraints:

```toml
[tool.uv]
override-dependencies = [
    "requests==2.28.0",
]
```

### Constraint Dependencies

Add upper bounds without adding to dependencies:

```toml
[tool.uv]
constraint-dependencies = [
    "numpy<2.0",
]
```

### Resolution Mode

```bash
# Lowest compatible versions (for testing)
uv lock --resolution lowest

# Lowest direct deps, highest transitive
uv lock --resolution lowest-direct
```

### Platform-Independent Resolution

```bash
# Generate universal lockfile
uv lock --universal

# Resolve for specific platform
uv lock --python-platform linux
```

## Caching

UV caches downloaded packages and metadata for speed.

### Cache Location

- Linux: `~/.cache/uv`
- macOS: `~/Library/Caches/uv`
- Windows: `%LOCALAPPDATA%\uv\cache`

### Cache Commands

```bash
# Show cache info
uv cache dir
uv cache info

# Clean cache
uv cache clean

# Clean specific package
uv cache clean requests

# Prune unused entries
uv cache prune
```

### Disable Cache

```bash
uv sync --no-cache
# or
UV_NO_CACHE=1 uv sync
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `UV_PYTHON` | Default Python version |
| `UV_INDEX_URL` | Primary package index |
| `UV_EXTRA_INDEX_URL` | Additional indexes (comma-separated) |
| `UV_CACHE_DIR` | Cache directory path |
| `UV_NO_CACHE` | Disable caching |
| `UV_SYSTEM_PYTHON` | Use system Python |
| `UV_PYTHON_PREFERENCE` | `only-managed`, `managed`, `system`, `only-system` |
| `UV_COMPILE_BYTECODE` | Compile to .pyc |
| `UV_NO_PROGRESS` | Disable progress bars |
| `UV_NATIVE_TLS` | Use system TLS |
| `UV_OFFLINE` | Offline mode |
| `UV_FROZEN` | Error if lockfile needs update |
| `UV_LOCKED` | Error if lockfile is missing |

## Docker Integration

### Minimal Dockerfile

```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (cached layer)
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

CMD ["uv", "run", "python", "-m", "myapp"]
```

### Multi-stage Build

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --compile-bytecode

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "myapp"]
```

### Using UV's Python

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
COPY . .
RUN uv sync --frozen
CMD ["uv", "run", "myapp"]
```

## Lockfile Management

### uv.lock

Cross-platform lockfile containing:
- Exact versions of all dependencies
- Package hashes for verification
- Platform-specific markers

### Commands

```bash
# Create/update lockfile
uv lock

# Upgrade all packages
uv lock --upgrade

# Upgrade specific package
uv lock --upgrade-package requests

# Check lockfile is up-to-date
uv lock --check

# Sync exactly what's in lockfile
uv sync --frozen
```

### CI Best Practices

```bash
# Fail if lockfile outdated
uv sync --locked

# Use exact lockfile versions
uv sync --frozen
```

## Authentication

### PyPI Tokens

```bash
# Environment variable
export UV_PUBLISH_TOKEN="pypi-..."
uv publish

# Or pass directly
uv publish --token "pypi-..."
```

### Private Indexes

```toml
# pyproject.toml
[tool.uv]
index-url = "https://pypi.example.com/simple"
```

```bash
# With credentials
UV_INDEX_URL="https://user:pass@pypi.example.com/simple" uv sync

# Keyring integration
uv sync --keyring-provider subprocess
```

### Git Authentication

UV uses standard git credential helpers:

```bash
# HTTPS with token
git config --global credential.helper store
echo "https://token:${GH_TOKEN}@github.com" >> ~/.git-credentials

# SSH (uses ssh-agent)
uv add git+ssh://git@github.com/org/repo
```

## Performance Tips

1. **Use `--frozen` in CI** - Skip lockfile check
2. **Layer Docker builds** - Copy lockfile before source
3. **Compile bytecode** - `uv sync --compile-bytecode`
4. **Parallel installs** - Default, no config needed
5. **Local cache in CI** - Cache `~/.cache/uv`

## Troubleshooting

### Resolution Conflicts

```bash
# Verbose output
uv lock -v

# Show resolution explanation
uv tree --why <package>
```

### Version Issues

```bash
# List available versions
uv pip index versions <package>

# Check why version selected
uv tree --package <package>
```

### Clean State

```bash
# Remove venv
rm -rf .venv

# Fresh sync
uv sync

# Or with cache clear
uv cache clean && uv sync
```
