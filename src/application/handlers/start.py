from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.domain.protocols import LocaleManager, UserManager

router = Router()


@router.message(Command('start'))
async def handle_start(
        msg: Message,
        locale_manager: FromDishka[LocaleManager],
        user_manager: FromDishka[UserManager],
        dialog_manager: DialogManager,
):
    user_id = msg.from_user.id

    is_new_user = await user_manager.create_user(
        user_id=user_id, locale_name=locale_manager.default_locale_name
    )

    if is_new_user and len(locale_manager.locales) != 1:
        await dialog_manager.start(
            state=states.user.LocaleSG.locale,
            data={
                'is_new_user': True
            }
        )
    else:
        await dialog_manager.start(
            state=states.user.MenuSG.main,
            mode=StartMode.RESET_STACK
        )
