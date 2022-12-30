import logging

from . import middleware, routers, services
from .bot import bot, dispatcher
from .phrases import phrases
from .utils.paths import ROOT_PATH, ROUTERS_PATH


@dispatcher.startup()
async def on_startup():
    await services.setup(dispatcher.services)
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
            if not handler_file_path.is_file():
                continue

            __import__(f"bot.routers.{router_path.stem}.{handler_file_path.stem}")


def main():
    log_filename = str((ROOT_PATH / "logs.log").resolve())

    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format=r"%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s",
    )

    middleware.setup(dispatcher)
    import_routers()
    dispatcher.include_router(routers.root_handlers_router)

    used_update_types = dispatcher.resolve_used_update_types()
    dispatcher.run_polling(bot, allowed_updates=used_update_types)


main()
