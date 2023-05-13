import asyncio
import logging

from . import routers, state
from .bot import bot, dispatcher
from .database import DatabaseService, bot_user_middleware
from .phrases import phrases
from .schedule import ScheduleService
from .utils.paths import ROOT_PATH, ROUTERS_PATH
from .utils.services.middleware import ServicesMiddleware


async def setup_services():
    schedule_service = ScheduleService()

    await dispatcher.services.register(DatabaseService(), schedule_service).setup_all()


def setup_middleware():
    dispatcher.message.middleware.register(state.state_data_middleware)
    dispatcher.callback_query.middleware.register(state.state_data_middleware)

    dispatcher.message.middleware.register(bot_user_middleware)  # type: ignore
    dispatcher.callback_query.middleware.register(bot_user_middleware)  # type: ignore
    dispatcher.my_chat_member.middleware.register(bot_user_middleware)  # type: ignore

    services_di_middleware = ServicesMiddleware(dispatcher)
    dispatcher.message.middleware.register(services_di_middleware)
    dispatcher.callback_query.middleware.register(services_di_middleware)


@dispatcher.startup()
async def on_startup():
    me = await bot.get_me()
    print(phrases.bot_started.format(me=me))


@dispatcher.shutdown()
async def on_shutdown():
    await dispatcher.services.dispose_all()


def import_routers():
    for router_path in ROUTERS_PATH.glob("*"):
        if router_path.stem.startswith("__") and router_path.stem.endswith("__"):
            continue

        if router_path.is_file():
            __import__(f"bot.routers.{router_path.stem}")
            continue

        sorted_handler_file_paths = sorted(
            router_path.glob("*.*"), key=lambda p: p.stem
        )

        for handler_file_path in sorted_handler_file_paths:
            if not handler_file_path.is_file() or (
                handler_file_path.stem.startswith("__")
                and handler_file_path.stem.endswith("__")
            ):
                continue

            __import__(f"bot.routers.{router_path.stem}.{handler_file_path.stem}")


async def main():
    log_filename = str((ROOT_PATH / "logs.log").resolve())

    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format=r"%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s",
    )

    setup_middleware()
    await setup_services()

    import_routers()
    dispatcher.include_router(routers.root_router)

    used_update_types = dispatcher.resolve_used_update_types()
    await dispatcher.start_polling(bot, allowed_updates=used_update_types)


asyncio.run(main())
