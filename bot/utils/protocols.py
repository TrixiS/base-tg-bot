from typing import Protocol

from aiogram import types


class TelegramUserEvent(Protocol):
    from_user: types.User | None
