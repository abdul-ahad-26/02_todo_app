from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    is_complete: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_complete: Optional[bool] = None


class TaskPublic(TaskBase):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
