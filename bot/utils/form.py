from abc import ABC, ABCMeta, abstractclassmethod, abstractmethod
from dataclasses import Field, dataclass
from typing import Any, Dict, Optional, Type, TypeVar

from aiogram import F, types
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.magic_filter import MagicFilter

# TODO: support for pattern enter message like
#       class SomeForm(Form, enter_message_pattern="Enter {field_name}")

# TODO: support for custom filters

# TODO: support for enter message callback

TForm = TypeVar("TForm", bound="Form")


class FormState(StatesGroup):
    waiting_field_value = State()


@dataclass
class FormFieldInfo:
    enter_message_text: str
    filter: Optional[MagicFilter]


def FormField(*, enter_message_text: str, filter: Optional[MagicFilter] = None) -> Any:
    return FormFieldInfo(enter_message_text=enter_message_text, filter=filter)


@dataclass
class _FormFieldData:
    name: str
    type: Any
    info: FormFieldInfo


class _ObjectFromDict:
    def __init__(self, values: Dict[Any, Any]):
        self.__dict__.update(values)


class Form(metaclass=ABCMeta):
    @classmethod
    def __current_field_generator(cls):
        for field_name, field_type in cls.__annotations__.items():
            field_info = getattr(cls, field_name)

            if not isinstance(field_info, FormFieldInfo):
                continue

            field_data = _FormFieldData(field_name, field_type, field_info)
            yield field_data

    @classmethod
    def __get_filter_from_type(cls, field_type: Type):
        default_filters = {
            str: F.text,
            int: F.text.func(int),
        }

        field_filter = default_filters.get(field_type)

        if field_filter is None:
            raise ValueError("This field type is not supported yet")

        return field_filter

    @classmethod
    async def start(
        cls,
        router: Router,
        state_ctx: FSMContext,
    ):
        field_generator = cls.__current_field_generator()
        first_field: _FormFieldData = next(field_generator)
        await state_ctx.set_state(FormState.waiting_field_value)
        await state_ctx.update_data(current_field=first_field, values={})

        async def resolve_callback(
            message: types.Message, state: FSMContext, value: Any, **data
        ):
            state_data = await state.get_data()
            current_field: _FormFieldData = state_data["current_field"]
            state_data["values"][current_field.name] = value
            await state.set_data(state_data)

            try:
                next_field = next(field_generator)
                await state.update_data(current_field=next_field)
            except StopIteration:
                state_data = await state.get_data()
                await state.clear()
                data_object = _ObjectFromDict(state_data["values"])
                return await cls.done(state_ctx.key.chat_id, data_object, **data)  # type: ignore

            await message.answer(next_field.info.enter_message_text)

        async def current_field_filter(message: types.Message, state: FSMContext):
            state_data = await state.get_data()
            current_field: _FormFieldData = state_data["current_field"]

            field_filter = current_field.info.filter or cls.__get_filter_from_type(
                current_field.type
            )

            filter_result = field_filter.resolve(message)
            return {"value": filter_result}

        if not getattr(cls, "__registered", False):
            router.message.register(
                resolve_callback, FormState.waiting_field_value, current_field_filter
            )

            cls.__registered = True

        await state_ctx.bot.send_message(
            state_ctx.key.chat_id, first_field.info.enter_message_text
        )

    @classmethod
    async def done(cls: Type[TForm], chat_id: int, form_data: TForm, **data):
        ...
