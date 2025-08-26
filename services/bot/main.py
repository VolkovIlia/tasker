"""Telegram bot service used in the microservice example.

The real project would expose a Telegram webhook and route messages to
other services.  For the purposes of this kata the service implements a
small subset of the behaviour so that it can be unit tested without any
external dependencies.
"""

from fastapi import FastAPI
from typing import Callable, Dict, List, Any
import re

from telegram import Bot, BotCommand


def configure_bot_menu(bot: Bot) -> None:
    """Register the commands shown in the Telegram UI.

    The stub ``Bot`` simply stores the commands, allowing tests to verify
    that the bot would expose the expected menu in a real environment.
    """

    commands: List[BotCommand] = [
        BotCommand("ping", "Health check"),
        BotCommand("who", "Identify bot instance"),
        BotCommand("task", "Create task"),
    ]
    bot.set_my_commands(commands)


def create_app(
    bot_name: str = "bot",
    bot_username: str | None = None,
    task_api: Callable[[Dict[str, Any]], Dict[str, Any]] | None = None,
) -> FastAPI:
    """Create and configure a bot service instance.

    Parameters
    ----------
    bot_name:
        Human readable name of the bot, returned by the ``/who`` command.
    bot_username:
        Optional username used to match commands in group chats
        (``/ping@mybot``).
    task_api:
        Callable used to create tasks via the API gateway.  The callable
        receives the task payload and should return the created task as a
        dictionary.  If ``None`` the ``/task`` command is disabled.
    """
    app = FastAPI()

    @app.get("/")
    def root() -> Dict[str, str]:
        """Health check endpoint used by tests and monitoring."""
        return {"status": "ok"}

    @app.post("/webhook")
    def telegram_webhook(update: Dict) -> Dict[str, str]:
        """Handle incoming Telegram updates.

        The handler understands three simple commands:

        ``/ping``
            Responds with ``{"reply": "pong"}``.
        ``/who``
            Returns the name of the bot instance which is useful for verifying
            load balancing behaviour through the API gateway.
        ``/task``
            Parses the message, forwards the task to the API gateway and
            replies with the created task identifier.
        """
        text = update.get("message", {}).get("text", "")
        command = text.split()[0]

        valid_pings = {"/ping"}
        valid_whos = {"/who"}
        valid_tasks = {"/task"}
        if bot_username:
            valid_pings.add(f"/ping@{bot_username}")
            valid_whos.add(f"/who@{bot_username}")
            valid_tasks.add(f"/task@{bot_username}")

        if command in valid_pings:
            return {"reply": "pong"}
        if command in valid_whos:
            return {"reply": bot_name}
        if command in valid_tasks and task_api:
            chat_id = update.get("message", {}).get("chat", {}).get("id")
            payload = parse_task_command(text)
            payload["chat_id"] = chat_id
            task = task_api(payload)
            return {"reply": f"created task {task['id']}"}
        return {"reply": "unknown"}

    return app


def parse_task_command(text: str) -> Dict[str, Any]:
    """Parse ``/task`` command arguments into a payload dictionary.

    Expected format::

        /task title @assignee YYYY-MM-DD #tag1 #tag2

    Only the title is required; other components are optional.
    """
    tokens = text.split()
    title_parts: List[str] = []
    assignee = None
    due_at = None
    tags: List[str] = []
    for token in tokens[1:]:
        if token.startswith("@"):
            assignee = token[1:]
        elif token.startswith("#"):
            tags.append(token[1:])
        elif re.match(r"\d{4}-\d{2}-\d{2}", token):
            due_at = token
        else:
            title_parts.append(token)
    payload: Dict[str, Any] = {"title": " ".join(title_parts)}
    if assignee:
        payload["assignee"] = assignee
    if due_at:
        payload["due_at"] = due_at
    if tags:
        payload["tags"] = tags
    return payload


# The default application used when running ``python main.py``.
app = create_app()
