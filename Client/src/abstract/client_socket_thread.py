# from abc import abstractmethod
from typing import ClassVar

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal
from PySide6.QtNetwork import QHostAddress, QTcpSocket

from Shared.abstract import SocketContainerBase, SocketThreadBase
from Shared.sockets import SocketThreadType


class ClientSocketThread(SocketThreadBase):
    """
    Клиентский поток для сокета
    """

    # В наследнике должен быть инициализирован, иначе выкинется исключение.
    # Принимаемый(-ые) типы у наследников могут быть разные
    responseRecieved = Signal((str,), (dict,))  # type: ignore

    _addContainer = Signal(SocketThreadType)
    containerAdded = Signal()

    client_token: ClassVar[str | None] = None

    def thread_workflow(self, socket: QTcpSocket) -> None:
        slot = self.slot_storage.create_slot(self._add_container, socket)
        self._addContainer.connect(slot)
        self.exec()
        self._addContainer.disconnect(slot)

    def create_socket(self) -> QTcpSocket | None:
        """
        Создает сокет и присодиняет его к хосту.
        Должен быть использован только в методе `run` или во всех волженных методах.

        ### Возвращает

        QTcpSocket или None, если не удалось присоединиться к хосту
        """

        host = QHostAddress(QHostAddress.SpecialAddress.LocalHost)
        port = 8888

        socket = QTcpSocket()
        socket.connect_to_host(host, port)
        if not socket.wait_for_connected():
            print("Can not connect to the host")
            return None

        return socket

    def add_container(self, socket_type: SocketThreadType) -> None:
        if not self.is_running():
            self.start()
            while True:
                if self.is_working:
                    break

        self._addContainer.emit(socket_type)

    def _add_container(self, socket: QTcpSocket, socket_type: SocketThreadType) -> None:
        if socket_type in self.containers.keys():
            return
        SocketContainerBase.remove_finish_condition_from_socket_stream(socket)

        container: SocketContainerBase = SocketContainerBase.create_container(socket, socket_type)
        slot = self.slot_storage.create_and_store_slot(f"{socket_type}", self.delete_container, container)
        container.finished.connect(slot)
        self.containers.update({socket_type: container})
        self.containerAdded.emit()

    def delete_container(self, container: SocketContainerBase) -> None:
        del self.containers[container.socket_type]
        container.finished.disconnect(self.slot_storage.pop(f"{container.socket_type}"))
