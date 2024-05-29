from dataclasses import dataclass


@dataclass
class PaymentField:
    value: str
    name: str = ''
    sep: str = ''

