from aiogram import Router

from src.application.filters import IS_OWNER
from . import locale, info, payment, sponsor, role, ban

router = Router()

filters = (IS_OWNER,)
router.message.filter(*filters)
router.callback_query.filter(*filters)

router.include_routers(
    locale.router,
    info.router,
    payment.router,
    sponsor.router,
    role.router,
    ban.router,
)
