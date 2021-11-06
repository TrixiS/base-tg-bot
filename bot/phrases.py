from typing import *

from pydantic import BaseModel, Field

from bot import root_path


class BotPhrases(BaseModel):
    __lang_code__: str = None

    bot_started: str = Field("Бот {bot.full_name} запущен")
    start_message: str = Field("Remove or update the start message")

    @classmethod
    def load_all(cls) -> List["BotPhrases"]:
        phrases_dir = root_path / "phrases"
        parsed_phrases: List[BotPhrases] = []

        for phrases_path in phrases_dir.glob("*.json"):
            phrases = BotPhrases.parse_file(phrases_path)
            parsed_phrases.append(phrases)

        return parsed_phrases
