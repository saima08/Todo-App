"""Dismiss reminder command implementation."""

from src.lib.storage import storage
from src.lib.display import format_success


def run_dismiss(task_id: int) -> str:
    """
    Dismiss reminder for a task.

    Args:
        task_id: ID of task to dismiss reminder

    Returns:
        Success message

    Raises:
        TaskNotFoundError: If task doesn't exist
    """
    task = storage.get(task_id)
    task.dismiss_reminder()
    storage.update(task)

    return format_success(f"Reminder dismissed for Task #{task_id}")
