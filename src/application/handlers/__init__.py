from aiogram import Router

from . import test, user, start

router = Router()
router.include_routers(
    test.router,
    user.router,
    start.router,
)
