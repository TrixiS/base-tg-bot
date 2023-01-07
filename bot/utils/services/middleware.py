from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, types

from ..dispatcher import Dispatcher


class ServicesMiddleware(BaseMiddleware):
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data.update(self.dispatcher.services._services)
        return await handler(event, data)
