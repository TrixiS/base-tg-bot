import asyncio

from aiogram import exceptions
from aiogram.client.bot import Bot as _Bot

from .config import config


class Bot(_Bot):
    async def __call__(self, *args, **kwargs):
        while True:
            try:
                return await super().__call__(*args, **kwargs)
            except exceptions.TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)


bot = Bot(token=config.bot_token, parse_mode="HTML")
