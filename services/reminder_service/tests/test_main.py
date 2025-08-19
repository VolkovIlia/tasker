import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_list_reminders():
    reminder = {
        "id": 1,
        "chat_id": 1,
        "target": "@user",
        "fire_at": "2024-01-01T00:00:00",
        "text": "do it"
    }
    resp = client.post("/reminders", json=reminder)
    assert resp.status_code == 200
    resp = client.get("/reminders")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
