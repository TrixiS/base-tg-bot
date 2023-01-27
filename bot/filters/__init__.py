from ..settings import settings
from ..utils.protocols import TelegramUserEvent


def is_admin(user_id: int):
    return settings.admin_user_id == user_id


async def admin_filter(telegram_object: TelegramUserEvent):
    return telegram_object.from_user and is_admin(telegram_object.from_user.id)
