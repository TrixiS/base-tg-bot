from tortoise import Tortoise

from ...settings import settings
from ..base import Service

TORTOISE_ORM = {
    "connections": {"default": settings.database_uri},
    "apps": {
        "models": {
            "models": ["bot.services.database.models", "aerich.models"],
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
