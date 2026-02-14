from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..db import get_session
from ..models import Task, TaskCreate, TaskPublic, TaskUpdate
from ..auth import get_user_id_from_token

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=List[TaskPublic])
def list_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_user_id_from_token)
) -> List[TaskPublic]:
    """
    List all tasks for the authenticated user.
    """
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskPublic)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_user_id_from_token)
) -> TaskPublic:
    """
    Create a new task for the authenticated user.
    """
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )

    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskPublic)
def get_task(
    task_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_user_id_from_token)
) -> TaskPublic:
    """
    Get a specific task by ID.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_user_id_from_token)
) -> TaskPublic:
    """
    Update an existing task.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Partial update
    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.is_complete is not None:
        task.is_complete = task_data.is_complete

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.patch("/{task_id}/complete", response_model=TaskPublic)
def toggle_complete(
    task_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_user_id_from_token)
) -> TaskPublic:
    """
    Toggle task completion status.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.is_complete = not task.is_complete
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_user_id_from_token)
) -> dict:
    """
    Delete a task.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
