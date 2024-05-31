from tortoise.exceptions import IntegrityError

from src.domain.enums import Role
from src.domain.models import UserRole


async def create_constant_roles(*user_ids: int, role: Role) -> None:
    kwargs = dict(
        role=role, constant=True
    )
    for user_id in user_ids:
        try:
            await UserRole.create(user_id=user_id, **kwargs)
        except IntegrityError:
            await UserRole.filter(user_id=user_id).update(**kwargs)


async def create_user_role(user_id: int, role: Role) -> None:
    try:
        await UserRole.create(user_id=user_id, role=role, constant=False)
    except IntegrityError:
        ...


async def get_user_role(user_id: int) -> Role:
    return await UserRole.get(user_id=user_id)


async def change_user_role(user_id: int, role: Role) -> None:
    await UserRole.filter(user_id=user_id).update(role=role)
