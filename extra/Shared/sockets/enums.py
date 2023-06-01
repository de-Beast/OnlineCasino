__all__ = [
    "SocketThreadType",
]

from enum import auto

from ..abstract import EnumBase


class SocketThreadType(EnumBase):
    """
    Перечисление, определяющее различные типы сокетов для клиента и сервера
    """

    ACCOUNT_INITIAL = auto()
    ACCOUNT_INFO = auto()
    CHAT = auto()
