"""Task data model for the Todo application."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """Represents a task to be tracked.

    Attributes:
        id: Unique identifier for the task (auto-generated, sequential integer)
        title: Brief name/summary of the task (required, non-empty string)
        description: Detailed information about the task (optional, can be empty)
        completed: Whether the task is done (default: False)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = field(default=False)

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title is required and cannot be empty")
