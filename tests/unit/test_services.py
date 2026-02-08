"""Unit tests for service modules."""

import pytest
from datetime import date, timedelta

from src.models.task import Task, Priority, Category, RecurrenceSchedule
from src.services.search import search_tasks
from src.services.filter import filter_tasks
from src.services.sort import sort_tasks
from src.services.reminder import (
    get_days_until_due,
    is_reminder_eligible,
    should_show_reminder,
    get_tasks_with_reminders,
)
from src.services.recurrence import (
    calculate_next_due_date,
    is_recurring,
    create_next_instance,
    handle_overdue_recurring,
)


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    today = date.today()
    return [
        Task(id=1, title="Buy groceries", priority=Priority.LOW, category=Category.HOME),
        Task(id=2, title="Project report", priority=Priority.HIGH, category=Category.WORK, completed=True),
        Task(id=3, title="Team meeting", priority=Priority.MEDIUM, category=Category.WORK),
        Task(id=4, title="Clean house", priority=Priority.LOW, category=Category.HOME, due_date=today + timedelta(days=2)),
        Task(id=5, title="Pay bills", priority=Priority.HIGH, category=Category.PERSONAL, due_date=today - timedelta(days=1)),
    ]


class TestSearchService:
    """Tests for search service."""

    def test_search_finds_matching(self, sample_tasks):
        """Test search finds tasks with matching keyword."""
        results = search_tasks(sample_tasks, "report")
        assert len(results) == 1
        assert results[0].id == 2

    def test_search_case_insensitive(self, sample_tasks):
        """Test search is case insensitive."""
        results = search_tasks(sample_tasks, "PROJECT")
        assert len(results) == 1
        assert results[0].id == 2

    def test_search_partial_match(self, sample_tasks):
        """Test search finds partial matches."""
        results = search_tasks(sample_tasks, "house")
        assert len(results) == 1
        assert results[0].id == 4

    def test_search_no_results(self, sample_tasks):
        """Test search returns empty list when no matches."""
        results = search_tasks(sample_tasks, "xyz")
        assert results == []

    def test_search_multiple_matches(self, sample_tasks):
        """Test search returns multiple matches."""
        # Both "Team meeting" and "Team" would match
        sample_tasks.append(Task(id=6, title="Team lunch"))
        results = search_tasks(sample_tasks, "team")
        assert len(results) == 2


class TestFilterService:
    """Tests for filter service."""

    def test_filter_by_status_complete(self, sample_tasks):
        """Test filtering by complete status."""
        results = filter_tasks(sample_tasks, status="complete")
        assert len(results) == 1
        assert results[0].id == 2

    def test_filter_by_status_incomplete(self, sample_tasks):
        """Test filtering by incomplete status."""
        results = filter_tasks(sample_tasks, status="incomplete")
        assert len(results) == 4

    def test_filter_by_status_all(self, sample_tasks):
        """Test filtering with status='all' returns all."""
        results = filter_tasks(sample_tasks, status="all")
        assert len(results) == 5

    def test_filter_by_priority(self, sample_tasks):
        """Test filtering by priority."""
        results = filter_tasks(sample_tasks, priority="high")
        assert len(results) == 2
        assert all(t.priority == Priority.HIGH for t in results)

    def test_filter_by_category(self, sample_tasks):
        """Test filtering by category."""
        results = filter_tasks(sample_tasks, category="work")
        assert len(results) == 2
        assert all(t.category == Category.WORK for t in results)

    def test_filter_combined(self, sample_tasks):
        """Test combining multiple filters."""
        results = filter_tasks(sample_tasks, status="incomplete", category="home")
        assert len(results) == 2
        assert all(t.category == Category.HOME and not t.completed for t in results)


class TestSortService:
    """Tests for sort service."""

    def test_sort_by_id_asc(self, sample_tasks):
        """Test sorting by ID ascending."""
        results = sort_tasks(sample_tasks, sort_by="id", order="asc")
        assert [t.id for t in results] == [1, 2, 3, 4, 5]

    def test_sort_by_id_desc(self, sample_tasks):
        """Test sorting by ID descending."""
        results = sort_tasks(sample_tasks, sort_by="id", order="desc")
        assert [t.id for t in results] == [5, 4, 3, 2, 1]

    def test_sort_by_title(self, sample_tasks):
        """Test sorting by title alphabetically."""
        results = sort_tasks(sample_tasks, sort_by="title", order="asc")
        titles = [t.title for t in results]
        assert titles == sorted(titles, key=str.lower)

    def test_sort_by_priority(self, sample_tasks):
        """Test sorting by priority (high first)."""
        results = sort_tasks(sample_tasks, sort_by="priority", order="asc")
        # High priority tasks should come first
        assert results[0].priority == Priority.HIGH
        assert results[1].priority == Priority.HIGH

    def test_sort_by_due(self, sample_tasks):
        """Test sorting by due date."""
        results = sort_tasks(sample_tasks, sort_by="due", order="asc")
        # Tasks with due dates come first, sorted by date
        # Tasks without due dates come last
        with_due = [t for t in results if t.due_date is not None]
        assert len(with_due) == 2
        assert with_due[0].due_date <= with_due[1].due_date

    def test_sort_stable_secondary_id(self, sample_tasks):
        """Test that sort is stable (secondary sort by ID)."""
        # Create tasks with same priority
        tasks = [
            Task(id=3, title="C", priority=Priority.HIGH),
            Task(id=1, title="A", priority=Priority.HIGH),
            Task(id=2, title="B", priority=Priority.HIGH),
        ]
        results = sort_tasks(tasks, sort_by="priority", order="asc")
        # Should be sorted by ID as secondary key
        assert [t.id for t in results] == [1, 2, 3]


class TestReminderService:
    """Tests for reminder service."""

    def test_get_days_until_due(self):
        """Test calculating days until due."""
        today = date.today()

        task_today = Task(id=1, title="Today", due_date=today)
        assert get_days_until_due(task_today) == 0

        task_future = Task(id=2, title="Future", due_date=today + timedelta(days=5))
        assert get_days_until_due(task_future) == 5

        task_past = Task(id=3, title="Past", due_date=today - timedelta(days=3))
        assert get_days_until_due(task_past) == -3

        task_no_due = Task(id=4, title="No due")
        assert get_days_until_due(task_no_due) is None

    def test_is_reminder_eligible(self):
        """Test reminder eligibility."""
        today = date.today()

        # Eligible: has due date, not completed, not dismissed
        eligible = Task(id=1, title="Eligible", due_date=today)
        assert is_reminder_eligible(eligible) is True

        # Not eligible: no due date
        no_due = Task(id=2, title="No due")
        assert is_reminder_eligible(no_due) is False

        # Not eligible: completed
        completed = Task(id=3, title="Completed", due_date=today, completed=True)
        assert is_reminder_eligible(completed) is False

        # Not eligible: dismissed
        dismissed = Task(id=4, title="Dismissed", due_date=today, reminder_dismissed=True)
        assert is_reminder_eligible(dismissed) is False

    def test_should_show_reminder(self):
        """Test whether reminder should be shown."""
        today = date.today()

        # Should show: due within 7 days
        soon = Task(id=1, title="Soon", due_date=today + timedelta(days=5))
        assert should_show_reminder(soon) is True

        # Should show: overdue
        overdue = Task(id=2, title="Overdue", due_date=today - timedelta(days=2))
        assert should_show_reminder(overdue) is True

        # Should not show: due in more than 7 days
        far = Task(id=3, title="Far", due_date=today + timedelta(days=10))
        assert should_show_reminder(far) is False

    def test_get_tasks_with_reminders(self):
        """Test getting tasks that need reminders."""
        today = date.today()
        tasks = [
            Task(id=1, title="Overdue", due_date=today - timedelta(days=1)),
            Task(id=2, title="Today", due_date=today),
            Task(id=3, title="Soon", due_date=today + timedelta(days=3)),
            Task(id=4, title="Far", due_date=today + timedelta(days=10)),
            Task(id=5, title="No due"),
            Task(id=6, title="Completed", due_date=today, completed=True),
        ]

        results = get_tasks_with_reminders(tasks)

        # Should include overdue, today, and soon (within 7 days)
        assert len(results) == 3
        # Should be sorted by urgency (overdue first)
        assert results[0].id == 1  # Overdue
        assert results[1].id == 2  # Today


class TestRecurrenceService:
    """Tests for recurrence service."""

    def test_calculate_next_due_date_daily(self):
        """Test daily recurrence."""
        today = date.today()
        next_due = calculate_next_due_date(today, RecurrenceSchedule.DAILY)
        assert next_due == today + timedelta(days=1)

    def test_calculate_next_due_date_weekly(self):
        """Test weekly recurrence."""
        today = date.today()
        next_due = calculate_next_due_date(today, RecurrenceSchedule.WEEKLY)
        assert next_due == today + timedelta(weeks=1)

    def test_calculate_next_due_date_monthly(self):
        """Test monthly recurrence (approx 30 days)."""
        today = date.today()
        next_due = calculate_next_due_date(today, RecurrenceSchedule.MONTHLY)
        assert next_due == today + timedelta(days=30)

    def test_is_recurring(self):
        """Test checking if task is recurring."""
        recurring = Task(id=1, title="Recurring", recurrence=RecurrenceSchedule.DAILY)
        assert is_recurring(recurring) is True

        not_recurring = Task(id=2, title="Not recurring", recurrence=RecurrenceSchedule.NONE)
        assert is_recurring(not_recurring) is False

    def test_create_next_instance(self):
        """Test creating next instance of recurring task."""
        today = date.today()
        task = Task(
            id=1,
            title="Weekly task",
            priority=Priority.HIGH,
            category=Category.WORK,
            due_date=today,
            recurrence=RecurrenceSchedule.WEEKLY,
        )

        next_task = create_next_instance(task)

        assert next_task is not None
        assert next_task.id == 0  # Will be assigned by storage
        assert next_task.title == "Weekly task"
        assert next_task.priority == Priority.HIGH
        assert next_task.category == Category.WORK
        assert next_task.due_date == today + timedelta(weeks=1)
        assert next_task.recurrence == RecurrenceSchedule.WEEKLY
        assert next_task.completed is False

    def test_create_next_instance_not_recurring(self):
        """Test that non-recurring task returns None."""
        task = Task(id=1, title="One time", recurrence=RecurrenceSchedule.NONE)
        assert create_next_instance(task) is None

    def test_create_next_instance_no_due_date(self):
        """Test that recurring task without due date returns None."""
        task = Task(id=1, title="No due", recurrence=RecurrenceSchedule.DAILY)
        assert create_next_instance(task) is None

    def test_handle_overdue_recurring(self):
        """Test detecting overdue recurring task."""
        today = date.today()

        # Overdue recurring (not completed)
        overdue = Task(
            id=1,
            title="Overdue",
            due_date=today - timedelta(days=1),
            recurrence=RecurrenceSchedule.DAILY,
        )
        assert handle_overdue_recurring(overdue) is True

        # Not overdue (future date)
        future = Task(
            id=2,
            title="Future",
            due_date=today + timedelta(days=1),
            recurrence=RecurrenceSchedule.DAILY,
        )
        assert handle_overdue_recurring(future) is False

        # Completed (not overdue in this context)
        completed = Task(
            id=3,
            title="Completed",
            due_date=today - timedelta(days=1),
            recurrence=RecurrenceSchedule.DAILY,
            completed=True,
        )
        assert handle_overdue_recurring(completed) is False
