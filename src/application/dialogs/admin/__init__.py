from aiogram import Router

from . import payment, sponsor
from ...filters import IsAdmin

router = Router()

filters = (IsAdmin(),)
router.message.filter(*filters)
router.callback_query.filter(*filters)

router.include_routers(
    payment.router,
    sponsor.router,
)
