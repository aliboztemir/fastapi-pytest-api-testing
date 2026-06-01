import pytest
from app.models import Task


@pytest.mark.integration
class TestTaskDatabaseOperations:
    def test_task_is_persisted_to_database_on_create(self, db_session):
        task = Task(title="Persisted task", description="Should be in DB")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        assert task.id is not None
        assert task.title == "Persisted task"

    def test_task_defaults_to_not_completed_on_create(self, db_session):
        task = Task(title="Default state task")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        assert task.completed is False

    def test_task_created_at_is_populated_automatically(self, db_session):
        task = Task(title="Timestamped task")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        assert task.created_at is not None

    def test_task_title_is_updated_in_database(self, db_session):
        task = Task(title="Original title")
        db_session.add(task)
        db_session.commit()
        task.title = "Updated title"
        db_session.commit()
        db_session.refresh(task)
        assert task.title == "Updated title"

    def test_task_completed_flag_is_updated_in_database(self, db_session):
        task = Task(title="Completable task")
        db_session.add(task)
        db_session.commit()
        task.completed = True
        db_session.commit()
        db_session.refresh(task)
        assert task.completed is True

    def test_deleted_task_is_removed_from_database(self, db_session):
        task = Task(title="Temporary task")
        db_session.add(task)
        db_session.commit()
        task_id = task.id
        db_session.delete(task)
        db_session.commit()
        result = db_session.query(Task).filter(Task.id == task_id).first()
        assert result is None

    def test_multiple_tasks_are_retrieved_from_database(self, db_session):
        db_session.add_all([Task(title="Task One"), Task(title="Task Two"), Task(title="Task Three")])
        db_session.commit()
        tasks = db_session.query(Task).all()
        assert len(tasks) == 3
