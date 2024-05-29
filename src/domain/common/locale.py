from dataclasses import dataclass


@dataclass
class Locale:
    name: str
    data: dict[str, str]
