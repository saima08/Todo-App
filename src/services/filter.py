"""Filter service for task filtering by various criteria."""

from typing import Optional

from src.models.task import Task, Priority, Category


def filter_tasks(
    tasks: list[Task],
    status: str = "all",
    priority: Optional[str] = None,
    category: Optional[str] = None,
) -> list[Task]:
    """
    Filter tasks by status, priority, and/or category.

    Args:
        tasks: List of tasks to filter
        status: Filter by completion status (complete/incomplete/all)
        priority: Filter by priority level (high/medium/low)
        category: Filter by category (work/home/personal)

    Returns:
        Filtered list of tasks
    """
    result = tasks

    # Filter by status
    if status == "complete":
        result = [t for t in result if t.completed]
    elif status == "incomplete":
        result = [t for t in result if not t.completed]
    # "all" doesn't filter

    # Filter by priority
    if priority:
        target_priority = Priority(priority)
        result = [t for t in result if t.priority == target_priority]

    # Filter by category
    if category:
        target_category = Category(category)
        result = [t for t in result if t.category == target_category]

    return result
