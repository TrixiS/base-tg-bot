from ...filters.admin import AdminFilter
from ...utils.router import Router
from .. import root_handlers_router

admin_filter = AdminFilter()

router = Router()

router.message.filter(admin_filter)
router.callback_query.filter(admin_filter)

root_handlers_router.include_router(router)
