from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button, Cancel
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.locale import LocaleConst
from src.domain.protocols import SponsorManager
from src.impl.di.inject import inject_on_click


@inject_on_click
async def confirm_delete(
        _: CallbackQuery,
        __: Button,
        dialog_manager: DialogManager,
        sponsor_manager: FromDishka[SponsorManager],
):

    await sponsor_manager.remove_sponsor(
        sponsor_id=dialog_manager.start_data['sponsor_id']
    )
    await dialog_manager.done()


dialog = Dialog(
    Window(
        LocaleConst('sponsor-delete-confirm'),
        Row(
            Button(LocaleConst('yes'), id='yes', on_click=confirm_delete),
            Cancel(LocaleConst('no'), id='no')
        ),
        state=states.admin.SponsorDeleteSG.confirm,
    ),
)
