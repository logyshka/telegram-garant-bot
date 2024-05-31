from aiogram.filters import Filter
from aiogram.types import Message
from dishka.integrations.aiogram import inject, FromDishka

from src.domain.protocols import LocaleManager


class IsSingleLocaled(Filter):
    @inject
    async def __call__(
            self,
            obj: Message,
            locale_manager: FromDishka[LocaleManager]
    ) -> bool:
        return len(locale_manager.locales) == 1
