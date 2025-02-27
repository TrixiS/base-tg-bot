from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils.paths import ROOT_PATH

ENCODING = "utf-8"

DEV_ENV_FILEPATH = ROOT_PATH / ".env.dev"
PROD_ENV_FILEPATH = ROOT_PATH / ".env"

current_env_filepath = (
    DEV_ENV_FILEPATH if DEV_ENV_FILEPATH.exists() else PROD_ENV_FILEPATH
)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(current_env_filepath.resolve().absolute()),
        env_file_encoding=ENCODING,
        extra="allow",
    )

    bot_token: str = "API токен бота из https://t.me/BotFather"  # type: ignore
    database_uri: str = "sqlite://database.sqlite3"


config = Config()
