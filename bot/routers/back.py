from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from ..phrases import phrases
from . import root_router

router = Router()
root_router.include_router(router)


@router.message(F.text == phrases.back_button_text)
async def back_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(phrases.start_message_text)
