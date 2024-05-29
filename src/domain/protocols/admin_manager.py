from abc import abstractmethod
from typing import Protocol, List


class AdminManager(Protocol):
    @abstractmethod
    async def get_admin_ids(self) -> List[int]:
        ...

    @abstractmethod
    async def set_admin(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def unset_admin(self, user_id: int) -> bool:
        ...


class AdminManagerFactory(Protocol):
    @abstractmethod
    async def create_admin_manager(self) -> AdminManager:
        ...
