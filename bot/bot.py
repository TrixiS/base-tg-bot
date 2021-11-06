import asyncio

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .config import BotConfig
from .phrases import BotPhrases

config = BotConfig.load_first()
all_phrases = BotPhrases.load_all()
phrases = all_phrases[0]

bot = Bot(loop=asyncio.get_event_loop(), token=config.bot_token)
dispatcher = Dispatcher(bot, loop=bot.loop, storage=MemoryStorage())
