import logging

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError

from src.domain.exceptions.sponsor import *
from src.domain.functions.sponsor import *
from src.domain.models.sponsor import Sponsor
from src.domain.protocols import SponsorManager, SponsorManagerFactory

IN_CHAT_STATUSES = [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]


class DefaultSponsorManager(SponsorManager):
    def __init__(self, bot: Bot):
        self._bot = bot

    async def get_sponsors(self) -> list[Sponsor]:
        return await get_sponsors()

    async def _is_following_sponsor(self, user_id: int, sponsor: Sponsor) -> bool:
        try:
            member = await self._bot.get_chat_member(chat_id=sponsor.id, user_id=user_id)
        except Exception as e:
            logging.error(e, exc_info=e)
            return True
        else:
            return member.status in IN_CHAT_STATUSES

    async def get_unfollowed_sponsors(self, user_id: int) -> list[Sponsor]:
        sponsors = await self.get_sponsors()
        unfollowed_sponsors = []
        for sponsor in sponsors:
            if not await self._is_following_sponsor(user_id=user_id, sponsor=sponsor):
                unfollowed_sponsors.append(sponsor)
        return unfollowed_sponsors

    async def is_following_all_sponsors(self, user_id: int) -> bool:
        sponsors = await self.get_sponsors()
        for sponsor in sponsors:
            if not await self._is_following_sponsor(user_id=user_id, sponsor=sponsor):
                return False
        return True

    async def add_sponsor(
            self,
            channel_id: int,
            creates_join_request: bool,
            expire_date: Optional[datetime]
    ) -> Sponsor:
        if await exists_sponsor(sponsor_id=channel_id):
            raise SponsorAlreadyExistsError()
        try:
            chat = await self._bot.get_chat(chat_id=channel_id)
            title = chat.title
            invite_link = await chat.create_invite_link(
                expire_date=expire_date,
                creates_join_request=creates_join_request
            )
            sponsor = await add_sponsor(
                sponsor_id=channel_id,
                title=title,
                invite_link=invite_link.invite_link,
                creates_join_request=creates_join_request,
                expire_date=expire_date
            )
        except TelegramAPIError:
            raise SponsorAccessDeniedError()
        else:
            return sponsor

    async def remove_sponsor(self, sponsor_id: int) -> None:
        await remove_sponsor(sponsor_id=sponsor_id)

    async def get_sponsor(
            self, sponsor_id: int
    ) -> Optional[Sponsor]:
        return await get_sponsor(sponsor_id=sponsor_id)

    async def update_invite_link(
            self,
            sponsor_id: int,
            creates_join_request: bool
    ) -> None:
        try:
            invite_link = await self._bot.create_chat_invite_link(
                chat_id=sponsor_id,
                creates_join_request=creates_join_request
            )
            await update_invite_link(
                sponsor_id=sponsor_id,
                invite_link=invite_link.invite_link,
                creates_join_request=creates_join_request
            )
        except TelegramAPIError:
            raise SponsorAccessDeniedError()

    async def update_title(
            self,
            sponsor_id: int,
    ) -> None:
        try:
            chat = await self._bot.get_chat(chat_id=sponsor_id)
            await update_title(
                sponsor_id=sponsor_id,
                title=chat.title
            )
        except TelegramAPIError:
            raise SponsorAccessDeniedError()

    async def update_expire_date(
            self,
            sponsor_id: int,
            expire_date: Optional[datetime]
    ):
        if expire_date and expire_date <= datetime.now(tz=TIME_ZONE):
            raise SponsorInvalidExpireDateError()
        await update_expire_date(sponsor_id=sponsor_id, expire_date=expire_date)


class DefaultSponsorManagerFactory(SponsorManagerFactory):
    def __init__(self, bot: Bot):
        self._bot = bot

    async def create_sponsor_manager(self) -> DefaultSponsorManager:
        manager = DefaultSponsorManager(bot=self._bot)
        return manager
