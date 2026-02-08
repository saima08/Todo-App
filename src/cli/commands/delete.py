"""Delete command implementation."""

from src.lib.storage import storage
from src.lib.display import format_success


def run_delete(task_id: int) -> str:
    """
    Delete a task.

    Args:
        task_id: ID of task to delete

    Returns:
        Success message confirming deletion

    Raises:
        TaskNotFoundError: If task doesn't exist
    """
    # This will raise TaskNotFoundError if task doesn't exist
    task = storage.delete(task_id)

    return format_success(f"Task #{task_id} '{task.title}' deleted")
