import logging

from . import routers, state
from .core import bot, dispatcher
from .database import DatabaseService, bot_user_middleware
from .schedule import ScheduleService
from .utils import loader, startup
from .utils.paths import ROOT_PATH
from .utils.services import ServiceMiddleware

LOGS_FILEPATH = str((ROOT_PATH / "logs.log").resolve())


def setup_logging():
    logging.basicConfig(
        filename=LOGS_FILEPATH,
        level=logging.INFO,
        format=r"%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    logging.getLogger("aiogram.events").setLevel(logging.ERROR)


async def setup_services():
    schedule_service = ScheduleService()

    await ServiceMiddleware.manager.register(
        DatabaseService(), schedule_service
    ).setup_all()


def setup_middleware():
    dispatcher.message.middleware.register(state.state_data_middleware)
    dispatcher.callback_query.middleware.register(state.state_data_middleware)

    dispatcher.message.middleware.register(bot_user_middleware)
    dispatcher.callback_query.middleware.register(bot_user_middleware)
    dispatcher.my_chat_member.outer_middleware.register(bot_user_middleware)

    services_middleware = ServiceMiddleware()
    dispatcher.message.middleware.register(services_middleware)
    dispatcher.callback_query.middleware.register(services_middleware)


@dispatcher.startup()
async def on_startup():
    await bot.get_me()


@dispatcher.shutdown()
async def on_shutdown():
    await ServiceMiddleware.manager.dispose_all()


async def main():
    setup_logging()
    setup_middleware()
    await setup_services()

    loader.import_routers()
    dispatcher.include_router(routers.root_router)

    used_update_types = dispatcher.resolve_used_update_types()
    await dispatcher.start_polling(bot, allowed_updates=used_update_types)


startup.run(main())
