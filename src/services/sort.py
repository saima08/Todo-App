"""Sort service for task sorting by various criteria."""

from datetime import date
from typing import Optional

from src.models.task import Task, Priority


# Priority sort order (high to low)
PRIORITY_ORDER = {
    Priority.HIGH: 0,
    Priority.MEDIUM: 1,
    Priority.LOW: 2,
    None: 3,  # No priority sorts last
}


def sort_tasks(
    tasks: list[Task],
    sort_by: str = "id",
    order: str = "asc",
) -> list[Task]:
    """
    Sort tasks by specified field.

    Uses secondary sort by ID for stable ordering when primary values are identical.

    Args:
        tasks: List of tasks to sort
        sort_by: Field to sort by (id/title/priority/due)
        order: Sort order (asc/desc)

    Returns:
        Sorted list of tasks
    """
    reverse = order == "desc"

    def sort_key(task: Task):
        """Generate sort key based on sort_by field."""
        if sort_by == "id":
            return (task.id,)
        elif sort_by == "title":
            # Secondary sort by ID for stability
            return (task.title.lower(), task.id)
        elif sort_by == "priority":
            # Priority order: high (0) < medium (1) < low (2) < none (3)
            # Secondary sort by ID for stability
            priority_val = PRIORITY_ORDER.get(task.priority, 3)
            return (priority_val, task.id)
        elif sort_by == "due":
            # Tasks without due date sort last
            # Secondary sort by ID for stability
            if task.due_date is None:
                return (date.max, task.id)
            return (task.due_date, task.id)
        else:
            return (task.id,)

    return sorted(tasks, key=sort_key, reverse=reverse)
