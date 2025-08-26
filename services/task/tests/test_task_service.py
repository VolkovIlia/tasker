import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SERVICE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.extend([str(ROOT), str(SERVICE_DIR)])

from fastapi.testclient import TestClient

spec = importlib.util.spec_from_file_location("task_main", ROOT / "services" / "task" / "main.py")
task_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_main)

client = TestClient(task_main.app)

def test_create_and_list_tasks():
    payload = {"chat_id": 1, "title": "Write docs", "assignee": "bob", "tags": ["docs"]}
    resp = client.post("/tasks", json=payload)
    assert resp.status_code == 200
    task = resp.json()
    assert task["id"] == 1
    assert task["title"] == "Write docs"

    list_resp = client.get("/tasks")
    assert list_resp.status_code == 200
    assert list_resp.json() == [task]
