from dataclasses import dataclass

from .enums import RouletteColor


@dataclass(frozen=True)
class RouletteBet:
    total: int
    color: RouletteColor
