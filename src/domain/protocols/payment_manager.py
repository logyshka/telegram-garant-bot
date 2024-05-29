from abc import abstractmethod
from typing import Protocol, List, Optional, Type, Dict, Any, Set, Union

from src.domain.common.currency_limits import CurrencyLimits
from src.domain.enums import Currency
from src.domain.models import Bill
from src.domain.protocols import ConfigManager
from src.domain.protocols.payment import Payment


class PaymentManager(Protocol):
    @abstractmethod
    async def get_available_currencies(self) -> List[Currency]:
        """
        Get currencies that available to refill
        :return: List of available currencies
        """

    @abstractmethod
    async def get_pending_bill(
            self,
            user_id: int,
    ) -> Optional[Bill]:
        """
        Get pending bill for given user
        :param user_id: Telegram user ID
        :return: Pending bill
        """

    @abstractmethod
    async def get_available_payments(
            self,
            currency: Currency
    ) -> List[Payment]:
        """
        Return all registered payments
        :param currency: Currency that payments should support
        :return: List of all registered payments
        """

    @abstractmethod
    async def get_all_payments(self) -> List[Payment]:
        """
        Return all registered payments
        :return: List of all registered payments
        """

    @abstractmethod
    async def get_payment_state(
            self,
            payment: Type[Payment]
    ) -> bool:
        """
        Get payment state
        :param payment: Payment to get state for
        :return: True if payment is active, False otherwise
        """

    @abstractmethod
    async def get_payment(
            self,
            payment: Union[Type[Payment], str],
            config_manager: Optional[ConfigManager] = None
    ) -> Payment:
        """
        Create through factory payment for given payment class name
        :param payment: Class name of payment
        :param config_manager: Optional. Config manager that contains data for payment.
        :return: Object of Payment
        """

    @abstractmethod
    async def get_limits(
            self,
            currency: Currency
    ) -> CurrencyLimits:
        """
        Resolve currency limits for given currency
        :param currency: Currency to resolve limits for
        :return: Resolved currency limits
        """

    @abstractmethod
    async def switch_payments_state(
            self,
            payment: Payment,
            new_state: Optional[bool] = None
    ) -> None:
        """
        If new state is not provided, switch payment state from True to False, or vice versa. If provided, just set new_state value
        :param payment: Payment to switch state for
        :param new_state: Optional. New state
        :return:
        """

    @abstractmethod
    async def switch_payment_account(
            self,
            payment_account: Dict[str, Any]
    ) -> None:
        """
        Switch payment account for given payment account data
        :param payment_account: Payment account data
        :return:
        """


class PaymentManagerFactory(Protocol):
    @abstractmethod
    async def create_payment_manager(
            self,
    ) -> PaymentManager:
        ...
