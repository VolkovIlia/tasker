import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_list_tasks():
    task = {
        "id": 1,
        "chat_id": 1,
        "message_id": 1,
        "title": "test",
        "created_by": "user",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    resp = client.post("/tasks", json=task)
    assert resp.status_code == 200
    assert resp.json()["title"] == "test"
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
