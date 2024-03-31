from aiogram import Router

from ... import filters
from .. import root_router

router = Router()

router.message.filter(filters.admin_filter)
router.callback_query.filter(filters.admin_filter)
root_router.include_router(router)
