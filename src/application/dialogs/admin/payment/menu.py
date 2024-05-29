from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.api.exceptions import UnregisteredDialogError
from aiogram_dialog.widgets.kbd import Select, Group, Button, Cancel, Back, Row
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.states.admin import CryptoBotPaymentSG
from src.application.widgets.locale import LocaleConst, LocaleJinja
from src.domain.protocols import PaymentManager, Payment, LocaleManager
from src.impl.di.inject import inject_getter, inject_on_click
from src.impl.protocols.config_manager import MemoryConfigManager
from src.impl.protocols.payment import CryptoBotPayment


async def get_payment(dialog_manager: DialogManager, payment_manager: FromDishka[PaymentManager]) -> Payment:
    payment: Payment = dialog_manager.dialog_data.get('payment')
    payment = await payment_manager.get_payment(payment=payment)
    dialog_manager.dialog_data['payment'] = payment
    return payment


@inject_on_click
async def select_payment(
        _call: CallbackQuery,
        _: Select,
        dialog_manager: DialogManager,
        payment: str,
        payment_manager: FromDishka[PaymentManager]
):
    payment: Payment = await payment_manager.get_payment(payment=payment)
    dialog_manager.dialog_data['payment'] = payment
    await dialog_manager.next()


@inject_getter
async def payment_getter(payment_manager: FromDishka[PaymentManager], **_kwargs):
    payments = await payment_manager.get_all_payments()
    payments = [(payment, await payment_manager.get_payment_state(payment)) for payment in payments]
    return {
        'payments': payments
    }


@inject_on_click
async def switch_payment_state(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        payment_manager: FromDishka[PaymentManager],
        locale_manager: FromDishka[LocaleManager]
):
    payment = dialog_manager.dialog_data['payment']
    if await payment.validate():
        await payment_manager.switch_payments_state(payment=payment)
    else:
        text = await locale_manager.get_text(
            text_id='payment-account-absent',
            user_id=call.from_user.id,
        )
        await call.answer(text=text, show_alert=True)


@inject_on_click
async def change_payment_account(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        locale_manager: FromDishka[LocaleManager]
):
    payment: Payment = dialog_manager.dialog_data['payment']
    states = {
        CryptoBotPayment: CryptoBotPaymentSG.token,
    }
    try:
        state = states[type(payment)]
        config_manager = MemoryConfigManager()
        await dialog_manager.start(
            state=state,
            data={
                'payment': payment,
                'config_manager': config_manager
            }
        )
    except (KeyError, UnregisteredDialogError):
        text = await locale_manager.get_text(
            text_id='payment-unknown-error',
            user_id=call.from_user.id,
        )
        return await call.answer(text=text, show_alert=True)


@inject_getter
async def settings_getter(
        payment_manager: FromDishka[PaymentManager],
        dialog_manager: DialogManager,
        **_kwargs
):
    payment = await get_payment(dialog_manager=dialog_manager, payment_manager=payment_manager)
    state = await payment_manager.get_payment_state(payment=payment)
    fields = []
    has_account = False
    if state:
        try:
            fields = await payment.get_info()
            has_account = True
        except:
            await payment_manager.switch_payments_state(payment=payment, new_state=False)
    else:
        has_account = await payment.validate()

    return {
        'payment': payment,
        'state': state,
        'fields': fields,
        'has_account': has_account
    }


dialog = Dialog(
    Window(
        LocaleConst('payment-settings-choice'),
        Group(
            Select(
                LocaleJinja('payment-settings-list-view'),
                id='select_payment',
                items='payments',
                item_id_getter=lambda item: item[0].name,
                on_click=select_payment
            ),
            width=2,
        ),
        Cancel(LocaleConst('back')),
        state=states.admin.PaymentSettingsSG.payments,
        getter=payment_getter
    ),
    Window(
        LocaleJinja('payment-settings-item-view'),
        Row(
            Button(
                LocaleJinja('on-off'),
                id='switch_payment_state',
                on_click=switch_payment_state
            ),
            Button(
                LocaleJinja('payment-settings-item-change'),
                id='change_payment_account',
                on_click=change_payment_account,
            )
        ),
        Back(LocaleConst('back')),
        state=states.admin.PaymentSettingsSG.settings,
        getter=settings_getter
    ),
)
