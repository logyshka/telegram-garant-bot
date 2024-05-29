from typing import Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import inject, FromDishka

from src.domain.protocols import SponsorManager


class IsFollowedSponsor(Filter):
    @inject
    async def __call__(self, obj: Union[CallbackQuery, Message], sponsor_manager: FromDishka[SponsorManager]) -> bool:
        user_id = obj.from_user.id
        return await sponsor_manager.is_following_all_sponsors(user_id=user_id)
