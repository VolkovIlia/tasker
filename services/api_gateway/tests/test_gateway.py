import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SERVICE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.extend([str(ROOT), str(SERVICE_DIR)])

from fastapi.testclient import TestClient
from main import app, gateway

# Dynamically load the bot service so we can create multiple instances
spec = importlib.util.spec_from_file_location("bot_main", ROOT / "services" / "bot" / "main.py")
bot_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot_main)

# Register two bot backends with distinct names to verify round-robin behaviour
bot_a = bot_main.create_app("A")
bot_b = bot_main.create_app("B")
gateway.register("bot", [bot_a, bot_b])

# Register the task service so the gateway can proxy task requests
task_spec = importlib.util.spec_from_file_location("task_main", ROOT / "services" / "task" / "main.py")
task_main = importlib.util.module_from_spec(task_spec)
task_spec.loader.exec_module(task_main)
gateway.register("task", [task_main.app])

client = TestClient(app)

def test_round_robin_forwarding():
    first = client.post("/bot/webhook", json={"message": {"text": "/who"}})
    second = client.post("/bot/webhook", json={"message": {"text": "/who"}})
    assert first.status_code == second.status_code == 200
    assert first.json()["reply"] == "A"
    assert second.json()["reply"] == "B"


def test_task_proxy():
    payload = {"chat_id": 1, "title": "Test"}
    created = client.post("/task", json=payload)
    assert created.status_code == 200
    task = created.json()
    assert task["id"] == 1
    listed = client.get("/task")
    assert listed.status_code == 200
    assert listed.json() == [task]
