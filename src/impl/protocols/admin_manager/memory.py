from typing import List

from src.domain.protocols import AdminManager, AdminManagerFactory


class MemoryAdminManager(AdminManager):
    def __init__(self, admin_ids: list[int]):
        self._admin_ids = admin_ids

    async def get_admin_ids(self) -> List[int]:
        return self._admin_ids

    async def set_admin(self, user_id: int) -> bool:
        if user_id in self._admin_ids:
            return False
        self._admin_ids.append(user_id)
        return True

    async def unset_admin(self, user_id: int) -> bool:
        try:
            self._admin_ids.remove(user_id)
            return True
        except ValueError:
            return False


class MemoryAdminManagerFactory(AdminManagerFactory):
    def __init__(self, admin_ids: list[int]):
        self._admin_ids = admin_ids

    async def create_admin_manager(self) -> AdminManager:
        manager = MemoryAdminManager(admin_ids=self._admin_ids)
        return manager
