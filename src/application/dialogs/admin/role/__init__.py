from aiogram import Router

from src.application.filters import IS_OWNER
from . import change

router = Router()

filters = (IS_OWNER,)
router.message.filter(*filters)
router.callback_query.filter(*filters)

router.include_routers(
    change.dialog,
)
