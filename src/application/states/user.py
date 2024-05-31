from aiogram.fsm.state import StatesGroup, State


class MenuSG(StatesGroup):
    main = State()


class PaymentSG(StatesGroup):
    currency = State()
    amount = State()
    payment = State()
    pending = State()


class SponsorSG(StatesGroup):
    unsubscribed = State()


class LocaleSG(StatesGroup):
    locale = State()
