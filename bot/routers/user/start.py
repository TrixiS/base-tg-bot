from aiogram import F, types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from ... import markups
from ...bot import bot
from ...database.models import BotUser
from ...phrases import phrases
from . import router


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(phrases.start_message)
