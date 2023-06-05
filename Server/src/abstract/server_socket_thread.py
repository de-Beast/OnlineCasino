import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QMutexLocker, QObject, QDataStream
from PySide6.QtNetwork import QTcpSocket

from Shared.abstract import SocketContainerBase, SocketThreadBase
from Shared.sockets import SocketType

from .server_socket_container import ServerSocketContainer


class ServerSocketThread(SocketThreadBase):
    """
    Базовый класс для серверных сокетов.

    ### Абстрактные методы
    >>> def thread_workflow(self, socket: QTcpSocket) -> None: ...

    Главный метод, в котором происходят основные вычисления потока.
    Должен быть обязательно переопределён. Не имеет базовой реализации
    """

    def __init__(self, socket_descriptor: int, parent: QObject | None = None) -> None:
        super().__init__(parent)

        if socket_descriptor is None:
            return

        self._socket_descriptor = socket_descriptor

    def create_socket(self) -> QTcpSocket | None:
        """
        Создаёт сокет, используя сохранённый дескриптор.
        Должен быть использован только в методе `run`.

        ### Возвращает

        `QTcpSocket` или `None`, если произошла ошибка.
        """

        with QMutexLocker(self.mutex):
            socket_descriptor = self._socket_descriptor

        if socket_descriptor is None:
            return None

        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            print(socket.error_string())
            return None

        return socket

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
            elif isinstance(data, SocketContainerBase.ContainerRequest):
                receive_stream.rollback_transaction()
                self.handle_container_request(socket)
                continue
            
            receive_stream.commit_transaction()

    def handle_container_request(self, socket: QTcpSocket) -> None:
        container_request, socket_type = ServerSocketContainer.receive_container_request(socket)
        match container_request:
            case SocketContainerBase.ContainerRequest.CONNECT:
                if socket_type is not None:
                    container = self.add_container(socket, socket_type)
                    container.readyRead.emit()
            case SocketContainerBase.ContainerRequest.DISCONNECT:
                if container := self.containers.get(socket_type, None):
                    container.quit()

    def add_container(self, socket: QTcpSocket, socket_type: SocketType) -> ServerSocketContainer:
        container = super().add_container(socket, socket_type)
        container.run()
        return container
