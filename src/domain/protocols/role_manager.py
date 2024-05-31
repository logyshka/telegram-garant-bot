from abc import abstractmethod
from typing import Protocol

from src.domain.enums import Role
from src.domain.models import UserRole


class RoleManager(Protocol):
    @abstractmethod
    async def get_user_role(self, user_id: int) -> UserRole:
        ...

    @abstractmethod
    async def change_user_role(self, user_id: int, role: Role) -> None:
        ...

    @abstractmethod
    async def create_constant_roles(self, *user_ids: int, role: Role) -> None:
        ...


class RoleManagerFactory(Protocol):
    @abstractmethod
    async def create_role_manager(self) -> RoleManager:
        ...
