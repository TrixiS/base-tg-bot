from typing import Any, Awaitable, Callable, Dict

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from ..protocols.telegram_user_event import TelegramUserEvent
from ..services.database.models import BotUser


class BotUserMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[TelegramUserEvent, Dict[str, Any]], Awaitable[Any]],
        event: TelegramUserEvent,
        data: Dict[str, Any],
    ) -> Any:
        from_user: types.User = event.from_user  # type: ignore
        bot_user = await BotUser.get_or_none(id=from_user.id)
        data["bot_user"] = bot_user
        return await handler(event, data)
