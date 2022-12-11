from aiogram import F, types
from aiogram3_form import Form, FormField
from aiogram.fsm.context import FSMContext

from ... import markups
from ...bot import bot
from ...services.database.models import BotUser
from . import router


class TestForm(Form):
    a: int = FormField(enter_message_text="Enter A")
    b: str = FormField(enter_message_text="Enter B")


@TestForm.submit()
async def test_form_submit_handler(form: TestForm, bot_user: BotUser):
    await bot.send_message(bot_user.id, f"{form.a} {form.b}")


@router.message(F.text == "/form")
async def form_start_handler(message: types.Message, state: FSMContext):
    await TestForm.start(router, state)
