__all__ = [
    "SocketThreadType",
    "AccountInitialRequest",
    "AccountInitialResponse",
]

from enum import IntEnum

from .account_initial import AccountInitialRequest, AccountInitialResponse


class SocketThreadType(IntEnum):
    """
    Перечисление, определяющее различные типы сокетов для клиента и сервера
    """

    AUTHORIZATION = 0
    ACCOUNT = 1
