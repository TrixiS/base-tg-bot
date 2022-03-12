import os
import sys
from pathlib import Path
from typing import Type

import typer
from pydantic import BaseModel

from bot import root_path
from bot.config import BotConfig
from bot.phrases import BotPhrases

app = typer.Typer()


@app.command()
def dev():
    for config_filepath in BotConfig.__config_filepaths__():
        create_json_file(config_filepath)
        fill_file_from_model(config_filepath, BotConfig)


@app.command()
def update():
    for config_filepath in BotConfig.__config_filepaths__():
        if not config_filepath.exists():
            continue

        update_file_from_model(config_filepath, BotConfig)

    for phrases_filepath in BotPhrases.__phrases_filepaths__():
        update_file_from_model(phrases_filepath, BotPhrases)


@app.command()
def refresh():
    for config_filepath in BotConfig.__config_filepaths__():
        if not config_filepath.exists() or config_filepath.name.startswith("_"):
            continue

        fill_file_from_model(config_filepath, BotConfig)

    for phrases_filepath in BotPhrases.__phrases_filepaths__():
        fill_file_from_model(phrases_filepath, BotPhrases)

    os.system(f"{sys.executable} -m pip freeze > requirements.txt")


@app.command()
def handler(name: str, jump: bool = False):
    handlers_dirpath = root_path / "bot/handlers"
    hander_path = create_handler(handlers_dirpath, name)

    if jump:
        os.system(f"code {hander_path.absolute()}")


def create_json_file(filepath: Path) -> bool:
    if filepath.exists():
        return False

    filepath.write_text(r"{}", encoding="utf-8")
    return True


def fill_file_from_model(filepath: Path, model_cls: Type[BaseModel]):
    model_object = model_cls()
    model_json = model_object.json(ensure_ascii=False, indent=2)
    filepath.write_text(model_json, encoding="utf-8")


def update_file_from_model(filepath: Path, model_cls: Type[BaseModel]):
    model_object = model_cls.parse_file(filepath)
    model_json = model_object.json(ensure_ascii=False, indent=2)
    filepath.write_text(model_json, encoding="utf-8")


def create_handler(handlers_dirpath: Path, handler_name: str):
    HANDLER_CODE = """from aiogram import types

from ..bot import dispatcher, bot
"""

    handler_path = handlers_dirpath / f"{handler_name.lower()}.py"
    handler_path.write_text(HANDLER_CODE, "utf-8")
    return handler_path


if __name__ == "__main__":
    app()
