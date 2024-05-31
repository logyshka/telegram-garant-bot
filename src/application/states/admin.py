from aiogram.fsm.state import StatesGroup, State


class PaymentSettingsSG(StatesGroup):
    payments = State()
    settings = State()


class CryptoBotPaymentSG(StatesGroup):
    token = State()


class SponsorCreateSG(StatesGroup):
    creates_join_request = State()
    expire_date = State()
    channel_id = State()


class SponsorDeleteSG(StatesGroup):
    confirm = State()


class SponsorMenuSG(StatesGroup):
    view_all = State()
    view_one = State()


class SponsorUpdateSG(StatesGroup):
    creates_join_request = State()
    expire_date = State()


class RoleMenuSG(StatesGroup):
    role = State()
    constant_role = State()


class BanMenuSG(StatesGroup):
    view_banned = State()
    view_unbanned = State()


class BanDeleteSG(StatesGroup):
    confirm = State()


class BanCreateSG(StatesGroup):
    reason = State()
    till = State()
    confirm = State()
