import asyncio
import ssl
from abc import abstractmethod, ABC
from typing import Optional, Any

import certifi
from aiohttp import ClientSession, TCPConnector, ClientResponse
from aiohttp.typedefs import StrOrURL

from src.utils.exceptions import PaymentApiError


class BaseClient(ABC):
    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._session: Optional[ClientSession] = None

    def get_session(self, **kwargs):
        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(connector=connector, **kwargs)
        return self._session

    async def _make_request(self, method: str, url: StrOrURL, **kwargs) -> Any:
        session = self.get_session()
        try:
            async with session.request(method, url, **kwargs) as response:
                return await self._validate_response(response=response)
        except TypeError:
            raise PaymentApiError()

    async def close(self):
        if not isinstance(self._session, ClientSession):
            return

        if self._session.closed:
            return

        await self._session.close()

    @abstractmethod
    async def _validate_response(self, response: ClientResponse) -> Any:
        raise NotImplementedError
