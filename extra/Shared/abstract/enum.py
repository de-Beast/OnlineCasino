__all__ = [
    "EnumBase",
]

from enum import Enum


class EnumBase(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
