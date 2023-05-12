import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QMutexLocker, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets import SocketThreadABC
from Shared.sockets.enums import SocketThreadType


class ServerSocketThreadFactory(SocketThreadABC):
    """
    Специальный класс для определения необходимого для корректной
    связи с клиентом потока. Рабочий процесс заключен в цикл, постоянно обрабатывая
    поступающие серверу сокеты
    """

    # Активируется, когда класс определил необходимый типа потока, передаёт типа потока и дескриптор сокета
    socketIdentified = Signal(SocketThreadType, int)

    def thread_workflow(self, *args) -> None:
        """
        Запускает цикл, в котором обрабатываются только что подключенные к хосту сокеты.
        Определяется, какого типа поток нужно будет создать

        ### Параметры
        - `*args`

        Пустой кортеж, не используется, существует для совместимости с базовым классом
        """

        with QMutexLocker(self.mutex):
            socket_descriptor = self._socket_descriptor

        while self.is_working:
            socket = self._create_socket(socket_descriptor)
            if socket is not None:
                slot = self.slot_storage.create_and_store_slot(
                    "_recieve_socket_thread_type", self._recieve_socket_thread_type, socket
                )
                socket.readyRead.connect(slot)
                self.wait_for_readyRead(socket)
                socket.readyRead.disconnect(self.slot_storage.pop(slot))

            with QMutexLocker(self.mutex):
                self.cond.wait(self.mutex)
                socket_descriptor = self._socket_descriptor

    def identify_socket(self, socket_descriptor: int) -> None:
        """
        Сохраняется переданный дескриптор, затем поток запускается или пробуждается

        ### Параметры
        - `socket_descriptor: int`

        Дескриптор сохраняется в атрибуте `_socket_descriptor`
        """

        self._socket_descriptor = socket_descriptor
        if not self.is_running():
            self.start()
        else:
            self.cond.wake_one()

    def _create_socket(self, socket_descriptor: int) -> QTcpSocket | None:
        """
        Создает сокет с помощью переданного дескриптора

        ### Возвращает

        QTcpSocket или None, если не удалось присоединиться к хосту
        """

        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            self.error.emit("Socket is already created")
            return None

        return socket

    def _recieve_socket_thread_type(self, socket: QTcpSocket) -> None:
        """
        Вызывается, когда данные готовы для чтения из `QTcpSocket`
        (сокет активирует сигнал `readyRead`). Определяет, какой тип потока сокета следует использовать
        для обработки данных. Вызывает `socketIdentified` при успешной соединении

        ### Параметры
        - `socket: QTcpSocket`

        Сокет, в котором есть данные, готовые для чтения.
        """

        data: tuple[SocketThreadType] | None = self.recieve_data_package(socket, SocketThreadType)
        if data is None:
            return

        (socket_thread_type,) = data
        connection_status = True
        if not isinstance(socket_thread_type, SocketThreadType):
            self.error.emit("Invalid socket thread type")
            connection_status = False

        self.send_data_package(socket, connection_status)
        if not connection_status:
            return

        self.socketIdentified.emit(socket_thread_type, socket.socket_descriptor())
