import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QMutexLocker, QObject
from PySide6.QtNetwork import QTcpSocket

from Shared.abstract import SocketContainerBase, SocketThreadBase


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

    def thread_workflow(self, socket: QTcpSocket) -> None:
        socket.readyRead.connect(self.slot_storage.create_slot(self.check_containers, socket))
        self.exec()

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

    def check_containers(self, socket: QTcpSocket) -> None:
        socket_type, finish_cond = SocketContainerBase.identify_socket_type(socket)
        if socket_type is None or socket_type in self.containers.keys():
            return
        if finish_cond and SocketContainerBase.remove_finish_condition_from_socket_stream(socket):
            return

        container: SocketContainerBase = SocketContainerBase.create_container(socket, socket_type)
        slot = self.slot_storage.create_and_store_slot(f"{socket_type}", self.delete_container, container)
        container.finished.connect(slot)
        self.containers.update({socket_type: container})
        container.run()

    def delete_container(self, container: SocketContainerBase) -> None:
        del self.containers[container.socket_type]
        container.finished.disconnect(self.slot_storage.pop(f"{container.socket_type}"))
