from aiogram.filters.base import BaseFilter

from ..bot import bot
from ..protocols.telegram_user_event import TelegramUserEvent


class AdminFilter(BaseFilter):
    async def __call__(self, telegram_object: TelegramUserEvent):
        if telegram_object.from_user is None:
            return False

        return telegram_object.from_user.id == bot.config.admin_user_id
