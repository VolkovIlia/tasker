"""Minimal stub of the python-telegram-bot package used for testing.

Only the parts required by the unit tests are implemented.
"""
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class BotCommand:
    """Represents a Telegram bot command and its description."""
    command: str
    description: str


class Bot:
    """Very small subset of the ``python-telegram-bot`` Bot API."""

    def __init__(self, token: str):
        self.token = token
        self.commands: List[BotCommand] = []
        self.sent_messages: List[Tuple[int, str]] = []

    def set_my_commands(self, commands: List[BotCommand]) -> None:
        """Store the list of supported commands for later inspection."""
        self.commands = commands

    def send_message(self, chat_id: int, text: str) -> None:
        """Record outgoing messages without performing network IO."""
        self.sent_messages.append((chat_id, text))
