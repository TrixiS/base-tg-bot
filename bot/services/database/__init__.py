from tortoise import Tortoise

from ...bot import bot
from . import models


async def setup():
    await Tortoise.init(
        modules={"models": ["bot.services.database.models"]},
        db_url=bot.config.database_uri,
    )

    await Tortoise.generate_schemas()


async def dispose():
    await Tortoise.close_connections()
