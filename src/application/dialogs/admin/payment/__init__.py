from aiogram import Router

from . import (
    crypto_bot,
    menu
)

router = Router()
router.include_routers(
    crypto_bot.dialog,
    menu.dialog,
)
