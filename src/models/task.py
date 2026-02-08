"""Task entity model for the Todo application."""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Category(Enum):
    """Task category labels."""
    WORK = "work"
    HOME = "home"
    PERSONAL = "personal"


class RecurrenceSchedule(Enum):
    """Recurrence schedule options."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Auto-generated unique integer ID
        title: Task title (required, max 200 characters)
        completed: Completion status (False = incomplete, True = complete)
        priority: Priority level (optional)
        category: Category label (optional)
        due_date: Due date (optional)
        recurrence: Recurrence schedule (optional)
        created_at: Creation timestamp
        modified_at: Last modification timestamp
        reminder_dismissed: Whether reminder has been dismissed
    """
    id: int
    title: str
    completed: bool = False
    priority: Optional[Priority] = None
    category: Optional[Category] = None
    due_date: Optional[date] = None
    recurrence: RecurrenceSchedule = RecurrenceSchedule.NONE
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    reminder_dismissed: bool = False

    def __post_init__(self):
        """Validate task after initialization."""
        # Enforce title length limit (max 200 characters)
        if len(self.title) > 200:
            self.title = self.title[:200]

    def mark_modified(self):
        """Update the modified timestamp."""
        self.modified_at = datetime.now()

    def toggle_complete(self) -> bool:
        """Toggle completion status and return new status."""
        self.completed = not self.completed
        self.mark_modified()
        return self.completed

    def update_title(self, new_title: str):
        """Update the task title."""
        if len(new_title) > 200:
            new_title = new_title[:200]
        self.title = new_title
        self.mark_modified()

    def update_priority(self, priority: Optional[Priority]):
        """Update the task priority."""
        self.priority = priority
        self.mark_modified()

    def update_category(self, category: Optional[Category]):
        """Update the task category."""
        self.category = category
        self.mark_modified()

    def update_due_date(self, due_date: Optional[date]):
        """Update the task due date."""
        self.due_date = due_date
        self.mark_modified()

    def update_recurrence(self, recurrence: RecurrenceSchedule):
        """Update the recurrence schedule."""
        self.recurrence = recurrence
        self.mark_modified()

    def dismiss_reminder(self):
        """Dismiss the reminder for this task."""
        self.reminder_dismissed = True
        self.mark_modified()

    def reset_reminder(self):
        """Reset the reminder dismissed state."""
        self.reminder_dismissed = False
        self.mark_modified()
