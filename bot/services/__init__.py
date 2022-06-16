from .database import DatabaseService

database_service = DatabaseService()


async def setup():
    await database_service.setup()


async def dispose():
    await database_service.dispose()
