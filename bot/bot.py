import asyncio

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .config import BotConfig
from .phrases import BotPhrases
from .utils.bot import Bot

config = BotConfig.load_first()
all_phrases = BotPhrases.load_all()

bot = Bot(config, all_phrases, loop=asyncio.get_event_loop())
dispatcher = Dispatcher(bot, loop=bot.loop, storage=MemoryStorage())
