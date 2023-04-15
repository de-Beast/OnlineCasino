from abc import ABC, abstractmethod

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_properties  # type: ignore # noqa: F401
from PySide6.QtCore import (
    QMutex,
    QMutexLocker,
    QObject,
    QThread,
    QWaitCondition,
    Signal,
)
from PySide6.QtNetwork import QTcpSocket


class ThreadABC(ABC, QThread):
    wait_timeout: int = 10000  # milliseconds

    error = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.finished.connect(self.delete_later)

        self.mutex = QMutex()
        self.cond = QWaitCondition()


class ServerSocketThreadABC(ThreadABC):
    def __init__(self, socket_descriptor: int, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._socket_descriptor: int = socket_descriptor

    def create_socket(self) -> QTcpSocket | None:
        """
        Этот метод создает объект QTcpSocket, используя заданный дескриптор сокета, и возвращает его
        или возвращает None, если сокет уже создан. Должен быть использован только в методе `run`.

        ### Параметры
        - `socket_descriptor: int`

        Параметр `socket_descriptor` используется для создания нового объекта QTcpSocket.
        Если сокет уже создан, метод вызызвает сигнал `error` и возвращает значение `None`.

        ### Возвращает
        Экземпляр `QTcpSocket` или `None`, если произошла ошибка.
        """

        with QMutexLocker(self.mutex):
            socket = QTcpSocket()
            if self._socket_descriptor is None:
                self.error.emit("Socket descriptor is None")
                return None
            elif socket.set_socket_descriptor(self._socket_descriptor):
                self.error.emit("Socket is already created")
                return None

            socket.readyRead.connect(lambda: self.on_readyRead(socket))
            return socket

    @abstractmethod
    def on_readyRead(self, socket: QTcpSocket) -> None:
        pass
