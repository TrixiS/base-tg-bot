import logging

from aiogram import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot import root_path, phrases
from .bot import bot, dispatcher

log_filename = str((root_path / "logs.log").resolve())

logging.basicConfig(
    filename=log_filename,
    level=logging.ERROR,
    format=r"%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s",
)

logger = logging.getLogger("bot")
dispatcher.middleware.setup(LoggingMiddleware(logger=logger))


async def on_startup(*_):
    me = await bot.get_me()
    print(phrases.bot_started.format(bot=me))


executor.start_polling(
    dispatcher,
    skip_updates=False,
    loop=bot.loop,
    on_startup=on_startup,
)
