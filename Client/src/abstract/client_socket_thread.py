import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal
from PySide6.QtNetwork import QHostAddress, QTcpSocket

from Shared.abstract import SocketContainerBase, SocketThreadBase
from Shared.sockets import SocketType


class ClientSocketThread(SocketThreadBase):
    """
    Клиентский поток для сокета
    """

    # В наследнике должен быть инициализирован, иначе выкинется исключение.
    # Принимаемый(-ые) типы у наследников могут быть разные
    responseReceived = Signal((str,), (dict,))  # type: ignore

    _addContainer = Signal(SocketType)
    containerAdded = Signal(SocketContainerBase)

    def thread_workflow(self, socket: QTcpSocket) -> None:
        slot = self.slot_storage.create_slot(self.add_container, socket)
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

        host = "192.168.0.107"
        # host = "localhost"
        port = 8888

        socket = QTcpSocket()
        socket.connect_to_host(host, port)
        if not socket.wait_for_connected():
            print("Can not connect to the host")
            return None

        return socket

    def append_container(self, socket_type: SocketType) -> None:
        if socket_type in self.containers.keys():
            return

        if not self.is_running():
            slot = self.slot_storage.create_slot(self._addContainer.emit, None, socket_type)
            self.workStarted.connect(slot)
            self.start()
            return

        self._addContainer.emit(socket_type)

    def add_container(self, socket: QTcpSocket, socket_type: SocketType) -> None:
        container = super().add_container(socket, socket_type)
        self.containerAdded.emit(container)
