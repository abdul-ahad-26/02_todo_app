from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    is_complete: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="tasks")

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_complete: Optional[bool] = None

class TaskPublic(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
