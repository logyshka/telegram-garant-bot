from aiogram import Router

from src.application.filters import IsAdmin
from . import locale, info, payment, sponsor

router = Router()
# filters = (IsAdmin(),)
# router.message.filter(*filters)
# router.callback_query.filter(*filters)
router.include_routers(
    locale.router,
    info.router,
    payment.router,
    sponsor.router,
)
