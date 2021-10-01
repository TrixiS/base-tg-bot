from aiogram import types

from ..bot import dispatcher


@dispatcher.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Remove or update the start handler")
