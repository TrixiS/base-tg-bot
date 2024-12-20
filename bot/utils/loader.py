import importlib
import logging
from pathlib import Path

from .paths import ROUTERS_PATH

_LOGGER = logging.getLogger("loader")

ROUTER_PRIORITIES = (
    "back",
    "admin",
    "user",
)


def import_routers():
    router_paths = __get_sorted_router_paths()
    package_name = __name__.split(".")[0]

    for router_path in router_paths:
        router_import_path = __get_router_import_path(package_name, router_path)

        if router_path.is_file():
            _LOGGER.info(f"Importing router {router_import_path}")
            importlib.import_module(router_import_path)
            continue

        for handler_filepath in __get_sorted_handler_paths(router_path):
            handler_import_path = __get_handler_import_path(
                router_import_path, handler_filepath
            )

            _LOGGER.info(f"Importing handler {handler_import_path}")
            importlib.import_module(handler_import_path)


def __get_router_import_path(package_name: str, router_path: Path):
    return f"{package_name}.routers.{router_path.stem}"


def __get_handler_import_path(router_import_path: str, handler_path: Path):
    return f"{router_import_path}.{handler_path.stem}"


def __get_router_priority(router_name: str):
    if router_name in ROUTER_PRIORITIES:
        return ROUTER_PRIORITIES.index(router_name)

    return len(ROUTER_PRIORITIES)


def __get_sorted_router_paths():
    router_paths = filter(lambda p: "__" not in p.name, ROUTERS_PATH.glob("*"))
    return sorted(router_paths, key=lambda p: (__get_router_priority(p.stem), p.stem))


def __get_sorted_handler_paths(router_path: Path):
    handler_paths = filter(
        lambda p: "__" not in p.name and p.is_file(), router_path.glob("*.*")
    )

    return sorted(handler_paths, key=lambda p: p.stem)
