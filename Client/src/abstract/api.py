from typing import Callable, Self, Type, TypeVar

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QObject

from Shared import SlotStorage
from Shared.abstract import QSingleton, SocketContainerBase
from Shared.sockets import SocketType

from .client_socket_thread import ClientSocketThread

T = TypeVar("T", bound=SocketContainerBase, covariant=True)


class APIBase(QObject, metaclass=QSingleton):
    _socket_thread: ClientSocketThread
    _login: str | None = None

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

    @property
    def login(self) -> str:
        if not APIBase._login:
            raise RuntimeError("Login is not set")

        return APIBase._login

    @property
    def containers(self) -> dict[SocketType, SocketContainerBase]:
        return self.socket_thread.containers

    @staticmethod
    def on_container_added(*, slot_name: str):
        def inner(func: Callable[[Self, T], None]):
            if slot_name != func.__name__:
                raise ValueError("Slot name does not match function name")

            def wrapper(self: Self, container_class: Type[T], *args) -> None:
                container = args[-1]

                if not isinstance(container, SocketContainerBase):
                    raise ValueError("No container received")

                if not isinstance(container, container_class):
                    return

                func(self, container)
                self.socket_thread.containerAdded.disconnect(self.slot_storage.pop(slot_name))
                container_args = [arg for arg in args if arg is not container]
                container.run(*container_args)

            return wrapper

        return inner
