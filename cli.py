import os
import sys
from pathlib import Path

import typer

from bot import ENCODING, root_path
from bot.models.config.bot_config import BotConfig
from bot.models.phrases.bot_phrases import BotPhrases

app = typer.Typer()


@app.command()
def dev():
    for config_filepath in BotConfig.__filepaths__():
        create_json_file(config_filepath)
        BotConfig.refresh(config_filepath)


@app.command()
def update():
    for config_filepath in BotConfig.__exist_filepaths__():
        BotConfig.update(config_filepath)

    for phrases_filepath in BotPhrases.__exist_filepaths__():
        BotPhrases.update(phrases_filepath)


@app.command()
def refresh():
    for config_filepath in BotConfig.__exist_filepaths__():
        if config_filepath.name.startswith("_"):
            continue

        BotConfig.refresh(config_filepath)

    for phrases_filepath in BotPhrases.__exist_filepaths__():
        BotPhrases.refresh(phrases_filepath)

    os.system(f"{sys.executable} -m pip freeze > requirements.txt")


# TODO: router command
# TODO: update handler command to the new structure
@app.command()
def handler(name: str, jump: bool = False):
    handlers_dirpath = root_path / "bot/handlers"
    hander_path = create_handler(handlers_dirpath, name)

    if jump:
        os.system(f"code {hander_path.absolute()}")


def create_json_file(filepath: Path) -> bool:
    if filepath.exists():
        return False

    filepath.write_text(r"{}", encoding="utf")
    return True


def create_handler(handlers_dirpath: Path, handler_name: str):
    HANDLER_CODE = """from aiogram import types

from ..bot import dispatcher, bot
"""

    handler_path = handlers_dirpath / f"{handler_name.lower()}.py"
    handler_path.write_text(HANDLER_CODE, ENCODING)
    return handler_path


if __name__ == "__main__":
    app()
