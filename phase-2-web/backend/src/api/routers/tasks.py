"""Task router with all 6 CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.api.auth import verify_jwt_token, verify_user_access
from src.crud.task import TaskRepository
from src.db import get_session
from src.models.task import TaskCreate, TaskPublic, TaskUpdate

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get(
    "/{user_id}/tasks",
    response_model=list[TaskPublic],
    status_code=status.HTTP_200_OK,
)
def list_tasks(
    user_id: str,
    payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session),
) -> list[TaskPublic]:
    verify_user_access(user_id, payload)
    return TaskRepository.get_all_by_user(session, user_id)


@router.post(
    "/{user_id}/tasks",
    response_model=TaskPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session),
) -> TaskPublic:
    verify_user_access(user_id, payload)
    return TaskRepository.create(session, user_id, task_data)


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskPublic,
    status_code=status.HTTP_200_OK,
)
def get_task(
    user_id: str,
    task_id: str,
    payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session),
) -> TaskPublic:
    verify_user_access(user_id, payload)
    task = TaskRepository.get_by_id(session, task_id, user_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' not found.",
        )
    return task


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskPublic,
    status_code=status.HTTP_200_OK,
)
def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session),
) -> TaskPublic:
    verify_user_access(user_id, payload)
    task = TaskRepository.update(session, task_id, user_id, task_data)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' not found.",
        )
    return task


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    user_id: str,
    task_id: str,
    payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session),
) -> None:
    verify_user_access(user_id, payload)
    deleted = TaskRepository.delete(session, task_id, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' not found.",
        )


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskPublic,
    status_code=status.HTTP_200_OK,
)
def toggle_complete(
    user_id: str,
    task_id: str,
    payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session),
) -> TaskPublic:
    verify_user_access(user_id, payload)
    task = TaskRepository.toggle_complete(session, task_id, user_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' not found.",
        )
    return task
