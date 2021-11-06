from typing import List

from aiogram.bot import Bot as BaseBot

from ..config import BotConfig
from ..phrases import BotPhrases


class Bot(BaseBot):
    def __init__(self, config: BotConfig, phrases: List[BotPhrases], *args, **kwargs):
        super().__init__(*args, token=config.bot_token, **kwargs)
        self.config = config
        self.all_phrases = phrases

    @property
    def phrases(self) -> BotPhrases:
        return self.all_phrases[0]
