import asyncio
import logging

from . import routers, state
from .core import bot, dispatcher
from .database import DatabaseService, bot_user_middleware
from .phrases import phrases
from .schedule import ScheduleService
from .utils import loader
from .utils.paths import ROOT_PATH
from .utils.services import ServiceMiddleware


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
    dispatcher.my_chat_member.middleware.register(bot_user_middleware)

    services_middleware = ServiceMiddleware()
    dispatcher.message.middleware.register(services_middleware)
    dispatcher.callback_query.middleware.register(services_middleware)


@dispatcher.startup()
async def on_startup():
    me = await bot.get_me()
    print(phrases.bot_started.format(me=me))


@dispatcher.shutdown()
async def on_shutdown():
    await ServiceMiddleware.manager.dispose_all()


async def main():
    log_filename = str((ROOT_PATH / "logs.log").resolve())

    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format=r"%(asctime)s %(levelname)s %(message)s",
    )

    setup_middleware()
    await setup_services()

    loader.import_routers()
    dispatcher.include_router(routers.root_router)

    used_update_types = dispatcher.resolve_used_update_types()
    await dispatcher.start_polling(bot, allowed_updates=used_update_types)


asyncio.run(main())
