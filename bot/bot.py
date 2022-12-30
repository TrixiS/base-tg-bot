from aiogram.fsm.storage.memory import MemoryStorage

from .settings import settings
from .utils.bot import Bot
from .utils.dispatcher import Dispatcher

bot = Bot(token=settings.bot_token, parse_mode="HTML")
dispatcher = Dispatcher(storage=MemoryStorage())
