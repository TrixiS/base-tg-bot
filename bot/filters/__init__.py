from aiogram import types

from ..settings import settings


async def admin_filter(telegram_object: types.CallbackQuery | types.Message):
    return (
        telegram_object.from_user
        and telegram_object.from_user.id == settings.admin_user_id
    )
