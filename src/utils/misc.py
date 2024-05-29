from src.domain.enums import Currency


def is_fiat(currency: Currency) -> bool:
    return currency in [
        Currency.RUB,
    ]

