"""Complete command implementation."""

from datetime import date, timedelta

from src.models.task import Task, RecurrenceSchedule
from src.lib.storage import storage
from src.lib.display import format_success, format_task_detail


def calculate_next_due_date(current_due: date, recurrence: RecurrenceSchedule) -> date:
    """Calculate the next due date based on recurrence schedule."""
    if recurrence == RecurrenceSchedule.DAILY:
        return current_due + timedelta(days=1)
    elif recurrence == RecurrenceSchedule.WEEKLY:
        return current_due + timedelta(weeks=1)
    elif recurrence == RecurrenceSchedule.MONTHLY:
        # Add approximately one month (30 days)
        # For more accurate month handling, use dateutil.relativedelta
        return current_due + timedelta(days=30)
    return current_due


def run_complete(task_id: int) -> str:
    """
    Toggle task completion status.

    For recurring tasks: when marked complete, creates a new instance
    with the due date advanced according to the schedule.

    Args:
        task_id: ID of task to toggle

    Returns:
        Success message with task status

    Raises:
        TaskNotFoundError: If task doesn't exist
    """
    task = storage.get(task_id)
    was_complete = task.completed

    # Toggle completion
    new_status = task.toggle_complete()
    storage.update(task)

    result = []

    if new_status:
        result.append(format_success(f"Task #{task_id} marked as complete"))

        # Handle recurring tasks - create new instance when completed
        if task.recurrence != RecurrenceSchedule.NONE and task.due_date:
            # Calculate next due date
            next_due = calculate_next_due_date(task.due_date, task.recurrence)

            # Create new task instance
            new_task = Task(
                id=0,  # Will be assigned by storage
                title=task.title,
                completed=False,
                priority=task.priority,
                category=task.category,
                due_date=next_due,
                recurrence=task.recurrence,
            )
            saved_task = storage.add(new_task)
            result.append(f"\n[RECUR] Recurring task: New instance created as Task #{saved_task.id}")
            result.append(f"   Next due date: {next_due.strftime('%Y-%m-%d')}")
    else:
        result.append(format_success(f"Task #{task_id} marked as incomplete"))

    result.append(format_task_detail(task))
    return "\n".join(result)
