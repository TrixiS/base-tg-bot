from pydantic import BaseSettings

from . import ENCODING
from .utils.paths import ROOT_PATH


class Settings(BaseSettings):
    bot_token: str = "API токен бота из https://t.me/BotFather"
    admin_user_id: int | str = "ID администратора бота из https://t.me/userinfobot"
    database_uri: str = "sqlite://database.sqlite3"

    class Config:
        env_file = ROOT_PATH / ".env", ROOT_PATH / ".env.dev"
        env_file_encoding = ENCODING


settings = Settings()
