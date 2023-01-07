import os
import sys
from pathlib import Path
from typing import Iterable

import typer

from bot import ENCODING
from bot.settings import Settings
from bot.utils.paths import ROOT_PATH, ROUTERS_PATH

app = typer.Typer()


@app.command()
def dev():
    for path in filepath_generator(Settings.Config.env_file):
        path.touch(exist_ok=True)

    update_settings()


@app.command()
def update():
    update_settings()


@app.command()
def refresh():
    refresh_settings()
    os.system(f"{sys.executable} -m pip freeze > requirements.txt")


@app.command()
def router(name: str, file: bool = False, jump: bool = False):
    FILE_ROUTER_CODE = """from aiogram import F, types
from aiogram.fsm.context import FSMContext

from .. import markups
from ..bot import bot
from ..phrases import phrases
from ..database.models import BotUser
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
from ...phrases import phrases
from ...database.models import BotUser
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


def filepath_generator(filenames: Iterable[Path]):
    yield from map(lambda filename: ROOT_PATH / filename, filenames)


def write_settings_files(text: str, filenames: Iterable[Path] | None = None):
    for path in filepath_generator(filenames or Settings.Config.env_file):
        path.write_text(text, encoding=ENCODING)


def update_settings():
    schema = Settings.schema()
    settings_object = Settings()

    def settings_properties_values_generator():
        for prop in schema["properties"].keys():
            value = getattr(settings_object, prop)
            yield prop, value

    write_settings_files(
        "\n".join(
            f"{prop.upper()}={value}"
            for prop, value in settings_properties_values_generator()
        ),
    )


def refresh_settings():
    schema = Settings.schema()

    def settings_properties_defaults_generator():
        for prop in schema["properties"].keys():
            yield prop, schema["properties"][prop]["default"]

    write_settings_files(
        "\n".join(
            f"{prop.upper()}={value}"
            for prop, value in settings_properties_defaults_generator()
        ),
        filter(
            lambda filepath: filepath.suffix != ".dev",
            Settings.Config.env_file,
        ),
    )


if __name__ == "__main__":
    app()
