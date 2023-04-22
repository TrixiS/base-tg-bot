from typing import Any, Awaitable, Callable

from prisma.models import BotUser

from prisma import Prisma

from .protocols import TelegramUserEvent
from .services.base import Service


class DatabaseService(Service):
    def __init__(self):
        self._prisma = Prisma(auto_register=True)

    async def setup(self):
        await self._prisma.connect()

    async def dispose(self):
        await self._prisma.disconnect()


async def bot_user_middleware(
    handler: Callable[[TelegramUserEvent, dict[str, Any]], Awaitable[Any]],
    event: TelegramUserEvent,
    data: dict[str, Any],
) -> Any:
    if event.from_user is None:
        return

    bot_user = await BotUser.prisma().upsert(
        where={"id": event.from_user.id},
        data={
            "create": {
                "id": event.from_user.id,
                "username": event.from_user.username,
                "full_name": event.from_user.full_name,
            },
            "update": {
                "username": event.from_user.username,
                "full_name": event.from_user.full_name,
            },
        },
    )

    data["bot_user"] = bot_user
    return await handler(event, data)
