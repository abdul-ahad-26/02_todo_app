# Better Auth FastAPI Monorepo - Backend

Backend implementation for the full-stack Todo application using FastAPI and SQLModel.

## Tech Stack
- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon (PostgreSQL)
- **Auth**: JWT (jose + passlib)

## Development
```bash
# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r deps.txt

# Run server
uvicorn main:app --reload
```

## Testing
```bash
pytest
```

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT signing
- `CORS_ORIGINS`: Allowed origins for CORS (comma-separated)
