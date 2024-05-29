from aiogram import Router

from . import admin, user

router = Router()
router.include_routers(
    admin.router,
    user.router,
)
