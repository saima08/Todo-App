"""Unit tests for Storage module."""

import pytest

from src.models.task import Task, Priority, Category
from src.lib.storage import Storage, MAX_TASKS
from src.lib.errors import TaskNotFoundError, StorageLimitError


@pytest.fixture
def storage():
    """Create a fresh storage instance for each test."""
    s = Storage()
    s.reset()
    return s


class TestStorage:
    """Tests for Storage class."""

    def test_add_task(self, storage):
        """Test adding a task."""
        task = Task(id=0, title="Test task")
        saved = storage.add(task)

        assert saved.id == 1
        assert saved.title == "Test task"
        assert storage.count() == 1

    def test_add_multiple_tasks(self, storage):
        """Test adding multiple tasks with auto-incrementing IDs."""
        task1 = Task(id=0, title="Task 1")
        task2 = Task(id=0, title="Task 2")
        task3 = Task(id=0, title="Task 3")

        saved1 = storage.add(task1)
        saved2 = storage.add(task2)
        saved3 = storage.add(task3)

        assert saved1.id == 1
        assert saved2.id == 2
        assert saved3.id == 3
        assert storage.count() == 3

    def test_get_task(self, storage):
        """Test getting a task by ID."""
        task = Task(id=0, title="Test task")
        storage.add(task)

        retrieved = storage.get(1)
        assert retrieved.title == "Test task"

    def test_get_nonexistent_task(self, storage):
        """Test getting a task that doesn't exist."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            storage.get(999)

        assert exc_info.value.task_id == 999

    def test_get_all_tasks(self, storage):
        """Test getting all tasks."""
        storage.add(Task(id=0, title="Task 1"))
        storage.add(Task(id=0, title="Task 2"))
        storage.add(Task(id=0, title="Task 3"))

        tasks = storage.get_all()
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_all_empty(self, storage):
        """Test getting all tasks when storage is empty."""
        tasks = storage.get_all()
        assert tasks == []

    def test_update_task(self, storage):
        """Test updating a task."""
        task = Task(id=0, title="Original")
        storage.add(task)

        task.title = "Updated"
        storage.update(task)

        retrieved = storage.get(1)
        assert retrieved.title == "Updated"

    def test_update_nonexistent_task(self, storage):
        """Test updating a task that doesn't exist."""
        task = Task(id=999, title="Ghost")

        with pytest.raises(TaskNotFoundError):
            storage.update(task)

    def test_delete_task(self, storage):
        """Test deleting a task."""
        task = Task(id=0, title="To delete")
        storage.add(task)

        deleted = storage.delete(1)
        assert deleted.title == "To delete"
        assert storage.count() == 0

    def test_delete_nonexistent_task(self, storage):
        """Test deleting a task that doesn't exist."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            storage.delete(999)

        assert exc_info.value.task_id == 999

    def test_exists(self, storage):
        """Test checking if a task exists."""
        storage.add(Task(id=0, title="Exists"))

        assert storage.exists(1) is True
        assert storage.exists(999) is False

    def test_count(self, storage):
        """Test counting tasks."""
        assert storage.count() == 0

        storage.add(Task(id=0, title="Task 1"))
        assert storage.count() == 1

        storage.add(Task(id=0, title="Task 2"))
        assert storage.count() == 2

        storage.delete(1)
        assert storage.count() == 1

    def test_storage_limit(self, storage):
        """Test that storage enforces the maximum task limit."""
        # Add tasks up to the limit
        for i in range(MAX_TASKS):
            storage.add(Task(id=0, title=f"Task {i}"))

        # Try to add one more
        with pytest.raises(StorageLimitError):
            storage.add(Task(id=0, title="Over limit"))

    def test_reset(self, storage):
        """Test resetting storage."""
        storage.add(Task(id=0, title="Task 1"))
        storage.add(Task(id=0, title="Task 2"))

        storage.reset()

        assert storage.count() == 0
        # ID counter should also reset
        new_task = storage.add(Task(id=0, title="New"))
        assert new_task.id == 1
