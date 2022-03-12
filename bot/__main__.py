import logging

from aiogram import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from . import root_path
from .bot import bot, dispatcher

handlers_path = root_path / "bot" / "handlers"


def load_handlers():
    for filepath in handlers_path.glob("*.py"):
        __import__(f"bot.handlers.{filepath.stem}")


def main():
    log_filename = str((root_path / "logs.log").resolve())

    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format=r"%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s",
    )

    logger = logging.getLogger("bot")
    dispatcher.middleware.setup(LoggingMiddleware(logger=logger))

    load_handlers()

    async def on_startup(*_):
        me = await bot.get_me()
        print(bot.phrases.bot_started.format(bot=me))

    executor.start_polling(
        dispatcher,
        skip_updates=False,
        loop=bot.loop,
        on_startup=on_startup,
    )


main()
