"""Search service for keyword matching in tasks."""

from src.models.task import Task


def search_tasks(tasks: list[Task], keyword: str) -> list[Task]:
    """
    Search tasks by keyword in title.

    Case-insensitive search.

    Args:
        tasks: List of tasks to search
        keyword: Search keyword

    Returns:
        List of tasks with keyword in title
    """
    keyword_lower = keyword.lower()
    return [task for task in tasks if keyword_lower in task.title.lower()]
