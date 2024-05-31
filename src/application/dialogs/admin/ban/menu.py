from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.buttons import StartWithDialogData
from src.application.widgets.locale import LocaleJinja, LocaleConst
from src.domain.protocols import BanManager
from src.impl.di.inject import inject_getter, inject_on_dialog_event


@inject_on_dialog_event
async def on_start_dialog(
        start_data: dict,
        dialog_manager: DialogManager,
        ban_manager: FromDishka[BanManager]
) -> None:
    user_id = start_data['user_id']

    ban = await ban_manager.get_user_ban(user_id=user_id)

    dialog_manager.dialog_data['user_id'] = user_id

    if ban:
        await dialog_manager.switch_to(state=states.admin.BanMenuSG.view_banned)
    else:
        await dialog_manager.switch_to(state=states.admin.BanMenuSG.view_unbanned)


@inject_getter
async def banned_getter(
        dialog_manager: DialogManager,
        ban_manager: FromDishka[BanManager],
        **_kwargs,
):
    user_id = dialog_manager.start_data['user_id']
    ban = await ban_manager.get_user_ban(user_id=user_id)
    return {
        'ban': ban,
        'user_id': user_id
    }


async def unbanned_getter(
        dialog_manager: DialogManager,
        **_kwargs,
) -> dict:
    user_id = dialog_manager.start_data['user_id']
    return {
        'user_id': user_id
    }


dialog = Dialog(
    Window(
        LocaleJinja('ban-user-banned'),
        StartWithDialogData(
            LocaleConst('unban'),
            id='unban',
            state=states.admin.BanDeleteSG.confirm,
            dialog_data_keys=['user_id'],
        ),
        Cancel(LocaleConst('close')),
        state=states.admin.BanMenuSG.view_banned,
        getter=banned_getter
    ),
    Window(
        LocaleJinja('ban-user-unbanned'),
        StartWithDialogData(
            LocaleConst('ban'),
            id='ban',
            state=states.admin.BanCreateSG.reason,
            dialog_data_keys=['user_id']
        ),
        Cancel(LocaleConst('close')),
        state=states.admin.BanMenuSG.view_unbanned,
        getter=unbanned_getter
    ),
    on_start=on_start_dialog
)
