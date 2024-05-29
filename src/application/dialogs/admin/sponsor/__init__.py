from aiogram import Router

from . import (
    create,
    update,
    delete,
    menu,
)

router = Router()
router.include_routers(
    create.dialog,
    update.dialog,
    delete.dialog,
    menu.dialog,
)
