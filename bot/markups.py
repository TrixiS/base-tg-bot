from aiogram import types
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .bot import bot

remove_markup = types.ReplyKeyboardRemove(remove_keyboard=True)
