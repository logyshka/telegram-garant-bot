from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.domain.protocols import UserManager, LocaleManager

router = Router()


@router.message(Command('role'))
async def role(
        msg: Message,
        command: CommandObject,
        dialog_manager: DialogManager,
        user_manager: FromDishka[UserManager],
        locale_manager: FromDishka[LocaleManager],
):
    user = await user_manager.get_user(command.args)

    if user:
        await dialog_manager.start(
            state=states.admin.RoleMenuSG.role,
            data={
                'user_id': user.id,
            }
        )
    else:
        text = await locale_manager.get_text(text_id='role-no-user-error', user_id=msg.from_user.id)
        await msg.reply(text)
