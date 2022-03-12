from typing import *

from pydantic import BaseModel, Field

from bot import root_path


class BaseBotPhrases(BaseModel):
    __lang_code__: str = None

    @classmethod
    def __phrases_filepaths__(cls):
        yield from (root_path / "phrases").glob("*.json")

    @classmethod
    def load_all(cls) -> List["BotPhrases"]:
        parsed_phrases: List[BotPhrases] = []

        for phrases_filepath in cls.__phrases_filepaths__():
            phrases = BotPhrases.parse_file(phrases_filepath)
            parsed_phrases.append(phrases)

        return parsed_phrases


class BotPhrases(BaseBotPhrases):
    bot_started: str = Field("Бот {bot.full_name} запущен")
    start_message: str = Field("Remove or update the start message")
