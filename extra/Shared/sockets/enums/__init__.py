__all__ = [
    "SocketThreadType",
    "AccountInitialRequest",
    "AccountInitialResponse",
]

from enum import auto

from .ABC import EnumBase
from .account_initial import AccountInitialRequest, AccountInitialResponse


class SocketThreadType(EnumBase):
    """
    Перечисление, определяющее различные типы сокетов для клиента и сервера
    """

    AUTHORIZATION = auto()
    ACCOUNT = auto()
