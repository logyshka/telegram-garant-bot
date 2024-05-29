from src.utils.strenum import StrEnum


class Asset(StrEnum):
    BTC = "BTC"
    TON = "TON"
    ETH = "ETH"
    USDT = "USDT"
    USDC = "USDC"
    BNB = "BNB"
    TRX = "TRX"
    LTC = "LTC"

    @classmethod
    def values(cls):
        return list(map(lambda asset: asset.value, cls))
