from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka

from src.domain.enums import Currency
from src.domain.functions.balance import top_up_balance, get_balances
from src.domain.protocols import LocaleManager

router = Router()


@router.message(Command('locale'))
async def handle_locale_test(msg: Message, locale_manager: FromDishka[LocaleManager]):
    text = await locale_manager.get_text(text_id='yes', user_id=msg.from_user.id)
    await msg.reply(text)


@router.message(Command('topup'))
async def handle_top_up(msg: Message):
    before = await get_balances(user_id=msg.from_user.id)
    await top_up_balance(user_id=msg.from_user.id, currency=Currency.RUB, value=100)
    after = await get_balances(user_id=msg.from_user.id)
    await msg.reply(f'Before: {before}\nAfter: {after}')