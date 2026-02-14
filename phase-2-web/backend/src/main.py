"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from sqlmodel import SQLModel

from src.config import get_settings
from src.db import engine
from src.api.routers.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    SQLModel.metadata.create_all(engine)
    yield


settings = get_settings()

app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application Backend",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(OperationalError)
async def database_error_handler(
    request: Request, exc: OperationalError
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable. Please try again later."},
    )


app.include_router(tasks_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
