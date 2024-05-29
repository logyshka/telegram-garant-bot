from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.domain.functions.user import create_user
from dishka.integrations.aiogram import FromDishka

from src.domain.protocols import LocaleManager

router = Router()


@router.message(Command('start'))
async def handle_start(msg: Message, locale_manager: FromDishka[LocaleManager]):
    user_id = msg.from_user.id
    await create_user(
        user_id=user_id,
        url=msg.from_user.url,
        locale_name=locale_manager.default_locale_name
    )
