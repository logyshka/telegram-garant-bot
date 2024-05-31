from aiogram import Router

from . import create, delete, menu

router = Router()
router.include_routers(
    create.dialog,
    delete.dialog,
    menu.dialog
)
