from aiogram import types

from ..settings import settings


def is_admin(user_id: int):
    return settings.admin_user_id == user_id


async def admin_filter(telegram_object: types.TelegramObject):
    from_user: types.User | None = getattr(telegram_object, "from_user", None)
    return from_user and is_admin(from_user.id)
