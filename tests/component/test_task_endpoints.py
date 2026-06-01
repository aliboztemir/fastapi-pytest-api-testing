import pytest


@pytest.mark.component
class TestHealthCheckEndpoint:
    def test_health_check_returns_ok_status(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


@pytest.mark.component
class TestCreateTaskEndpoint:
    def test_create_task_returns_201_with_valid_payload(self, client):
        payload = {"title": "Write tests", "description": "Cover all endpoints"}
        response = client.post("/tasks/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Write tests"
        assert data["description"] == "Cover all endpoints"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_task_returns_201_with_title_only(self, client):
        response = client.post("/tasks/", json={"title": "Minimal task"})
        assert response.status_code == 201
        assert response.json()["description"] is None

    def test_create_task_returns_422_when_title_is_missing(self, client):
        response = client.post("/tasks/", json={"description": "No title provided"})
        assert response.status_code == 422

    def test_create_task_returns_422_when_title_is_empty(self, client):
        response = client.post("/tasks/", json={"title": ""})
        assert response.status_code == 422


@pytest.mark.component
class TestGetTaskEndpoint:
    def test_get_existing_task_returns_200(self, client):
        created = client.post("/tasks/", json={"title": "Fetch me"}).json()
        response = client.get(f"/tasks/{created['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == "Fetch me"

    def test_get_nonexistent_task_returns_404(self, client):
        response = client.get("/tasks/99999")
        assert response.status_code == 404

    def test_get_task_response_contains_all_required_fields(self, client):
        created = client.post("/tasks/", json={"title": "Check fields"}).json()
        response = client.get(f"/tasks/{created['id']}")
        data = response.json()
        assert all(key in data for key in ["id", "title", "description", "completed", "created_at"])


@pytest.mark.component
class TestListTasksEndpoint:
    def test_list_tasks_returns_empty_list_when_no_tasks_exist(self, client):
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_returns_all_created_tasks(self, client):
        client.post("/tasks/", json={"title": "Task A"})
        client.post("/tasks/", json={"title": "Task B"})
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert len(response.json()) == 2


@pytest.mark.component
class TestUpdateTaskEndpoint:
    def test_update_task_title_returns_updated_value(self, client):
        created = client.post("/tasks/", json={"title": "Old title"}).json()
        response = client.put(f"/tasks/{created['id']}", json={"title": "New title"})
        assert response.status_code == 200
        assert response.json()["title"] == "New title"

    def test_mark_task_as_completed_returns_completed_true(self, client):
        created = client.post("/tasks/", json={"title": "Finish me"}).json()
        response = client.put(f"/tasks/{created['id']}", json={"completed": True})
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_nonexistent_task_returns_404(self, client):
        response = client.put("/tasks/99999", json={"title": "Ghost"})
        assert response.status_code == 404


@pytest.mark.component
class TestDeleteTaskEndpoint:
    def test_delete_existing_task_returns_204(self, client):
        created = client.post("/tasks/", json={"title": "Delete me"}).json()
        response = client.delete(f"/tasks/{created['id']}")
        assert response.status_code == 204

    def test_deleted_task_is_no_longer_retrievable(self, client):
        created = client.post("/tasks/", json={"title": "Delete me"}).json()
        client.delete(f"/tasks/{created['id']}")
        response = client.get(f"/tasks/{created['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_task_returns_404(self, client):
        response = client.delete("/tasks/99999")
        assert response.status_code == 404
