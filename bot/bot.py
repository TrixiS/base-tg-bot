from aiogram import Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from .config import BotConfig
from .phrases import BotPhrases
from .utils.bot import Bot

config = BotConfig.load_first()
all_phrases = BotPhrases.load_all()

bot = Bot(config, all_phrases, parse_mode="HTML")  # type: ignore
dispatcher = Dispatcher(MemoryStorage())  # type: ignore
