from aiogram.fsm.state import StatesGroup, State


class PaymentSG(StatesGroup):
    currency = State()
    amount = State()
    payment = State()
    pending = State()


class SponsorSG(StatesGroup):
    unsubscribed = State()
