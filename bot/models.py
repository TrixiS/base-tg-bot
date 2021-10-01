from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    bot_token: str = Field("")


class PhrasesModel(BaseModel):
    bot_started: str = Field("")
