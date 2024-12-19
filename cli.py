import os
from pathlib import Path
from typing import Iterable

import typer

from bot.config import DEV_ENV_FILEPATH, ENCODING, PROD_ENV_FILEPATH, Config
from bot.utils.paths import ROOT_PATH, ROUTERS_PATH

app = typer.Typer()


@app.command()
def update():
    os.system("uv export --no-hashes > requirements.txt")
    update_env_files()


@app.command("r")
@app.command("router")
def router(name: str, file: bool = False, jump: bool = False):
    FILE_ROUTER_CODE = """from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from .. import markups
from ..client import bot
from ..database.models import BotUser
from ..phrases import phrases
from . import root_router

router = Router()
root_router.include_router(router)
"""

    DIR_ROUTER_CODE = """from aiogram import Router

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


@app.command("h")
@app.command("handler")
def handler(router: str, name: str, jump: bool = False):
    HANDLER_CODE = """from aiogram import F, types
from aiogram.fsm.context import FSMContext

from ... import markups
from ...client import bot
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
    settings_object: Config, field_names: Iterable[str]
):
    for field_name in field_names:
        value = getattr(settings_object, field_name)
        yield field_name, value


def update_env_file(filepath: Path):
    settings_object = Config(
        _env_file=str(filepath.absolute()),  # type: ignore
        _env_file_encoding=ENCODING,  # type: ignore
    )

    env_file_content = "\n".join(
        f"{field_name.upper()}={field_value}"
        for field_name, field_value in _settings_properties_values_generator(
            settings_object, settings_object.model_fields.keys()
        )
    )

    env_file_content += "\n"  # trailing new line

    filepath.write_text(
        env_file_content,
        encoding=ENCODING,
    )


def update_env_files():
    update_env_file(PROD_ENV_FILEPATH)
    update_env_file(DEV_ENV_FILEPATH)


if __name__ == "__main__":
    app()
