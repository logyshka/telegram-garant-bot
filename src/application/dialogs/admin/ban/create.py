from datetime import datetime, timedelta

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Next
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.common.window.confirm import create_confirm_window
from src.application.widgets.locale import LocaleConst, LocaleJinja
from src.data.config import TIME_ZONE
from src.domain import validators
from src.domain.exceptions.validation import OutOfRangeError
from src.domain.protocols import BanManager, LocaleManager
from src.impl.di.inject import inject_on_click


@inject_on_click
async def input_reason(
        msg: Message,
        _: TextInput,
        dialog_manager: DialogManager,
        reason: str,
        locale_manager: FromDishka[LocaleManager]
):
    try:
        await validators.ban.validate_reason(reason=reason)
    except OutOfRangeError as error:
        text = await locale_manager.get_text(text_id='ban-create-reason-error', user_id=msg.from_user.id)
        await msg.answer(text=text.format(max=error.max_value))
    else:
        dialog_manager.dialog_data['reason'] = reason
        await dialog_manager.next()


@inject_on_click
async def input_till(
        msg: Message,
        _: TextInput,
        dialog_manager: DialogManager,
        till: int,
        locale_manager: FromDishka[LocaleManager]
):
    try:
        await validators.ban.validate_till(till=till)
    except OutOfRangeError as error:
        text = await locale_manager.get_text(text_id='ban-create-till-error', user_id=msg.from_user.id)
        await msg.answer(text=text.format(min=error.min_value))
    else:
        till = datetime.now(tz=TIME_ZONE) + timedelta(seconds=till)
        dialog_manager.dialog_data['till'] = till
        await dialog_manager.next()


@inject_on_click
async def confirm_create(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        ban_manager: FromDishka[BanManager]
):
    user_id = dialog_manager.start_data['user_id']
    reason = dialog_manager.dialog_data.get('reason')
    till = dialog_manager.dialog_data.get('till')

    created, ban = await ban_manager.ban_user(user_id=user_id, reason=reason, till=till)

    if created:
        await call.answer('ban-create-success', show_alert=True)
    else:
        await call.answer('ban-create-error', show_alert=True)

    await dialog_manager.done()
    await dialog_manager.done()
    await dialog_manager.start(state=states.admin.BanMenuSG.view_banned, data={
        'user_id': user_id
    })


async def confirm_getter(
        dialog_manager: DialogManager,
        **_kwargs
):
    user_id = dialog_manager.start_data['user_id']
    reason = dialog_manager.dialog_data.get('reason')
    till = dialog_manager.dialog_data.get('till')
    return {
        'user_id': user_id,
        'reason': reason,
        'till': till
    }


dialog = Dialog(
    Window(
        LocaleConst('ban-create-reason'),
        TextInput(
            id='reason',
            on_success=input_reason,
        ),
        Next(LocaleConst('skip')),
        state=states.admin.BanCreateSG.reason
    ),
    Window(
        LocaleConst('ban-create-till'),
        TextInput(
            id='till',
            on_success=input_till,
            type_factory=int
        ),
        Next(LocaleConst('skip')),
        state=states.admin.BanCreateSG.till
    ),
    create_confirm_window(
        text=LocaleJinja('ban-create-confirm'),
        state=states.admin.BanCreateSG.confirm,
        on_confirm=confirm_create,
        getter=confirm_getter
    )
)
