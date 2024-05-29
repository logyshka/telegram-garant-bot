from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel
from dishka.integrations.aiogram import FromDishka

from src.application.states.admin import CryptoBotPaymentSG
from src.application.widgets.locale import LocaleConst
from src.domain.protocols import PaymentManager, ConfigManager, LocaleManager
from src.impl.di.inject import inject_on_click
from src.impl.protocols.payment.crypto_bot import CryptoBotConfigKeys
from .common import connect_new_account


@inject_on_click
async def input_token(
        msg: Message,
        _: TextInput,
        dialog_manager: DialogManager,
        token: str,
        payment_manager: FromDishka[PaymentManager],
        config_manager: FromDishka[ConfigManager],
        locale_manager: FromDishka[LocaleManager],
):
    account = {
        CryptoBotConfigKeys.TOKEN.value: token
    }
    is_connected = await connect_new_account(
        dialog_manager=dialog_manager,
        account=account,
        payment_manager=payment_manager,
        config_manager=config_manager,
    )

    if not is_connected:
        text = await locale_manager.get_text(
            text_id='payment-crypto-bot-token-error',
            user_id=msg.from_user.id,
        )
        return await msg.reply(text=text)

    text = await locale_manager.get_text(
        text_id='payment-account-connected',
        user_id=msg.from_user.id,
    )

    await msg.reply(text=text)
    await dialog_manager.done()


dialog = Dialog(
    Window(
        LocaleConst('payment-crypto-bot-token-input'),
        TextInput(
            id='input_token',
            on_success=input_token
        ),
        Cancel(LocaleConst('cancel')),
        state=CryptoBotPaymentSG.token
    )
)
