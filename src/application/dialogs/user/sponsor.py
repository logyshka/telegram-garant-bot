from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Url, ListGroup, Button
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.locale import LocaleConst
from src.domain.protocols import SponsorManager, LocaleManager
from src.impl.di.inject import inject_on_click, inject_getter


@inject_on_click
async def check_subscription(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        sponsor_manager: FromDishka[SponsorManager],
        locale_manager: FromDishka[LocaleManager]
):
    is_following = await sponsor_manager.is_following_all_sponsors(user_id=call.from_user.id)

    if is_following:
        text = await locale_manager.get_text(
            text_id='sponsor-following-success',
            user_id=call.from_user.id
        )
        await call.answer(text=text, show_alert=True)
        return await dialog_manager.done()
    text = await locale_manager.get_text(
        text_id='sponsor-following-error',
        user_id=call.from_user.id
    )
    await call.answer(text=text, show_alert=True)


@inject_getter
async def unsubscribed_getter(
        sponsor_manager: FromDishka[SponsorManager],
        dialog_manager: DialogManager,
        **_kwargs
):
    sponsors = await sponsor_manager.get_unfollowed_sponsors(user_id=dialog_manager.event.from_user.id)
    return {
        'sponsors': sponsors
    }


dialog = Dialog(
    Window(
        LocaleConst('sponsor-menu-view-all'),
        Group(
            ListGroup(
                Url(
                    Format('{item.title}'),
                    Format('{item.invite_link}')
                ),
                id='sponsors',
                item_id_getter=lambda item: item.id,
                items='sponsors',
            ),
            width=1
        ),
        Button(
            LocaleConst('sponsor-following-confirm'),
            id='check_subscription',
            on_click=check_subscription
        ),
        state=states.user.SponsorSG.unsubscribed,
        getter=unsubscribed_getter
    )
)
