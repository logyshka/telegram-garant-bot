from datetime import date, datetime
from typing import Union, Optional

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button, Cancel, Calendar
from aiogram_dialog.widgets.text import Const
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.locale import LocaleConst
from src.domain.exceptions.sponsor import SponsorAccessDeniedError
from src.domain.protocols import SponsorManager, LocaleManager
from src.impl.di.inject import inject_on_click


@inject_on_click
async def select_creates_join_request(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        sponsor_manager: FromDishka[SponsorManager],
        locale_manager: FromDishka[LocaleManager],
):
    creates_join_request = bool(call.data == 'yes')
    try:
        await sponsor_manager.update_invite_link(
            sponsor_id=dialog_manager.start_data['sponsor_id'],
            creates_join_request=creates_join_request
        )
    except SponsorAccessDeniedError:
        text = await locale_manager.get_text(
            text_id='bot-channel-access-error',
            user_id=call.from_user.id,
        )
        await call.message.answer(text=text)
    else:
        text = await locale_manager.get_text(
            text_id='success-channel-link-changed',
            user_id=call.from_user.id
        )
        await call.message.answer(text=text)
        await dialog_manager.done()


async def select_expire_date(
        call: CallbackQuery,
        _: Union[Button, Calendar],
        dialog_manager: DialogManager,
        locale_manager: FromDishka[LocaleManager],
        sponsor_manager: FromDishka[SponsorManager],
        expire_date: Optional[date] = None,
):
    if expire_date and expire_date < date.today():
        text = await locale_manager.get_text(
            text_id='invalid-date-error',
            user_id=call.from_user.id
        )
        return await call.answer(text=text, show_alert=True)

    if expire_date:
        expire_date = datetime(year=expire_date.year, month=expire_date.month, day=expire_date.day)

    await sponsor_manager.update_expire_date(
        sponsor_id=dialog_manager.start_data['sponsor_id'],
        expire_date=expire_date
    )
    await dialog_manager.next()


dialog = Dialog(
    Window(
        LocaleConst('sponsor-create-join-request'),
        Row(
            Button(LocaleConst('yes'), id='yes', on_click=select_creates_join_request),
            Button(LocaleConst('no'), id='no', on_click=select_creates_join_request)
        ),
        Cancel(LocaleConst('cancel')),
        state=states.admin.SponsorUpdateSG.creates_join_request
    ),
    Window(
        LocaleConst('sponsor-create-expire-date'),
        Calendar(
            id='select_expire_date',
            on_click=select_expire_date
        ),
        Button(
            LocaleConst('skip'),
            id='select_expire_date',
            on_click=select_expire_date
        ),
        Cancel(LocaleConst('cancel')),
        state=states.admin.SponsorUpdateSG.expire_date,
    )
)
