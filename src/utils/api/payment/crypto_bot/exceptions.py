from src.utils.exceptions import PaymentApiError


class CryptoBotApiError(PaymentApiError):
    def __init__(
            self,
            code: int,
            error: str
    ):
        self.code = code
        self.error = error

    def __str__(self):
        return f"[{self.code}] {self.error}"
