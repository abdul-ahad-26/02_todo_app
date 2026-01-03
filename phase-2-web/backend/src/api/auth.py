from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session
from ..models import User, UserCreate, UserPublic
from ..auth import create_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def signup(user_data: UserCreate, session: Session = Depends(get_session)) -> UserPublic:
    """
    Register a new user.
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Bad Request",
                "message": "Email already registered"
            }
        )

    # Create new user
    user = User(email=user_data.email)
    user.set_password(user_data.password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.post("/signin")
def signin(user_data: UserCreate, session: Session = Depends(get_session)) -> dict:
    """
    Sign in existing user.
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if not user or not user.verify_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Unauthorized",
                "message": "Invalid email or password"
            }
        )

    # Create and return JWT token
    token = create_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserPublic(id=user.id, email=user.email, created_at=user.created_at)
    }
