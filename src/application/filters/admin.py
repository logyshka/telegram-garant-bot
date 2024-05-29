from typing import Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import FromDishka, inject

from src.domain.protocols import AdminManager


class IsAdmin(Filter):
    @inject
    async def __call__(self, obj: Union[CallbackQuery, Message], admin_manager: FromDishka[AdminManager]) -> bool:
        user_id = obj.from_user.id
        admin_ids = await admin_manager.get_admin_ids()
        return user_id in admin_ids
