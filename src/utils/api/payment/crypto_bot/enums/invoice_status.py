from src.utils.strenum import StrEnum

class InvoiceStatus(StrEnum):
    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"
