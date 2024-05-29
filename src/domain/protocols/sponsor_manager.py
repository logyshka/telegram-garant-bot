from abc import abstractmethod
from datetime import datetime
from typing import Protocol, Optional

from src.domain.models.sponsor import Sponsor


class SponsorManager(Protocol):
    @abstractmethod
    async def get_sponsors(self) -> list[Sponsor]:
        ...

    @abstractmethod
    async def get_unfollowed_sponsors(self, user_id: int) -> list[Sponsor]:
        ...

    @abstractmethod
    async def is_following_all_sponsors(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def add_sponsor(
            self,
            channel_id: int,
            creates_join_request: bool,
            expire_date: Optional[datetime]
    ) -> Sponsor:
        """
            Adds a new sponsor to the system.

            Parameters:
             channel_id (int): The unique identifier of the Telegram sponsor channel.
             creates_join_request (bool): A flag indicating whether creates join requests.
             expire_date (Optional[datetime]): The expiration date and time of the sponsorship. If None, the sponsorship is permanent.

            Returns:
             Sponsor: The newly created sponsor object.

            Raises:
             SponsorAlreadyExistsError: If same sponsor already exists.
             SponsorAccessDeniedError: If bot has no access to sponsor channel.
        """

    @abstractmethod
    async def remove_sponsor(
            self, sponsor_id: int,
    ) -> None:
        ...

    @abstractmethod
    async def get_sponsor(
            self, sponsor_id: int
    ) -> Optional[Sponsor]:
        ...

    @abstractmethod
    async def update_invite_link(
            self,
            sponsor_id: int,
            creates_join_request: bool
    ) -> None:
        """
        Updates the invite link of a sponsor.

        Parameters:
         sponsor_id (int): The unique identifier of the sponsor.
         creates_join_request (bool): A flag indicating whether creates join requests.

        Raises:
         SponsorAccessDeniedError: If bot has no access to sponsor channel.
        """

    @abstractmethod
    async def update_title(
            self,
            sponsor_id: int,
    ) -> None:
        """
        Updates the title of a sponsor.

        Parameters:
         sponsor_id (int): The unique identifier of the sponsor.

        Raises:
         SponsorAccessDeniedError: If bot has no access to sponsor channel.
        """

    @abstractmethod
    async def update_expire_date(
            self,
            sponsor_id: int,
            expire_date: Optional[datetime]
    ):
        """
        Updates the expiration date of a sponsor.

        Parameters:
         sponsor_id (int): The unique identifier of the sponsor.
         expire_date (Optional[datetime]): The expiration date and time of the sponsorship. If None, the sponsorship is permanent.
        Raises:
         SponsorInvalidExpireDateError: If expire date is less or equal than current date.
        """


class SponsorManagerFactory(Protocol):
    @abstractmethod
    async def create_sponsor_manager(self) -> SponsorManager:
        ...
