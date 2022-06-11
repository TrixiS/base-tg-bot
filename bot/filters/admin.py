from typing import Union

from aiogram import types
from aiogram.dispatcher.filters.base import BaseFilter

from ..bot import bot


class AdminFilter(BaseFilter):
    async def __call__(
        self, telegram_object: Union[types.Message, types.CallbackQuery]
    ):
        if telegram_object.from_user is None:
            return False

        return telegram_object.from_user.username == bot.config.admin_username
