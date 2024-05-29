from datetime import datetime
from typing import Optional

from src.data.config import TIME_ZONE
from src.domain.models.sponsor import Sponsor


async def add_sponsor(
        sponsor_id: int,
        title: str,
        invite_link: str,
        creates_join_request: bool,
        expire_date: Optional[datetime],
) -> Sponsor:
    return await Sponsor.create(
        id=sponsor_id,
        title=title,
        invite_link=invite_link,
        creates_join_request=creates_join_request,
        expire_date=expire_date,
    )


async def get_sponsors() -> list[Sponsor]:
    now_time = datetime.now(tz=TIME_ZONE)
    await Sponsor.filter(expire_date__lt=now_time).delete()
    return await Sponsor.all()


async def exists_sponsor(sponsor_id: int) -> bool:
    return await Sponsor.exists(id=sponsor_id)


async def update_invite_link(
        sponsor_id: int,
        invite_link: str,
        creates_join_request: bool
) -> None:
    await Sponsor.filter(id=sponsor_id).update(
        invite_link=invite_link,
        creates_join_request=creates_join_request,
    )


async def update_title(
        sponsor_id: int,
        title: str,
) -> None:
    await Sponsor.filter(id=sponsor_id).update(
        title=title,
    )


async def update_expire_date(
        sponsor_id: int,
        expire_date: Optional[datetime],
) -> None:
    await Sponsor.filter(id=sponsor_id).update(
        expire_date=expire_date
    )


async def get_sponsor(sponsor_id: int) -> Optional[Sponsor]:
    return await Sponsor.get_or_none(id=sponsor_id)


async def remove_sponsor(sponsor_id: int) -> None:
    await Sponsor.filter(id=sponsor_id).delete()
