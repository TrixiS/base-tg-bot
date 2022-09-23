from aiogram import F, types
from aiogram.fsm.context import FSMContext

from ... import filters, markups
from ...bot import bot
from ...services.database.models import BotUser
from . import router


@router.message(filters.bot_user_filter)
async def bot_user_handler(message: types.Message, target_bot_user: BotUser):
    await message.answer(str(target_bot_user.id))
