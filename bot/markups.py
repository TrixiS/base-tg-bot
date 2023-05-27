from aiogram import types
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .phrases import phrases

remove_markup = types.ReplyKeyboardRemove(remove_keyboard=True)
