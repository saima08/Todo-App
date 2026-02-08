"""Integration tests for CLI commands."""

import pytest

from src.lib.storage import Storage
from src.cli.commands.add import run_add
from src.cli.commands.list import run_list
from src.cli.commands.update import run_update
from src.cli.commands.complete import run_complete
from src.cli.commands.delete import run_delete
from src.cli.commands.search import run_search
from src.cli.commands.check_due import run_check_due
from src.lib.errors import EmptyTitleError, TaskNotFoundError, InvalidDateError


@pytest.fixture(autouse=True)
def reset_storage():
    """Reset storage before each test."""
    storage = Storage()
    storage.reset()
    yield
    storage.reset()


class TestAddCommand:
    """Tests for add command."""

    def test_add_basic_task(self):
        """Test adding a basic task."""
        result = run_add(title="Buy groceries")

        assert "[OK] Task #1 created" in result
        assert "Buy groceries" in result

    def test_add_task_with_priority(self):
        """Test adding task with priority."""
        result = run_add(title="Urgent task", priority="high")

        assert "[OK] Task #1 created" in result
        assert "high" in result

    def test_add_task_with_category(self):
        """Test adding task with category."""
        result = run_add(title="Work task", category="work")

        assert "[OK] Task #1 created" in result
        assert "work" in result

    def test_add_task_with_due_date(self):
        """Test adding task with due date."""
        result = run_add(title="Deadline task", due="2026-02-15")

        assert "[OK] Task #1 created" in result
        assert "2026-02-15" in result

    def test_add_task_with_recurrence(self):
        """Test adding recurring task."""
        result = run_add(title="Daily task", recur="daily", due="2026-02-10")

        assert "[OK] Task #1 created" in result
        assert "daily" in result

    def test_add_empty_title_fails(self):
        """Test that empty title raises error."""
        with pytest.raises(EmptyTitleError):
            run_add(title="   ")

    def test_add_invalid_date_fails(self):
        """Test that invalid date raises error."""
        with pytest.raises(InvalidDateError):
            run_add(title="Task", due="invalid-date")


class TestListCommand:
    """Tests for list command."""

    def test_list_empty(self):
        """Test listing when no tasks exist."""
        result = run_list()
        assert "No tasks found" in result

    def test_list_all_tasks(self):
        """Test listing all tasks."""
        run_add(title="Task 1")
        run_add(title="Task 2")

        result = run_list()

        assert "Task 1" in result
        assert "Task 2" in result
        assert "2 tasks" in result

    def test_list_filter_by_status(self):
        """Test filtering by status."""
        run_add(title="Task 1")
        run_add(title="Task 2")
        run_complete(1)

        incomplete = run_list(status="incomplete")
        assert "Task 2" in incomplete
        assert "1 task" in incomplete

        complete = run_list(status="complete")
        assert "Task 1" in complete

    def test_list_filter_by_priority(self):
        """Test filtering by priority."""
        run_add(title="High", priority="high")
        run_add(title="Low", priority="low")

        result = run_list(priority="high")

        assert "High" in result
        assert "Low" not in result

    def test_list_filter_by_category(self):
        """Test filtering by category."""
        run_add(title="Work task", category="work")
        run_add(title="Home task", category="home")

        result = run_list(category="work")

        assert "Work task" in result
        assert "Home task" not in result

    def test_list_sort_by_priority(self):
        """Test sorting by priority."""
        run_add(title="Low", priority="low")
        run_add(title="High", priority="high")
        run_add(title="Medium", priority="medium")

        result = run_list(sort="priority", order="asc")

        # High priority should appear before Medium and Low
        high_pos = result.find("High")
        medium_pos = result.find("Medium")
        low_pos = result.find("Low")

        assert high_pos < medium_pos < low_pos


class TestUpdateCommand:
    """Tests for update command."""

    def test_update_title(self):
        """Test updating task title."""
        run_add(title="Original")
        result = run_update(task_id=1, title="Updated")

        assert "[OK] Task #1 updated" in result
        assert "Updated" in result

    def test_update_priority(self):
        """Test updating task priority."""
        run_add(title="Task")
        result = run_update(task_id=1, priority="high")

        assert "[OK] Task #1 updated" in result
        assert "high" in result

    def test_update_nonexistent_task(self):
        """Test updating non-existent task fails."""
        with pytest.raises(TaskNotFoundError):
            run_update(task_id=999, title="Ghost")


class TestCompleteCommand:
    """Tests for complete command."""

    def test_complete_task(self):
        """Test marking task as complete."""
        run_add(title="Task")
        result = run_complete(task_id=1)

        assert "marked as complete" in result

    def test_uncomplete_task(self):
        """Test toggling back to incomplete."""
        run_add(title="Task")
        run_complete(task_id=1)
        result = run_complete(task_id=1)

        assert "marked as incomplete" in result

    def test_complete_recurring_creates_instance(self):
        """Test that completing recurring task creates new instance."""
        run_add(title="Weekly", recur="weekly", due="2026-02-07")
        result = run_complete(task_id=1)

        assert "marked as complete" in result
        assert "New instance created" in result
        assert "Task #2" in result

    def test_complete_nonexistent_task(self):
        """Test completing non-existent task fails."""
        with pytest.raises(TaskNotFoundError):
            run_complete(task_id=999)


class TestDeleteCommand:
    """Tests for delete command."""

    def test_delete_task(self):
        """Test deleting a task."""
        run_add(title="To delete")
        result = run_delete(task_id=1)

        assert "[OK] Task #1" in result
        assert "deleted" in result

    def test_delete_nonexistent_task(self):
        """Test deleting non-existent task fails."""
        with pytest.raises(TaskNotFoundError):
            run_delete(task_id=999)


class TestSearchCommand:
    """Tests for search command."""

    def test_search_finds_matching(self):
        """Test search finds matching tasks."""
        run_add(title="Buy groceries")
        run_add(title="Project report")

        result = run_search(keyword="groceries")

        assert "groceries" in result.lower()
        assert "report" not in result.lower()

    def test_search_no_results(self):
        """Test search with no matches."""
        run_add(title="Some task")

        result = run_search(keyword="xyz")

        assert "No tasks found matching" in result


class TestCheckDueCommand:
    """Tests for check-due command."""

    def test_check_due_no_tasks(self):
        """Test check-due with no tasks."""
        result = run_check_due()
        assert "No tasks found" in result

    def test_check_due_no_reminders(self):
        """Test check-due with no upcoming due dates."""
        run_add(title="No due date")

        result = run_check_due()

        assert "all caught up" in result

    def test_check_due_with_upcoming(self):
        """Test check-due with upcoming due dates."""
        run_add(title="Soon", due="2026-02-07")

        result = run_check_due()

        assert "Soon" in result or "Upcoming" in result
