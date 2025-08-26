import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
module_path = ROOT / "services" / "bot" / "main.py"
# Ensure the repository root is on sys.path so the fastapi stub can be imported
sys.path.append(str(ROOT))

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
    ]
