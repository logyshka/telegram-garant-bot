from typing import List

from src.domain.enums import Role
from src.domain.functions.user_role import create_user_role, get_user_role, change_user_role, create_constant_roles
from src.domain.models import UserRole
from src.domain.protocols import RoleManager, RoleManagerFactory


class DefaultRoleManager(RoleManager):
    async def get_user_role(self, user_id: int) -> UserRole:
        return await get_user_role(user_id=user_id)

    async def change_user_role(self, user_id: int, role: Role) -> None:
        await change_user_role(user_id=user_id, role=role)

    async def create_constant_roles(self, *user_ids: int, role: Role) -> None:
        await create_constant_roles(*user_ids, role=role)


class DefaultRoleManagerFactory(RoleManagerFactory):
    def __init__(self, owner_ids: List[int]):
        self.owner_ids = owner_ids

    async def create_role_manager(self) -> RoleManager:
        manager = DefaultRoleManager()
        await manager.create_constant_roles(*self.owner_ids, role=Role.OWNER)
        return DefaultRoleManager()
