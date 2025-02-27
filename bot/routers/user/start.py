from aiogram import F, types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from ... import markups, phrases
from ...client import bot
from . import router


@router.message(CommandStart())
async def start_command_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(phrases.start_message_text)
