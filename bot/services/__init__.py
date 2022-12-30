from .database import DatabaseService
from .manager import ServiceManager
from .schedule import ScheduleService, jobs


async def setup(manager: ServiceManager):
    schedule_service = ScheduleService()

    manager.register(DatabaseService())
    manager.register(schedule_service)

    await manager.setup_all()
