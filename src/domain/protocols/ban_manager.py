from abc import abstractmethod
from datetime import datetime
from typing import Protocol, Optional, Tuple

from src.domain.models import Ban


class BanManager(Protocol):
    @abstractmethod
    async def get_user_ban(self, user_id: int) -> Optional[Ban]:
        ...

    @abstractmethod
    async def ban_user(self, user_id: int, reason: str, till: Optional[datetime]) -> Tuple[bool, Ban]:
        ...

    @abstractmethod
    async def unban_user(self, user_id: int) -> None:
        ...


class BanManagerFactory(Protocol):
    @abstractmethod
    async def create_ban_manager(self) -> BanManager:
        ...
