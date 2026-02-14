"""Application settings loaded from environment variables."""

import os
from dataclasses import dataclass, field
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes")


def _parse_origins(value: str) -> list[str]:
    return [origin.strip() for origin in value.split(",") if origin.strip()]


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str = field(default_factory=lambda: os.environ["DATABASE_URL"])
    BETTER_AUTH_SECRET: str = field(
        default_factory=lambda: os.environ["BETTER_AUTH_SECRET"]
    )
    BETTER_AUTH_URL: str = field(
        default_factory=lambda: os.environ.get(
            "BETTER_AUTH_URL", "http://localhost:3000"
        )
    )
    ALLOWED_ORIGINS: list[str] = field(
        default_factory=lambda: _parse_origins(
            os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000")
        )
    )
    DEBUG: bool = field(
        default_factory=lambda: _parse_bool(os.environ.get("DEBUG", "false"))
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
