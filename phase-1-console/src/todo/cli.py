"""CLI interface for the Todo application."""

from todo.manager import TaskManager


def display_menu() -> None:
    """Display the main menu."""
    print("=" * 40)
    print("         TODO APPLICATION")
    print("=" * 40)
    print()
    print("Please select an option:")
    print()
    print("  1. Add Task")
    print("  2. View Tasks")
    print("  3. Update Task")
    print("  4. Delete Task")
    print("  5. Toggle Complete/Incomplete")
    print("  6. Exit")
    print()


def get_menu_choice() -> str:
    """Get and validate menu choice from user."""
    return input("Enter your choice (1-6): ").strip()


def add_task_flow(manager: TaskManager) -> None:
    """Handle the Add Task flow."""
    print()
    print("--- Add New Task ---")
    print()

    title = input("Enter task title: ").strip()

    if not title:
        print()
        print("Error: Title is required. Task not created.")
        return

    description = input("Enter task description (press Enter to skip): ")

    try:
        task = manager.add_task(title, description)
        print()
        print(f"Success! Task added with ID: {task.id}")
    except ValueError as e:
        print()
        print(f"Error: {e}. Task not created.")


def view_tasks_flow(manager: TaskManager) -> None:
    """Handle the View Tasks flow."""
    print()
    print("--- Your Tasks ---")
    print()

    tasks = manager.get_all_tasks()

    if not tasks:
        print("No tasks yet. Add a task to get started!")
        return

    completed_count = 0
    pending_count = 0

    for task in tasks:
        status = "[X]" if task.completed else "[ ]"
        print(f"[{task.id}] {status} {task.title}")

        description_display = task.description if task.description else "(none)"
        print(f"    Description: {description_display}")
        print()

        if task.completed:
            completed_count += 1
        else:
            pending_count += 1

    print(f"Total: {len(tasks)} tasks ({completed_count} completed, {pending_count} pending)")


def validate_task_id(id_str: str) -> int | None:
    """Validate and convert task ID string to integer.

    Args:
        id_str: The string to validate

    Returns:
        The task ID as integer if valid, None otherwise
    """
    if not id_str.isdigit() or int(id_str) <= 0:
        return None
    return int(id_str)


def toggle_status_flow(manager: TaskManager) -> None:
    """Handle the Toggle Task Status flow."""
    print()
    print("--- Toggle Task Status ---")
    print()

    id_str = input("Enter task ID to toggle: ").strip()

    task_id = validate_task_id(id_str)
    if task_id is None:
        print()
        print("Error: Invalid task ID. Please enter a positive number.")
        return

    task = manager.toggle_task_status(task_id)

    if task is None:
        print()
        print(f"Error: Task with ID {task_id} not found.")
        return

    status_text = "complete" if task.completed else "incomplete"
    print()
    print(f"Success! Task {task_id} marked as {status_text}.")


def update_task_flow(manager: TaskManager) -> None:
    """Handle the Update Task flow."""
    print()
    print("--- Update Task ---")
    print()

    id_str = input("Enter task ID to update: ").strip()

    task_id = validate_task_id(id_str)
    if task_id is None:
        print()
        print("Error: Invalid task ID. Please enter a positive number.")
        return

    task = manager.get_task_by_id(task_id)
    if task is None:
        print()
        print(f"Error: Task with ID {task_id} not found.")
        return

    print()
    print(f"Current title: {task.title}")
    print(f"Current description: {task.description if task.description else '(none)'}")
    print()

    new_title = input("Enter new title (press Enter to keep current): ")
    new_description = input("Enter new description (press Enter to keep current): ")

    # Determine what to update
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None

    if title_to_update is None and description_to_update is None:
        print()
        print("No changes made.")
        return

    try:
        updated_task = manager.update_task(
            task_id, title=title_to_update, description=description_to_update
        )
        if updated_task:
            print()
            print(f"Success! Task {task_id} updated.")
    except ValueError as e:
        print()
        print(f"Error: {e}. Task not updated.")


def delete_task_flow(manager: TaskManager) -> None:
    """Handle the Delete Task flow."""
    print()
    print("--- Delete Task ---")
    print()

    id_str = input("Enter task ID to delete: ").strip()

    task_id = validate_task_id(id_str)
    if task_id is None:
        print()
        print("Error: Invalid task ID. Please enter a positive number.")
        return

    result = manager.delete_task(task_id)

    if not result:
        print()
        print(f"Error: Task with ID {task_id} not found.")
        return

    print()
    print(f"Success! Task {task_id} deleted.")


def main() -> None:
    """Main entry point for the CLI application."""
    manager = TaskManager()

    while True:
        try:
            display_menu()
            choice = get_menu_choice()

            if choice == "1":
                add_task_flow(manager)
            elif choice == "2":
                view_tasks_flow(manager)
            elif choice == "3":
                update_task_flow(manager)
            elif choice == "4":
                delete_task_flow(manager)
            elif choice == "5":
                toggle_status_flow(manager)
            elif choice == "6":
                print()
                print("Goodbye! Your tasks have not been saved (in-memory only).")
                break
            else:
                print()
                print("Error: Invalid option. Please enter a number between 1 and 6.")

            print()  # Add spacing before next menu

        except KeyboardInterrupt:
            print()
            print()
            print("Goodbye! Your tasks have not been saved (in-memory only).")
            break


if __name__ == "__main__":
    main()
