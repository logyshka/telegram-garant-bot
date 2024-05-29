from aiogram import Router

from . import test, user

router = Router()
router.include_routers(
    test.router,
    user.router,
)
