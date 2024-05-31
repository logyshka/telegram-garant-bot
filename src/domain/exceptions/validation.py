from typing import Any, Optional


class ValidationError(Exception):
    pass


class OutOfRangeError(ValidationError):
    def __init__(self, min_value: Optional[Any] = None, max_value: Optional[Any] = None):
        self.min_value = min_value
        self.max_value = max_value
