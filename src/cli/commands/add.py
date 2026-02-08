"""Add command implementation."""

from datetime import datetime
from typing import Optional

from src.models.task import Task, Priority, Category, RecurrenceSchedule
from src.lib.storage import storage
from src.lib.errors import EmptyTitleError, InvalidDateError
from src.lib.display import format_success, format_task_detail


def parse_date(date_str: str) -> datetime:
    """Parse a date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise InvalidDateError(date_str)


def run_add(
    title: str,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    due: Optional[str] = None,
    recur: Optional[str] = None,
) -> str:
    """
    Add a new task.

    Args:
        title: Task title (required)
        priority: Priority level (high/medium/low)
        category: Category label (work/home/personal)
        due: Due date (YYYY-MM-DD format)
        recur: Recurrence schedule (none/daily/weekly/monthly)

    Returns:
        Success message with task details

    Raises:
        EmptyTitleError: If title is empty
        InvalidDateError: If date format is invalid
    """
    # Validate title
    title = title.strip()
    if not title:
        raise EmptyTitleError()

    # Parse optional fields
    task_priority = None
    if priority:
        task_priority = Priority(priority)

    task_category = None
    if category:
        task_category = Category(category)

    task_due = None
    if due:
        task_due = parse_date(due)

    task_recur = RecurrenceSchedule.NONE
    if recur and recur != "none":
        task_recur = RecurrenceSchedule(recur)

    # Create and save task
    task = Task(
        id=0,  # Will be assigned by storage
        title=title,
        priority=task_priority,
        category=task_category,
        due_date=task_due,
        recurrence=task_recur,
    )

    saved_task = storage.add(task)

    return format_success(f"Task #{saved_task.id} created") + format_task_detail(saved_task)
