from typing import Dict, Any

from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import inject, FromDishka

from src.domain.protocols import Payment, PaymentManager, ConfigManager


async def connect_new_account(
        dialog_manager: DialogManager,
        payment_manager: FromDishka[PaymentManager],
        config_manager: FromDishka[ConfigManager],
        account: Dict[str, Any]
) -> bool:
    payment: Payment = dialog_manager.start_data.get('payment')

    await config_manager.set_values(values=account)

    payment = await payment_manager.get_payment(
        payment=payment,
        config_manager=config_manager
    )
    is_valid = await payment.validate()

    if not is_valid:
        return False

    await payment_manager.switch_payment_account(payment_account=account)

    return True
