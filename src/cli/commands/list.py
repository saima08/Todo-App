"""List command implementation."""

from typing import Optional

from src.models.task import Task, Priority, Category
from src.lib.storage import storage
from src.lib.display import format_task_list, format_count
from src.services.filter import filter_tasks
from src.services.sort import sort_tasks


def run_list(
    status: str = "all",
    priority: Optional[str] = None,
    category: Optional[str] = None,
    sort: str = "id",
    order: str = "asc",
) -> str:
    """
    List tasks with optional filtering and sorting.

    Args:
        status: Filter by completion status (complete/incomplete/all)
        priority: Filter by priority level
        category: Filter by category
        sort: Sort field (id/title/priority/due)
        order: Sort order (asc/desc)

    Returns:
        Formatted task list
    """
    tasks = storage.get_all()

    if not tasks:
        return "No tasks found. Use 'todo add' to create your first task."

    # Apply filters
    tasks = filter_tasks(
        tasks,
        status=status,
        priority=priority,
        category=category,
    )

    if not tasks:
        # Build filter description
        filters = []
        if status != "all":
            filters.append(f"status={status}")
        if priority:
            filters.append(f"priority={priority}")
        if category:
            filters.append(f"category={category}")
        filter_desc = ", ".join(filters) if filters else "current filters"
        return f"No tasks match {filter_desc}."

    # Apply sorting
    tasks = sort_tasks(tasks, sort_by=sort, order=order)

    # Build title based on filters
    title = "Tasks"
    if status == "complete":
        title = "Completed Tasks"
    elif status == "incomplete":
        title = "Incomplete Tasks"

    return format_task_list(tasks, title)
