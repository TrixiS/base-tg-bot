from typing import Any, Awaitable, Callable

from aiogram import types
from tortoise import Tortoise

from ..config import config
from ..database.models import BotUser
from ..utils.services import Service

TORTOISE_ORM = {
    "connections": {"default": config.database_uri},
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
    handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
    event: types.TelegramObject,
    data: dict[str, Any],
) -> Any:
    from_user: types.User | None = getattr(event, "from_user", None)

    if from_user is None:
        raise TypeError(f"{event.__class__.__name__} has no 'from_user' attribute")

    bot_user = await BotUser.get_or_none(id=from_user.id)

    if bot_user is None:
        bot_user = await BotUser.create(
            id=from_user.id,
            username=from_user.username,
            full_name=from_user.full_name,
        )
    elif (
        from_user.username != bot_user.username
        or from_user.full_name != bot_user.full_name
    ):
        bot_user.full_name = from_user.full_name  # type: ignore
        bot_user.username = from_user.username  # type: ignore
        await bot_user.save()

    data["bot_user"] = bot_user
    return await handler(event, data)
