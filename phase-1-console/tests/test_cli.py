"""Integration tests for CLI flows."""

import pytest

from todo.cli import (
    add_task_flow,
    view_tasks_flow,
    toggle_status_flow,
    update_task_flow,
    delete_task_flow,
    validate_task_id,
)
from todo.manager import TaskManager


class TestAddViewFlow:
    """Integration tests for Add and View task flows."""

    def test_add_task_flow_success(self, monkeypatch, capsys) -> None:
        """Test adding a task through CLI flow."""
        manager = TaskManager()
        inputs = iter(["Test Task", "Test Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        add_task_flow(manager)

        captured = capsys.readouterr()
        assert "Success! Task added with ID: 1" in captured.out
        assert len(manager.get_all_tasks()) == 1

    def test_add_task_flow_empty_title_error(self, monkeypatch, capsys) -> None:
        """Test adding a task with empty title shows error."""
        manager = TaskManager()
        inputs = iter(["", "Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        add_task_flow(manager)

        captured = capsys.readouterr()
        assert "Error: Title is required" in captured.out
        assert len(manager.get_all_tasks()) == 0

    def test_view_tasks_flow_with_tasks(self, capsys) -> None:
        """Test viewing tasks displays formatted list."""
        manager = TaskManager()
        manager.add_task("Task 1", "Description 1")
        manager.add_task("Task 2", "Description 2")

        view_tasks_flow(manager)

        captured = capsys.readouterr()
        assert "[1] [ ] Task 1" in captured.out
        assert "[2] [ ] Task 2" in captured.out
        assert "Total: 2 tasks (0 completed, 2 pending)" in captured.out

    def test_view_tasks_flow_empty(self, capsys) -> None:
        """Test viewing tasks when empty shows message."""
        manager = TaskManager()

        view_tasks_flow(manager)

        captured = capsys.readouterr()
        assert "No tasks yet. Add a task to get started!" in captured.out

    def test_full_add_view_flow(self, monkeypatch, capsys) -> None:
        """Test complete add then view flow."""
        manager = TaskManager()

        # Add first task
        inputs = iter(["Buy groceries", "Milk and eggs"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task_flow(manager)

        # Add second task
        inputs = iter(["Call dentist", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task_flow(manager)

        # View tasks
        view_tasks_flow(manager)

        captured = capsys.readouterr()
        assert "Buy groceries" in captured.out
        assert "Call dentist" in captured.out
        assert "Total: 2 tasks" in captured.out


class TestToggleUpdateDeleteFlows:
    """Integration tests for Toggle, Update, and Delete flows."""

    def test_toggle_status_flow_success(self, monkeypatch, capsys) -> None:
        """Test toggling task status through CLI flow."""
        manager = TaskManager()
        manager.add_task("Test Task", "Description")
        monkeypatch.setattr("builtins.input", lambda _: "1")

        toggle_status_flow(manager)

        captured = capsys.readouterr()
        assert "Task 1 marked as complete" in captured.out
        assert manager.get_task_by_id(1).completed is True

    def test_toggle_status_flow_invalid_id(self, monkeypatch, capsys) -> None:
        """Test toggling with invalid ID shows error."""
        manager = TaskManager()
        monkeypatch.setattr("builtins.input", lambda _: "abc")

        toggle_status_flow(manager)

        captured = capsys.readouterr()
        assert "Invalid task ID" in captured.out

    def test_toggle_status_flow_nonexistent(self, monkeypatch, capsys) -> None:
        """Test toggling nonexistent task shows error."""
        manager = TaskManager()
        monkeypatch.setattr("builtins.input", lambda _: "99")

        toggle_status_flow(manager)

        captured = capsys.readouterr()
        assert "Task with ID 99 not found" in captured.out

    def test_update_task_flow_title_only(self, monkeypatch, capsys) -> None:
        """Test updating only task title through CLI flow."""
        manager = TaskManager()
        manager.add_task("Original Title", "Original Description")
        inputs = iter(["1", "New Title", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_flow(manager)

        captured = capsys.readouterr()
        assert "Task 1 updated" in captured.out
        task = manager.get_task_by_id(1)
        assert task.title == "New Title"
        assert task.description == "Original Description"

    def test_update_task_flow_both_fields(self, monkeypatch, capsys) -> None:
        """Test updating both title and description."""
        manager = TaskManager()
        manager.add_task("Original Title", "Original Description")
        inputs = iter(["1", "New Title", "New Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_flow(manager)

        captured = capsys.readouterr()
        assert "Task 1 updated" in captured.out
        task = manager.get_task_by_id(1)
        assert task.title == "New Title"
        assert task.description == "New Description"

    def test_update_task_flow_no_changes(self, monkeypatch, capsys) -> None:
        """Test updating with no changes shows message."""
        manager = TaskManager()
        manager.add_task("Original Title", "Original Description")
        inputs = iter(["1", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_flow(manager)

        captured = capsys.readouterr()
        assert "No changes made" in captured.out

    def test_update_task_flow_nonexistent(self, monkeypatch, capsys) -> None:
        """Test updating nonexistent task shows error."""
        manager = TaskManager()
        monkeypatch.setattr("builtins.input", lambda _: "99")

        update_task_flow(manager)

        captured = capsys.readouterr()
        assert "Task with ID 99 not found" in captured.out

    def test_delete_task_flow_success(self, monkeypatch, capsys) -> None:
        """Test deleting a task through CLI flow."""
        manager = TaskManager()
        manager.add_task("Test Task", "Description")
        monkeypatch.setattr("builtins.input", lambda _: "1")

        delete_task_flow(manager)

        captured = capsys.readouterr()
        assert "Task 1 deleted" in captured.out
        assert len(manager.get_all_tasks()) == 0

    def test_delete_task_flow_nonexistent(self, monkeypatch, capsys) -> None:
        """Test deleting nonexistent task shows error."""
        manager = TaskManager()
        monkeypatch.setattr("builtins.input", lambda _: "99")

        delete_task_flow(manager)

        captured = capsys.readouterr()
        assert "Task with ID 99 not found" in captured.out


class TestValidateTaskId:
    """Tests for validate_task_id helper."""

    def test_valid_positive_integer(self) -> None:
        """Test valid positive integer returns integer."""
        assert validate_task_id("1") == 1
        assert validate_task_id("42") == 42

    def test_zero_returns_none(self) -> None:
        """Test zero returns None."""
        assert validate_task_id("0") is None

    def test_negative_returns_none(self) -> None:
        """Test negative number returns None."""
        assert validate_task_id("-1") is None

    def test_non_numeric_returns_none(self) -> None:
        """Test non-numeric string returns None."""
        assert validate_task_id("abc") is None
        assert validate_task_id("") is None
        assert validate_task_id("1.5") is None
