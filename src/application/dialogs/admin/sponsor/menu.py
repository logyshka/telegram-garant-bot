from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Select, Cancel, Back, Row, Button, Start, Url
from aiogram_dialog.widgets.text import Format
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.buttons import StartWithDialogData
from src.application.widgets.locale import LocaleConst, LocaleJinja
from src.domain.exceptions.sponsor import SponsorAccessDeniedError
from src.domain.protocols import SponsorManager, LocaleManager
from src.impl.di.inject import inject_getter, inject_on_click


async def select_sponsor(_: CallbackQuery, __: Select, dialog_manager: DialogManager, sponsor_id: int):
    dialog_manager.dialog_data['sponsor_id'] = sponsor_id
    await dialog_manager.next()


@inject_getter
async def view_all_getter(sponsor_manager: FromDishka[SponsorManager], **_kwargs):
    sponsors = await sponsor_manager.get_sponsors()
    return {
        'sponsors': sponsors
    }


@inject_on_click
async def sync_channel(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        sponsor_manager: FromDishka[SponsorManager],
        locale_manager: FromDishka[LocaleManager]
):
    try:
        await sponsor_manager.update_title(
            sponsor_id=dialog_manager.dialog_data['sponsor_id']
        )
        text = await locale_manager.get_text(
            text_id='sponsor-update-title-success',
            user_id=call.from_user.id
        )
        await call.answer(text=text, show_alert=True)
    except SponsorAccessDeniedError:
        text = await locale_manager.get_text(
            text_id='sponsor-bot-access-error',
            user_id=call.from_user.id
        )
        await call.answer(text=text, show_alert=True)


@inject_getter
async def view_one_getter(
        dialog_manager: DialogManager,
        sponsor_manager: FromDishka[SponsorManager],
        **_kwargs
):
    sponsor = await sponsor_manager.get_sponsor(
        sponsor_id=dialog_manager.dialog_data['sponsor_id']
    )
    return {
        'sponsor': sponsor
    }


dialog = Dialog(
    Window(
        LocaleConst('sponsor-menu-view-all'),
        Group(
            Select(
                Format('{item.title}'),
                id='select_sponsor',
                item_id_getter=lambda x: x.id,
                items='sponsors',
                on_click=select_sponsor,
                type_factory=int,
            ),
            width=1,
        ),
        Start(
            LocaleConst('add'),
            id='create_channel',
            state=states.admin.SponsorCreateSG.creates_join_request,
        ),
        Cancel(LocaleConst('back')),
        state=states.admin.SponsorMenuSG.view_all,
        getter=view_all_getter
    ),
    Window(
        LocaleJinja(
            'sponsor-menu-view-one',
            when=F['sponsor']
        ),
        LocaleConst(
            'sponsor-menu-view-one-deleted',
            when=~F['sponsor']
        ),
        Url(
            text=LocaleConst('sponsor-menu-go'),
            url=Format('{sponsor.invite_link}')
        ),
        Button(
            LocaleConst('sponsor-menu-update-title'),
            id='sync_channel',
            on_click=sync_channel
        ),
        Row(
            StartWithDialogData(
                LocaleConst('sponsor-menu-invite-link'),
                id='new_invite_link',
                state=states.admin.SponsorUpdateSG.creates_join_request,
                dialog_data_keys=['sponsor_id']
            ),
            StartWithDialogData(
                LocaleConst('sponsor-menu-expire-date'),
                id='new_expire_date',
                state=states.admin.SponsorUpdateSG.expire_date,
                dialog_data_keys=['sponsor_id']
            )
        ),
        StartWithDialogData(
            LocaleConst('delete'),
            id='delete_channel',
            state=states.admin.SponsorDeleteSG.confirm,
            dialog_data_keys=['sponsor_id']
        ),
        Back(LocaleConst('back')),
        state=states.admin.SponsorMenuSG.view_one,
        getter=view_one_getter
    ),
)
