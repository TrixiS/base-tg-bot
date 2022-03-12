from pydantic import BaseModel, Field

from bot import root_path


class BaseBotConfig(BaseModel):
    __config_filenames__ = ("_config_dev.json", "config.json")

    @classmethod
    def __config_filepaths__(cls):
        for config_filename in cls.__config_filenames__:
            yield root_path / config_filename

    @classmethod
    def load_first(cls):
        for config_filepath in cls.__config_filepaths__():
            if config_filepath.exists():
                return cls.parse_file(config_filepath)


class BotConfig(BaseBotConfig):
    bot_token: str = Field("API токен из @BotFather")
    admin_username: str = Field("Username администратора бота")
