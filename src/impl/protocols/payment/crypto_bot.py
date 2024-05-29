from src.domain.common import PaymentField
from src.domain.enums import Currency
from src.domain.functions.bill import create_bill
from src.domain.models import Bill
from src.domain.protocols import Payment
from src.utils.api.payment import CryptoBotApi, CryptoBotApiError
from src.utils.api.payment.crypto_bot.enums import CurrencyType, InvoiceStatus
from src.utils.exceptions import PaymentApiError
from src.utils.misc import is_fiat
from src.utils.strenum import StrEnum


class CryptoBotConfigKeys(StrEnum):
    TOKEN = 'CRYPTO_BOT_TOKEN'


CURRENCIES = [
    Currency.RUB,
    Currency.USDT,
]


class CryptoBotPayment(Payment, currencies=CURRENCIES, config_keys=CryptoBotConfigKeys):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._token = kwargs[CryptoBotConfigKeys.TOKEN.value]
        self._api = CryptoBotApi(token=self._token)

    @classmethod
    def __call__(cls, **kwargs):
        return cls(**kwargs)

    async def validate(self) -> bool:
        try:
            await self._api.get_me()
        except PaymentApiError:
            return False
        else:
            return True

    async def create_bill(self, user_id: int, amount: float, currency: Currency) -> Bill:
        invoice_kwargs = dict(
            amount=amount
        )
        if is_fiat(currency=currency):
            invoice_kwargs['currency_type'] = CurrencyType.FIAT
            invoice_kwargs['fiat'] = currency
        else:
            invoice_kwargs['currency_type'] = CurrencyType.CRYPTO
            invoice_kwargs['asset'] = currency

        invoice = await self._api.create_invoice(
            **invoice_kwargs,
        )
        bill = await create_bill(
            amount=amount,
            currency=currency,
            user_id=user_id,
            payment=self.name,
            payment_display_name=self.display_name,
            check_info=invoice.invoice_id,
            pay_url=invoice.bot_invoice_url,
            expires_at=None
        )
        return bill

    async def check_bill_is_paid(self, bill: Bill) -> bool:
        invoice = await self._api.get_invoices(
            invoice_ids=bill.check_info,
            status=InvoiceStatus.PAID
        )
        return invoice is not None

    async def cancel_bill(
            self, bill: Bill,
    ) -> None:
        await super().cancel_bill(bill=bill)
        await self._api.delete_invoice(invoice_id=bill.check_info)

    async def get_info(self) -> list[PaymentField]:
        fields = []
        balances = await self._api.get_balance()
        for i in range(len(balances)):
            balance = balances[i]
            fields.append(PaymentField(
                value=f'{balance.available} {balance.currency_code}',
            ))
        return fields
