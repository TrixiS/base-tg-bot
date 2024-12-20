import os
from pathlib import Path

import typer

from bot import config
from bot.utils import paths

app = typer.Typer()

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

HANDLER_CODE = """from aiogram import F, types
from aiogram.fsm.context import FSMContext

from ... import markups
from ...client import bot
from ...database.models import BotUser
from ...phrases import phrases
from . import router
"""


@app.command()
def update():
    os.system("uv export --no-hashes > requirements.txt")
    update_env_file(config.PROD_ENV_FILEPATH)
    update_env_file(config.DEV_ENV_FILEPATH)


@app.command("router")
def router(name: str, file: bool = False, jump: bool = False):
    if file:
        router_filepath = paths.ROUTERS_PATH / f"{name}.py"
        router_filepath.write_text(FILE_ROUTER_CODE, encoding=config.ENCODING)
        typer.echo(f"Created router in {router_filepath}")

        if jump:
            jump_to_file(router_filepath)

        return

    router_dirpath = paths.ROUTERS_PATH / name
    init_filepath = router_dirpath / "__init__.py"
    router_dirpath.mkdir(exist_ok=True)
    init_filepath.write_text(DIR_ROUTER_CODE, encoding=config.ENCODING)
    typer.echo(f"Created router in {init_filepath}")

    if jump:
        jump_to_file(init_filepath)


@app.command("handler")
def handler(router: str, name: str, jump: bool = False):
    router_dirpath = paths.ROUTERS_PATH / router

    if not router_dirpath.exists():
        return typer.echo(f"Router {router} does not exist")

    handler_filepath = router_dirpath / f"{name}.py"

    if handler_filepath.exists():
        typer.echo(f"Handler {handler_filepath} is already created")
    else:
        handler_filepath.write_text(HANDLER_CODE, encoding=config.ENCODING)
        typer.echo(f"Handler {handler_filepath} has been created")

    if jump:
        jump_to_file(handler_filepath)


def jump_to_file(path: Path):
    os.system(f"code {path.absolute()}")


def update_env_file(filepath: Path):
    env_file_content = "\n".join(
        f"{name.upper()}={value.default}"
        for name, value in config.Config.model_fields.items()
    )

    env_file_content += "\n"
    filepath.write_text(env_file_content, encoding=config.ENCODING)


if __name__ == "__main__":
    app()
