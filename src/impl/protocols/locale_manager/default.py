import logging
from pathlib import Path
from typing import Optional, List

import aiofiles

from src.domain.common.locale import Locale
from src.domain.enums import LocaleName
from src.domain.functions.user import get_user_locale_name, change_user_locale_name
from src.domain.protocols import LocaleManager, LocaleManageFactory


class DefaultLocaleManager(LocaleManager):
    def __init__(self, default_locale_name: str, locales_dir: Path):
        super().__init__(default_locale_name)
        self._locales_dir = locales_dir

    @staticmethod
    async def _fetch_locale_data(locale_file: Path) -> dict[str, str]:
        async with aiofiles.open(locale_file, 'r', encoding='utf-8') as f:
            lines = (await f.read()).split('\n')

        locale_data = {}
        last_key = None

        for line in lines:
            is_continuation = line.startswith(' ')
            line = line.strip().replace('\\n', '\n')

            if line == '':
                continue
            elif is_continuation:
                if last_key:
                    locale_data[last_key] += f'\n{line}'
            else:
                key, line = map(lambda x: x.strip(), line.split('=', maxsplit=1))
                locale_data[key] = line
                last_key = key

        return locale_data

    async def fetch_locales(self) -> list[Locale]:
        if not self._locales_dir.is_dir():
            raise ValueError(f'Given path is not directory: {self._locales_dir}')

        for locale_dir in self._locales_dir.iterdir():
            if locale_dir.is_dir():
                locale_name = locale_dir.name.upper()
                locale_exists = False
                locale_data = {}
                for existed_locale_name in LocaleName:
                    if existed_locale_name == locale_name:
                        locale_exists = True
                        locale_name = existed_locale_name
                        locale_data = {}
                        for locale_file in locale_dir.iterdir():
                            if locale_file.is_file():
                                locale_data.update(
                                    await self._fetch_locale_data(locale_file=locale_file)
                                )
                        break
                if locale_exists:
                    self.locales.append(Locale(locale_name, locale_data))
                else:
                    logging.warning(f'{locale_name} was skipped! Please add {locale_name} to LocaleName enum.')
        return self.locales

    async def get_user_locale_name(self, user_id: int) -> Optional[LocaleName]:
        locale_name = await get_user_locale_name(user_id=user_id)
        return locale_name

    async def change_user_locale_name(
            self,
            user_id: int,
            locale_name: LocaleName
    ) -> None:
        await change_user_locale_name(user_id=user_id, locale_name=locale_name)


class DefaultLocaleManageFactory(LocaleManageFactory):
    def __init__(
            self,
            locales_dir: Path,
            default_locale_name: LocaleName,
    ):
        self._locales_dir = locales_dir
        self._default_locale_name = default_locale_name

    async def create_locale_manager(self) -> DefaultLocaleManager:
        manager = DefaultLocaleManager(
            locales_dir=self._locales_dir,
            default_locale_name=self._default_locale_name
        )
        await manager.fetch_locales()
        return manager
