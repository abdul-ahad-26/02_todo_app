"""
JWT utilities for authentication and token management.
"""
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .config import settings


security = HTTPBearer()


def create_token(user_id: UUID) -> str:
    """
    Create a JWT token for the given user ID.

    Args:
        user_id: The user's UUID

    Returns:
        Encoded JWT token string
    """
    expiration = datetime.utcnow() + timedelta(
        hours=settings.jwt_expiration_hours
    )
    payload = {
        "user_id": str(user_id),
        "exp": expiration,
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return token


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token.

    Args:
        token: The JWT token string

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token is invalid or expired
    """
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm]
    )
    return payload


def verify_token(token: str) -> Optional[UUID]:
    """
    Verify a JWT token and extract the user ID.

    Args:
        token: The JWT token string

    Returns:
        User UUID if valid, None otherwise
    """
    try:
        payload = decode_token(token)
        user_id_str = payload.get("user_id")
        if user_id_str:
            return UUID(user_id_str)
        return None
    except JWTError:
        return None


def get_user_id_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """
    FastAPI dependency to extract user_id from Authorization header.

    Args:
        credentials: HTTP Bearer credentials from security

    Returns:
        User UUID

    Raises:
        HTTPException: 401 if token is invalid or missing
    """
    token = credentials.credentials
    user_id = verify_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Unauthorized",
                "message": "Invalid or expired JWT token"
            }
        )

    return user_id


# Export functions for use in tests
__all__ = [
    "create_token",
    "decode_token",
    "verify_token",
    "get_user_id_from_token",
    "security",
]
