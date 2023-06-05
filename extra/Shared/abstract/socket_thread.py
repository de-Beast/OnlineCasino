__all__ = [
    "SocketThreadBase",
]

from abc import ABC, abstractmethod
from typing import TypeVar

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QDataStream, QObject
from PySide6.QtNetwork import QTcpSocket

from Shared.slot_storage import SlotStorage
from Shared.sockets import SocketType

from .socket_container import SocketContainerBase
from .thread import ThreadBase

T = TypeVar("T", bound=object)


class SocketThreadBase(ThreadBase, ABC):
    """
    Абстрактный базовый класс потоков для сокетов

    ### Абстрактные методы

    #>>> thread_workflow(self, socket: QTcpSocket) -> None
    #>>> create_socket(self) -> QTcpSocket | None
    """

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._slot_storage = SlotStorage()
        self._containers: dict[SocketType, SocketContainerBase] = {}

    @property
    def slot_storage(self) -> SlotStorage:
        return self._slot_storage

    @property
    def containers(self) -> dict[SocketType, SocketContainerBase]:
        return self._containers

    def run(self) -> None:
        import sys

        if sys.argv.count("debug_threads") > 0:
            import debugpy  # type: ignore

            debugpy.debug_this_thread()

        if (socket := self.create_socket()) is None:
            return

        socket.disconnected.connect(self.stop_work)
        socket.readyRead.connect(self.slot_storage.create_slot(self.check_socket_stream, socket))

        self._is_working = True
        self.workStarted.emit()
        self.thread_workflow(socket)
        self._is_working = False
        self._containers.clear()
        self._disconnect_socket(socket)

    def thread_workflow(self, socket: QTcpSocket) -> None:
        self.exec()

    @abstractmethod
    def create_socket(self) -> QTcpSocket | None:
        raise NotImplementedError

    def check_socket_stream(self, socket: QTcpSocket) -> None:
        receive_stream = QDataStream(socket)
        while True:
            if socket.bytes_available() == 0:
                    return
            
            receive_stream.start_transaction()
            data = receive_stream.readQVariant()
            if isinstance(data, SocketType) and (container := self.containers.get(data, None)):
                receive_stream.rollback_transaction()
                container.readyRead.emit()
                continue
            
            receive_stream.commit_transaction()

    def add_container(self, socket: QTcpSocket, socket_type: SocketType) -> SocketContainerBase:
        container: SocketContainerBase = SocketContainerBase.create_container(socket, socket_type)
        slot = self.slot_storage.create_and_store_slot(f"{socket_type}", self.delete_container, container)
        container.exit.connect(slot)
        self.containers.update({socket_type: container})
        return container

    def delete_container(self, container: SocketContainerBase) -> None:
        del self.containers[container.socket_type]
        container.exit.disconnect(self.slot_storage.pop(f"{container.socket_type}"))

    def _disconnect_socket(self, socket: QTcpSocket) -> None:
        """
        Отключает сокет от хоста, работает и на стороне клиента, и на стороне сервера.
        Ничего не делает, если сокет уже был отключён

        ### Параметры
        - `socket: QTcpSocket`
        """

        socket.disconnect_from_host()
        if socket.state() is not socket.SocketState.UnconnectedState:
            socket.wait_for_disconnected()
