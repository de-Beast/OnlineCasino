__all__ = [
    "RouletteColor",
    "RouletteBetResponse",
]

from enum import auto

from ...abstract import EnumBase


class RouletteColor(EnumBase):
    RED = auto()
    BLACK = auto()
    GREEN = auto()


class RouletteBetResponse(EnumBase):
    SUCCESS = auto()
    CLOSED = auto()
    OUT_OF_BALANCE = auto()
    ALREADY_BET = auto()
