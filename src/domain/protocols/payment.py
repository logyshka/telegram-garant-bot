from abc import abstractmethod, ABC
from typing import Optional, List, Any, Type

from src.domain.common import PaymentField
from src.domain.enums import Currency
from src.domain.models import Bill
from src.domain.protocols import ConfigManager
from src.utils.strenum import StrEnum
from src.utils.text import camel_case_to_words


class Payment(ABC):
    currencies: list[Currency]
    name: str
    display_name: str
    state_key: str
    config_keys: StrEnum

    def __init__(self, **kwargs):
        self.data = kwargs

    def __init_subclass__(
            cls,
            currencies: Optional[List[Currency]] = None,
            config_keys: Optional[StrEnum] = None,
            **kwargs,
    ):
        cls.name = cls.__name__
        cls.display_name = camel_case_to_words(cls.__name__)
        cls.state_key = cls.name + 'State'
        cls.config_keys = config_keys
        super().__init_subclass__(**kwargs)

        if config_keys is None:
            raise ValueError(f"Config keys is not provided: class {cls.name}(Payment, config_keys=?) ")
        if currencies is None:
            raise ValueError(f"Currencies is not provided: class {cls.name}(Payment, currency=?) ")
        if not isinstance(currencies, List):
            raise TypeError(f"Currencies must be an instance of {List[Currency]}")
        if any(not isinstance(c, Currency) for c in currencies):
            raise TypeError(f"Currencies must be an instance of {List[Currency]}")

        cls.currencies = currencies

    async def cancel_bill(
            self, bill: Bill,
    ) -> None:
        await bill.delete()

    @abstractmethod
    async def validate(self) -> bool:
        """
        Validate if payment is valid
        :return: True if payment is valid, False otherwise
        """

    @abstractmethod
    async def create_bill(
            self,
            user_id: int,
            amount: float,
            currency: Currency,
    ) -> Bill:
        """
        Creates bill for payment.
        :param user_id: Telegram user ID
        :param amount: Amount to refill
        :param currency: Currency to refill
        :return:
        """

    @abstractmethod
    async def check_bill_is_paid(
            self,
            bill: Bill,
    ) -> bool:
        """
        Check if bill is paid
        :param bill: Bill to check
        :return: True if bill is paid, False otherwise
        """

    @abstractmethod
    async def get_info(
            self
    ) -> list[PaymentField]:
        """
        Get payment info: balance, account number, etc.
        :return: List of PaymentField
        """


class PaymentFactory:
    def __init__(self, config_manager: ConfigManager, payment_class: Type[Payment]):
        self._config_manager = config_manager
        self._payment_class = payment_class

    async def get_payment_data(self) -> dict[str, Any]:
        return {
            key: await self._config_manager.get_value(key.value)
            for key in self._payment_class.config_keys.all()
        }

    async def create_payment(self) -> Payment:
        payment_data = await self.get_payment_data()
        return self._payment_class(**payment_data)
