import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
module_path = ROOT / "services" / "bot" / "main.py"
# Ensure repository root takes precedence on sys.path so stubs are used
sys.path.insert(0, str(ROOT))
sys.modules.pop("telegram", None)

spec = importlib.util.spec_from_file_location("bot_main", module_path)
bot_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot_main)

from fastapi.testclient import TestClient
from telegram import Bot, BotCommand
client = TestClient(bot_main.app)

def test_root_health():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_ping_command():
    resp = client.post("/webhook", json={"message": {"text": "/ping"}})
    assert resp.status_code == 200
    assert resp.json()["reply"] == "pong"


def test_ping_command_in_group_chat():
    """Commands with ``@botname`` should be recognised in group chats."""
    app = bot_main.create_app(bot_username="testbot")
    local_client = TestClient(app)
    resp = local_client.post(
        "/webhook",
        json={"message": {"text": "/ping@testbot", "chat": {"id": 1, "type": "group"}}},
    )
    assert resp.status_code == 200
    assert resp.json()["reply"] == "pong"


def test_configure_bot_menu_registers_commands():
    bot = Bot("dummy-token")
    bot_main.configure_bot_menu(bot)
    assert bot.commands == [
        BotCommand("ping", "Health check"),
        BotCommand("who", "Identify bot instance"),
        BotCommand("task", "Create task"),
    ]


def test_task_command_creates_task_via_gateway():
    recorded: dict = {}

    def fake_task_api(payload: dict) -> dict:
        recorded["payload"] = payload
        return {"id": 1}

    app = bot_main.create_app(task_api=fake_task_api)
    local_client = TestClient(app)
    resp = local_client.post(
        "/webhook",
        json={
            "message": {
                "text": "/task write tests @alice 2024-01-01 #dev #qa",
                "chat": {"id": 42},
            }
        },
    )
    assert resp.status_code == 200
    assert resp.json()["reply"] == "created task 1"
    assert recorded["payload"] == {
        "chat_id": 42,
        "title": "write tests",
        "assignee": "alice",
        "due_at": "2024-01-01",
        "tags": ["dev", "qa"],
    }
