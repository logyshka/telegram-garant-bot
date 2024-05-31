from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from dishka.integrations.aiogram import inject, FromDishka

from src.domain.enums import Role
from src.domain.protocols import RoleManager


class HasRole(Filter):
    def __init__(self, *roles: Role):
        self._roles = set(roles)

    @inject
    async def __call__(
            self,
            obj: Union[Message, CallbackQuery],
            role_manager: FromDishka[RoleManager]
    ) -> bool:
        user_role = await role_manager.get_user_role(user_id=obj.from_user.id)
        return user_role.role in self._roles


IS_OWNER = HasRole(Role.OWNER)
IS_ADMIN = HasRole(Role.OWNER, Role.ADMIN)
