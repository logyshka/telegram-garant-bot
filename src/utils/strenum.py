from enum import Enum


class StrEnum(str, Enum):
    __str__ = str.__str__
    __repr__ = str.__repr__

    @classmethod
    def all(cls) -> list["StrEnum"]:
        return list(cls)

    def __eq__(self, other):
        if isinstance(other, Enum):
            return self.value == other.value
        return self.name == other

    def __hash__(self):
        return hash(self.name)

def get_enum_by_name(name: str, enum: StrEnum) -> StrEnum:
    for e in enum.all():
        if e.name == name:
            return e
    raise ValueError('There is no enum with name %s' % name)
