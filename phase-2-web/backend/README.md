# Todo Backend (Phase 2)

FastAPI implementation for the Phase 2 Web application. This backend provides a stateless REST API with JWT authentication and SQLModel persistence.

## Prerequisites

- **Python**: 3.14+ (as per `pyproject.toml`)
- **UV**: Fast Python package manager (Required)
- **Database**: Neon (PostgreSQL) connection string

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure Environment**:
   Create a `.env` file in this directory with the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@host/dbname
   JWT_SECRET=your-secret-key
   CORS_ORIGINS=http://localhost:3000
   ```

## Running the Server

Start the development server with reload enabled:

```bash
uv run uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.
Swagger documentation can be found at `http://localhost:8000/docs`.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/)
- **Management**: [uv](https://github.com/astral-sh/uv)
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT (Stateless)

## Project Structure

- `src/`: Main source code
  - `api/`: Route handlers (Auth, Tasks)
  - `models/`: SQLModel data definitions
  - `core/`: Config and utilities
- `tests/`: Pytest suite
