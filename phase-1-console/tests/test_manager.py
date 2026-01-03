"""Unit tests for TaskManager."""

import pytest

from todo.manager import TaskManager


class TestTaskManagerInitialization:
    """Tests for TaskManager initialization."""

    def test_manager_initializes_empty(self) -> None:
        """Test that manager starts with no tasks."""
        manager = TaskManager()

        assert manager._tasks == []
        assert manager._next_id == 1


class TestAddTask:
    """Tests for add_task method (US1)."""

    def test_add_task_creates_task_with_sequential_id(self) -> None:
        """Test adding a task creates it with correct fields and sequential ID."""
        manager = TaskManager()

        task = manager.add_task("Test Task", "Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

        # Add another task to verify sequential ID
        task2 = manager.add_task("Second Task", "Second Description")
        assert task2.id == 2

    def test_add_task_with_empty_description(self) -> None:
        """Test adding a task with empty description is allowed."""
        manager = TaskManager()

        task = manager.add_task("Test Task", "")

        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_with_empty_title_raises_error(self) -> None:
        """Test adding a task with empty title raises ValueError."""
        manager = TaskManager()

        with pytest.raises(ValueError, match="Title is required"):
            manager.add_task("", "Description")

    def test_add_task_with_whitespace_title_raises_error(self) -> None:
        """Test adding a task with whitespace-only title raises ValueError."""
        manager = TaskManager()

        with pytest.raises(ValueError, match="Title is required"):
            manager.add_task("   ", "Description")


class TestGetAllTasks:
    """Tests for get_all_tasks method (US2)."""

    def test_get_all_tasks_returns_all_tasks(self) -> None:
        """Test get_all_tasks returns list of all tasks."""
        manager = TaskManager()
        manager.add_task("Task 1", "Description 1")
        manager.add_task("Task 2", "Description 2")
        manager.add_task("Task 3", "Description 3")

        tasks = manager.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_get_all_tasks_on_empty_manager(self) -> None:
        """Test get_all_tasks returns empty list when no tasks exist."""
        manager = TaskManager()

        tasks = manager.get_all_tasks()

        assert tasks == []


class TestGetTaskById:
    """Tests for get_task_by_id method (US3)."""

    def test_get_task_by_id_returns_task(self) -> None:
        """Test get_task_by_id returns the correct task."""
        manager = TaskManager()
        manager.add_task("Task 1", "Description 1")
        manager.add_task("Task 2", "Description 2")

        task = manager.get_task_by_id(2)

        assert task is not None
        assert task.id == 2
        assert task.title == "Task 2"

    def test_get_task_by_id_returns_none_for_nonexistent(self) -> None:
        """Test get_task_by_id returns None for non-existent ID."""
        manager = TaskManager()
        manager.add_task("Task 1", "Description 1")

        task = manager.get_task_by_id(99)

        assert task is None


class TestToggleTaskStatus:
    """Tests for toggle_task_status method (US3)."""

    def test_toggle_incomplete_to_complete(self) -> None:
        """Test toggling task from incomplete to complete."""
        manager = TaskManager()
        manager.add_task("Test Task", "Description")

        task = manager.toggle_task_status(1)

        assert task is not None
        assert task.completed is True

    def test_toggle_complete_to_incomplete(self) -> None:
        """Test toggling task from complete to incomplete."""
        manager = TaskManager()
        task = manager.add_task("Test Task", "Description")
        task.completed = True

        toggled_task = manager.toggle_task_status(1)

        assert toggled_task is not None
        assert toggled_task.completed is False

    def test_toggle_nonexistent_returns_none(self) -> None:
        """Test toggling non-existent task returns None."""
        manager = TaskManager()

        task = manager.toggle_task_status(99)

        assert task is None


class TestUpdateTask:
    """Tests for update_task method (US4)."""

    def test_update_task_title_only(self) -> None:
        """Test updating only the title."""
        manager = TaskManager()
        manager.add_task("Original Title", "Original Description")

        task = manager.update_task(1, title="New Title")

        assert task is not None
        assert task.title == "New Title"
        assert task.description == "Original Description"

    def test_update_task_description_only(self) -> None:
        """Test updating only the description."""
        manager = TaskManager()
        manager.add_task("Original Title", "Original Description")

        task = manager.update_task(1, description="New Description")

        assert task is not None
        assert task.title == "Original Title"
        assert task.description == "New Description"

    def test_update_task_both_fields(self) -> None:
        """Test updating both title and description."""
        manager = TaskManager()
        manager.add_task("Original Title", "Original Description")

        task = manager.update_task(1, title="New Title", description="New Description")

        assert task is not None
        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_update_nonexistent_returns_none(self) -> None:
        """Test updating non-existent task returns None."""
        manager = TaskManager()

        task = manager.update_task(99, title="New Title")

        assert task is None

    def test_update_with_empty_title_raises_error(self) -> None:
        """Test updating with empty title raises ValueError."""
        manager = TaskManager()
        manager.add_task("Original Title", "Description")

        with pytest.raises(ValueError, match="Title.*empty"):
            manager.update_task(1, title="")


class TestDeleteTask:
    """Tests for delete_task method (US5)."""

    def test_delete_task_returns_true(self) -> None:
        """Test deleting existing task returns True."""
        manager = TaskManager()
        manager.add_task("Test Task", "Description")

        result = manager.delete_task(1)

        assert result is True

    def test_delete_nonexistent_returns_false(self) -> None:
        """Test deleting non-existent task returns False."""
        manager = TaskManager()

        result = manager.delete_task(99)

        assert result is False

    def test_deleted_task_not_in_get_all(self) -> None:
        """Test deleted task no longer appears in get_all_tasks."""
        manager = TaskManager()
        manager.add_task("Task 1", "Description 1")
        manager.add_task("Task 2", "Description 2")

        manager.delete_task(1)
        tasks = manager.get_all_tasks()

        assert len(tasks) == 1
        assert tasks[0].id == 2
