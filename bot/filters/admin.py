from aiogram.filters.base import Filter

from ..protocols import TelegramUserEvent
from ..settings import settings


class AdminFilter(Filter):
    async def __call__(self, telegram_object: TelegramUserEvent):
        return telegram_object.from_user.id == settings.admin_user_id
