from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager

from src.application import states
from src.application.filters import IsFollowedSponsor

router = Router()


@router.message(Command('asponsor'))
async def handle_asponsor(_, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.admin.SponsorMenuSG.view_all
    )


@router.message(~IsFollowedSponsor())
async def handle_asponsor(_, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.user.SponsorSG.unsubscribed
    )
