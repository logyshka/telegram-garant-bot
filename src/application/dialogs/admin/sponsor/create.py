from datetime import date, datetime
from typing import Optional

from aiogram.enums import ChatType
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Button, Calendar, Cancel
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.locale import LocaleConst
from src.domain.protocols import LocaleManager, SponsorManager
from src.impl.di.inject import inject_on_click
from src.utils.exceptions import BotChannelAccessError


async def select_creates_join_request(call: CallbackQuery, _: Button, dialog_manager: DialogManager):
    creates_join_request = call.data == 'yes'
    dialog_manager.dialog_data['creates_join_request'] = creates_join_request
    await dialog_manager.next()


async def _select_expire_date(
        call: CallbackQuery,
        expire_date: Optional[date],
        dialog_manager: DialogManager,
        locale_manager: LocaleManager,
) -> None:
    if expire_date:
        if expire_date <= date.today():
            text = await locale_manager.get_text(
                text_id='sponsor-expire-date-error',
                user_id=call.from_user.id
            )
            return await call.answer(text, show_alert=True)
        else:
            expire_date = datetime(year=expire_date.year, month=expire_date.month, day=expire_date.day)

    dialog_manager.dialog_data['expire_date'] = expire_date
    await dialog_manager.next()


@inject_on_click
async def select_expire_date(
        call: CallbackQuery,
        _: Calendar,
        dialog_manager: DialogManager,
        expire_date: date,
        locale_manager: FromDishka[LocaleManager],
):
    await _select_expire_date(
        call=call, expire_date=expire_date,
        dialog_manager=dialog_manager, locale_manager=locale_manager
    )


@inject_on_click
async def skip_expire_date(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        locale_manager: FromDishka[LocaleManager],
):
    await _select_expire_date(
        call=call, expire_date=None,
        dialog_manager=dialog_manager, locale_manager=locale_manager
    )


@inject_on_click
async def input_channel_id(
        msg: Message,
        _: MessageInput,
        dialog_manager: DialogManager,
        locale_manager: FromDishka[LocaleManager],
        sponsor_manager: FromDishka[SponsorManager]
):
    if msg.forward_from_chat and msg.forward_from_chat.type == ChatType.CHANNEL:
        channel_id = msg.forward_from_chat.id
    elif msg.text and msg.text.isdigit():
        channel_id = int(msg.text)
    else:
        text = await locale_manager.get_text(
            text_id='invalid-channel-id-error',
            user_id=msg.from_user.id
        )
        return await msg.answer(text=text)
    creates_join_request = dialog_manager.dialog_data['creates_join_request']
    expire_date = dialog_manager.dialog_data['expire_date']

    try:
        channel = await sponsor_manager.add_sponsor(
            channel_id=channel_id,
            creates_join_request=creates_join_request,
            expire_date=expire_date
        )
    except BotChannelAccessError:
        text = await locale_manager.get_text(
            text_id='sponsor-bot-access-error',
            user_id=msg.from_user.id
        )
        await msg.reply(text=text)
    else:
        text = await locale_manager.get_text(
            text_id='sponsor-create-success',
            user_id=msg.from_user.id
        )
        await msg.answer(text=text)
        await dialog_manager.done()


dialog = Dialog(
    Window(
        LocaleConst('sponsor-create-join-request'),
        Row(
            Button(
                LocaleConst('yes'),
                id='yes',
                on_click=select_creates_join_request
            ),
            Button(
                LocaleConst('no'),
                id='no',
                on_click=select_creates_join_request
            ),
        ),
        Cancel(LocaleConst('cancel')),
        state=states.admin.SponsorCreateSG.creates_join_request
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
            on_click=skip_expire_date
        ),
        Cancel(LocaleConst('cancel')),
        state=states.admin.SponsorCreateSG.expire_date,
    ),
    Window(
        LocaleConst('sponsor-create-channel-id'),
        MessageInput(
            func=input_channel_id
        ),
        Cancel(LocaleConst('cancel')),
        state=states.admin.SponsorCreateSG.channel_id
    )
)
