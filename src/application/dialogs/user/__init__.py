from aiogram import Router

from . import payment, sponsor, locale, menu

router = Router()
router.include_routers(
    payment.dialog,
    sponsor.dialog,
    locale.dialog,
    menu.dialog
)
