from typing import Optional

from src.domain.models import User
from ..enums import LocaleName


async def create_user(user_id: int, locale_name: LocaleName) -> None:
    await User.create(id=user_id, locale_name=locale_name)


async def get_user(user_id: int) -> Optional[User]:
    return await User.get_or_none(id=user_id)


async def get_user_locale_name(user_id: int) -> Optional[LocaleName]:
    return await User.get(id=user_id) \
        .values_list('locale_name', flat=True)


async def change_user_locale_name(user_id: int, locale_name: LocaleName) -> None:
    await User.filter(id=user_id).update(locale_name=locale_name)
