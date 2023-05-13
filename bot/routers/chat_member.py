import datetime

from aiogram import F, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter

from ..database.models import BotChat, BotUser
from ..utils.router import Router
from . import root_router

router = Router()
root_router.include_router(router)


@router.chat_member(
    F.chat.type == "private", ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def joined_user_handler(_: types.ChatMemberUpdated, bot_user: BotUser):
    await BotUser.filter(id=bot_user.id).update(
        joined_at=datetime.datetime.utcnow(), left_at=None
    )


@router.chat_member(
    F.chat.type == "private", ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def left_user_handler(_: types.ChatMemberUpdated, bot_user: BotUser):
    await BotUser.filter(id=bot_user.id).update(left_at=datetime.datetime.utcnow())


@router.my_chat_member(
    F.chat.type != "private", ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def new_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.update_or_create(
        dict(
            title=update.chat.title,
            username=update.chat.username,
            type=update.chat.type,
        ),
        id=update.chat.id,
    )


@router.my_chat_member(
    F.chat.type != "private", ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def removed_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.filter(id=update.chat.id).delete()
