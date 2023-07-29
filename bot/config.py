from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict, sources

from . import ENCODING
from .utils.paths import ROOT_PATH

DEV_ENV_FILEPATH = ROOT_PATH / ".env.dev"
PROD_ENV_FILEPATH = ROOT_PATH / ".env"


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    bot_token: str = "API токен бота из https://t.me/BotFather"  # type: ignore
    admin_user_id: int | str = "ID администратора бота из https://t.me/userinfobot"
    database_uri: str = "sqlite://database.sqlite3"

    @classmethod
    def from_file(cls, path: Path):
        content = sources.read_env_file(path, encoding=ENCODING)
        return cls.model_validate(content)


if DEV_ENV_FILEPATH.exists():
    config = Config.from_file(DEV_ENV_FILEPATH)
else:
    config = Config.from_file(PROD_ENV_FILEPATH)
