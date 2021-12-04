from aiogram import types

from ..bot import bot, dispatcher


@dispatcher.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(bot.phrases.start_message)
