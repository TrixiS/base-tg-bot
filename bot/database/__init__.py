from typing import Any, Awaitable, Callable

from tortoise import Tortoise

from ..database.models import BotUser
from ..settings import settings
from ..utils.protocols import TelegramUserEvent
from ..utils.services.base import Service

TORTOISE_ORM = {
    "connections": {"default": settings.database_uri},
    "apps": {
        "models": {
            "models": ["bot.database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class DatabaseService(Service):
    async def setup(self):
        await Tortoise.init(TORTOISE_ORM)
        await Tortoise.generate_schemas()

    async def dispose(self):
        await Tortoise.close_connections()


async def bot_user_middleware(
    handler: Callable[[TelegramUserEvent, dict[str, Any]], Awaitable[Any]],
    event: TelegramUserEvent,
    data: dict[str, Any],
) -> Any:
    if event.from_user is None:
        return

    bot_user, _ = await BotUser.update_or_create(
        dict(username=event.from_user.username, full_name=event.from_user.full_name),
        id=event.from_user.id,
    )

    data["bot_user"] = bot_user
    return await handler(event, data)
