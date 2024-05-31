from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Select, Cancel, Group
from aiogram_dialog.widgets.text import Format
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.locale import LocaleJinja, LocaleConst
from src.domain.enums import Role
from src.domain.protocols import RoleManager, LocaleManager
from src.impl.di.inject import inject_on_dialog_event, inject_on_click
from src.utils.strenum import get_enum_by_name


@inject_on_dialog_event
async def on_start_dialog(
        start_data: dict,
        dialog_manager: DialogManager,
        role_manager: FromDishka[RoleManager]
):
    user_id = start_data['user_id']
    current_role = await role_manager.get_user_role(user_id=user_id)

    dialog_manager.dialog_data.update(
        current_role=current_role.role,
        user_id=user_id
    )

    if current_role.constant:
        await dialog_manager.switch_to(state=states.admin.RoleMenuSG.constant_role)


@inject_on_click
async def select_role(
        call: CallbackQuery,
        _widget: Select,
        dialog_manager: DialogManager,
        role_name: str,
        locale_manager: FromDishka[LocaleManager],
        role_manager: FromDishka[RoleManager]
):
    role = get_enum_by_name(name=role_name, enum=Role)
    user_id = dialog_manager.dialog_data['user_id']
    text = await locale_manager.get_text(text_id='role-changed-success', user_id=user_id)

    dialog_manager.dialog_data['current_role'] = role

    await role_manager.change_user_role(user_id=user_id, role=role)
    await call.answer(text=text, show_alert=True)


async def user_info_getter(
        dialog_manager: DialogManager,
        **_kwargs
):
    current_role = dialog_manager.dialog_data['current_role']
    user_id = dialog_manager.dialog_data['user_id']
    return {
        'current_role': current_role,
        'user_id': user_id
    }


async def user_role_getter(
        dialog_manager: DialogManager,
        **_kwargs
):
    data = await user_info_getter(dialog_manager, **_kwargs)
    data['roles'] = Role.all()
    data['roles'].remove(data['current_role'])
    return data


dialog = Dialog(
    Window(
        LocaleJinja('role-menu-info'),
        Group(
            Select(
                Format('{item.value}'),
                id='select_role',
                items='roles',
                item_id_getter=lambda role: role.name,
                on_click=select_role
            ),
            width=2,
        ),
        Cancel(LocaleConst('cancel')),
        state=states.admin.RoleMenuSG.role,
        getter=user_role_getter
    ),
    Window(
        LocaleJinja('role-constant-error'),
        Cancel(LocaleConst('cancel')),
        state=states.admin.RoleMenuSG.constant_role,
        getter=user_info_getter
    ),
    on_start=on_start_dialog
)
