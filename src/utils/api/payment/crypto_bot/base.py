from aiohttp import ClientResponse

from .exceptions import CryptoBotApiError
from ...base import BaseClient


class CryptoBotBaseClient(BaseClient):
    async def _validate_response(self, response: ClientResponse) -> dict:
        response = await response.json()
        if not response.get("ok"):
            name = response["error"]["name"]
            code = response["error"]["code"]
            raise CryptoBotApiError(code, name)
        return response
