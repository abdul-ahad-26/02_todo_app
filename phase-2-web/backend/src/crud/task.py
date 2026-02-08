"""TaskRepository with CRUD operations."""

from datetime import datetime, timezone

from sqlmodel import Session, select

from src.models.task import Task, TaskCreate, TaskUpdate


class TaskRepository:
    @staticmethod
    def create(session: Session, user_id: str, task_data: TaskCreate) -> Task:
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_by_id(session: Session, task_id: str, user_id: str) -> Task | None:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_all_by_user(session: Session, user_id: str) -> list[Task]:
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        return list(session.exec(statement).all())

    @staticmethod
    def update(
        session: Session, task_id: str, user_id: str, task_data: TaskUpdate
    ) -> Task | None:
        task = TaskRepository.get_by_id(session, task_id, user_id)
        if task is None:
            return None
        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete(session: Session, task_id: str, user_id: str) -> bool:
        task = TaskRepository.get_by_id(session, task_id, user_id)
        if task is None:
            return False
        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_complete(session: Session, task_id: str, user_id: str) -> Task | None:
        task = TaskRepository.get_by_id(session, task_id, user_id)
        if task is None:
            return None
        task.completed = not task.completed
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
