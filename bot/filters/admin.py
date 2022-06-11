from aiogram.dispatcher.filters.base import BaseFilter

from ..bot import bot
from .argument_protocol import BoundFilterArgumentProtocol


class AdminFilter(BaseFilter):
    async def __call__(self, telegram_object: BoundFilterArgumentProtocol):
        if telegram_object.from_user is None:
            return False

        return telegram_object.from_user.id == bot.config.admin_user_id
