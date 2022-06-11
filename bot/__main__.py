import logging

from . import middleware, root_path, routers, routers_path, services
from .bot import bot, dispatcher


@dispatcher.startup()
async def on_startup():
    await services.setup()
    me = await bot.get_me()
    print(bot.phrases.bot_started.format(me=me))


@dispatcher.shutdown()
async def on_shutdown():
    await services.dispose()


def import_routers():
    for router_dir_path in routers_path.glob("*"):
        if not router_dir_path.is_dir() or (
            router_dir_path.stem.startswith("__")
            and router_dir_path.stem.endswith("__")
        ):
            continue

        for router_file_path in router_dir_path.glob("*.*"):
            if not router_file_path.is_file():
                continue

            __import__(f"bot.routers.{router_dir_path.stem}.{router_file_path.stem}")


def main():
    log_filename = str((root_path / "logs.log").resolve())

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
