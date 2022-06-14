from aiogram import types

from ...bot import bot
from . import router


@router.message(commands=["start"], state=None)
async def start_handler(message: types.Message):
    await message.answer(bot.phrases.start_message)
