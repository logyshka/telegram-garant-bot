from abc import abstractmethod
from typing import Protocol, Optional

from src.domain.enums import LocaleName
from src.domain.models import User


class UserManager(Protocol):
    @abstractmethod
    async def create_user(
            self,
            user_id: int,
            locale_name: LocaleName
    ) -> bool:
        ...

    @abstractmethod
    async def get_user(
            self,
            user_id: int
    ) -> Optional[User]:
        ...


class UserManagerFactory(Protocol):
    @abstractmethod
    async def create_user_manager(self) -> UserManager:
        ...
