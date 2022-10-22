import datetime

from aiogram import Dispatcher, F, types
from aiogram.fsm.context import FSMContext

from ... import markups
from ...bot import bot
from ...services.database.models import BotUser
from ...utils.form import Form, FormField
from . import router


class TestForm(Form):
    # photo: types.PhotoSize = FormField(enter_message_text="Enter photo")
    document: types.Document = FormField(enter_message_text="Enter document")

    async def submit(self, **data):
        await bot.send_document(data["event_chat"].id, self.document.file_id)


@router.message(F.text == "/form")
async def form_handler(message: types.Message, state: FSMContext):
    await TestForm.start(router, state)
