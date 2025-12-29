"""Unit tests for Task model."""

import pytest

from todo.models import Task


class TestTaskCreation:
    """Tests for Task creation and field access."""

    def test_create_task_with_all_fields(self) -> None:
        """Test creating a task with all fields specified."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=True)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is True

    def test_create_task_with_defaults(self) -> None:
        """Test creating a task with default values."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_create_task_with_empty_description(self) -> None:
        """Test creating a task with empty description is allowed."""
        task = Task(id=1, title="Test Task", description="")

        assert task.description == ""

    def test_create_task_with_empty_title_raises_error(self) -> None:
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title is required"):
            Task(id=1, title="")

    def test_create_task_with_whitespace_title_raises_error(self) -> None:
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title is required"):
            Task(id=1, title="   ")
