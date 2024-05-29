from enum import Enum


class StrEnum(str, Enum):
    __str__ = str.__str__
    __repr__ = str.__repr__

    @classmethod
    def all(cls) -> list["StrEnum"]:
        return list(cls)
