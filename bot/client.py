import asyncio
import logging

from aiogram import exceptions
from aiogram.client.bot import Bot as _Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from .config import config

TELEGRAM_REQUEST_TIMEOUT_SECONDS = 2 * 60


class Bot(_Bot):
    async def __call__(self, *args, **kwargs):
        while True:
            try:
                return await super().__call__(*args, **kwargs)
            except exceptions.TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except (
                exceptions.TelegramNetworkError,
                asyncio.exceptions.TimeoutError,
            ) as e:
                logging.error(e, exc_info=True)


bot = Bot(
    token=config.bot_token,
    default=DefaultBotProperties(parse_mode="HTML"),
    session=AiohttpSession(timeout=TELEGRAM_REQUEST_TIMEOUT_SECONDS),
)
