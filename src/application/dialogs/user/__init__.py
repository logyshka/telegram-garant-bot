from aiogram import Router

from . import payment, sponsor

router = Router()
router.include_routers(
    payment.dialog,
    sponsor.dialog,
)
