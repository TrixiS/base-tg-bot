from .config import config
from .utils.bot import Bot

bot = Bot(token=config.bot_token, parse_mode="HTML")
