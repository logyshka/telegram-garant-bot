from abc import abstractmethod
from typing import Protocol, Any, Optional, Dict


class ConfigManager(Protocol):
    @abstractmethod
    async def get_value(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        ...

    @abstractmethod
    async def set_value(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    async def set_values(self, values: Dict[str, Any]) -> None:
        ...


class ConfigManagerFactory(Protocol):
    @abstractmethod
    async def create_config_manager(self) -> ConfigManager:
        ...
