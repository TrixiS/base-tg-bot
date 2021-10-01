import asyncio

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import root_path
from .models import ConfigModel, PhrasesModel

config_path = root_path / "config.json"
config_dev_path = root_path / "config_dev.json"

config = ConfigModel.parse_file(
    config_dev_path if config_dev_path.exists() else config_path
)

phrases = PhrasesModel.parse_file(root_path / "phrases.json")

bot = Bot(loop=asyncio.get_event_loop(), token=config.bot_token)
dispatcher = Dispatcher(bot, loop=bot.loop, storage=MemoryStorage())
