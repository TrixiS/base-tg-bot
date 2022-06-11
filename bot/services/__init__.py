from . import database


async def setup():
    await database.setup()


async def dispose():
    await database.dispose()
