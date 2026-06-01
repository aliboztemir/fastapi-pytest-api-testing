import pytest


@pytest.mark.e2e
class TestTaskLifecycleWorkflow:
    def test_full_create_read_update_delete_workflow(self, client):
        # Create
        create_response = client.post("/tasks/", json={"title": "E2E task", "description": "Full lifecycle"})
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Read
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "E2E task"
        assert get_response.json()["completed"] is False

        # Update
        update_response = client.put(f"/tasks/{task_id}", json={"completed": True, "title": "E2E task (done)"})
        assert update_response.status_code == 200
        assert update_response.json()["completed"] is True

        # Delete
        delete_response = client.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 204

        # Verify deletion
        verify_response = client.get(f"/tasks/{task_id}")
        assert verify_response.status_code == 404

    def test_multiple_tasks_are_independently_manageable(self, client):
        ids = []
        for i in range(1, 4):
            response = client.post("/tasks/", json={"title": f"Task {i}"})
            assert response.status_code == 201
            ids.append(response.json()["id"])

        # Complete only the second task
        client.put(f"/tasks/{ids[1]}", json={"completed": True})

        tasks = client.get("/tasks/").json()
        completed = [t for t in tasks if t["completed"]]
        pending = [t for t in tasks if not t["completed"]]
        assert len(completed) == 1
        assert len(pending) == 2

    def test_task_list_reflects_deletions(self, client):
        r1 = client.post("/tasks/", json={"title": "Keep me"}).json()
        r2 = client.post("/tasks/", json={"title": "Delete me"}).json()

        client.delete(f"/tasks/{r2['id']}")

        tasks = client.get("/tasks/").json()
        ids = [t["id"] for t in tasks]
        assert r1["id"] in ids
        assert r2["id"] not in ids

    def test_updated_task_fields_are_reflected_in_list(self, client):
        created = client.post("/tasks/", json={"title": "Draft"}).json()
        client.put(f"/tasks/{created['id']}", json={"title": "Final", "completed": True})

        tasks = client.get("/tasks/").json()
        updated = next(t for t in tasks if t["id"] == created["id"])
        assert updated["title"] == "Final"
        assert updated["completed"] is True
