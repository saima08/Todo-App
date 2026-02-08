"""Search command implementation."""

from src.lib.storage import storage
from src.lib.display import format_task_list, format_count
from src.services.search import search_tasks


def run_search(keyword: str) -> str:
    """
    Search tasks by keyword in title.

    Args:
        keyword: Search keyword

    Returns:
        Formatted list of matching tasks
    """
    tasks = storage.get_all()

    if not tasks:
        return "No tasks found. Use 'todo add' to create your first task."

    # Search tasks
    matching = search_tasks(tasks, keyword)

    if not matching:
        return f"No tasks found matching '{keyword}'."

    return format_task_list(matching, f"Search results for '{keyword}'")
