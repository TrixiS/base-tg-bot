import os
from pathlib import Path
from typing import Any, Iterable

import typer

from bot import ENCODING
from bot.settings import Settings
from bot.utils.paths import ROOT_PATH, ROUTERS_PATH

app = typer.Typer()


@app.command()
def dev():
    for path in generate_filepaths(Settings.Config.env_file):
        path.touch(exist_ok=True)

    update_env_files()


@app.command()
def update():
    os.system(
        "poetry export -f requirements.txt --output requirements.txt --without-hashes"
    )

    update_env_files()


@app.command()
def router(name: str, file: bool = False, jump: bool = False):
    FILE_ROUTER_CODE = """from aiogram import F, types
from aiogram.fsm.context import FSMContext

from .. import markups
from ..bot import bot
from ..database.models import BotUser
from ..phrases import phrases
from ..utils.router import Router
from . import root_router

router = Router()
root_router.include_router(router)
"""

    DIR_ROUTER_CODE = """from ...utils.router import Router
from .. import root_router

router = Router()
root_router.include_router(router)
"""

    if file:
        router_filepath = ROUTERS_PATH / f"{name}.py"
        router_filepath.write_text(FILE_ROUTER_CODE, encoding=ENCODING)
        typer.echo(f"Created router in {router_filepath}")

        if jump:
            jump_to_file(router_filepath)

        return

    router_dirpath = ROUTERS_PATH / name
    init_filepath = router_dirpath / "__init__.py"
    router_dirpath.mkdir(exist_ok=True)
    init_filepath.write_text(DIR_ROUTER_CODE, encoding=ENCODING)
    typer.echo(f"Created router in {init_filepath}")

    if jump:
        jump_to_file(init_filepath)


@app.command()
def handler(router: str, name: str, jump: bool = False):
    HANDLER_CODE = """from aiogram import F, types
from aiogram.fsm.context import FSMContext

from ... import markups
from ...bot import bot
from ...database.models import BotUser
from ...phrases import phrases
from . import router
"""

    router_dirpath = ROUTERS_PATH / router

    if not router_dirpath.exists():
        return typer.echo(f"Router {router} does not exist")

    handler_filepath = router_dirpath / f"{name}.py"

    if handler_filepath.exists():
        typer.echo(f"Handler {handler_filepath} is already created")
    else:
        handler_filepath.write_text(HANDLER_CODE, encoding=ENCODING)
        typer.echo(f"Handler {handler_filepath} has been created")

    if jump:
        jump_to_file(handler_filepath)


def jump_to_file(path: Path):
    os.system(f"code {path.absolute()}")


def generate_filepaths(filenames: Iterable[Path]):
    yield from map(lambda filename: ROOT_PATH / filename, filenames)


def _settings_properties_values_generator(
    schema: dict[str, Any], settings_object: Settings
):
    for prop in schema["properties"].keys():
        value = getattr(settings_object, prop)
        yield prop, value


def update_env_files():
    schema = Settings.schema()

    for env_file in Settings.Config.env_file:
        if not env_file.exists():
            continue

        settings_object = Settings(_env_file=env_file)  # type: ignore

        env_file.write_text(
            "\n".join(
                f"{prop.upper()}={value}"
                for prop, value in _settings_properties_values_generator(
                    schema, settings_object
                )
            ),
            encoding=ENCODING,
        )


if __name__ == "__main__":
    app()
