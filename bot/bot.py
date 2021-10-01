import asyncio

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot import config

bot = Bot(loop=asyncio.get_event_loop(), token=config.bot_token)
dispatcher = Dispatcher(bot, loop=bot.loop, storage=MemoryStorage())
