"""Unit tests for Task model."""

import pytest
from datetime import date, datetime

from src.models.task import Task, Priority, Category, RecurrenceSchedule


class TestTask:
    """Tests for Task entity."""

    def test_create_task_basic(self):
        """Test creating a basic task with required fields."""
        task = Task(id=1, title="Test task")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.completed is False
        assert task.priority is None
        assert task.category is None
        assert task.due_date is None
        assert task.recurrence == RecurrenceSchedule.NONE

    def test_create_task_with_all_fields(self):
        """Test creating a task with all optional fields."""
        due = date(2026, 2, 15)
        task = Task(
            id=1,
            title="Full task",
            completed=False,
            priority=Priority.HIGH,
            category=Category.WORK,
            due_date=due,
            recurrence=RecurrenceSchedule.WEEKLY,
        )

        assert task.priority == Priority.HIGH
        assert task.category == Category.WORK
        assert task.due_date == due
        assert task.recurrence == RecurrenceSchedule.WEEKLY

    def test_title_length_limit(self):
        """Test that title is truncated to 200 characters."""
        long_title = "x" * 250
        task = Task(id=1, title=long_title)

        assert len(task.title) == 200

    def test_toggle_complete(self):
        """Test toggling completion status."""
        task = Task(id=1, title="Test")

        assert task.completed is False
        result = task.toggle_complete()
        assert result is True
        assert task.completed is True

        result = task.toggle_complete()
        assert result is False
        assert task.completed is False

    def test_update_title(self):
        """Test updating task title."""
        task = Task(id=1, title="Original")
        task.update_title("Updated")

        assert task.title == "Updated"

    def test_update_title_truncates(self):
        """Test that update_title truncates long titles."""
        task = Task(id=1, title="Original")
        task.update_title("x" * 250)

        assert len(task.title) == 200

    def test_update_priority(self):
        """Test updating task priority."""
        task = Task(id=1, title="Test")

        task.update_priority(Priority.HIGH)
        assert task.priority == Priority.HIGH

        task.update_priority(None)
        assert task.priority is None

    def test_update_category(self):
        """Test updating task category."""
        task = Task(id=1, title="Test")

        task.update_category(Category.WORK)
        assert task.category == Category.WORK

        task.update_category(None)
        assert task.category is None

    def test_update_due_date(self):
        """Test updating task due date."""
        task = Task(id=1, title="Test")
        due = date(2026, 3, 1)

        task.update_due_date(due)
        assert task.due_date == due

        task.update_due_date(None)
        assert task.due_date is None

    def test_update_recurrence(self):
        """Test updating recurrence schedule."""
        task = Task(id=1, title="Test")

        task.update_recurrence(RecurrenceSchedule.DAILY)
        assert task.recurrence == RecurrenceSchedule.DAILY

    def test_dismiss_reminder(self):
        """Test dismissing reminder."""
        task = Task(id=1, title="Test")
        assert task.reminder_dismissed is False

        task.dismiss_reminder()
        assert task.reminder_dismissed is True

    def test_reset_reminder(self):
        """Test resetting reminder."""
        task = Task(id=1, title="Test", reminder_dismissed=True)

        task.reset_reminder()
        assert task.reminder_dismissed is False

    def test_mark_modified_updates_timestamp(self):
        """Test that modifications update the modified timestamp."""
        task = Task(id=1, title="Test")
        original_modified = task.modified_at

        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)

        task.update_title("New title")
        assert task.modified_at > original_modified


class TestPriorityEnum:
    """Tests for Priority enum."""

    def test_priority_values(self):
        """Test priority enum values."""
        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"


class TestCategoryEnum:
    """Tests for Category enum."""

    def test_category_values(self):
        """Test category enum values."""
        assert Category.WORK.value == "work"
        assert Category.HOME.value == "home"
        assert Category.PERSONAL.value == "personal"


class TestRecurrenceScheduleEnum:
    """Tests for RecurrenceSchedule enum."""

    def test_recurrence_values(self):
        """Test recurrence enum values."""
        assert RecurrenceSchedule.NONE.value == "none"
        assert RecurrenceSchedule.DAILY.value == "daily"
        assert RecurrenceSchedule.WEEKLY.value == "weekly"
        assert RecurrenceSchedule.MONTHLY.value == "monthly"
