from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.application import states
from src.application.filters import IsSingleLocaled

router = Router()


@router.message(~IsSingleLocaled(), Command('lang'))
async def handle_lang(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.user.LocaleSG.locale,
        mode=StartMode.RESET_STACK
    )
