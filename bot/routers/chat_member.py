import datetime

from aiogram import F, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from prisma.models import BotChat, BotUser

from ..utils.router import Router
from . import root_router

router = Router()
root_router.include_router(router)


@router.chat_member(
    F.chat.type == "private", ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def joined_user_handler(_: types.ChatMemberUpdated, bot_user: BotUser):
    await BotUser.prisma().update(
        where={"id": bot_user.id},
        data={"joined_at": datetime.datetime.utcnow(), "left_at": None},
    )


@router.chat_member(
    F.chat.type == "private", ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def left_user_handler(_: types.ChatMemberUpdated, bot_user: BotUser):
    await BotUser.prisma().update(
        where={"id": bot_user.id},
        data={"joined_at": datetime.datetime.utcnow(), "left_at": None},
    )


@router.my_chat_member(
    F.chat.type != "private", ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def new_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.prisma().create(
        data={
            "id": update.chat.id,
            "title": update.chat.title,
            "username": update.chat.username,
            "type": update.chat.type,
        }
    )


@router.my_chat_member(
    F.chat.type != "private", ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def removed_chat_handler(update: types.ChatMemberUpdated):
    await BotChat.prisma().delete(where={"id": update.chat.id})
