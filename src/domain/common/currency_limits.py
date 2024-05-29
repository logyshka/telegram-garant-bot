from dataclasses import dataclass

from _decimal import Decimal

from src.domain.enums import Currency


@dataclass
class CurrencyLimits:
    currency: Currency
    min: Decimal = Decimal(1)
    max: Decimal = Decimal(1_000_000)

    @property
    def min_str(self) -> str:
        return f"{self.min:f} {self.currency}"

    @property
    def max_str(self) -> str:
        return f"{self.max:f} {self.currency}"

    def check(self, amount: float) -> bool:
        return self.min <= amount <= self.max
