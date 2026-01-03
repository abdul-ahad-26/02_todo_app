# Evolution of Todo - Phase 2 Web

This directory contains the full-stack web implementation of the Todo application, featuring a FastAPI backend and a Next.js frontend.

## Structure

- `/backend`: FastAPI service using Python 3.13+, managed with `uv`.
- `/frontend`: Next.js 16+ application styled with the project's high-contrast dark theme.

## Quick Start

To run the entire Phase 2 application, you need to start both the backend and the frontend.

1. **Backend**: Navigate to `backend/` and follow the instructions in [backend/README.md](./backend/README.md).
2. **Frontend**: Navigate to `frontend/` and follow the instructions in [frontend/README.md](./frontend/README.md).

## Key Features

- **Auth**: Secure JWT-based authentication via Better Auth patterns.
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM.
- **UI**: Modern Dark/High-Contrast theme using CSS variables.
- **Tooling**: `uv` for ultra-fast Python dependency management.

## Project Guidelines

This project follows **Spec-Driven Development (SDD)** and the **Project Constitution**. Architecture decisions and specifications can be found in `specs/003-web-todo-update/`.
