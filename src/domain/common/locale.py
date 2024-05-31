from dataclasses import dataclass

from src.domain.enums import LocaleName


@dataclass
class Locale:
    name: LocaleName
    data: dict[str, str]
