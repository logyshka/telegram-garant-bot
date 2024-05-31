from typing import Optional

from src.domain import functions
from src.domain.enums import LocaleName, Role
from src.domain.models import User
from src.domain.protocols import UserManager, UserManagerFactory


class DefaultUserManager(UserManager):
    async def create_user(self, user_id: int, locale_name: LocaleName) -> bool:
        user = await self.get_user(user_id=user_id)

        if user:
            return False

        await functions.user.create_user(
            user_id=user_id,
            locale_name=locale_name
        )
        await functions.balance.create_balances(
            user_id=user_id
        )
        await functions.user_role.create_user_role(
            user_id=user_id,
            role=Role.USER
        )

        return True

    async def get_user(self, user_id: int) -> Optional[User]:
        return await functions.user.get_user(user_id=user_id)


class DefaultUserManagerFactory(UserManagerFactory):
    async def create_user_manager(self) -> DefaultUserManager:
        manager = DefaultUserManager()
        return manager
