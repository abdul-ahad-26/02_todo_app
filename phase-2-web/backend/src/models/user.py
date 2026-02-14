from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import bcrypt

if TYPE_CHECKING:
    from .task import Task

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(back_populates="user")

    def set_password(self, password: str):
        # bcrypt has a maximum password length of 72 bytes
        # We use bcrypt library directly to avoid passlib Python 3.14 issues
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password[:72].encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password[:72].encode('utf-8'),
            self.hashed_password.encode('utf-8')
        )

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: UUID
    created_at: datetime
