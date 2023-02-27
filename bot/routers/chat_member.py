import datetime

from aiogram import F, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.fsm.context import FSMContext

from .. import markups
from ..bot import bot
from ..database.models import BotChat, BotUser
from ..phrases import phrases
from ..utils.router import Router
from . import root_router

router = Router()
root_router.include_router(router)


@router.chat_member(
    F.chat.type == "private", ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def joined_user_handler(update: types.ChatMemberUpdated, bot_user: BotUser):
    bot_user.joined_at = datetime.datetime.utcnow()  # type: ignore
    bot_user.left_at = None  # type: ignore
    await bot_user.save()


@router.chat_member(
    F.chat.type == "private", ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def left_user_handler(update: types.ChatMemberUpdated, bot_user: BotUser):
    bot_user.left_at = datetime.datetime.utcnow()  # type: ignore
    await bot_user.save()


@router.my_chat_member(
    F.chat.type != "private", ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def new_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.create(
        id=update.chat.id,
        title=update.chat.title,
        username=update.chat.username,
        type=update.chat.type,
    )


@router.my_chat_member(
    F.chat.type != "private", ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def removed_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.filter(id=update.chat.id).delete()
