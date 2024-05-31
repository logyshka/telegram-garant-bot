from abc import abstractmethod
from pathlib import Path
from typing import Protocol, List


class BackupManager(Protocol):
    def __init__(self, *files: Path):
        self.files = files

    @abstractmethod
    async def send_backups(self, user_ids: List[int]) -> None:
        ...

    @abstractmethod
    async def edit_backup_delay(self, new_delay: int) -> None:
        ...
