__all__ = [
    "RouletteColor",
    "RouletteBetResponse",
    "RouletteState",
]

from ...abstract import EnumBase, auto


class RouletteColor(EnumBase):
    RED = auto()
    BLACK = auto()
    GREEN = auto()


class RouletteBetResponse(EnumBase):
    SUCCESS = auto()
    CLOSED = auto()
    OUT_OF_BALANCE = auto()
    ALREADY_BET = auto()


class RouletteState(EnumBase):
    STOPPED = auto()
    SPINNING = auto()
