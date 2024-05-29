from typing import Dict, Any, Optional, Type, List, Set, Union

from src.domain.common.currency_limits import CurrencyLimits
from src.domain.enums import Currency
from src.domain.functions.bill import get_pending_bill
from src.domain.models import Bill
from src.domain.protocols import ConfigManager, Payment, PaymentFactory, PaymentManager, PaymentManagerFactory


class DefaultPaymentManager(PaymentManager):
    def __init__(
            self,
            payments: List[Type[Payment]],
            limits: CurrencyLimits,
            config_manager: ConfigManager,
    ):
        self._payments = [
            payment for payment in payments
            if any(limit.currency in payment.currencies for limit in limits)
        ]
        self._limits = limits
        self._currencies = list(map(lambda limit: limit.currency, self._limits))
        self._config_manager = config_manager

    async def get_available_currencies(self) -> List[Currency]:
        currencies = set()

        for payment in self._payments:
            payment_currencies = [currency for currency in payment.currencies if currency in self._currencies]
            state = await self.get_payment_state(payment=payment)

            if not state: continue

            for currency in payment_currencies:
                currencies.add(currency)

        return list(currencies)

    async def get_pending_bill(self, user_id: int) -> Optional[Bill]:
        return await get_pending_bill(user_id=user_id)

    async def get_available_payments(self, currency: Currency) -> List[Payment]:
        available_payments = []

        for payment in self._payments:
            if await self.get_payment_state(payment=payment):
                payment = await self.get_payment(payment=payment)
                if await payment.validate():
                    available_payments.append(payment)

        return available_payments

    async def get_all_payments(self) -> List[Payment]:
        return self._payments

    async def get_payment_state(self, payment: Type[Payment]) -> bool:
        state = await self._config_manager.get_value(key=payment.state_key, default=False)
        return state

    def _get_payment(self, payment: str) -> Type[Payment]:
        for p in self._payments:
            if p.name == payment:
                return p
        raise ValueError('There is no payment with name %s' % payment)

    async def get_payment(
            self,
            payment: Union[str, Type[Payment]],
            config_manager: Optional[ConfigManager] = None
    ) -> Payment:
        if isinstance(payment, str):
            payment = self._get_payment(payment=payment)
        config_manager = config_manager if config_manager else self._config_manager
        factory = PaymentFactory(
            config_manager=config_manager,
            payment_class=payment,
        )
        payment = await factory.create_payment()
        return payment

    async def get_limits(self, currency: Currency) -> CurrencyLimits:
        for limit in self._limits:
            if limit.currency == currency:
                return limit
        raise ValueError(f'There is no limit for currency: {currency}')

    async def switch_payments_state(self, payment: Payment, new_state: Optional[bool] = None) -> None:
        if not new_state:
            new_state = not await self.get_payment_state(payment=payment)
        await self._config_manager.set_value(key=payment.state_key, value=new_state)

    async def switch_payment_account(self, payment_account: Dict[str, Any]) -> None:
        await self._config_manager.set_values(values=payment_account)


class DefaultPaymentManagerFactory(PaymentManagerFactory):
    def __init__(
            self,
            payments: List[Type[Payment]],
            limits: CurrencyLimits,
            config_manager: ConfigManager,
    ):
        self._payments = payments
        self._limits = limits
        self._config_manager = config_manager

    async def create_payment_manager(self) -> DefaultPaymentManager:
        manager = DefaultPaymentManager(
            payments=self._payments,
            limits=self._limits,
            config_manager=self._config_manager,
        )
        return manager
