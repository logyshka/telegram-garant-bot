from typing import Any, Optional, Dict

from src.domain.protocols import ConfigManager, ConfigManagerFactory


class MemoryConfigManager(ConfigManager):
    def __init__(self):
        self._data = {}

    async def get_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        return self._data.get(key) or default

    async def set_value(self, key: str, value: Any) -> None:
        self._data[key] = value

    async def set_values(self, values: Dict[str, Any]) -> None:
        self._data.update(values)


class MemoryConfigManagerFactory(ConfigManagerFactory):
    async def create_config_manager(self) -> MemoryConfigManager:
        manager = MemoryConfigManager()
        return manager
