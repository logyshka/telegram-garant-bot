from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.application import states

router = Router()


@router.message(Command('apay'))
async def handle_apay(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.admin.PaymentSettingsSG.payments
    )


@router.message(Command('pay'))
async def handle_pay(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=states.user.PaymentSG.currency
    )
