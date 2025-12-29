"""Task Manager for in-memory task storage and operations."""

from todo.models import Task


class TaskManager:
    """Manages in-memory task collection with CRUD operations.

    Provides add, get, update, delete, and toggle operations for tasks.
    All data is stored in memory and lost when the program exits.
    """

    def __init__(self) -> None:
        """Initialize an empty task manager."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create a new task and add it to the collection.

        Args:
            title: Task title (must be non-empty)
            description: Task description (default: "")

        Returns:
            The newly created task with assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        # Task model validates title in __post_init__
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks in the collection.

        Returns:
            List of all tasks (may be empty), ordered by creation time
        """
        return list(self._tasks)

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Find a task by its ID.

        Args:
            task_id: The task ID to find

        Returns:
            The task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def toggle_task_status(self, task_id: int) -> Task | None:
        """Toggle a task's completion status.

        Args:
            task_id: The task ID to toggle

        Returns:
            The updated task, or None if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None
        task.completed = not task.completed
        return task

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Task | None:
        """Update a task's title and/or description.

        Args:
            task_id: The task ID to update
            title: New title (optional, None means keep current)
            description: New description (optional, None means keep current)

        Returns:
            The updated task, or None if not found

        Raises:
            ValueError: If title is provided but empty/whitespace
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return None

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title

        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            True if task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True
