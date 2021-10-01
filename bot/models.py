from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    bot_token: str = Field("API токен из @BotFather")


class PhrasesModel(BaseModel):
    bot_started: str = Field("Бот {bot.full_name} запущен")
