from typing import Callable, Iterable, TypeVar

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from . import phrases

_T = TypeVar("_T")


def _create_list_markup_builder(
    it: Iterable[_T], cb: Callable[[_T], tuple[str, CallbackData]]
):
    builder = InlineKeyboardBuilder()

    for i in it:
        text, cb_data = cb(i)
        builder.button(text=text, callback_data=cb_data.pack())

    return builder


def create_list_markup(
    it: Iterable[_T], cb: Callable[[_T], tuple[str, CallbackData]]
) -> types.InlineKeyboardMarkup:
    return _create_list_markup_builder(it, cb).adjust(1, repeat=True).as_markup()  # type: ignore
