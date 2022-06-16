from .database import DatabaseService
from .schedule import ScheduleService, jobs

database_service = DatabaseService()
schedule_service = ScheduleService()


async def setup():
    await database_service.setup()
    await schedule_service.setup()


async def dispose():
    await database_service.dispose()
    await schedule_service.dispose()
