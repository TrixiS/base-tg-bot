import asyncio
from typing import List

from aiogram import exceptions
from aiogram.client.bot import Bot as AiogramBot

from ..config import BotConfig
from ..phrases import BotPhrases


class Bot(AiogramBot):
    def __init__(self, config: BotConfig, phrases: List[BotPhrases], *args, **kwargs):
        super().__init__(*args, token=config.bot_token, **kwargs)
        self.config = config
        self.all_phrases = phrases

    @property
    def phrases(self) -> BotPhrases:
        return self.all_phrases[0]

    async def __call__(self, *args, **kwargs):
        while True:
            try:
                return await super().__call__(*args, **kwargs)
            except exceptions.TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
