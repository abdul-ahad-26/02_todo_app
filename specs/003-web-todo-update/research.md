# Technical Research: Phase II Web Update

## Decision 1: Monorepo Organization
**Decision**: Adopt a structured monorepo pattern with `phase-2-web/` as the root containing `/backend` and `/frontend` directories.
**Rationale**: Aligns with Constitution Section V.3 (Phase-Based Project Structure) and ensures separation of concerns between FastAPI and Next.js while keeping documentation shared.
**Alternatives Considered**: Separate repositories (too much overhead), integrated source (messy).

## Decision 2: UV Package Manager
**Decision**: Use UV as the primary package manager for Phase 2 backend with a `pyproject.toml` file.
**Rationale**: UV is mandated by Constitution Section II. It provides ultra-fast dependency resolution and reproducible builds using `uv.lock`.
**Alternatives Considered**: Pip with requirements.txt (legacy), Poetry (heavier).

## Decision 3: Modern Dark/High-Contrast Theme
**Decision**: Implement the constitution's palette using Tailwind CSS with CSS variables defined in `globals.css` at the `:root` level.
**Rationale**: Ensures 100% adherence to Constitution Section III.1-2. CSS variables allow for consistent transition across phases.
**Alternatives Considered**: Hardcoded hex values (violates DRY and maintenance principles).

## Decision 4: Stateless JWT Authentication
**Decision**: Implement shared-secret JWT validation using `python-jose` and `pydantic-settings` to load secrets from environment variables.
**Rationale**: Meets the statelessness requirement in Constitution Section IV.1.
**Alternatives Considered**: Stateful sessions (rejected per constitution).
