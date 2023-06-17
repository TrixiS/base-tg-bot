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
        raise TypeError(f"{event.__class__.__name__}.from_user is None")

    bot_user = await BotUser.get_or_none(id=event.from_user.id)

    if bot_user is None:
        bot_user = await BotUser.create(
            id=event.from_user.id,
            username=event.from_user.username,
            full_name=event.from_user.full_name,
        )
    elif (
        event.from_user.username != bot_user.username
        or event.from_user.full_name != bot_user.full_name
    ):
        bot_user.full_name = event.from_user.full_name  # type: ignore
        bot_user.username = event.from_user.username  # type: ignore
        await bot_user.save()

    data["bot_user"] = bot_user
    return await handler(event, data)
