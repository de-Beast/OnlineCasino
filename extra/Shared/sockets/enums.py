from enum import IntEnum


class SocketThreadType(IntEnum):
    """
    Перечисление, определяющее различные типы сокетов для клиента и сервера
    """

    AUTHORIZATION: int = 0
    ACCOUNT: int = 1
