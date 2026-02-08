"""Reminder service for due date tracking and alerts."""

from datetime import date
from typing import Optional

from src.models.task import Task


# Reminder intervals in days before due date
REMINDER_INTERVALS = [7, 3, 1, 0]  # 7 days, 3 days, 1 day, and on due date


def get_days_until_due(task: Task) -> Optional[int]:
    """
    Calculate days until task is due.

    Returns:
        Number of days until due (negative if overdue), or None if no due date
    """
    if task.due_date is None:
        return None

    today = date.today()
    return (task.due_date - today).days


def is_reminder_eligible(task: Task) -> bool:
    """
    Check if task is eligible for a reminder.

    A task is eligible if:
    - It has a due date
    - It is not completed
    - Reminder has not been dismissed

    Args:
        task: Task to check

    Returns:
        True if task should show reminder
    """
    if task.due_date is None:
        return False

    if task.completed:
        return False

    if task.reminder_dismissed:
        return False

    return True


def should_show_reminder(task: Task) -> bool:
    """
    Check if task should show a reminder based on escalating intervals.

    Shows reminders at: 7 days, 3 days, 1 day before, on due date, and overdue.

    Args:
        task: Task to check

    Returns:
        True if reminder should be shown
    """
    if not is_reminder_eligible(task):
        return False

    days_until = get_days_until_due(task)
    if days_until is None:
        return False

    # Show for overdue tasks
    if days_until < 0:
        return True

    # Show for tasks within reminder intervals
    return days_until <= max(REMINDER_INTERVALS)


def get_tasks_with_reminders(tasks: list[Task]) -> list[Task]:
    """
    Get tasks that should show due date reminders.

    Returns tasks sorted by urgency (overdue first, then by days until due).

    Args:
        tasks: List of all tasks

    Returns:
        List of tasks needing reminders, sorted by urgency
    """
    reminder_tasks = [t for t in tasks if should_show_reminder(t)]

    # Sort by urgency: overdue first, then by days until due
    def urgency_key(task: Task):
        days = get_days_until_due(task)
        if days is None:
            return float('inf')
        return days

    return sorted(reminder_tasks, key=urgency_key)


def get_startup_reminders(tasks: list[Task]) -> list[Task]:
    """
    Get tasks to show as reminders on app startup.

    Same as get_tasks_with_reminders, but intended for display on app start.

    Args:
        tasks: List of all tasks

    Returns:
        List of tasks needing attention at startup
    """
    return get_tasks_with_reminders(tasks)
