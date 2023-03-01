from dataclasses import dataclass

from .admin_phrases import AdminPhrases


@dataclass
class BotPhrases:
    admin = AdminPhrases()
    bot_started = "Бот {me.username} успешно запущен"
    start_message_text = "..."


phrases = BotPhrases()
