from pydantic import Field

from ..config_model import ConfigModel


class BotPhrases(ConfigModel):
    __filenames__ = ("phrases.json",)

    bot_started: str = Field("Бот {me.username} успешно запущен")
    start_message: str = Field("Remove or update the start handler")
