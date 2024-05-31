from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.common.window import create_confirm_window
from src.application.widgets.locale import LocaleJinja
from src.domain.protocols import BanManager, LocaleManager
from src.impl.di.inject import inject_on_click


@inject_on_click
async def confirm_delete(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        ban_manager: FromDishka[BanManager],
        locale_manager: FromDishka[LocaleManager]
):
    user_id = dialog_manager.start_data['user_id']
    await ban_manager.unban_user(user_id=user_id)
    text = await locale_manager.get_text(text_id='ban-user-unbanned', user_id=user_id)
    await call.answer(text=text, show_alert=True)
    await dialog_manager.done()
    await dialog_manager.done()
    await dialog_manager.start(state=states.admin.BanMenuSG.view_banned, data={
        'user_id': user_id
    })


async def confirm_getter(
        dialog_manager: DialogManager,
        **_kwargs
) -> dict:
    user_id = dialog_manager.start_data['user_id']
    return {
        'user_id': user_id
    }


dialog = Dialog(
    create_confirm_window(
        LocaleJinja('ban-delete-confirm'),
        state=states.admin.BanDeleteSG.confirm,
        on_confirm=confirm_delete,
        getter=confirm_getter
    )
)
