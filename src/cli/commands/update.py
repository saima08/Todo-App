"""Update command implementation."""

from datetime import datetime
from typing import Optional

from src.models.task import Priority, Category, RecurrenceSchedule
from src.lib.storage import storage
from src.lib.errors import EmptyTitleError, InvalidDateError, InvalidArgumentError
from src.lib.display import format_success, format_task_detail


def parse_date(date_str: str) -> datetime:
    """Parse a date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise InvalidDateError(date_str)


def run_update(
    task_id: int,
    title: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    due: Optional[str] = None,
    recur: Optional[str] = None,
) -> str:
    """
    Update an existing task.

    Args:
        task_id: ID of task to update
        title: New title (optional)
        priority: New priority (optional, 'none' to clear)
        category: New category (optional, 'none' to clear)
        due: New due date (optional, 'none' to clear)
        recur: New recurrence (optional)

    Returns:
        Success message with updated task details

    Raises:
        TaskNotFoundError: If task doesn't exist
        EmptyTitleError: If title is empty
    """
    # Get existing task
    task = storage.get(task_id)

    # Track if anything changed
    changes = []

    # Update title if provided
    if title is not None:
        title = title.strip()
        if not title:
            raise EmptyTitleError()
        task.update_title(title)
        changes.append("title")

    # Update priority if provided
    if priority is not None:
        if priority == "none":
            task.update_priority(None)
        else:
            task.update_priority(Priority(priority))
        changes.append("priority")

    # Update category if provided
    if category is not None:
        if category == "none":
            task.update_category(None)
        else:
            task.update_category(Category(category))
        changes.append("category")

    # Update due date if provided
    if due is not None:
        if due == "none":
            task.update_due_date(None)
        else:
            task.update_due_date(parse_date(due))
        changes.append("due date")

    # Update recurrence if provided
    if recur is not None:
        task.update_recurrence(RecurrenceSchedule(recur))
        changes.append("recurrence")

    if not changes:
        raise InvalidArgumentError(
            "No updates specified",
            "Provide at least one field to update (--title, --priority, --category, --due, --recur)"
        )

    # Save changes
    storage.update(task)

    changes_str = ", ".join(changes)
    return format_success(f"Task #{task_id} updated ({changes_str})") + format_task_detail(task)
