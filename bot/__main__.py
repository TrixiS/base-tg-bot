import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from . import database, routers, state
from .client import bot
from .schedule import ScheduleService
from .utils import loader, startup
from .utils.paths import ROOT_PATH
from .utils.services import ServiceManager, ServiceMiddleware

LOGS_FILEPATH = str((ROOT_PATH / "logs.log").resolve())


def setup_logging():
    logging.basicConfig(
        filename=LOGS_FILEPATH,
        level=logging.INFO,
        format=r"%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    logging.getLogger("aiogram.events").setLevel(logging.ERROR)


def setup_services(service_manager: ServiceManager):
    schedule_service = ScheduleService()

    service_manager.register(
        database.DatabaseService(),
        schedule_service,
    )


async def main():
    setup_logging()

    dispatcher = Dispatcher(storage=MemoryStorage())

    dispatcher.message.middleware.register(state.state_data_middleware)
    dispatcher.callback_query.middleware.register(state.state_data_middleware)

    dispatcher.message.middleware.register(database.bot_user_middleware)
    dispatcher.callback_query.middleware.register(database.bot_user_middleware)
    dispatcher.my_chat_member.outer_middleware.register(database.bot_user_middleware)

    service_middleware = ServiceMiddleware()
    dispatcher.message.middleware.register(service_middleware)
    dispatcher.callback_query.middleware.register(service_middleware)

    setup_services(service_middleware.manager)
    await service_middleware.manager.setup_all()

    dispatcher.startup.register(bot.get_me)  # so .me would be cached on startup
    dispatcher.shutdown.register(service_middleware.manager.dispose_all)

    loader.import_routers()
    dispatcher.include_router(routers.root_router)

    used_update_types = dispatcher.resolve_used_update_types()
    await dispatcher.start_polling(bot, allowed_updates=used_update_types)


startup.run(main())
