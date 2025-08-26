"""Telegram bot service used in the microservice example.

The real project would expose a Telegram webhook and route messages to
other services.  For the purposes of this kata the service implements a
small subset of the behaviour so that it can be unit tested without any
external dependencies.
"""

from fastapi import FastAPI
from typing import Dict, List

from telegram import Bot, BotCommand


def configure_bot_menu(bot: Bot) -> None:
    """Register the commands shown in the Telegram UI.

    The stub ``Bot`` simply stores the commands, allowing tests to verify
    that the bot would expose the expected menu in a real environment.
    """

    commands: List[BotCommand] = [
        BotCommand("ping", "Health check"),
        BotCommand("who", "Identify bot instance"),
    ]
    bot.set_my_commands(commands)


def create_app(bot_name: str = "bot", bot_username: str | None = None) -> FastAPI:
    """Create and configure a bot service instance.

    Parameters
    ----------
    bot_name:
        Human readable name of the bot, returned by the ``/who`` command.
    bot_username:
        Optional username used to match commands in group chats
        (``/ping@mybot``).
    """
    app = FastAPI()

    @app.get("/")
    def root() -> Dict[str, str]:
        """Health check endpoint used by tests and monitoring."""
        return {"status": "ok"}

    @app.post("/webhook")
    def telegram_webhook(update: Dict) -> Dict[str, str]:
        """Handle incoming Telegram updates.

        The handler understands two simple commands:

        ``/ping``
            Responds with ``{"reply": "pong"}``.
        ``/who``
            Returns the name of the bot instance which is useful for verifying
            load balancing behaviour through the API gateway.
        """
        text = update.get("message", {}).get("text", "")
        command = text.split()[0]

        valid_pings = {"/ping"}
        valid_whos = {"/who"}
        if bot_username:
            valid_pings.add(f"/ping@{bot_username}")
            valid_whos.add(f"/who@{bot_username}")

        if command in valid_pings:
            return {"reply": "pong"}
        if command in valid_whos:
            return {"reply": bot_name}
        return {"reply": "unknown"}

    return app


# The default application used when running ``python main.py``.
app = create_app()
