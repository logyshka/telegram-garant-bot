from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Group, Select, Cancel, Url, Row, Button
from aiogram_dialog.widgets.text import Format
from dishka.integrations.aiogram import FromDishka

from src.application import states
from src.application.widgets.locale import LocaleConst, LocaleJinja
from src.domain.common import CurrencyLimits
from src.domain.enums import Currency
from src.domain.models import Bill
from src.domain.protocols import PaymentManager, Payment, LocaleManager
from src.impl.di.inject import inject_on_click, inject_getter, inject_on_dialog_event


@inject_on_click
async def select_currency(
        _call: CallbackQuery,
        _: Select,
        dialog_manager: DialogManager,
        currency: Currency,
        payment_manager: FromDishka[PaymentManager],
):
    limits = await payment_manager.get_limits(currency=currency)
    dialog_manager.dialog_data['limits'] = limits
    await dialog_manager.next()


@inject_getter
async def currency_getter(payment_manager: FromDishka[PaymentManager], **_kwargs):
    currencies = await payment_manager.get_available_currencies()
    return {
        'currencies': currencies
    }


@inject_on_click
async def input_amount(
        msg: Message,
        _: TextInput,
        dialog_manager: DialogManager,
        amount: float,
        payment_manager: FromDishka[PaymentManager],
        locale_manager: FromDishka[LocaleManager]
):
    limits: CurrencyLimits = dialog_manager.dialog_data.get('limits')

    if not limits.check(amount=amount):
        text = await locale_manager.get_text(
            text_id='payment-amount-invalid',
            user_id=msg.from_user.id
        )
        return await msg.reply(text=text)

    payments = await payment_manager.get_available_payments(currency=limits.currency)

    if len(payments) > 1:
        dialog_manager.dialog_data.update(
            amount=amount,
            payments=payments
        )
        return await dialog_manager.next()

    payment = await payment_manager.get_payment(
        payment=payments[0]
    )
    bill = await payment.create_bill(
        user_id=msg.from_user.id,
        amount=amount,
        currency=limits.currency,
    )
    dialog_manager.dialog_data.update(
        payment=payment,
        bill=bill,
    )
    await dialog_manager.switch_to(state=states.user.PaymentSG.pending)


async def amount_getter(dialog_manager: DialogManager, **_kwargs):
    limits = dialog_manager.dialog_data.get('limits')
    return {
        'limits': limits
    }


async def select_payment(
        call: CallbackQuery,
        _: Select,
        dialog_manager: DialogManager,
        payment: str,
        payment_manager: FromDishka[PaymentManager],
):
    amount: float = dialog_manager.dialog_data['amount']
    limits: CurrencyLimits = dialog_manager.dialog_data['limits']

    payment = await payment_manager.get_payment(payment=payment)

    bill = await payment.create_bill(
        user_id=call.from_user.id,
        amount=amount,
        currency=limits.currency,
    )

    dialog_manager.dialog_data.update(
        payment=payment,
        bill=bill
    )
    await dialog_manager.next()


async def payment_getter(dialog_manager: DialogManager, **_kwargs):
    payments = dialog_manager.dialog_data['payments']
    return {
        'payments': payments
    }


@inject_on_click
async def check_bill(
        call: CallbackQuery,
        _: Button,
        dialog_manager: DialogManager,
        locale_manager: FromDishka[LocaleManager]
):
    bill: Bill = dialog_manager.dialog_data['bill']
    payment: Payment = dialog_manager.dialog_data['payment']

    is_paid = await payment.check_bill_is_paid(bill=bill)

    if is_paid:
        text = await locale_manager.get_text(
            text_id='bill-paid',
            user_id=call.from_user.id,
        )
        await call.message.answer(text=text.format(bill=bill))
    elif call.data == 'check_bill':
        text = await locale_manager.get_text(
            text_id='bill-non-paid',
            user_id=call.from_user.id,
        )
        return await call.answer(text=text, show_alert=True)
    elif call.data == 'cancel_bill':
        text = await locale_manager.get_text(
            text_id='bill-cancelled',
            user_id=call.from_user.id,
        )
        await payment.cancel_bill(bill=bill)
        await call.answer(text=text, show_alert=True)

    await dialog_manager.done()


async def pending_getter(dialog_manager: DialogManager, **_kwargs):
    bill: Bill = dialog_manager.dialog_data['bill']
    return {
        'bill': bill
    }


@inject_on_dialog_event
async def check_pending_bill(_, dialog_manager: DialogManager, payment_manager: FromDishka[PaymentManager]):
    user_id = dialog_manager.event.from_user.id
    bill = await payment_manager.get_pending_bill(user_id=user_id)
    if bill:
        payment = await payment_manager.get_payment(payment=bill.payment)
        dialog_manager.dialog_data.update(
            bill=bill,
            payment=payment
        )
        return await dialog_manager.switch_to(
            state=states.user.PaymentSG.pending
        )

    currencies = await payment_manager.get_available_currencies()

    if len(currencies) == 1:
        limits = await payment_manager.get_limits(currency=currencies[0])
        dialog_manager.dialog_data['limits'] = limits
        return await dialog_manager.switch_to(
            state=states.user.PaymentSG.amount
        )


dialog = Dialog(
    Window(
        LocaleConst('bill-create-currency'),
        Group(
            Select(
                Format('{item.name}'),
                id='select_currency',
                item_id_getter=lambda item: item.name,
                items='currencies',
                type_factory=Currency,
                on_click=select_currency
            ),
            width=2,
        ),
        Cancel(LocaleConst('cancel')),
        state=states.user.PaymentSG.currency,
        getter=currency_getter,
    ),
    Window(
        LocaleJinja('bill-create-amount'),
        TextInput(
            id='input_amount',
            on_success=input_amount,
            type_factory=float
        ),
        Cancel(LocaleConst('cancel')),
        state=states.user.PaymentSG.amount,
        getter=amount_getter
    ),
    Window(
        LocaleConst('bill-create-payment'),
        Group(
            Select(
                Format('{item.display_name}'),
                id='select_payment',
                item_id_getter=lambda item: item.class_name,
                items='payments',
                on_click=select_payment
            ),
            width=2
        ),
        Cancel(LocaleConst('cancel')),
        state=states.user.PaymentSG.payment,
        getter=payment_getter
    ),
    Window(
        LocaleJinja('bill-pending'),
        Row(
            Url(LocaleConst('bill-pay-url'), Format('{bill.pay_url}')),
            Button(
                LocaleConst('bill-check'),
                id='check_bill',
                on_click=check_bill
            )
        ),
        Button(
            LocaleConst('cancel'),
            id='cancel_bill',
            on_click=check_bill,
        ),
        state=states.user.PaymentSG.pending,
        getter=pending_getter
    ),
    on_start=check_pending_bill
)
