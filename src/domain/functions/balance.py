from _decimal import Decimal
from tortoise.expressions import F

from src.domain.enums import Currency
from src.domain.models import Balance


async def create_balances(user_id: int) -> list[Balance]:
    for currency in Currency:
        await Balance.create(
            currency=currency,
            value=0,
            user_id=user_id
        )


async def get_balances(user_id: int) -> list[Balance]:
    return await Balance.filter(user_id=user_id)


async def top_up_balance(user_id: int, currency: Currency, value: Decimal) -> None:
    await Balance.filter(user_id=user_id, currency=currency).update(
        value=F('value') + value
    )
