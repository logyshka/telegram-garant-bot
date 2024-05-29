from typing import Optional

from src.domain.models import User
from .balance import create_balances


async def create_user(user_id: int, url: str, locale_name: str) -> None:
    try:
        await User.create(id=user_id, url=url, locale_name=locale_name)
        await create_balances(user_id=user_id)
    except Exception:
        ...


async def get_user_locale_name(user_id: int) -> Optional[str]:
    return await User.get_or_none(id=user_id) \
        .values_list('locale_name', flat=True)


