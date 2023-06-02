from typing import Self

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QObject

from Shared import SlotStorage
from Shared.abstract import QSingleton, SocketContainerBase
from Shared.sockets import SocketType

from .client_socket_thread import ClientSocketThread


class APIBase(QObject, metaclass=QSingleton):
    _socket_thread: ClientSocketThread
    login: str | None = None

    def __new__(cls) -> Self:
        if not hasattr(APIBase, "_socket_thread"):
            APIBase._socket_thread = ClientSocketThread()

        return super().__new__(cls)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._slot_storage = SlotStorage()

    @property
    def slot_storage(self) -> SlotStorage:
        if not isinstance(self._slot_storage, SlotStorage):
            raise RuntimeError("Slot storage is not initialized")

        return self._slot_storage

    @property
    def socket_thread(self) -> ClientSocketThread:
        if not hasattr(APIBase, "_socket_thread") or not isinstance(APIBase._socket_thread, ClientSocketThread):
            raise RuntimeError("Socket thread is not initialized")

        return APIBase._socket_thread

    #@property
    #def login(self) -> str:
    #    if not self._login:
    #        raise RuntimeError("Login is not set")

    #    return self._login

    @property
    def containers(self) -> dict[SocketType, SocketContainerBase]:
        return self.socket_thread.containers
