from aiogram import F, types
from aiogram.dispatcher.fsm.context import FSMContext

from ... import markups, state
from ...bot import bot
from ...services.database.models import BotUser
from . import router


@router.message(commands=["start"], state=None)
async def start_handler(message: types.Message):
    await message.answer(bot.phrases.start_message)
