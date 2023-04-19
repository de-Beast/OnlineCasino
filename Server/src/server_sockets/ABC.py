# from abc import abstractmethod
import debugpy  # type:ignore
import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import (
    QMutexLocker,
    QObject,
)
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets import SocketThreadABC


class ServerSocketThreadABC(SocketThreadABC):
    def __init__(self, socket_descriptor: int, parent: QObject | None = None) -> None:
        super().__init__(parent)

        if socket_descriptor is None:
            self.error.emit("Socket descriptor can not be None")
            return

        self._socket_descriptor = socket_descriptor

    def run(self) -> None:
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
