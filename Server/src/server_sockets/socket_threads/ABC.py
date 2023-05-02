# from abc import abstractmethod
from abc import ABC
from typing import ClassVar, Type

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QMutexLocker, QObject
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets import SocketThreadABC
from Shared.sockets.enums import SocketThreadType


class ServerSocketThreadABC(SocketThreadABC, ABC):
    """
    Базовый класс для серверных сокетов.

    ### Абстрактные методы
    >>> def thread_workflow(self, socket: QTcpSocket) -> None: ...

    Главный метод, в котором происходят основные вычисления потока.
    Должен быть обязательно переопределён. Не имеет базовой реализации
    """

    _socket_type_bindings: dict[SocketThreadType, Type["ServerSocketThreadABC"]] = {}

    socket_type: ClassVar[SocketThreadType]

    @classmethod
    def __init_subclass__(cls, **kwards) -> None:
        super().__init_subclass__(**kwards)

        if not hasattr(cls, "socket_type") or not isinstance(cls.socket_type, SocketThreadType):
            raise TypeError("socket_type must be a Class variable of SocketThreadType enum")

        if ServerSocketThreadABC._socket_type_bindings.get(cls.socket_type, None) is not None:
            raise RuntimeError("Can not create subclass with the same socket type")

        ServerSocketThreadABC._socket_type_bindings.update({cls.socket_type: cls})

    def __init__(self, socket_descriptor: int, parent: QObject | None = None) -> None:
        super().__init__(parent)

        if socket_descriptor is None:
            self.error.emit("Socket descriptor can not be None")
            return

        self._socket_descriptor = socket_descriptor

    def run(self) -> None:
        import sys

        if sys.argv.count("debug_threads") > 0:
            import debugpy  # type: ignore

            debugpy.debug_this_thread()

        if (socket := self._create_socket()) is None:
            return

        self._is_working = True
        self.thread_workflow(socket)
        self._is_working = False
        self._disconnect_socket(socket)

    def _create_socket(self, *args, **kwargs) -> QTcpSocket | None:
        """
        Создаёт сокет, используя сохранённый дескриптор.
        Должен быть использован только в методе `run`.

        ### Возвращает

        `QTcpSocket` или `None`, если произошла ошибка.
        """

        with QMutexLocker(self.mutex):
            socket_descriptor = self._socket_descriptor

        if socket_descriptor is None:
            self.error.emit("Socket descriptor can not be None")
            return None

        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            print(socket.error_string())
            self.error.emit("Socket is already created")
            return None

        return socket
