import logging

from . import root_path, routers
from .bot import bot, dispatcher


def import_routers():
    routers_path = root_path / "bot/routers"

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

    # TODO: handler middlewares
    # TODO: test sql model as middleware

    import_routers()
    dispatcher.include_router(routers.root_handlers_router)

    used_update_types = dispatcher.resolve_used_update_types()
    dispatcher.run_polling(bot, allowed_updates=used_update_types)


main()
