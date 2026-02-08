"""Check-due command implementation."""

from datetime import date

from src.lib.storage import storage
from src.lib.display import format_reminder_list
from src.services.reminder import get_tasks_with_reminders


def run_check_due() -> str:
    """
    Show tasks with upcoming or overdue due dates.

    Shows reminders for tasks with due dates at escalating intervals:
    - Overdue tasks
    - Due today
    - Due within 7 days

    Only shows incomplete tasks (completed tasks don't trigger reminders).

    Returns:
        Formatted reminder list
    """
    tasks = storage.get_all()

    if not tasks:
        return "No tasks found. Use 'todo add' to create your first task."

    # Get tasks with due date reminders (excludes completed tasks)
    reminder_tasks = get_tasks_with_reminders(tasks)

    if not reminder_tasks:
        return "[OK] No upcoming or overdue tasks. You're all caught up!"

    return format_reminder_list(reminder_tasks)
