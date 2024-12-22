from dataclasses import dataclass


@dataclass(frozen=True)
class BotPhrases:
    start_message_text = "..."


phrases = BotPhrases()
