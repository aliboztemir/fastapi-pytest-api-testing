import pytest
from pydantic import ValidationError
from app.schemas import TaskCreate, TaskUpdate


@pytest.mark.unit
class TestTaskCreateSchema:
    def test_valid_task_is_created_with_title_only(self):
        task = TaskCreate(title="Buy groceries")
        assert task.title == "Buy groceries"
        assert task.description is None

    def test_valid_task_is_created_with_title_and_description(self):
        task = TaskCreate(title="Buy groceries", description="Milk, eggs, bread")
        assert task.description == "Milk, eggs, bread"

    def test_task_creation_fails_when_title_is_empty(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_task_creation_fails_when_title_is_missing(self):
        with pytest.raises(ValidationError):
            TaskCreate()

    def test_task_creation_fails_when_title_exceeds_max_length(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="x" * 256)

    def test_task_creation_fails_when_description_exceeds_max_length(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="Valid title", description="x" * 1001)


@pytest.mark.unit
class TestTaskUpdateSchema:
    def test_partial_update_accepts_no_fields(self):
        update = TaskUpdate()
        assert update.title is None
        assert update.completed is None

    def test_partial_update_accepts_completed_true(self):
        update = TaskUpdate(completed=True)
        assert update.completed is True

    def test_partial_update_accepts_completed_false(self):
        update = TaskUpdate(completed=False)
        assert update.completed is False

    def test_partial_update_fails_when_title_is_empty(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="")
