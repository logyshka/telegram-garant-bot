from abc import abstractmethod, ABC
from typing import Protocol, Optional

from ..common.locale import Locale


class LocaleManager(ABC):
    def __init__(self, default_locale_name: str):
        self.default_locale_name: str = default_locale_name
        self.locales: list[Locale] = []

    async def get_text(self, text_id: str, user_id: int) -> str:
        locale_name = await self.get_user_locale_name(user_id=user_id)

        if not locale_name:
            locale_name = self.default_locale_name

        locale_name = locale_name.lower()

        for locale in self.locales:
            if locale.name.lower() == locale_name:
                return locale.data.get(text_id, text_id)

        return text_id

    @abstractmethod
    async def fetch_locales(self) -> list[Locale]:
        ...

    @abstractmethod
    async def get_user_locale_name(self, user_id: int) -> Optional[str]:
        ...


class LocaleManageFactory(Protocol):
    @abstractmethod
    async def create_locale_manager(self) -> LocaleManager:
        ...
