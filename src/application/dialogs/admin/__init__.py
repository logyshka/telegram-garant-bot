from aiogram import Router

from . import payment, sponsor, role, ban
from ...filters import IS_ADMIN

router = Router()

filters = (IS_ADMIN,)
router.message.filter(*filters)
router.callback_query.filter(*filters)

router.include_routers(
    payment.router,
    sponsor.router,
    role.router,
    ban.router
)
