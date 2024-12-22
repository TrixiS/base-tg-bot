import os
import threading
from pathlib import Path

import httpx
import rich
import typer
from github import ContentFile, Github
from github.ContentFile import ContentFile
from github.Repository import Repository

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
    os.system("uv export --no-dev --no-hashes > requirements.txt")
    update_env_file(config.PROD_ENV_FILEPATH)
    rich.print(
        "[green]Updated [bold].env[/bold] and [bold]requrements.txt[/bold][/green]"
    )


@app.command("router")
def router(name: str, file: bool = False, jump: bool = False):
    if file:
        router_filepath = paths.ROUTERS_PATH / f"{name}.py"
        router_filepath.write_text(FILE_ROUTER_CODE, encoding=config.ENCODING)
        rich.print(f"[green]Created router in {router_filepath}[/green]")

        if jump:
            jump_to_file(router_filepath)

        return

    router_dirpath = paths.ROUTERS_PATH / name
    init_filepath = router_dirpath / "__init__.py"
    router_dirpath.mkdir(exist_ok=True)
    init_filepath.write_text(DIR_ROUTER_CODE, encoding=config.ENCODING)
    rich.print(f"[green]Created router in {init_filepath}[/green]")

    if jump:
        jump_to_file(init_filepath)


@app.command("handler")
def handler(router: str, name: str, jump: bool = False):
    router_dirpath = paths.ROUTERS_PATH / router

    if not router_dirpath.exists():
        return rich.print(f"[bold red]Router {router} does not exist[/bold red]")

    handler_filepath = router_dirpath / f"{name}.py"

    if handler_filepath.exists():
        rich.print(f"[magenta]Handler {handler_filepath} is already created[/magenta]")
    else:
        handler_filepath.write_text(HANDLER_CODE, encoding=config.ENCODING)
        rich.print(f"[green]Handler {handler_filepath} has been created[/green]")

    if jump:
        jump_to_file(handler_filepath)


@app.command("mod")
def mod_command_handler(module_names: list[str]):
    client = Github()

    repo = client.get_repo("TrixiS/base-tg-bot-modules")
    module_content_files_map = get_module_content_files_map(repo)

    for module_name in module_names:
        try:
            module_content_file = module_content_files_map[module_name]
        except KeyError:
            rich.print(f"[bold red]Module {module_name} not found[/bold red]")
            continue

        threads: list[threading.Thread] = []

        for file in walk_module(repo, module_content_file):
            thread = threading.Thread(
                target=write_module_local_file, args=(module_name, file)
            )

            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    client.close()
    os.system("ruff format .")


def write_module_local_file(module_name: str, file: ContentFile):
    res = httpx.get(file.download_url)

    if res.status_code != 200:
        return rich.print(
            f"[bold red]Failed to download file {file.path} -> {res.reason_phrase}[/bold red]"
        )

    filepath = file.path[len(module_name) :]
    local_filepath = paths.ROOT_PATH / f"bot{filepath}"

    try:
        local_filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(local_filepath, "ab") as f:
            f.write(res.content)
    except Exception as e:
        return rich.print(
            f"[bold red]Failed to write {local_filepath} -> {e}[/bold red]"
        )

    rich.print(f"[green]Written {local_filepath}[/green]")


def walk_module(repo: Repository, module_content_file: ContentFile):
    module_files: list[ContentFile] = repo.get_contents(module_content_file.path)  # type: ignore

    for file in module_files:
        if file.type == "file":
            yield file

        if file.type == "dir":
            yield from walk_module(repo, file)


def get_module_content_files_map(repo: Repository):
    root_contents: list[ContentFile] = repo.get_contents("/")  # type: ignore
    return {f.path: f for f in root_contents if f.type == "dir"}


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
