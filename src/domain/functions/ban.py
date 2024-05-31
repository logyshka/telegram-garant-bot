from datetime import datetime
from typing import Optional, Tuple

from tortoise.exceptions import IntegrityError

from src.domain.models import Ban


async def get_user_ban(user_id: int) -> Optional[Ban]:
    return await Ban.get_or_none(user_id=user_id)


async def ban_user(user_id: int, reason: Optional[str], till: Optional[datetime]) -> Tuple[bool, Ban]:
    try:
        return True, await Ban.create(user_id=user_id, reason=reason, till=till)
    except IntegrityError:
        return False, await get_user_ban(user_id)


async def unban_user(user_id: int) -> None:
    await Ban.filter(user_id=user_id).delete()
