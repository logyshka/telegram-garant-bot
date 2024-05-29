from pydantic import BaseModel

from typing import Union
from datetime import datetime

from ..enums import Asset, CheckStatus


class Check(BaseModel):
    check_id: int
    hash: str
    asset: Union[Asset, str]
    amount: Union[int, float]
    bot_check_url: str
    status: Union[CheckStatus, str]
    created_at: datetime
