from typing import Any, Awaitable, Callable, Dict

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from ..protocols import TelegramUserEvent
from ..services.database.models import BotUser


class BotUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramUserEvent, Dict[str, Any]], Awaitable[Any]],
        event: TelegramUserEvent,
        data: Dict[str, Any],
    ) -> Any:
        bot_user, _ = await BotUser.update_or_create(
            dict(
                username=event.from_user.username, full_name=event.from_user.full_name
            ),
            id=event.from_user.id,
        )

        data["bot_user"] = bot_user
        return await handler(event, data)
