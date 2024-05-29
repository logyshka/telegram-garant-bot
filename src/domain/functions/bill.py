from datetime import datetime
from typing import Optional

from _decimal import Decimal

from src.data.config import TIME_ZONE
from src.domain.enums import Currency
from src.domain.models import Bill


async def create_bill(
        user_id: int,
        currency: Currency,
        amount: Decimal,
        payment: str,
        payment_display_name: str,
        pay_url: str,
        check_info: str,
        expires_at: Optional[datetime],
) -> Bill:
    return await Bill.create(
        user_id=user_id,
        currency=currency,
        amount=amount,
        payment=payment,
        payment_display_name=payment_display_name,
        pay_url=pay_url,
        check_info=check_info,
        expires_at=expires_at,
        is_paid=False,
    )


async def get_pending_bill(user_id: int) -> Optional[Bill]:
    await Bill.filter(expires_at__lt=datetime.now(tz=TIME_ZONE))
    return await Bill.filter(user_id=user_id, is_paid=False).first()
