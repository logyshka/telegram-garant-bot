from datetime import datetime
from typing import Tuple, Optional

from src.domain import functions
from src.domain.models import Ban
from src.domain.protocols import BanManager, BanManagerFactory


class DefaultBanManager(BanManager):
    async def get_user_ban(self, user_id: int) -> Optional[Ban]:
        return await functions.ban.get_user_ban(user_id=user_id)

    async def ban_user(self, user_id: int, reason: Optional[str], till: Optional[datetime]) -> Tuple[bool, Ban]:
        return await functions.ban.ban_user(user_id=user_id, reason=reason, till=till)

    async def unban_user(self, user_id: int) -> None:
        await functions.ban.unban_user(user_id=user_id)


class DefaultBanManagerFactory(BanManagerFactory):
    async def create_ban_manager(self) -> BanManager:
        manager = DefaultBanManager()
        return manager
