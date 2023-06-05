__all__ = [
    "SocketType",
]


from ..abstract import EnumBase, auto


class SocketType(EnumBase):
    """
    Перечисление, определяющее различные типы сокетов для клиента и сервера
    """
    
    NONE = auto()
    ACCOUNT_INITIAL = auto()
    ACCOUNT_INFO = auto()
    CHAT = auto()
    ROULETTE = auto()
