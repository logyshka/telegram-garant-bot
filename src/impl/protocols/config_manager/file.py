import pickle
from contextlib import suppress
from pathlib import Path
from typing import Any, Optional, Dict

import aiofiles

from src.domain.protocols import ConfigManager, ConfigManagerFactory


class FileConfigManager(ConfigManager):
    def __init__(self, path: Path):
        self._data = {}
        self._path = path

    async def _save_data(self) -> None:
        pickled_data = pickle.dumps(self._data)
        async with aiofiles.open(self._path, 'wb') as f:
            await f.write(pickled_data)

    async def recover(self) -> None:
        with suppress(Exception):
            async with aiofiles.open(self._path, 'rb') as f:
                pickled_data = await f.read()
            self._data = pickle.loads(pickled_data)

    async def get_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        return self._data.get(key, default)

    async def set_value(self, key: str, value: Any) -> None:
        self._data[key] = value
        await self._save_data()

    async def set_values(self, values: Dict[str, Any]) -> None:
        self._data.update(values)
        await self._save_data()


class FileConfigManagerFactory(ConfigManagerFactory):
    def __init__(self, path: Path):
        self._path = path

    async def create_config_manager(self) -> FileConfigManager:
        manager = FileConfigManager(path=self._path)
        await manager.recover()
        return manager
