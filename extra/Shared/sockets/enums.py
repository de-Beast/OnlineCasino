__all__ = [
    "SocketType",
]

from enum import auto

from ..abstract import EnumBase


class SocketType(EnumBase):
    """
    Перечисление, определяющее различные типы сокетов для клиента и сервера
    """

    ACCOUNT_INITIAL = auto()
    ACCOUNT_INFO = auto()
    CHAT = auto()
    ROULETTE = auto()
