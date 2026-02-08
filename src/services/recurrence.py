"""Recurrence service for recurring task management."""

from datetime import date, timedelta
from typing import Optional

from src.models.task import Task, RecurrenceSchedule


def calculate_next_due_date(current_due: date, recurrence: RecurrenceSchedule) -> date:
    """
    Calculate the next due date based on recurrence schedule.

    Args:
        current_due: Current due date
        recurrence: Recurrence schedule

    Returns:
        Next due date
    """
    if recurrence == RecurrenceSchedule.DAILY:
        return current_due + timedelta(days=1)
    elif recurrence == RecurrenceSchedule.WEEKLY:
        return current_due + timedelta(weeks=1)
    elif recurrence == RecurrenceSchedule.MONTHLY:
        # Add approximately one month (30 days)
        # For production, consider using dateutil.relativedelta for accurate month handling
        return current_due + timedelta(days=30)
    return current_due


def is_recurring(task: Task) -> bool:
    """Check if a task is recurring."""
    return task.recurrence != RecurrenceSchedule.NONE


def create_next_instance(completed_task: Task) -> Optional[Task]:
    """
    Create the next instance of a recurring task after completion.

    Only creates a new instance if:
    - Task is recurring
    - Task has a due date

    Note: The new task needs to be saved by the caller using storage.add()

    Args:
        completed_task: The task that was just completed

    Returns:
        New task instance if applicable, None otherwise
    """
    if not is_recurring(completed_task):
        return None

    if completed_task.due_date is None:
        return None

    next_due = calculate_next_due_date(completed_task.due_date, completed_task.recurrence)

    # Create new instance (id=0 will be assigned by storage)
    return Task(
        id=0,
        title=completed_task.title,
        completed=False,
        priority=completed_task.priority,
        category=completed_task.category,
        due_date=next_due,
        recurrence=completed_task.recurrence,
        reminder_dismissed=False,
    )


def handle_overdue_recurring(task: Task) -> bool:
    """
    Check if a recurring task is overdue.

    Overdue recurring tasks:
    - Show as overdue (not auto-advanced)
    - New instance is NOT created until task is marked complete

    Args:
        task: Task to check

    Returns:
        True if task is recurring and overdue
    """
    if not is_recurring(task):
        return False

    if task.due_date is None:
        return False

    if task.completed:
        return False

    return task.due_date < date.today()
