from src.domain.exceptions.validation import OutOfRangeError


async def validate_reason(reason: str) -> None:
    if len(reason) > 100:
        raise OutOfRangeError(max_value=100)


async def validate_till(till: int) -> None:
    min_till = 60
    if till < min_till:
        raise OutOfRangeError(min_value=min_till)
