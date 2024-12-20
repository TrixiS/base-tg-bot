from dataclasses import dataclass

from .admin_phrases import AdminPhrases


@dataclass(frozen=True)
class BotPhrases:
    admin = AdminPhrases()
    start_message_text = "..."
    back_button_text = "Назад"


phrases = BotPhrases()
